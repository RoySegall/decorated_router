def url_decoration(*args, **kwargs):

    def inner(func):
        func.decorated_url_data = kwargs
        return func

    return inner
