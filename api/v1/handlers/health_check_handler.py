from fastapi import APIRouter, HTTPException, status

health_check_router = APIRouter()


@health_check_router.post("/")
async def health_check_endpoint():
    try:
        return {
            "message": "API  created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))