from os import getcwd
from os.path import join
from django.urls import reverse
from django.test import TestCase
from django.test import override_settings
from decorated_router.api.api import auto_register
from decorated_router.api.api import get_recursive_files
from decorated_router.api.api import get_decorated_classes
from decorated_router.tests.assets.blog import BlogControllerForTests
from decorated_router.tests.assets.products import ProductsController
from decorated_router.tests.assets.blog import BlogsControllerForTests

# This section intend for writing the default urlpatterns and register the
# route for the tests.
routes = get_decorated_classes(include_tests=True)
urlpatterns = []
auto_register(urlpatterns, routes=routes)


class TestApi(TestCase):

    def setUp(self):
        self.base_path = join(
            getcwd(),
            'decorated_router',
            'tests',
            'assets',
        )

    def test_get_recursive_files(self):
        """
        Testing the function which get all the files which can include
        decorated routers.
        """
        # Preparing the calculated path list and the assets file path.
        files = []
        expected_files = [
            ['users', 'login.py'],
            ['users', 'logout.py'],
            ['users', 'permissions.py'],
            ['blog.py'],
            ['products.py'],
        ]

        # Get all the files.
        get_recursive_files(self.base_path, files)

        for expected_file in expected_files:
            joined_path = join(self.base_path, join(*expected_file))
            self.assertIn(joined_path, files)

        self.assertEqual(len(files), len(expected_files))

    def test_get_decorated_classes(self):
        routes = get_decorated_classes(include_tests=True)

        expected_items = [
            {
                'path': {
                    'path': 'api/test/blogs',
                    'name': 'blogs',
                    'extra': {'show_title': '🍕'}
                },
                'object': BlogsControllerForTests
            },
            {
                'path': {
                    're_path': '^api/test/blog/(?P<blog_id>\\d+)/?$',
                    'name': 'blog',
                },
                'object': BlogControllerForTests
            },

        ]

        self.assertIn(expected_items[0], routes)
        self.assertIn(expected_items[1], routes)

        # Checking to the ProductsController is available in the routes.
        for route in routes:
            self.assertNotEqual(ProductsController, route['object'])

    @override_settings(ROOT_URLCONF=__name__)
    def testing_auto_register_urls(self):
        """
        Checking the interaction with the router.
        """
        self.assertEqual(
            self.client.get('/api/test/blogs').json(),
            {'blogs': [
                {'id': 1, 'title': 'Nice Blog'},
                {'id': 2, 'title': '🍕'}
            ]}
        )

        # Checking that the reverse method works for auto register routes.
        self.assertEqual(reverse('blogs'), '/api/test/blogs')