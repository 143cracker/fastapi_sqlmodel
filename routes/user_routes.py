import time
from fastapi import Query, Depends, APIRouter
from starlette.requests import Request
from controller.user_controller import UserController
from entity.basemodel import UserBase,UserId
class CRUDUser:
    application=app = {}

    def __init__(self):
        self.app = APIRouter()
        self.application = self.app
        self.users_controller = UserController()
        self.__add_routes()

    def __add_routes(self):
        self.app.add_api_route(path='/getUserInfo', endpoint=self.get_user_info, methods=['GET'])

        self.app.add_api_route(
            path='/createUserInfo'
            , endpoint=self.create_user
            , methods=['POST']
            )

        
        self.app.add_api_route(
            path='/deleteUserInfo'
            , endpoint=self.delete_user
            , methods=['DELETE']
            )

 
    async def get_user_info(self, request: Request):
        start_time = time.time()
        # add logic for api processing here

        rtn = self.users_controller.get_users()


        return {"time":time.time()-start_time,"resuts":rtn}
    
    async def create_user(self, request: Request,params:UserBase):
        start_time = time.time()
        # add logic for api processing here

        rtn = self.users_controller.create_users(params)


        return {"time":time.time()-start_time,"resuts":rtn}

    async def delete_user(self, request: Request,params:UserId):
        start_time = time.time()
        # add logic for api processing here

        rtn = self.users_controller.delete_users(params)


        return {"time":time.time()-start_time,"resuts":rtn}
