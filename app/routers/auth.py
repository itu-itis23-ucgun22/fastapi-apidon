from fastapi import Depends,HTTPException,Response,APIRouter,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oauth2
 

router=APIRouter(tags=['Authentication'])
 
@router.post('/login')
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="ndk")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="bnlkb")
    
    accessed_token=oauth2.create_access_token(data={"user_id":user.id})
    return {f"token":accessed_token ,"token_type":"bearer_token"}