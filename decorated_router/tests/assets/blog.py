from django.http import JsonResponse
from django.views import View
from decorated_router.api.decorators import url_decoration


@url_decoration(path="api/test/blogs", name="blogs", extra={'show_title': '🍕'})
class BlogsControllerForTests(View):
    def get(self, request, show_title):
        return JsonResponse({'blogs': [
            {'id': 1, 'title': 'Nice Blog'},
            {'id': 2, 'title': show_title},
        ]})


@url_decoration(re_path=r'^api/test/blog/(?P<blog_id>\d+)/?$', name="blog")
class BlogControllerForTests(View):
    def get(self, request, blog_id):
        return JsonResponse({'id': 1, 'title': f'Nice Blog {blog_id}'})
