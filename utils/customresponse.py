from rest_framework.response import Response
from rest_framework import status

# <------------------------ API SUCCESS Responses ------------------------>
# api success response
def GET_SuccessResponse(message, data=None):
    """
    Returns a successful GET response with HTTP 200 OK status.
    
    Args:
        message (str): Success message to be included in the response
        data (optional): Data payload to be included in the response. Defaults to None.
    
    Returns:
        Response: DRF Response object with success flag, message, data, and 200 status code
    """
    return Response({"success": True, "message": message, "data": data} if data is not None else {"success": True, "message": message}, status=status.HTTP_200_OK)

def PUTPATCH_SuccessResponse(message, data=None):
    """
    Returns a successful PUT/PATCH response with HTTP 200 OK status.
    
    Args:
        message (str): Success message to be included in the response
        data (optional): Updated data payload to be included in the response. Defaults to None.
    
    Returns:
        Response: DRF Response object with success flag, message, data, and 200 status code
    """
    return Response({"success": True, "message": message, "data": data}, status=status.HTTP_200_OK)

def POST_SuccessResponse(message, data=None):
    """
    Returns a successful POST response with HTTP 201 Created status.
    
    Args:
        message (str): Success message to be included in the response
        data (optional): Created resource data to be included in the response. Defaults to None.
    
    Returns:
        Response: DRF Response object with success flag, message, data, and 201 status code
    """
    return Response({"success": True, "message": message, "data": data} if data is not None else {"success": True, "message": message}, status=status.HTTP_201_CREATED)

def DELETE_SuccessResponse(message):
    """
    Returns a successful DELETE response with HTTP 204 No Content status.
    
    Args:
        message (str): Success message to be included in the response
    
    Returns:
        Response: DRF Response object with success flag, message, and 204 status code
    """
    return Response({"success": True, "message": message}, status=status.HTTP_204_NO_CONTENT)



# <------------------------ API ERROR Responses ------------------------>

# error responses
## for bad requests
def BadRequestException(message,data=None):
    """
    Returns a Bad Request error response with HTTP 400 status.
    Used when the client sends malformed or invalid request data.
    
    Args:
        message (str): Error message describing the bad request
    
    Returns:
        Response: DRF Response object with success=False, error message, and 400 status code
    """
    return Response({"success":False, "message": message,"error":data}, status=status.HTTP_400_BAD_REQUEST)

## for authentication denied or login failed
def UnauthorizedException(message):
    """
    Returns an Unauthorized error response with HTTP 401 status.
    Used when authentication is required but has failed or not been provided.
    
    Args:
        message (str): Error message describing the authentication failure
    
    Returns:
        Response: DRF Response object with success=False, error message, and 401 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_401_UNAUTHORIZED)

## for payment required
def PaymentRequiredException(message):
    """
    Returns a Payment Required error response with HTTP 402 status.
    Used when payment is required to access the requested resource.
    
    Args:
        message (str): Error message describing the payment requirement
    
    Returns:
        Response: DRF Response object with success=False, error message, and 402 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_402_PAYMENT_REQUIRED)

## for permission denied
def ForbiddenException(message):
    """
    Returns a Forbidden error response with HTTP 403 status.
    Used when the user is authenticated but lacks permission to access the resource.
    
    Args:
        message (str): Error message describing the permission denial
    
    Returns:
        Response: DRF Response object with success=False, error message, and 403 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_403_FORBIDDEN)

## for not found
def NotFoundException(message):
    """
    Returns a Not Found error response with HTTP 404 status.
    Used when the requested resource cannot be found.
    
    Args:
        message (str): Error message describing what was not found
    
    Returns:
        Response: DRF Response object with success=False, error message, and 404 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_404_NOT_FOUND)

## for method not allowed
def MethodNotAllowedException(message):
    """
    Returns a Method Not Allowed error response with HTTP 405 status.
    Used when the HTTP method is not supported for the requested resource.
    
    Args:
        message (str): Error message describing the method restriction
    
    Returns:
        Response: DRF Response object with success=False, error message, and 405 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

## for conflict
def ConflictException(message):
    """
    Returns a Conflict error response with HTTP 409 status.
    Used when the request conflicts with the current state of the resource.
    
    Args:
        message (str): Error message describing the conflict
    
    Returns:
        Response: DRF Response object with success=False, error message, and 409 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_409_CONFLICT)

## for request timeout
def RequestTimeoutException(message):
    """
    Returns a Request Timeout error response with HTTP 408 status.
    Used when the server times out waiting for the request from the client.
    
    Args:
        message (str): Error message describing the request timeout
    
    Returns:
        Response: DRF Response object with success=False, error message, and 408 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_408_REQUEST_TIMEOUT)



# <------------------------ SERVER and RELATED ERROR Responses ------------------------>

# internal Server Error
def InternalServerError(message):
    """
    Returns an Internal Server Error response with HTTP 500 status.
    Used when an unexpected condition prevents the server from fulfilling the request.
    
    Args:
        message (str): Error message describing the internal server error
    
    Returns:
        Response: DRF Response object with success=False, error message, and 500 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def NotImplementedException(message):
    """
    Returns a Not Implemented error response with HTTP 501 status.
    Used when the server does not support the functionality required to fulfill the request.
    
    Args:
        message (str): Error message describing what is not implemented
    
    Returns:
        Response: DRF Response object with success=False, error message, and 501 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_501_NOT_IMPLEMENTED)

def ServiceUnavailableException(message):
    """
    Returns a Service Unavailable error response with HTTP 503 status.
    Used when the server is temporarily overloaded or under maintenance.
    
    Args:
        message (str): Error message describing the service unavailability
    
    Returns:
        Response: DRF Response object with success=False, error message, and 503 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

def GatewayTimeoutException(message):
    """
    Returns a Gateway Timeout error response with HTTP 504 status.
    Used when the server acting as a gateway or proxy does not receive a timely response.
    
    Args:
        message (str): Error message describing the gateway timeout
    
    Returns:
        Response: DRF Response object with success=False, error message, and 504 status code
    """
    return Response({"success":False, "message": message}, status=status.HTTP_504_GATEWAY_TIMEOUT)
