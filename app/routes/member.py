from fastapi import APIRouter , Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

member_router = APIRouter()

#jinja2 설정
templates = Jinja2Templates(directory='views/templates')
member_router.mount('/static',StaticFiles(directory='views/static'), name='static')

@member_router.get('/Join', response_class=HTMLResponse)
def join(req: Request):
    return templates.TemplateResponse('Join.html',{'request':req})



@member_router.get('/login')
def login(req: Request):
    return templates.TemplateResponse('login.html',{'request':req})


@member_router.get('/Myinfo')
def myinfo(req: Request):
    return templates.TemplateResponse('Myinfo.html',{'request':req})