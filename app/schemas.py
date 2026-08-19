
from typing import Optional

from pydantic import BaseModel,EmailStr,conint,ConfigDict
from datetime import datetime







class frontend_info(BaseModel):

    Caption : str
    Body : str
    Username : str
    user_id : int
    user_info : Account_info_Out
    id : int


class Votes(BaseModel):

    Post_id : int #user needs to enter a specific post id
    Vote: int = conint(le=1) # user needs to input either the two:  Remove vote <- 0 or 1 -> Vote(Like)

class Voting_End(BaseModel):

    Post : frontend_info
    Votes : int


    model_config = ConfigDict(from_attributes=True)




class frontend_info_POST(frontend_info):
    pass



class frontend_info_PUT(BaseModel):
    
    Caption : str
    Body : str
    Username : str


    class config():
        
        orm_mode = True


class Account_info(BaseModel):

    Gmail : EmailStr
    Name : str
    Password :  str




class User_login(BaseModel):

    Gmail : EmailStr
    Password : str


class token(BaseModel):

    id : int






class Account_info_Out(BaseModel):

    Gmail : EmailStr
    Name : str

    class config():

        orm_mode = True