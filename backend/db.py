from sqlmodel import SQLModel, create_engine, Session, select
from models import User, Tevkil, Template, Hearing

engine = create_engine("sqlite:///yarginet.db", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)
    # Seed templates (first run)
    with Session(engine) as s:
        if not s.exec(select(Template)).first():
            samples = [
                Template(code="DIL-ICRA-001", title="İcra Takibine İtirazın İptali Dilekçesi",
                         body="Sayın Mahkeme,\nMüvekkil {{mukekkil}} adına {{borclu}} aleyhine ..."),
                Template(code="DIL-CEZA-001", title="Suça İtiraz Dilekçesi",
                         body="Sayın Savcılık,\nMüvekkil {{mukekkil}} hakkında ... {{olay_tarihi}} ..."),
                Template(code="DIL-AILE-001", title="Boşanma Dava Dilekçesi",
                         body="Sayın Mahkeme,\nTaraflar {{evlilik_tarihi}} tarihinde evlenmiş ..."),
                Template(code="DIL-IS-001", title="Kıdem Tazminatı Talep Dilekçesi",
                         body="Sayın Mahkeme,\nMüvekkil {{mukekkil}} iş akdi {{fesih_tarihi}} tarihinde ..."),
                Template(code="DIL-TIC-001", title="Alacak Davası Dilekçesi",
                         body="Sayın Mahkeme,\nDavalı {{davali}} tarafından ..."),
            ]
            for t in samples:
                s.add(t)
            s.commit()
