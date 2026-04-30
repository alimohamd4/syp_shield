from rest_framework.response import Response
from rest_framework import status
from .messages import get_message


def get_lang(request):
    """استخراج اللغة من الـ Request"""
    lang = request.headers.get('Accept-Language', 'en')
    return 'ar' if 'ar' in lang else 'en'


class ApiResponse:

    @staticmethod
    def success(data=None, message_key='success', message=None, 
                status_code=status.HTTP_200_OK, lang='en'):
        return Response({
            "success": True,
            "message": message or get_message(message_key, lang),
            "data": data
        }, status=status_code)

    @staticmethod
    def created(data=None, message_key='success', message=None, lang='en'):
        return Response({
            "success": True,
            "message": message or get_message(message_key, lang),
            "data": data
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def error(message_key='error', message=None, errors=None,
              status_code=status.HTTP_400_BAD_REQUEST, lang='en'):
        return Response({
            "success": False,
            "message": message or get_message(message_key, lang),
            "errors": errors
        }, status=status_code)

    @staticmethod
    def not_found(message_key='not_found', message=None, lang='en'):
        return Response({
            "success": False,
            "message": message or get_message(message_key, lang),
            "errors": None
        }, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def unauthorized(message_key='unauthorized', message=None, lang='en'):
        return Response({
            "success": False,
            "message": message or get_message(message_key, lang),
            "errors": None
        }, status=status.HTTP_403_FORBIDDEN)