from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers.wallet_router import router as wallet_router
from app.exception.exception import InsufficientFunds

app = FastAPI()


@app.exception_handler(InsufficientFunds)
async def insufficient_funds_exception_handler(request: Request, exc: InsufficientFunds):
    return JSONResponse(
        status_code=400,
        content={"detail": "Insufficient funds"},
    )


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


app.include_router(wallet_router)
