import datetime


def year(request):
    """Функция добавляет в контекст переменную year."""
    return {
        'year': datetime.datetime.today().year}
