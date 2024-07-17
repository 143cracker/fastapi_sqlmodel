from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
Base = declarative_base()
class DbSession:
    def get_db1(self) :
        SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 
        engine = create_engine(   SQLALCHEMY_DATABASE_URL)
        SessionLocal=  sessionmaker(autocommit=False, autoflush=False, bind= engine )
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            return db
        except:
            db.close()
    def get_db2(self):
        SQLALCHEMY_DATABASE_URL = "sqlite:///./test1.db" 
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal=  sessionmaker(autocommit=False, autoflush=False, bind= engine )
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            return db
        except:
            db.close()
  
        

          
