import os
from sqlmodel import SQLModel, create_engine, Session, select
from models import User, Tevkil, Template, Hearing

# Ortam değişkeninden veritabanı bağlantısını al
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///yarginet.db")

# Eğer Render'da PostgreSQL varsa ona bağlan, yoksa local SQLite'a dön
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def init_db():
    SQLModel.metadata.create_all(engine)

    # Seed templates (ilk yükleme)
    with Session(engine) as s:
        if not s.exec(select(Template)).first():
            samples = [
                Template(code="DIL-ICRA-001", title="İcra Takibine İtirazın İptali Dilekçesi",
                         body="Sayın Mahkeme,\nMüvekkil {{mukekkil}} adına {{borclu}} aleyhine ..."),
                Template(code="DIL-CEZA-001", title="Suç İhbarı Dilekçesi",
                         body="Sayın Savcılık,\nMüvekkil {{mukekkil}} hakkında {{olay_tarihi}} ..."),
                Template(code="DIL-AILE-001", title="Boşanma Davası Dilekçesi",
                         body="Sayın Mahkeme,\nTaraflar {{evlilik_tarihi}} tarihinde evlenmiş ..."),
                Template(code="DIL-IS-001", title="Kıdem Tazminatı Talep Dilekçesi",
                         body="Sayın Mahkeme,\nMüvekkil {{mukekkil}} iş akdi {{fesih_tarihi}} tarihinde ..."),
                Template(code="DIL-IC-001", title="Alacak Davası Dilekçesi",
                         body="Sayın Mahkeme,\nDavalı {{davali}} tarafından ..."),
            ]
            for t in samples:
                s.add(t)
            s.commit()
