# YargıNet MVP (Tevkil + Dilekçe + Takvim)
Sürüm: 2025-11-04

## Çalıştırma
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```
Aç: http://localhost:8000/docs

## Uçlar (özet)
- `POST /users` (kayıt), `POST /login` (dummy token)
- `GET/POST /tevkil` (ilan liste/ekle)
- `GET /templates` (hazır 10 şablon özetleri)
- `POST /dilekce/render` (seçili şablonu alanlara göre doldurup **metin** döner)
- `GET/POST /hearings` (duruşma ekle/listele)

## Veritabanı
- SQLite (`yarginet.db`)

## Frontend (statik)
`web/` klasörünü tarayıcıda aç. `script.js` içindeki `API_BASE` adresini değiştir.
