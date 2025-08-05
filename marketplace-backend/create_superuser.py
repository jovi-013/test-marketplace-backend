import asyncio
from getpass import getpass
from marketplace.database import SessionLocal
from marketplace.schemas import UserCreate
from marketplace.crud import create_user, get_user_by_email

async def main():
    print("Creating admin user...")
    email = input("Enter email: ")
    password = getpass("Enter password: ")
    
    db = SessionLocal()
    
    db_user = await get_user_by_email(db, email=email)
    if db_user:
        print("User with this email already exists.")
        await db.close()
        return

    admin_user = UserCreate(email=email, password=password, user_type="admin")
    await create_user(db, user=admin_user)
    
    print(f"Admin user {email} created successfully.")
    await db.close()

if __name__ == "__main__":
    asyncio.run(main())