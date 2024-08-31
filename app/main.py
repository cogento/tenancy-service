from cogento_core.config.settings import settings, init_settings
from cogento_core.db.connection import engine, init_engine
from cogento_core.db.session import init_session_factory
from cogento_core.exceptions import EntityNotFoundError
from cogento_core.logging.config import logger, init_logger
from cogento_core.api.errors import http_error_handler, http422_error_handler, http404_error_handler
from cogento_core.api.handlers import create_start_app_handler, create_stop_app_handler
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.timing import add_timing_middleware
from starlette.exceptions import HTTPException

from controllers import company_controller, user_controller


def get_app() -> FastAPI:
    """
    Get the configured FastAPI application
    :return: FastAPI object
    """
    # Initialize settings singleton
    init_settings(prefix="TENANCY", settings_files=("../settings.toml", "../.secrets.toml"))
    init_logger(settings=settings)
    init_engine()
    init_session_factory(sql_engine=engine)

    app = FastAPI(
        title="Tenant Manager",
        description="Create and manage tenants",
        version=settings.version,
        debug=settings.debug
    )

    add_timing_middleware(app, record=logger.info, exclude="health")

    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.get("cors_allowed_origins", []),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.add_event_handler(event_type="startup", func=create_start_app_handler(app))
    app.add_event_handler(event_type="shutdown", func=create_stop_app_handler(app))

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_exception_handler(EntityNotFoundError, http404_error_handler)
    app.include_router(company_controller.router)
    app.include_router(user_controller.router)
    return app


APP = get_app()


@APP.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    :return: A simple JSON response
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(APP, host="0.0.0.0", port=8798)
