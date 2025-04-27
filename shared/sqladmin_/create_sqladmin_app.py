from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend  # Измененный импорт

from shared.config import get_cached_settings
from shared.sqladmin_.model_view import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        if username == get_cached_settings().admin.ADMIN_USERNAME and password == get_cached_settings().admin.ADMIN_PASSWORD:
            request.session.update({"token": "authenticated"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if token == "authenticated":
            return True
        return False

def create_sqladmin_app():
    sqladmin_app = FastAPI(
        title="Health Guard",
        description="Admin for Health Guard project",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    sqladmin_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Добавляем SessionMiddleware для работы с сессиями
    from fastapi.middleware import Middleware
    from starlette.middleware.sessions import SessionMiddleware
    
    sqladmin_app.add_middleware(
        SessionMiddleware,
        secret_key=get_cached_settings().admin.SECRET_KEY,
        session_cookie="sqladmin_session"
    )

    # Используем правильный класс аутентификации
    authentication_backend = AdminAuth(secret_key=get_cached_settings().admin.SECRET_KEY)
    admin = Admin(
        app=sqladmin_app,
        engine=get_cached_sqlalchemy_db().engine,
        authentication_backend=authentication_backend
    )

    for model_view in SimpleMV.__subclasses__():
        admin.add_model_view(model_view)

    @sqladmin_app.get("/admin/login", response_class=HTMLResponse)
    async def login_form():
        return '''
        <form method="post" action="/admin/login">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Login</button>
        </form>
        '''

    @sqladmin_app.post("/admin/login")
    async def login(request: Request):
        auth = AdminAuth(secret_key=get_cached_settings().admin.SECRET_KEY)
        if await auth.login(request):
            return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return sqladmin_app