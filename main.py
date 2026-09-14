from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import engine, Base
from exceptions import NotFoundError, ConflictError, ValidationError, DatabaseError, ForbiddenError
from routers import author, book, user , vote   # <-- IMPORT ROUTER


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

# ĐĂNG KÝ ROUTER (GIỐNG "GẮN" MINI APP VÀO APP CHÍNH)
app.include_router(author.router)
app.include_router(book.router)
app.include_router(user.router)
app.include_router(vote.router)


# EXCEPTION HANDLER VẪN Ở ĐÂY (KHÔNG THAY ĐỔI)
@app.exception_handler(NotFoundError)
def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(ConflictError)
def conflict_handler(request, exc):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(ValidationError)
def validation_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(DatabaseError)
def database_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": str(exc)})
@app.exception_handler(ForbiddenError)
def access_error_handler(request, exc):
    return JSONResponse(status_code=403, content={"detail":str(exc)})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)