from fastapi import APIRouter,HTTPException,status,Depends
from database import cursor,conn
import auth,schemas
router=APIRouter(prefix='/users',tags=['users'])
@router.post('/userCreation',response_model=schemas.userOut)
def userCreation(user:schemas.userCreation):
 if user.role=='buyer'or user.role=='seller':
   try:
      hashed_password=auth.password_hash(user.password)
      cursor.execute("""INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s) RETURNING name,email,role,id;""",(user.name,user.email,hashed_password,user.role))
      new_user=cursor.fetchone()
      conn.commit()
      return new_user
   except Exception as error:
      conn.rollback()
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"the {user.email} alrady exist")
 else:
   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="NOT VALID USER ROLE.PLEASE CHOOSE THE CORRECT ROLE:buyer or seller")
@router.get('/login')
def login(userCredentials:schemas.loginUser):
  cursor.execute("""SELECT id,email,password from users WHERE email=%s""",(userCredentials.email,))
  user=cursor.fetchone()
  if user:
    verify=auth.verify_password(userCredentials.password,user['password'])
    if verify is True:
      access_token=auth.create_access_token({"id":user['id']})
      return {"token":access_token}
    else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="INVALID CREDENTIALS")
  else:
    raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="INVALID CREDENTIALS")
