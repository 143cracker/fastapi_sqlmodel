from functools import wraps
from fastapi import Request, HTTPException,FastAPI,status
import time
import base64, json
import requests
from utils.helpers import HTTPStatus,validate_jwt
def jwt_auth_required(f):
    @wraps(f)
    def authenticate( *args, **kwargs):
        authtoken=''
        start_time = time.time()
        request = kwargs.get('request')
        req_path = request.scope.get('path')[1:]

        if 'Authorization' in request.headers or 'authorization' in request.headers:
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
                authtoken = token
            else:
                token = request.headers['authorization']
                authtoken = token
        else:
            raise HTTPException(status_code=HTTPStatus.unauthorized.value[0], detail="Credentials not sent")
        #here we check in valid or not 
        if authtoken:
            payload = validate_jwt(authtoken)
            if "message" in payload:
                raise HTTPException(status_code=HTTPStatus.unauthorized.value[0], detail="Credentials not sent")

        else:
            raise CustomException(status_code=HTTPStatus.unauthorized.value[0], status=HTTPStatus.unauthorized.value[1],
                                      fetch_time=time.time() - start_time, row_count=0,
                                      result = {
                                          'payload': [],
                                          'errorStack': [],
                                         'message': "Invalid or Expired Token"
                                      },
                                  request_logging=None, response_logging=None)

        return f(*args, **kwargs)

    return authenticate






  