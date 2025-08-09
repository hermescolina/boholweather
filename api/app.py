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


@app.get("/tours/{tour_id}", response_model=TourSchema)
def read_tour(tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    return tour

