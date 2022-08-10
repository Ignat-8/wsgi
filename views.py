from framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', 
                                data=request.get('data', None),
                                path=request.get('path', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', render('page_404.html')
