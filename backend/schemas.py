from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr
from datetime import date, time
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

# --- Tevkil ---
class TevkilIn(BaseModel):
    title: str
    city: str
    court: str
    fee: float
    detail: Optional[str] = None

class TevkilOut(TevkilIn):
    id: int
    owner_id: int


# --- Duruşma (Hearing) ---
class HearingIn(BaseModel):
    title: str
    date: date
    time: Optional[time] = None
    court: Optional[str] = None
    note: Optional[str] = None

class HearingOut(HearingIn):
    id: int
    owner_id: int


# --- Dilekçe Şablonu listesi için (TemplateOut) ---
class TemplateOut(BaseModel):
    id: int
    code: str
    title: str

class RenderIn(BaseModel):
    template_id: int
    fields: Dict[str, str]
