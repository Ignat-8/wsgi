from framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', 
                                data=request.get('data', None),
                                path=request.get('path', None))


class Curs:
    def __call__(self, request):
        return '200 OK', render(f"curs_{request['curs_id']}.html", 
                                curs_id=request['curs_id'],
                                data=request.get('data', None))


class Curses:
    def __call__(self, request):
        return '200 OK', render("curses.html",
                                data=request.get('data', None))


class About:
    def __call__(self, request):
        return '200 OK', render('contacts.html')


class Admins:
    def __call__(self, request):
        return '200 OK', render('admins.html')


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', render('page_404.html')
