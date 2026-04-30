from rest_framework.views import exception_handler
from .responses import ApiResponse
from .messages import get_message


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        request = context.get('request')
        lang = 'en'
        if request:
            accept_lang = request.headers.get('Accept-Language', 'en')
            lang = 'ar' if 'ar' in accept_lang else 'en'

        message_key = 'error'
        if response.status_code == 400:
            message_key = 'invalid_data'
        elif response.status_code == 401:
            message_key = 'login_required'
        elif response.status_code == 403:
            message_key = 'unauthorized'
        elif response.status_code == 404:
            message_key = 'not_found'
        elif response.status_code == 500:
            message_key = 'server_error'

        return ApiResponse.error(
            message_key=message_key,
            errors=response.data,
            status_code=response.status_code,
            lang=lang
        )

    return response