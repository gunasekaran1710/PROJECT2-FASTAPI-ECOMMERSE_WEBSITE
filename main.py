from fastapi import FastAPI
from router import user,selling_product,buying_product
app=FastAPI()
app.include_router(user.router)
app.include_router(selling_product.router)
app.include_router(buying_product.router)
