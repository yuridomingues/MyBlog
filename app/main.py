from fastapi import FastAPI
from .database import engine, Base
from .routers import articles

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MyBlog",
    description="Blog by Yuri Domingues",
    version="1.0"
)

app.include_router(articles.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to my personal blog"}
