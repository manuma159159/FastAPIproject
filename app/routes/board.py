from fastapi import Request, status

from fastapi import APIRouter

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from app.schemas.board import NewBoard
from app.services.board import BoardService
from math import ceil
board_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')
#board_router.mount('/static',StaticFiles(directory='views/static'), name='static')

# 페이징 알고리즘 : 전체
# 페이지당 게시글 수 : 25
# 1page : 1 ~ 25
# 2page : 26 ~ 50
# 3page : 51 ~ 75
#...
# npage : 25*(n-1)+1, 25*n

#페이지네이션 알고리즘
#현재 페이지에 다라 보여줄 페이지 블록 결정
#ex) 총 페이지 수 :27일 때
#cpg=1 : 1 2 3 4 5 6 7 8 9 10
#cpg=3 : 1 2 3 4 5 6 7 8 9 10
#cpg=9 : 1 2 3 4 5 6 7 8 9 10
#cpg=11 : 11 12 13 14 15 16 17 18 19 20
#cpg=17 : 11 12 13 14 15 16 17 18 19 20
#cpg=22 : 21 22 23 24 25 26 27 28 29 30
#cpg=n : m m+1 m+2 ..... m+9
# 따라서, cpg값에 따라 페이지 블록의 시작값 계산
#m=((cpg -1)/10)*10+1


@board_router.get('/list/{cpg}', response_class=HTMLResponse)
def list(req: Request, cpg:int ):
    stpg = int((cpg -1)/10)*10+1 #stpg = start page / 페이지네이션 시작값
    bdlist,cnt = BoardService.select_board(cpg)
    allpage = ceil(cnt/25)
    return templates.TemplateResponse(
        'board/list.html',{'request':req, 'bdlist':bdlist, 'cpg':cpg,
                           'stpg':stpg, 'allpage':allpage, 'baseurl':'/board/list'})



@board_router.get('/list/{ftype}/{fkey}/{cpg}', response_class=HTMLResponse)
def find(req: Request, ftype:str, fkey:str, cpg:int):
    stpg = int((cpg -1)/10)*10+1 #stpg = start page / 페이지네이션 시작값
    bdlist,cnt = BoardService.find_select_board(ftype, '%'+fkey+'%', cpg)
    allpage = ceil(cnt/25)
    return templates.TemplateResponse(
        'board/list.html',{'request':req, 'bdlist':bdlist, 'cpg':cpg,
                           'stpg':stpg, 'allpage':allpage, 'baseurl':f'/board/list/{ftype}/{fkey}'})





@board_router.get('/write', response_class=HTMLResponse)
def write(req: Request):
    return templates.TemplateResponse('board/write.html',{'request':req})

#구글 recaptcha 확인 url
# https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
@board_router.post('/write')
def writeok(bdto:NewBoard):
    res_url = '/captcha_error'
    if BoardService.check_captcha(bdto): #캡챠체크가 true라면 아래가 실행
        result = BoardService.insert_board(bdto)
        res_url = '/write_error'
        if result.rowcount > 0: res_url = '/board/list/1'

    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)


@board_router.get('/view/{bno}', response_class=HTMLResponse)
def view(req: Request, bno:int):
    bd=BoardService.selectone_board(bno)[0]
    BoardService.update_count_board(bno)
    return templates.TemplateResponse('board/view.html',{'request':req, 'bd':bd})

