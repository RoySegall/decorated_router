from django.test import TestCase, override_settings
from django.urls import reverse
from decorated_router.api.api import get_recursive_files, \
    get_decorated_classes, auto_register
from os import getcwd, path
from decorated_router.tests.assets.blog import BlogsControllerForTests, \
    BlogControllerForTests
from decorated_router.tests.assets.products import ProductsController


# This section intend for writing the default urlpatterns and register the
# route for the tests.
routes = get_decorated_classes(include_tests=True)
urlpatterns = []
auto_register(urlpatterns, routes=routes)


class TestApi(TestCase):

    def setUp(self):
        self.base_path = path.join(
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
            joined_path = path.join(self.base_path, path.join(*expected_file))
            self.assertIn(joined_path, files)

        self.assertEquals(len(files), len(expected_files))

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
            self.assertNotEquals(ProductsController, route['object'])

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
        self.assertEquals(reverse('blogs'), '/api/test/blogs')
