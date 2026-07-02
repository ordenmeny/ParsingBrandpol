class AppException(Exception):
    """Родительский класс для всех доменных ошибок"""


class PageNotFoundException(AppException):
    msg = "Страница не найдена"
