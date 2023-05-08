from models import User, UserRole
from auth import get_password_hash

async def create_superuser():
    username = "admin"
    email = "admin@example.com"
    password = "111222"
    hashed_password = get_password_hash(password)

    superuser = await User.get_or_none(username=username)

    if not superuser:
        await User.create(
            username=username,
            email=email,
            password_hash=hashed_password,
            role=UserRole.ADMIN
        )
        print("Superuser created.")
    else:
        print("Superuser already exists.")
