import os
from datetime import datetime

import requests
from sqlalchemy import select, update, insert,func, or_
from app.dbfactory import session
from app.models.gallery import Gallery, GalAttach

# 이미지 파일 저장 경로
UPLOAD_DIR = r'C:\Java\nginx-1.25.3\html\cdn'


class GalleryService():
    @staticmethod
    def gallery_convert(gdto):
        data = gdto.model_dump()
        # data.pop('response') # 캡챠 확인용 변수 response는 제거 pop사용하면 변수 제거 response는 키 이름
        gal = Gallery(**data)
        data = {'userid':gal.userid, 'title':gal.title, 'contents':gal.contents}
        return data

    @staticmethod
    def insert_gallery(gdto,fname,fsize):
        # 변환된 이미지 정보를 gallery 테이블에 저장
        data = GalleryService.gallery_convert(gdto)

        with session() as sess:
            stmt = insert(Gallery).values(data)
            result = sess.execute(stmt)
            sess.commit()

            data = {'fname': fname, 'fsize': fsize,
                    'gno' : result.inserted_primary_key[0]}
            print(result.inserted_primary_key)
            stmt = insert(GalAttach).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result


    @staticmethod
    async def process_upload(attach):
        today = datetime.today().strftime('%Y%m%d%H%M%S')
        nfname =  f'{today}{attach.filename}' # 파일 이름
        fsize = attach.size  # 파일 크기
        # os.path.join(A,B) =< A/B (경로 생성)
        fname = os.path.join(UPLOAD_DIR, nfname) # os는 \\ 이거 알아서 가져다대주는거
        # fname = UPLOAD_DIR + r'\\20240214' + attach.filename
        content = await attach.read()
        with open(fname,'wb') as f:
            f.write(content)

        return nfname,fsize



    @staticmethod
    def select_gallery(cpg):
        stnum=(cpg-1)*25

        with (session() as sess):

            cnt= sess.query(func.count(Gallery.gno)).scalar() # 총 게시글 수

            stmt = select(Gallery.gno,Gallery.title,Gallery.userid,
                          Gallery.regdate,Gallery.views, GalAttach.fname)\
                .join_from(Gallery,GalAttach)\
                .order_by(Gallery.gno.desc()).offset(stnum).limit(25)
            result = sess.execute(stmt)

        return result, cnt

    # @staticmethod
    # def find_select_board(ftype, fkey, cpg):
    #     stnum=(cpg-1)*25
    #
    #     with (session() as sess):
    #
    #         stmt = select(Board.bno,Board.title,Board.userid,
    #                       Board.regdate,Board.views)
    #         # 동적 쿼리 작성 - 조건에 다라 where절이 바뀜
    #         myfilter = Board.title.like(fkey)
    #         if ftype=='userid':myfilter=Board.userid.like(fkey)
    #         elif ftype=='contents':myfilter=Board.contents.like(fkey)
    #         elif ftype=='titconts':myfilter=or_(Board.title.like(fkey), Board.contents.like(fkey))
    #         stmt = stmt.filter(myfilter)\
    #             .order_by(Board.bno.desc()).offset(stnum).limit(25)
    #         result = sess.execute(stmt)
    #
    #         cnt= sess.query(func.count(Board.bno)).filter(myfilter).scalar() # 검색하고 나온 결과물의 총 개수를 위해 뒤에 씀
    #
    #     return result ,cnt

    @staticmethod
    def selectone_gallery(gno):

        with (session() as sess):

            stmt = select(Gallery,GalAttach)\
                .join_from(Gallery,GalAttach)\
                .filter_by(gno=gno)
            result = sess.execute(stmt).first()
        return result


    # @staticmethod
    # def update_count_board(bno):
    #
    #     with (session() as sess):
    #
    #         stmt = update(Board).filter_by(bno=bno).values(views=Board.views+1)
    #         result = sess.execute(stmt)
    #         sess.commit()
    #
    #     return result



    #구글 recaptcha 확인 url
    # https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
    # @staticmethod
    # def check_captcha(bdto):
    #     data = bdto.model_dump()
    #     req_url = 'https://www.google.com/recaptcha/api/siteverify'
    #     params = {'secret':'#',
    #               'response':data['response']
    #               }
    #     res = requests.get(req_url, params=params)
    #     result = res.json()
    #     # print('check',result)
    #     #
    #     # return result['success']
    #     return True





