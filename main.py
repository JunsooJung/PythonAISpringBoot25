# post 요청을 통해 이미지가 전송되면 인공지능 객체 탐지 모델을 이용해서 객체를 탐지하고
# 그 결과 이미지를 base64 인코딩된 문자열로 반화하는 서비스를 구현
# 라이브러릴 및 모듈 임포트

# 관련 라이브러리 설치 터미널에서 진행

# pip install fastapi uvicorn pydantic Pillow numpy requests
# pip install ultralytics opencv_python python-multipart

# fastapi : 비동기 웹 프레임워크 , 자동 openapi 문서 생성
# uvicorn 고성능 비동기 서버, asgi 표준 지원
# pydantic 데이터 검증 , 직렬화, 타입힌팅, 설정관리
# Pillow : 이미지 열기, 저장, 변환, 다양한 이미지 처리용
# numpy : 수치계산, 배열, 행렬연산, 수학함수 등
# requests : 간단한 http 요청 및 응답처리
# ultralytics : YOLOv8 객체 탐지 모델 제공
# opencv_python 이미지 및 비디오 처리, 컴퓨터 비전 기능
# python-multipart : 멀티파트 폼데이터 파싱

# uvicorn main:app --reload 로 실행


from fastapi import FastAPI, UploadFile, File, Form # 라우팅, 파일 관리, 폼 관리
from pydantic import BaseModel  # 데이터 모델정의
from PIL import Image           # 이미지 처리
import numpy as np              # 넘피
import io                       # 파일 입출력
import base64                   # 이미지 인/디코딩
from ultralytics import YOLO    # yolo8
import cv2                      # 컴퓨터 비전작업
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logging



app = FastAPI()

model = YOLO('yolov8n.pt') # yolo 8번 버전의 가중치모델

# 객체 탐지 클래스
# pydantic 사용 데이터 모델 정의
class DetectionResult(BaseModel):
    message : str       # 클라이언트 메세지
    image : str         # Base64 탐지 결과 이미지

# 객체 탐지 함수
# 객체 탐지를 위한 함수 정의로 모델에 이미지를 넣어 객체를 탐지하고
# 그 결과에서 바운딩 박스 정보를 추출한 후 이미지에
# 바인딩 박스와 클래스 이름, 신뢰도를 표시한 후 반환
def detect_objects(image:Image):
    img = np.array(image)           # 이미지 넘피 변환
    results = model(img)            # 객체 탐지
    class_names = model.names       # 클래스 이름 반환

    for result in results:
        boxes = result.boxes.xyxy
        confidences = result.boxes.conf
        class_ids = result.boxes.cls

        for box, confidences, class_ids in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int,box)
            label = class_names[int(class_ids)]
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0), 2)
            cv2.putText(img, text=f'{label} {confidences:.2f}',
                        org=(x1,y1), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.9, color=(255,0,0), thickness=2)


    result_image = Image.fromarray(img)
    return result_image
    # 결론 : yolo 모델 객체 탐지 수행, 박스화, 정확도 표시.
    # 결과 PIL 로 반환.

class LoggingMiddleware(BaseHTTPMiddleware):
    logging.basicConfig(level= logging.INFO)
    async def dispatch(self, request,call_next):
        logging.info(f"req : {request.method}{request.url}")
        response = await call_next(request)
        logging.info(f"Status code: {response.status_code}")
        return response
app.add_middleware(LoggingMiddleware)
#모든 요청 과 결과값 로깅




@app.get("/") #port : 8000
#async def read_root():
async def index():
    return {"message": "Jump to FastAPI"}



@app.post("/detect", response_model=DetectionResult)
async def detect_service(message:str = Form(...), file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))

    if image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    # 객체 탐지 수행
    result_image = detect_objects(image)

    #이미지 인코딩 base64
    buffered = io.BytesIO()
    result_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return DetectionResult(message=message, image=img_str)
    # 스프링부트 ->json 처리
    # detect 경로에 post 요청 처리
    # 클라에서 받은 이미지를 읽고 PIL 이미지 변환, 알파 채널 소거
    # https://developer.mozilla.org/ko/docs/Glossary/Alpha
    # 객체 탐지 함수 호출, 결과 이미지 반환
    # 다시 base64 인코딩
    # 받은 메세지와 이미지를 json 으로 반환







if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) # main.py 실행시 포트번호 기재
    # --reload << 수정후 저장시 재시작