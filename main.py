from datetime import datetime
from typing import Union

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Note

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "hello world"}


@app.get("/notes/")
def get_notes(date: Union[datetime, None] = None, db: Session = Depends(get_db)):
    if date:
        notes = db.query(Note).filter(Note.created_at >= date).all()
    else:
        notes = db.query(Note).all()
    return notes


@app.post("/note")
def create_note(heading: str, body: str, db: Session = Depends(get_db)):
    note = Note(heading=heading, body=body)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
