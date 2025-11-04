from typing import Optional, List
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str  # MVP: demo amaçlı düz metin (prod'da hash)
    role: str = "avukat"  # avukat | stajyer | admin
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Tevkil(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    city: str
    court: str
    fee: float
    details: Optional[str] = ""
    owner_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Template(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str  # e.g., DIL-ICRA-001
    title: str
    body: str  # {deger} şeklinde alanlar

class Hearing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    court: str
    date: str  # ISO datetime string (MVP sade)
    room: Optional[str] = ""
    note: Optional[str] = ""
    owner_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
