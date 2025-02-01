class MatchNotFoundException(Exception):
    def __init__(self, message='Матча с таким UUID не существует в базе данных'):
        self.message = message
        super().__init__(self.message)


class PlayerNotFoundException(Exception):
    def __init__(self, message='Игрока с таким именем нет в базе данных'):
        self.message = message
        super().__init__(self.message)


class IntegrityError(Exception):
    def __init__(self, message='Вам нужно ввести другое, уникальное имя'):
        self.message = message
        super().__init__(self.message)


class SameNamesError(Exception):
    def __init__(self, message='Вы ввели одинаковые имена, а надо разные:)'):
        self.message = message
        super().__init__(self.message)


class DatabaseErrorException(Exception):
    def __init__(self, message="База данных недоступна"):
        self.message = message
        super().__init__(self.message)


class InvalidPlayernameError(Exception):
    def __init__(self, message="Введите буквенное имя"):
        self.message = message
        super().__init__(self.message)


class NonExistentNameError(Exception):
    def __init__(self, message="Вы ввели несуществующее имя"):
        self.message = message
        super().__init__(self.message)


class BaseAPIException:
    @classmethod
    def error_response(cls, exception: Exception):
        error_code = 200
        error_message = "OK"
        if isinstance(exception, IntegrityError):
            error_code = 400
            error_message = exception.message
        elif isinstance(exception, DatabaseErrorException):
            error_code = 500
            error_message = "База данных недоступна"
        elif isinstance(exception, InvalidPlayernameError):
            error_code = 400
            error_message = "Введите буквенное имя"
        elif isinstance(exception, SameNamesError):
            error_code = 400
            error_message = "Вы ввели одинаковые имена, а надо разные"
        elif isinstance(exception, NonExistentNameError):
            error_code = 400
            error_message = "Вы ввели несуществующее имя"
        elif isinstance(exception, MatchNotFoundException):
            error_code = 506
            error_message = 'Матча с таким UUID не существует в базе данных'
        elif isinstance(exception, PlayerNotFoundException):
            error_code = 507
            error_message = 'Игрока с таким именем нет в базе данных'
        return {error_code: error_message}
