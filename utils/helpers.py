import jwt
import datetime
from enum import Enum
import time
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Any, Union

from fastapi import HTTPException


# Secret key for encoding and decoding JWT tokens
SECRET_KEY = 'your@secret@key'

class HTTPStatus(Enum):
    success = (200, 'success')
    created = (201, 'created')
    accepted = (202, 'accepted')
    no_content = (204, 'no content')
    bad_request = (400, 'bad_request')
    unauthorized = (401, 'unauthorized request')
    unauthorized_new = (402, 'unauthorized request')
    not_found = (404, 'resource not found')
    conflict = (409, 'duplicate conflict')
    unprocessable_entity = (422, 'Unprocessable Entity')
    method_failure = (420, 'Method Failure')
    error = (500, 'application error occured')
    existing_session = (435, 'session already exists')


class AppStatus(Enum):
    success = {'code': 200, 'message': 'success'}
    logging_error = {'code': 900, 'message': 'error in logging request'}

class ExceptionMessage(Enum):
    aws_connecion_error = 'Error in connecting to AWS resources'
    aws_cloudwatch_loggroup_exception = 'Error in creating application events log group'
    aws_cloudwatch_logstream_exception = 'Error in creating application events log stream'
    aws_cloudwatch_log_exception = 'Error in sending application events log'
    aws_s3_write_exception = 'Error in writing to S3 bucket'
    aws_s3_download_exception = 'Error in generating download link'
    # DB #
    db_connection_error = 'Error in connecting to host database'
    db_cursor_fetch_error = 'Error in fetching results from database'
    success = (200, 'success')
    created = (201, 'created')
    accepted = (202, 'accepted')
    no_content = (204, 'no content')
    bad_request = (400, 'bad_request')
    unauthorized = (401, 'unauthorized request')
    unauthorized_new = (402, 'unauthorized request')
    not_found = (404, 'resource not found')
    conflict = (409, 'duplicate conflict')
    unprocessable_entity = (422, 'Unprocessable Entity')
    method_failure = (420, 'Method Failure')
    error = (500, 'application error occured')
    existing_session = (435, 'session already exists')

class AWSConnectionException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_connecion_error.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class AWSCloudWatchLogGroupException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_cloudwatch_loggroup_exception.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class AWSCloudWatchLogStreamException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_cloudwatch_logstream_exception.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class AWSLogException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_cloudwatch_log_exception.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class AWSS3WriteException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_s3_write_exception.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)

class AWSS3PresignedURLException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_s3_write_exception.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)

class DBConnectionException(Exception):
    def __init__(self, obj, message=ExceptionMessage.db_connection_error.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class DBCursorFetchException(Exception):
    def __init__(self, obj, message=ExceptionMessage.db_cursor_fetch_error.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class CustomException(HTTPException):
    def __init__(self, status_code: int, status: HTTPStatus, fetch_time: Union[int, float], row_count: int, result: Any,
                 request_logging: Any, response_logging: Any):
        self.status_code = status_code
        self.status = status
        self.fetch_time = fetch_time
        self.row_count = row_count
        self.result = result
        self.request_logging = request_logging
        self.response_logging = response_logging
        super().__init__(status_code=self.status_code, detail=None)




class jwtBearer(HTTPBearer):
    def __int__(self, auto_Error: bool = True):
        super(jwtBearer, self.__int__(auto_Error=auto_Error)
              )

    async def __call__(self, request: Request):
        start_time = time.time()
        try:

            credentails: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
            if credentails:
                if not credentails.scheme == "Bearer":
                    raise HTTPException(status_code=403, detail="Invalid Token")
                return credentails.credentials
            else:
                raise HTTPException(status_code=403, detail="Invalid Token")
        except Exception as e:
            raise CustomException(status_code=HTTPStatus.unauthorized.value[0], status=HTTPStatus.unauthorized.value[1],
                                  fetch_time=time.time()-start_time, row_count=0,
                                  result=e.detail if e.detail else "Invalid Token", request_logging=None, response_logging=None)

 


def generate_jwt(payload):
    secret_key=SECRET_KEY
    algorithm='HS256'
    expiration_minutes=30
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    payload['exp'] = expiration
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def validate_jwt(token):
    try:
        secret_key=SECRET_KEY
        algorithms=['HS256']
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return payload
    except jwt.ExpiredSignatureError:
        return {"message":"Token has expired"}
    except jwt.InvalidTokenError:
        return {"message":"Invalid token"}

