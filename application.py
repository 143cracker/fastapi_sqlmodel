# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.user_routes import CRUDUser
from dao.db_manager import DbSession

application = app = FastAPI(
    title="Testing Project",
    version="dev-1",
    description="Testing APIs for UI Integration",
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(CRUDUser().app, tags=["CRUD OPERATION"])
# obj=DbSession()
# print("skdjfdsk",obj)
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9002,
    )
    
  

