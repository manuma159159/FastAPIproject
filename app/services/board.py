from sqlalchemy import insert
from sqlalchemy import select
from app.models.member import Member
from app.dbfactory import session
from app.models.board import Board

class BoardService():
    @staticmethod
    def board_convert(bdto):
        data = bdto.model_dump()
        bd = Board(**data)
        data = {'userid':bd.userid, 'title':bd.title, 'contents':bd.contents}
        return data

    @staticmethod
    def insert_board(bdto):
        # 변환된 회원정보를 member 테이블에 저장
        data = BoardService.board_convert(bdto)

        with session() as sess:
            stmt = insert(Board).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result

    @staticmethod
    def select_board():

        with (session() as sess):

            stmt = select(Board.bno,Board.title,Board.userid,
                          Board.regdate,Board.views).order_by(Board.bno.desc()).offset(0).limit(25)
            result = sess.execute(stmt)


        return result









