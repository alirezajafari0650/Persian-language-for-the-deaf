from rest_framework import status
from rest_framework.response import Response

from ..conf import conf


class Error:
    def __init__(self, message):
        self.message = message

    def render(self):
        error = {"code": 1000, "message": self.message, "errors": []}

        return error


class ResponsesMixin:
    @staticmethod
    def simple_text_response(message=None):
        if message is None:
            message = conf.SMS_REQUEST_SUCCESS
        data = {"detail": message}

        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def success_objects_response(data):
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def error_response(error_message):
        error = error_message
        if type(error_message) is str:
            error = Error(error_message).render()

        return Response(error, status=status.HTTP_400_BAD_REQUEST)
