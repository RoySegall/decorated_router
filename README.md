# Decorated routes

This is litterly magic! 🧙‍

## Install

In your `settings.py` register the ap:
```python
INSTALLED_APPS = [
    # ...
    'decorated_router',
]
```

Your `urls.py` should look like this:

```python
"""djangoTesting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from decorated_router.api.api import auto_register


urlpatterns = [
    # what ever you got here...
]

auto_register(urlpatterns, path)
```

## Creating routes:

```python
from django.http import JsonResponse
from rest_framework.views import APIView
from decorated_router.api.decorators import url_decoration


@url_decoration(path="api/blog/")
class Blog(APIView):
    def get(self, request):
        return JsonResponse({'foo': 'bar'})
```

You can now just write your routes and decorate them with the URL and that's
it. No longer long `url.py` file.

🤘🍕
