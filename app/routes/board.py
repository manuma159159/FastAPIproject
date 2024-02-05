from fastapi import APIRouter

board_router = APIRouter()

@board_router.get('/list')
def list():
    return {'msg':'Hello, Board list!'}


@board_router.get('/write')
def write():
    return {'msg':'Hello, Board write!'}


@board_router.get('/view')
def view():
    return {'msg':'Hello, Board view!'}