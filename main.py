from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional

# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Aaditya%2332%401@localhost/sqlalchemy project"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: int
    class Config:
        from_attributes = True

class SequentialItemResponse(BaseModel):
    display_id: int
    id: int
    name: str
    description: Optional[str] = None
    price: int

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD functions
def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).order_by(Item.id).offset(skip).limit(limit).all()

def get_items_sequential(db: Session, skip: int = 0, limit: int = 100):
    items = db.query(Item).order_by(Item.id).offset(skip).limit(limit).all()
    sequential_items = []
    for index, item in enumerate(items, start=skip + 1):
        sequential_items.append({
            "display_id": index,
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price
        })
    return sequential_items

def find_available_id(db: Session):
    # Get all existing IDs
    existing_ids = {item.id for item in db.query(Item.id).all()}
    # Find the first missing ID starting from 1
    for potential_id in range(1, max(existing_ids) + 2 if existing_ids else 2):
        if potential_id not in existing_ids:
            return potential_id
    return None

def create_item(db: Session, item: ItemCreate):
    # Find available ID to fill gaps
    available_id = find_available_id(db)
    if available_id:
        db_item = Item(id=available_id, **item.model_dump())
    else:
        db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item_update: ItemUpdate):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# FastAPI app
app = FastAPI(title="CRUD API with FastAPI and SQLAlchemy")

@app.post("/items/", response_model=ItemResponse, status_code=201)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@app.get("/items/", response_model=List[ItemResponse])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_items(db, skip=skip, limit=limit)

@app.get("/items/sequential/", response_model=List[SequentialItemResponse])
def read_items_sequential(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_items_sequential(db, skip=skip, limit=limit)

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_existing_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    db_item = update_item(db, item_id, item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", status_code=204)
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    db_item = delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return
