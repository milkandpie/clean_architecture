from exceptions import ServiceException


class MethodNotAllowException(ServiceException):
    def __init__(self):
        super().__init__('Method not allowed', code=405)
