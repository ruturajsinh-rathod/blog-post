from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

import constants
from apps.handlers import start_exception_handlers
from apps.v1.auth.controllers import auth_router as v1_auth_router
from apps.v1.blog.controllers import blog_router as v1_blog_router
from apps.v1.blog.controllers import like_router as v1_like_router
from apps.v1.user.controllers import role_router as v1_role_router
from apps.v1.user.controllers import user_router as v1_user_router
from config import settings


def init_routers(_app: FastAPI) -> None:
    """
    Initialize all routers.
    """
    _app.include_router(v1_blog_router)
    _app.include_router(v1_auth_router)
    _app.include_router(v1_user_router)
    _app.include_router(v1_role_router)
    _app.include_router(v1_like_router)


def root_health_path(_app: FastAPI) -> None:
    """
    Health Check Endpoint.
    """

    @_app.get("/", include_in_schema=False)
    def root() -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": constants.SUCCESS}
        )

    @_app.get("/healthcheck", include_in_schema=False)
    def healthcheck() -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": constants.SUCCESS}
        )


def init_middlewares(_app: FastAPI) -> None:
    """
    Middleware initialization.
    """
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app(debug: bool = False) -> FastAPI:
    """
    Create a Initialize the FastAPI app.
    """
    _app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc" if debug else None,
    )
    init_routers(_app)
    root_health_path(_app)
    init_middlewares(_app)
    start_exception_handlers(_app)
    add_pagination(_app)
    return _app


debug_app = create_app(debug=True)
