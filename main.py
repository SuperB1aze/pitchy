import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.app.routers.auth_routes import router_auth
from src.app.routers.user_routes import router_user
from src.app.routers.form_routes import router_form
from src.app.routers.doc_routes import router_doc

app = FastAPI(title = 'Pitchy API', docs_url = '/api/v1/docs', redoc_url = '/api/v1/redoc')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('FRONTEND_ORIGIN', 'http://localhost:3000')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app_v1 = APIRouter(prefix = '/api/v1')

app_v1.include_router(router_auth)
app_v1.include_router(router_user)
app_v1.include_router(router_form)
app_v1.include_router(router_doc)

app.include_router(app_v1)

if __name__ == '__main__':
    uvicorn.run("main:app", reload = True)