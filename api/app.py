from typing import List, Optional
from datetime import date, datetime

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    Date,
    Enum,
    Float,
    Integer,
    String,
    Text,
    DECIMAL,
    JSON,
    Boolean,
    TIMESTAMP,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

# Database configuration - replace with actual credentials
DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Tour(Base):
    __tablename__ = "tours"

    id = Column(Integer, primary_key=True, index=True)
    about = Column(Text)
    history = Column(Text)
    expectations = Column(JSON)
    tips = Column(JSON)
    views = Column(Integer, default=0)
    inclusions = Column(Text)
    exclusions = Column(Text)
    tour_itinerary = Column(JSON)

    item = relationship("Item", back_populates="tour", uselist=False)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer)
    item_type = Column(Enum("tour", "hotel", "car"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    location = Column(String(100))
    image = Column(String(255))
    available_slots = Column(Integer, default=0)
    start_date = Column(Date)
    end_date = Column(Date)
    duration_days = Column(Integer)
    capacity = Column(Integer)
    rating = Column(Float, default=0)
    is_featured = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)
    vendor_id = Column(Integer)
    slug = Column(String(255))
    status = Column(Enum("active", "draft", "archived"), default="active")
    promo_price = Column(DECIMAL(10, 2))
    max_guests = Column(Integer)
    last_updated = Column(TIMESTAMP)
    tags = Column(Text)
    category_id = Column(Integer)

    tour = relationship(
        "Tour",
        back_populates="item",
        primaryjoin="Item.item_id==Tour.id",
        foreign_keys=[item_id],
        uselist=False,
    )


class TourSchema(BaseModel):
    id: int
    about: Optional[str]
    history: Optional[str]
    expectations: Optional[dict]
    tips: Optional[dict]
    views: int
    inclusions: Optional[str]
    exclusions: Optional[str]
    tour_itinerary: Optional[dict]

    class Config:
        orm_mode = True


class ItemSchema(BaseModel):
    id: int
    item_id: Optional[int]
    item_type: str
    title: str
    description: Optional[str]
    price: Optional[float]
    location: Optional[str]
    image: Optional[str]
    available_slots: Optional[int]
    start_date: Optional[date]
    end_date: Optional[date]
    duration_days: Optional[int]
    capacity: Optional[int]
    rating: float
    is_featured: bool
    created_at: Optional[datetime]
    vendor_id: Optional[int]
    slug: Optional[str]
    status: Optional[str]
    promo_price: Optional[float]
    max_guests: Optional[int]
    last_updated: Optional[datetime]
    tags: Optional[str]
    category_id: Optional[int]
    tour: Optional[TourSchema]

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    item_id: Optional[int] = None
    item_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    image: Optional[str] = None
    available_slots: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_days: Optional[int] = None
    capacity: Optional[int] = None
    rating: Optional[float] = None
    is_featured: Optional[bool] = None
    created_at: Optional[datetime] = None
    vendor_id: Optional[int] = None
    slug: Optional[str] = None
    status: Optional[str] = None
    promo_price: Optional[float] = None
    max_guests: Optional[int] = None
    last_updated: Optional[datetime] = None
    tags: Optional[str] = None
    category_id: Optional[int] = None


class ItemCreate(ItemBase):
    item_type: str
    title: str


class ItemUpdate(ItemBase):
    pass


class TourBase(BaseModel):
    about: Optional[str] = None
    history: Optional[str] = None
    expectations: Optional[dict] = None
    tips: Optional[dict] = None
    views: Optional[int] = 0
    inclusions: Optional[str] = None
    exclusions: Optional[str] = None
    tour_itinerary: Optional[dict] = None


class TourCreate(TourBase):
    pass


class TourUpdate(TourBase):
    pass


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items", response_model=List[ItemSchema])
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/items/{item_id}", response_model=ItemSchema)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=ItemSchema)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/items/{item_id}", response_model=ItemSchema)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.patch("/items/{item_id}", response_model=ItemSchema)
def patch_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}


@app.get("/tours/{tour_id}", response_model=TourSchema)
def read_tour(tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    return tour


@app.post("/tours", response_model=TourSchema)
def create_tour(tour: TourCreate, db: Session = Depends(get_db)):
    db_tour = Tour(**tour.dict())
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)
    return db_tour


@app.put("/tours/{tour_id}", response_model=TourSchema)
def update_tour(tour_id: int, tour: TourUpdate, db: Session = Depends(get_db)):
    db_tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not db_tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    for key, value in tour.dict().items():
        setattr(db_tour, key, value)
    db.commit()
    db.refresh(db_tour)
    return db_tour


@app.patch("/tours/{tour_id}", response_model=TourSchema)
def patch_tour(tour_id: int, tour: TourUpdate, db: Session = Depends(get_db)):
    db_tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not db_tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    update_data = tour.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tour, key, value)
    db.commit()
    db.refresh(db_tour)
    return db_tour


@app.delete("/tours/{tour_id}")
def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    db_tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not db_tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    db.delete(db_tour)
    db.commit()
    return {"detail": "Tour deleted"}

