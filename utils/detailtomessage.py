from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call DRF's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        if "detail" in response.data:
            response.data = {"message": response.data["detail"]}
        else:
            response.data = {"message": response.data}

    return response
