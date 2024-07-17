from dao.db_manager import DbSession
from models.model import User
from sqlalchemy.orm import Session

class UserController:

    def __init__(self) -> None:
        pass

    def get_users(self):
  
        try:
            users = DbSession().get_db().query(User).all()
            if users:
               return   {"message":"User Data",'data':users,'error':True}

            else:
                return   {"message":"User Not Found",'data':[],'error':True}


        except Exception as e:
            return   {"message":f"something went wrong"+str(e),'data':[],'error':False}

    def delete_users(self,params):
  
        try:
            id=params.dict().get('id')
            with DbSession().get_db() as session:
                user_obj= session.query(User).filter(User.id==id).first()
                if user_obj is not None:
                    session.delete(user_obj)
                    session.commit()
                    return {"message":"User Delete Successfuly",'error':True}
                else:
                    return {"message":"User Not Found",'error':True}



        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"message":f"something went wrong"+str(e),'error':True}

    
    def create_users(self,params):
  
        try:
           
            db_session = DbSession()
            with db_session.get_db() as session:
                user_obj = User(**params.dict())
                session.add(user_obj)
                session.commit()
                session.refresh(user_obj)
            return {"message":"User Created Successfuly",'error':False}

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"message":f"something went wrong"+str(e),'error':True}
        

        
