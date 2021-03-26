from rest_framework.exceptions import APIException


class ValidationErrorMy(APIException):
    status_code = 400
    default_detail = "A server error occurred."
    default_code = "validation_error"

    def __init__(self, detail):
        if detail is not None:
            self.detail = dict(validation_error=detail)
        else:
            self.detail = dict(detail=self.default_detail)
