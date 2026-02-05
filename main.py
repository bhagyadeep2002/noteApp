from datetime import datetime
from typing import List, Optional, Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Note
from schemas import NoteCreate, NoteResponse

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


@app.get("/notes", response_model=List[NoteResponse])
def get_notes(
    search: Optional[str] = None,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Note)
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Note.heading.ilike(search_filter)) | (Note.body.ilike(search_filter))
            )
        if start_date:
            query = query.filter(Note.created_at >= start_date)
        if end_date:
            query = query.filter(Note.created_at <= end_date)
        notes = query.order_by(Note.created_at.desc()).limit(limit).all()
        return notes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/notes")
def create_note(heading: str, body: str, db: Session = Depends(get_db)):
    try:
        note = Note(heading=heading, body=body)
        db.add(note)
        db.commit()
        db.refresh(note)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return note
