from fastapi import FastAPI, Path, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []


class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/')
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id]})

@app.post("/user/{username}/{age}")
async def user_id(username: str = Path(min_length=5, max_length=20,description='Enter username', example='UrbanUser'),
                  age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> User:
    new_id = max((i.id for i in users), default=0) + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: int = Path(ge=1, le=100, description='Enter id', example='2'),
                       username: str = Path(min_length=5, max_length=20,description='Enter username', example='UrbanUser'),
                       age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> User:
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
            return i
    raise HTTPException(status_code=404, detail='User was not found')




@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    for k, v in enumerate(users):
        if v.id == user_id:
            del users[k]
            return v
    raise HTTPException(status_code=404, detail='User was not found')

