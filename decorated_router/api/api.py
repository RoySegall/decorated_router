import os
import inspect
import sys
import logging
from os import getcwd
from glob import glob
from django.urls import path, re_path
from django.views.generic.base import View


def get_recursive_files(path, files):
    """
    Get all the files from a given path.
    """
    if not os.path.isfile(path):
        for directory_member in glob(os.path.join(path, '*')):
            if '__' in directory_member:
                continue

            if '.py' in directory_member:
                files.append(directory_member)

            get_recursive_files(directory_member, files)


def get_decorated_classes(routes_folder=getcwd(), include_tests=False):
    """
    Get all the decorated classes in a given path.

    :param routes_folder: The folder which we need to look decorated routes.
        By default the value of the os.getcwd()

    :param include_tests: The flag determines if a folder named 'tests' should
        be included or not. When testing the application it should not.
    """
    files = []
    get_recursive_files(routes_folder, files)

    routes = []
    for file in files:
        if not include_tests and f'{os.path.sep}tests{os.path.sep}' in file:
            # When not in testing mod we need to skip on files which located
            # in a test folder.
            continue

        # Go over the files we got and compile an import path.
        import_path = file.replace(routes_folder + os.path.sep, '') \
            .replace('.py', '') \
            .replace(os.path.sep, '.')

        # Import the module and inspect the members (the object which were
        # imported).
        if import_path == 'setup':
            # This one breaks when running tests with tox. Don't know why but
            # I'll go with the flow.
            continue

        try:
            __import__(import_path)
        except Exception as e:
            logging.error(f"An error during importing the file: {e}")
            continue

        for name, obj in inspect.getmembers(sys.modules[import_path]):
            if not inspect.isclass(obj):
                # This is not a class. Skip.
                continue

            if not issubclass(obj, View):
                continue

            if not hasattr(obj, 'decorated_url_data'):
                continue

            routes.append({
                'path': obj.decorated_url_data,
                'object': obj
            })

    return routes


def auto_register(urlpatterns, routes=None):
    """
    Appending url patterns to the urlpatterns variable we pass from the url.py
    file.
    """
    if not routes:
        routes = get_decorated_classes()

    for route in routes:

        if 're_path' in route['path']:
            # Setting the handler the pattern for a regex handler.
            pattern = route['path']['re_path']
            handler = re_path
        else:
            handler = path
            pattern = route['path']['path']

        # Setting some variables.
        name = route['path'].get('name', None)
        extra = route['path'].get('extra', {})
        url_pattern = handler(
            pattern,
            route['object'].as_view(),
            extra,
            name=name,
        )
        urlpatterns.append(url_pattern)
