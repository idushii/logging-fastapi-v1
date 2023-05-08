from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.base import BaseHTTPMiddleware
from auth import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthMiddleware(BaseHTTPMiddleware):
    async def __call__(self, request: Request, call_next):
        if request.url.path not in ["/token"]:  # Список исключений (публичные роуты)
            try:
                token = request.headers["Authorization"].replace("Bearer ", "")
                user = await get_current_user(token)
                request.state.user = user
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e),
                )
        response = await call_next(request)
        return response
