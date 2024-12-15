from fastapi import APIRouter,HTTPException,status,Depends
import auth
from database import cursor,conn
router=APIRouter(prefix='/buy',tags=['buying product'])
@router.get('/buyingProduct/{product_id}')
def buyProduct(product_id:int,user=Depends(auth.verify_access_token)):
    cursor.execute("""SELECT * FROM products WHERE id=%s """,(product_id,))
    product=cursor.fetchone()
    if product is not None:
      if user['role']=="buyer":
          cursor.execute("""UPDATE products SET available_quantity=available_quantity-1 WHERE id=%s""",(product_id,))
          conn.commit()
          raise HTTPException(status_code= status.HTTP_200_OK,detail="PRODUCT WILL DELIVER ON YOUR ADDDRESS")
      else:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="YOY ARE A SELLER NOT A BUYER")
    else:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id:{product_id} does not exist")
         
    
    

        
