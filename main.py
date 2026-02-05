from datetime import datetime
from typing import List, Optional

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


@app.get("/", tags=["Health"])
def home():
    return {"message": "hello world"}


@app.get("/notes", response_model=List[NoteResponse], tags=["Notes"])
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


@app.post("/notes", response_model=NoteResponse, tags=["Notes"])
def create_note(noteData: NoteCreate, db: Session = Depends(get_db)):
    try:
        note = Note(heading=noteData.heading, body=noteData.body)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/notes/{note_id}", tags=["Notes"])
def delete_note(note_id: str, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        db.delete(note)
        db.commit()
        return {"message": "Note deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
