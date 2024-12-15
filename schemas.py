from pydantic import BaseModel,EmailStr
from typing import Optional
class userCreation(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:str
class userOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    role:str
class loginUser(BaseModel):
    email:EmailStr
    password:str
class token(BaseModel):
    token:str
class createProducts(BaseModel):
    product_type:str
    product_name:str
    price:int
    discount_in_percentage:int
    available_quantity:int
class productOut(BaseModel):
    id:int
    product_type:str
    product_name:str
    price:int
    discount_in_percentage:int
    available_quantity:int
    seller_id:int   
class updateProduct(BaseModel):
    product_type:Optional[str]=None
    product_name:Optional[str]=None
    price:Optional[int]=None
    discount_in_percentage:Optional[int]=None
    available_quantity:Optional[int]=None
