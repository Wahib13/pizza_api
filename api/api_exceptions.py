from rest_framework.exceptions import APIException


class IllegalOrderUpdateException(APIException):
    status_code = 422
