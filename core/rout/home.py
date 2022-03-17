from fastapi import APIRouter


home_router = APIRouter(
    tags=["home"],
    responses={404: {"description": "Not found"}}

)

@home_router.get("/")
async def index():
    return {"message": { "API INFO" : {
        "version": f"555"
    }}}
