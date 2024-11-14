
class IntegrityError(Exception):
    def __init__(self, message='You need to enter a different, unique name'):
        # Вам нужно ввести другое, уникальное имя
        self.message = message
        super().__init__(self.message)

class DatabaseErrorException(Exception):
    def __init__(self, message="The database is unavailable"):
        self.message = message
        super().__init__(self.message)

class InvalidPlayernameError(Exception):
    def __init__(self, message="Enter the letter name of the player"):
        self.message = message
        super().__init__(self.message)


class ErrorResponse:
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
        return {error_code: error_message}

