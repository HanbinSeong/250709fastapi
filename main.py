from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import bord, user, product, order, test, board, todo

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 특정 출처의 도메인을 허용
    allow_credentials=False,  # 로그인 세션유지, 인증 토큰 사용 시 true
    allow_methods=["*"],  # GET, PUT, POST, DELETE
    allow_headers=["*"],  # 대표적인 예) Authorization, X-Custom-Header
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


# DB 테이블 생성 (개발용)
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(bord.router, prefix="/bords", tags=["Bords"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
app.include_router(test.router, prefix="/test", tags=["Test"])
app.include_router(board.router, prefix="/board", tags=["Board"])
app.include_router(todo.router, prefix="/todo", tags=["Todo"])
