from fastapi import Request, status, Form, File, UploadFile

from fastapi import APIRouter

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from app.schemas.gallery import NewGallery


from app.services.gallery import GalleryService

gallery_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')
gallery_router.mount('/static',StaticFiles(directory='views/static'), name='static')



@gallery_router.get('/list/{cpg}', response_class=HTMLResponse)
def list(req: Request, cpg:int ):
    # stpg = int((cpg -1)/10)*10+1 #stpg = start page / 페이지네이션 시작값
    gallist,cnt = GalleryService.select_gallery(cpg)
    # allpage = ceil(cnt/25)
    return templates.TemplateResponse(
        'gallery/list.html',{'request':req, 'gallist':gallist, 'cpg':cpg,
                           'stpg':1, 'allpage':1, 'baseurl':'/gallery/list'})



@gallery_router.get('/list/{ftype}/{fkey}/{cpg}', response_class=HTMLResponse)
def find(req: Request, ftype:str, fkey:str, cpg:int):
    # stpg = int((cpg -1)/10)*10+1 #stpg = start page / 페이지네이션 시작값
    # bdlist,cnt = BoardService.find_select_board(ftype, '%'+fkey+'%', cpg)
    # allpage = ceil(cnt/25)
    return templates.TemplateResponse(
        'gallery/list.html',{'request':req, 'gallist':None, 'cpg':cpg,
                           'stpg':1, 'allpage':1, 'baseurl':f'/gallery/list/{ftype}/{fkey}'})





@gallery_router.get('/write', response_class=HTMLResponse)
def write(req: Request):
    return templates.TemplateResponse('gallery/write.html',{'request':req})

#구글 recaptcha 확인 url
# https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
@gallery_router.post('/write')
async def writeok(title:str = Form(),userid:str = Form(),contents:str = Form(), attach: UploadFile = File()):
    res_url = '/gallery/list/1'

    # # print(title, userid, contents)
    # # print(attach.filename, attach.content_type, attach.size)
    #
    # UPLOAD_DIR = r'C:\Java\nginx-1.25.3\html\cdn' # r을 쓰는 이유는 \ 이걸 / 로 바꾸려고 그런듯
    # fname = UPLOAD_DIR + r'\\20240214' + attach.filename
    #
    # #비동기 처리를 위해 함수에 await 지시자 추가
    # #이럴 경우 함수 정의부분에 async 라는 지시자 추가 필요함
    # content = await attach.read() # 업로드한 파일의 내용을 비동기로 모두 읽어옴
    # with open(fname,'wb') as f: # write binary 라는 뜻
    #     f.write(content) # 파일 내용을 지정한 파일 이름으로 저장

    fname, fsize = await GalleryService.process_upload(attach)
    gdto = NewGallery(title=title, userid=userid, contents=contents)
    GalleryService.insert_gallery(gdto, fname, fsize)

    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)


@gallery_router.get('/view/{gno}', response_class=HTMLResponse)
def view(req: Request, gno:int):
    # bd=BoardService.selectone_board(gno)[0]
    # BoardService.update_count_board(gno)
    return templates.TemplateResponse('gallery/view.html',{'request':req, 'bd':None})

