

from fastapi import FastAPI, status, HTTPException, Depends, Response,APIRouter
from typing import List, Optional
import idna
from sqlalchemy import func
from .. import models,schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags= ["Get Profile Post","Create Profile Post", "Delete Profile Post",
           "Change a Profile Post"]
)


@router.get("/Profile", response_model=List[schemas.frontend_info])
def get_all_post(limit: int = 10 , skip: int = 0, search: Optional[str] = "", db: Session = Depends(get_db),user: int = Depends(oauth2.get_user) ):

   post = db.query(models.Post).filter(models.Post.Caption.contains(search)).limit(limit).offset(skip).all()

   new_post = db.query(models.Post, func.count(models.vote.Post_id).label("Votes")).join(
       models.vote, models.Post.id == models.vote.Post_id, isouter= True).group_by(models.Post.id).all()              


   return post




@router.get("/Profile/{id}", response_model=schemas.Voting_End)
def get_specific_post(id: int , db: Session = Depends(get_db), user: int = Depends(oauth2.get_user)):


    post = db.query(models.Post, func.count(models.vote.Post_id).label("Votes")).join(
        models.vote, models.Post.id == models.vote.Post_id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id
        ).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if post.Post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return post






@router.post("/Profile/Create", response_model=schemas.frontend_info_POST, status_code=status.HTTP_201_CREATED)
def Create_Post(data: schemas.frontend_info_PUT,  db: Session = Depends(get_db), user: int = Depends(oauth2.get_user)):

    post = models.Post(user_id = user.id, **data.dict())



    db.add(post)
    db.commit()
    db.refresh(post)

    return post








@router.delete("/Profile/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),user: int = Depends(oauth2.get_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    check = post.first()

    if check == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if check.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return {"Message": "Deleted Success!!"}



@router.put("/Profile/{id}", response_model=schemas.frontend_info_PUT)
def change_specific_post(id: int, data: schemas.frontend_info_PUT, db: Session = Depends(get_db),user: int = Depends(oauth2.get_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    check = post.first()

    if check == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if check.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    post.update(data.dict(), synchronize_session=False)
    db.commit()

    return post.first()






