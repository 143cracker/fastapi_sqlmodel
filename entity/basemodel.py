# schemas.py

from typing import List, Optional, Union
from fastapi import Query
from pydantic import BaseModel, Field,validators

class UserBase(BaseModel):
    name: str
    email: str



class UserId(BaseModel):
    id: int

