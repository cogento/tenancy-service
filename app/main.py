from cogento_core.api import create_fastapi_app
from controllers import user_controller, company_controller

app = create_fastapi_app(
    title="Tenancy",
    description="Service responsible for managing tenants",
    additional_routers=[
        user_controller.router,
        company_controller.router
    ]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8798)
