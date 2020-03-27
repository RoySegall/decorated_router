from django.http import JsonResponse
from django.views import View


class ProductsController(View):
    def get(self, request, show_title):
        return JsonResponse({'blogs': [
            {'id': 1, 'title': 'Nice Blog'},
            {'id': 2, 'title': show_title},
        ]})
