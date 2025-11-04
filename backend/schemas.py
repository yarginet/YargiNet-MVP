from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "avukat"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TevkilIn(BaseModel):
    title: str
    city: str
    court: str
    fee: float
    details: Optional[str] = ""

class TevkilOut(BaseModel):
    id: int
    title: str
    city: str
    court: str
    fee: float
    details: Optional[str]
    owner_id: int

class HearingIn(BaseModel):
    court: str
    date: str
    room: Optional[str] = ""
    note: Optional[str] = ""

class HearingOut(BaseModel):
    id: int
    court: str
    date: str
    room: Optional[str]
    note: Optional[str]
    owner_id: int

class TemplateOut(BaseModel):
    id: int
    code: str
    title: str

class RenderIn(BaseModel):
    template_id: int
    fields: Dict[str, str]
