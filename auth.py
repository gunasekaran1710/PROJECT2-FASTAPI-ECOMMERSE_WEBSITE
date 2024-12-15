from passlib.context import CryptContext
import jwt
from database import cursor,conn
from fastapi.security import OAuth2PasswordBearer
from fastapi import status,HTTPException,Depends
from datetime import datetime,timedelta,timezone
oauth2_schema=OAuth2PasswordBearer(tokenUrl='token')
access_token_expire_minutes=30
ALGORITHM="HS256"
secret_key="VERY  VERY SECRET"
credential_exception=HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="INVALID CREDETIALS",headers={"WWW-Authenticate":"Bearer"})
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def password_hash(password):
    hashed_password=pwd_context.hash(password)
    return hashed_password
def verify_password(password,hashed_password):
    verification=pwd_context.verify(password,hashed_password)
    return verification
def create_access_token(data):
    to_encoded=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=access_token_expire_minutes)
    to_encoded.update({"exp":expire})
    jwt_token=jwt.encode(to_encoded,secret_key,algorithm=ALGORITHM)
    return jwt_token
def verify_access_token(token:str=Depends(oauth2_schema)):
    try:
        user=jwt.decode(token,secret_key,algorithms=ALGORITHM)
        cursor.execute("""SELECT id,name,email,role FROM users WHERE id=%s""",(user['id'],))
        user=cursor.fetchone()
        if user is None:
            raise credential_exception
        return user
    except jwt.ExpiredSignatureError:
        raise credential_exception
    except jwt.DecodeError:
        raise credential_exception

    




