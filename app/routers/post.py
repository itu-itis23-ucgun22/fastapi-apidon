from typing import List
from fastapi import FastAPI,status,HTTPException,Depends,APIRouter,Response
from sqlalchemy.orm import Session
from .. import models, schemas,oauth2
from ..database import get_db

router=APIRouter(
     prefix="/posts",
     tags=['Posts']
)



@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.CreatePost,db: Session = Depends(get_db),user_id:str=Depends(oauth2.get_current_user)):
    print(user_id)
    new_post= models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}")
def get_post(id: str, db: Session = Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)

   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f"post can not with {id} id")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id)
    

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"got deligi{id}")
    
    post.delete(synchronize_session=False)
                        
    db.commit()
    return post
    
@router.put("/{id}",response_model=list[schemas.Post])
def update_post(id: int, post: schemas.CreatePost,db: Session = Depends(get_db)):
    updatedpost=db.query(models.Post).filter(models.Post.id==id)
    poster=updatedpost.first()
    if poster == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"got deliigi{id}")
    updatedpost.update(post.dict(),synchronize_session=False)
    db.commit()
        
    return updatedpost
