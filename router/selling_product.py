from fastapi import APIRouter,HTTPException,status,Depends
from database import cursor,conn
import auth,schemas
router=APIRouter(prefix='/sell',tags=['selling_products'])
@router.post('/createProduct',response_model=schemas.productOut)
def createProduct(product:schemas.createProducts,user=Depends(auth.verify_access_token)):
    if "seller"==user['role']:
        cursor.execute("""INSERT INTO products(product_type,product_name,price,discount_in_percentage,available_quantity,seller_id) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *""",(product.product_type,product.product_name,product.price,product.discount_in_percentage,product.available_quantity,user['id']))
        product=cursor.fetchone()
        conn.commit()
        return product
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="YOU ARE A BUYER ,NOT A SELLER")

@router.get('/getOwnProduct',response_model=list[schemas.productOut])
def getOwnProduct(user=Depends(auth.verify_access_token)):
    if "seller"==user['role']:
        cursor.execute("""SELECT * FROM  products WHERE seller_id=%s""",(user['id'],))
        products=cursor.fetchall()
        return products
    else:
        raise HTTPException (status_code= status.HTTP_403_FORBIDDEN,detail="you are buyer, not a seller")
@router.get('/getAllProduct',response_model=list[schemas.productOut])
def getAllProduct(skip:int=0,limit:int=100,search:str="",user=Depends(auth.verify_access_token)):
    cursor.execute("""SELECT * FROM products WHERE product_type LIKE %s OR product_name LIKE %s LIMIT %s OFFSET %s""",(f"%{search}%",f"%{search}%",limit,skip))
    products=cursor.fetchall()
    return products
@router.put('/updateProduct/{product_id}',response_model=schemas.productOut)
def updateProduct(product_id:int,product:schemas.updateProduct,user=Depends(auth.verify_access_token)):
    cursor.execute("""SELECT * FROM products WHERE id=%s AND seller_id=%s""",(product_id,user['id']))
    exist_product=cursor.fetchone()
    if exist_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id:{product_id} or seller with seller_id{user['id']} does not exist ")
    fields_to_update={key:value for key,value in product .dict().items() if value is not None}
    if not fields_to_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="not valid fields to update")
    set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
    values = list(fields_to_update.values()) + [product_id]
    querry=f"UPDATE products SET {set_clause} WHERE id=%s RETURNING *"
    cursor.execute(querry,values)
    new_product=cursor.fetchone()
    conn.commit()
    return new_product
@router.delete('/deleteProduct/{product_id}')
def deleteProduct(product_id:int,user=Depends(auth.verify_access_token)):
    cursor.execute("""SELECT * FROM products WHERE id=%s""",(product_id,))
    product=cursor.fetchone()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id:{product_id} does not exist")
    if product['seller_id']!=user['id']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="YOU ARE NOT A AUTHORISED PERSON TO DELETE THE PRODUCT")
    cursor.execute("""DELETE from products WHERE id=%s RETURNING*""",(product_id,))
    conn.commit()
    raise HTTPException (status_code=status.HTTP_204_NO_CONTENT,detail=f"PRODUCT WITH ID:{product_id} IS DELETED SUCCESSFULLY")



