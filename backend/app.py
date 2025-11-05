from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

from sqlmodel import Session, select
from typing import List
import re
from io import BytesIO

from jinja2 import Template as JinjaTemplate
from docx import Document
from pydantic import BaseModel

from models import User, Tevkil, Template, Hearing
from schemas import UserIn, UserOut, LoginIn, TevkilIn, TevkilOut, HearingIn, HearingOut, TemplateOut
from db import engine, init_db

app = FastAPI(title="YargıNet MVP API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
# ---- Şablon değişkenlerini çıkar ({{degisken}}) ----
VAR_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")

def extract_vars(text: str):
    return sorted(set(VAR_RE.findall(text or "")))

class RenderIn(BaseModel):
    code: str
    data: dict  # {"mukekkil": "...", "borclu": "..."}
def get_s():
    with Session(engine) as s:
        yield s

@app.get("/", tags=["meta"])
def root():
    return {"name":"YargıNet MVP API","version":"0.1.0","docs":"/docs"}

# --- Users ---
@app.post("/users", response_model=UserOut, tags=["auth"])
def register(user: UserIn, s: Session = Depends(get_s)):
    exists = s.exec(select(User).where(User.email == user.email)).first()
    if exists:
        raise HTTPException(400, "Email kayıtlı")
    u = User(email=user.email, password=user.password, role=user.role or "avukat")
    s.add(u); s.commit(); s.refresh(u)
    return UserOut(id=u.id, email=u.email, role=u.role)

@app.post("/login", tags=["auth"])
def login(payload: LoginIn, s: Session = Depends(get_s)):
    u = s.exec(select(User).where(User.email == payload.email)).first()
    if not u or u.password != payload.password:
        raise HTTPException(401, "Geçersiz kimlik bilgisi")
    # MVP: gerçek JWT yerine basit token
    token = f"token-{u.id}-{int(datetime.utcnow().timestamp())}"
    return {"token": token, "user":{"id":u.id,"email":u.email,"role":u.role}}

# --- Tevkil ---
@app.get("/tevkil", response_model=List[TevkilOut], tags=["tevkil"])
def list_tevkil(s: Session = Depends(get_s)):
    rows = s.exec(select(Tevkil).order_by(Tevkil.created_at.desc())).all()
    return rows

@app.post("/tevkil", response_model=TevkilOut, tags=["tevkil"])
def create_tevkil(item: TevkilIn, s: Session = Depends(get_s)):
    # MVP: owner_id=1 gibi kabul
    owner_id = 1
    t = Tevkil(**item.model_dump(), owner_id=owner_id)
    s.add(t); s.commit(); s.refresh(t)
    return t

# --- Hearings ---
@app.get("/hearings", response_model=List[HearingOut], tags=["hearings"])
def list_hearings(s: Session = Depends(get_s)):
    rows = s.exec(select(Hearing).order_by(Hearing.date.desc())).all()
    return rows

@app.post("/hearings", response_model=HearingOut, tags=["hearings"])
def create_hearing(h: HearingIn, s: Session = Depends(get_s)):
    owner_id = 1
    row = Hearing(**h.model_dump(), owner_id=owner_id)
    s.add(row); s.commit(); s.refresh(row)
    return row

# --- Templates & Dilekçe ---
@app.get("/templates", response_model=List[TemplateOut], tags=["dilekce"])
def list_templates(s: Session = Depends(get_s)):
    rows = s.exec(select(Template)).all()
    return [TemplateOut(id=r.id, code=r.code, title=r.title) for r in rows]

# 1) Şablonları listele + ihtiyaç duyduğu alanları döndür
@app.get("/templates", response_model=List[TemplateOut], tags=["dilekce"])
def list_templates(s: Session = Depends(get_s)):
    rows = s.exec(select(Template)).all()
    out = []
    for r in rows:
        # {{degisken}} yakala
        vars_ = re.findall(r"\{\{(\w+)\}\}", r.body or "")
        out.append(TemplateOut(id=r.id, code=r.code, title=r.title, variables=vars_))
    return out

# 2) Önizleme: metni doldurup düz HTML/metin döndür
@app.post("/templates/render")
def render_template(payload: RenderIn):
    with Session(engine) as s:
        t = s.exec(select(Template).where(Template.code == payload.code)).first()
        if not t:
            raise HTTPException(status_code=404, detail="Şablon bulunamadı")

    html = JinjaTemplate(t.body or "").render(**payload.data)
    return {"html": html}


# 3) DOCX oluşturup indir
@app.post("/templates/docx")
def render_docx(payload: RenderIn):
    with Session(engine) as s:
        t = s.exec(select(Template).where(Template.code == payload.code)).first()
        if not t:
            raise HTTPException(status_code=404, detail="Şablon bulunamadı")

    filled = JinjaTemplate(t.body or "").render(**payload.data)

    doc = Document()
    for line in filled.split("\n"):
        doc.add_paragraph(line)

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)

    filename = f"{payload.code}.docx"
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
