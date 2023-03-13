from typing import Union

from fastapi import FastAPI

from agroturismo_api.routes import main_router

app = FastAPI(
    title="Agroturismo API",
    description="API para o projeto de agroturismo 🚀",
    contact={
        "name": "Douglas Gusson",
        "url": "http://capixaba.dev/",
        "email": "douglas@capixaba.dev",
    },
)

app.include_router(main_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
