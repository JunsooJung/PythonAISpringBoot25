from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
#요청의 중간다리
#요청 응답 반환전에 검증 등 특정 작업 껴넣기 가능
import logging #로깅 처리용 메소드




app = FastAPI(
    title="MBC AI STUDY",        #웹사이트 제목
    Description="MBC AI STUDY",  #설명
    version="0.0.1",
    docs_url=None, # docs 숨김
    redoc_url=None # redoc 숨김
)

class LoggingMiddleware(BaseHTTPMiddleware): #로그 콘솔 출력
    logging.basicConfig(level=logging.INFO) #로그 출력
    async def dispatch(self, request, call_next):
        logging.info(f"Request: {request.method}{request.url}")
        response = await call_next(request)
        logging.info(f"Status code: {response.status_code}")
        return response
app.add_middleware(LoggingMiddleware) #모든 요청 로그화 -> 로깅미들웨어


class Item(BaseModel): #item 객체 검증용
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
async def create_item(item: Item):
    #basemodel 데이터 모델링 쉽게 도와줌, 유효성 검사 수행
    # 422 오류코드 - 잘못된 데이터
    return item


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id : int, q : str = None):
    return {"item_id": item_id, "q": q}
# ITEM ID = ITEM ID
# q = Query
#postman => 프론트 없는 백엔드 테스트용
# 서버실행 uvicorn main:app --reload --port 8001
#some change


