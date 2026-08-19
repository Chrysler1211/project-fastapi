


from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, oauth2, models

router = APIRouter(
    tags=["Votes"]
)



@router.post("/Vote")
def User_Voting( data: schemas.Votes, db: Session = Depends(get_db), user: int = Depends(oauth2.get_user)):

    post_query = db.query(models.vote).filter(models.vote.Post_id == data.Post_id, models.vote.User_id == user.id)

    post = post_query.first()

    if data.Vote == 1:
        if post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"This Current user {user.id} Has already Vote this post with a id of {data.Post_id}")

        new_vote = models.vote(Post_id= data.Post_id, User_id= user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Success"}
    
    else:
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        post_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Success"}