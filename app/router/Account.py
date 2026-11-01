


from fastapi import FastAPI, status, HTTPException, Depends, Response, APIRouter
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from ..import models,schemas,utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Create & Login"]
)

@router.post("/Register", status_code=status.HTTP_201_CREATED ,response_model=schemas.Account_info_Out)
def Create_Account(data: schemas.Account_info, db: Session = Depends(get_db)):


    data.Password = utils.hash(data.Password)

    create_account = models.Account(**data.dict())
   

    db.add(create_account)
    db.commit()
    db.refresh(create_account)


    print("CREATED ID:", create_account.id)
    print("CREATED EMAIL:", create_account.Gmail)

    return create_account


@router.post("/Login", response_model=schemas.Token)
def user_login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    login = db.query(models.Account).filter(models.Account.Gmail == data.username).first()

    if not login:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gmail doesn't exist")
    
    if not utils.verify(data.password, login.Password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password doesn't exist")

    access_token = oauth2.create_token({"user_id": login.id})

    return {"id": login.id, "access_token": access_token, "token_type": "bearer"}




@router.post("/Users")
def get_all_Accounts(db: Session = Depends(get_db), user: int = Depends(oauth2.get_user)):

    all = db.query(models.Account).all()
    
    return all




@router.get("/Users/{id}", response_model=schemas.Account_info_Out)
def retrive_account(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_user)):

    retrive_user = db.query(models.Account).filter(models.Account.id == id).first()

    if retrive_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="NOT FOUND")



    if retrive_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Your not the owner of the account")

    return retrive_user


