from django.http import JsonResponse
from rest_framework.views import APIView


class ProductsController(APIView):
    def get(self, request, show_title):
        return JsonResponse({'blogs': [
            {'id': 1, 'title': 'Nice Blog'},
            {'id': 2, 'title': show_title},
        ]})
