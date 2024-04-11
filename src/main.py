from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from faker import Faker

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World. You can populate the database with `/populate-database` endpoint."}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# Populate the database with dummy data
@app.post("/populate-database")
async def populate_database(db: Session = Depends(get_db)):
    fake = Faker()
    dummy_users = [
        schemas.UserCreate(email=fake.email(), password=fake.password()),
        schemas.UserCreate(email=fake.email(), password=fake.password()),
    ]
    dummy_items = [
        schemas.ItemCreate(title=fake.word(), description=fake.word()),
        schemas.ItemCreate(title=fake.word(), description=fake.word()),
    ]

    for user_data in dummy_users:
        crud.create_user(db=db, user=user_data)

    for item_data in dummy_items:
        crud.create_user_item(db=db, item=item_data, user_id=1)  # Assuming user_id=1 for all items
    return {"message": "Database populated with dummy data"}
