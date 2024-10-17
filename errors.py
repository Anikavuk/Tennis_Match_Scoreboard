from sqlalchemy.exc import IntegrityError


class IntegrityError(Exception):
    def __init__(self, message=None):
        if not message:
            self.message = ("It looks like the name you are trying to use is "
                            "already taken. To continue, you need to enter "
                            "a different, unique name")
        # Похоже, что имя, которое вы пытаетесь использовать, уже занято.
        # Чтобы продолжить, вам нужно ввести другое, уникальное имя
        else:
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
        # elif isinstance(exception, CurrencyNotFoundException):
        #     error_code = 404
        #     error_message = "Валюта не найдена"
        # elif isinstance(exception, IndexError):
        #     error_code = 404
        #     error_message = "Обменный курс для пары не найден"
        # elif isinstance(exception, ExchangeRateNotFoundException):
        #     if exception.value == 'post_rate':
        #         error_code = 404
        #         error_message = "Валютная пара отсутствует в базе данных"
        # elif isinstance(exception, CurrencyAlreadyExistsException):
        #     if exception.value == 'code':
        #         error_code = 409
        #         error_message = "Валюта с таким кодом уже существует"
        #     else:
        #         error_code = 409
        #         error_message = "Валютная пара с таким кодом уже существует"
        # elif isinstance(exception, MissingFieldsException):
        #     if exception.field == 'code':
        #         error_code = 400
        #         error_message = "Код валюты отсутствует в адресе"
        #     elif exception.field == 'full_name, code, sign':
        #         error_code = 400
        #         error_message = "Отсутствует нужное поле формы"
        #     elif exception.field == 'rate':
        #         error_code = 400
        #         error_message = "Коды валютной пары отсутствуют в адресе"
        return {error_code: error_message}
