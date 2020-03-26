from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file.
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-decorated-router',
    version='0.0.1',
    description=u"Auto registering routes in Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[],
    keywords='',
    author=u"Roy Segall",
    author_email='roy@segall.io',
    url='https://github.com/RoySegall/django-decorated-router',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
