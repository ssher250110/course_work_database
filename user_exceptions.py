class ApiError(Exception):
    """
    Класс исключение при соединении к HeadHunter.
    """
    pass


class ConnectError(Exception):
    """
    Класс исключение при соединении к базе данных.
    """
    pass
