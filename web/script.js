const API_BASE = "https://yarginet-mvp-api.onrender.com";

const reg = document.getElementById("reg");
const login = document.getElementById("login");
const authOut = document.getElementById("authOut");
let TOKEN = null;

reg.onsubmit = async (e) => {
  e.preventDefault();
  const body = { email: e.target.email.value, password: e.target.password.value };
  const r = await fetch(API_BASE + "/users",{ method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  authOut.textContent = await r.text();
};

login.onsubmit = async (e) => {
  e.preventDefault();
  const body = { email: e.target.email.value, password: e.target.password.value };
  const r = await fetch(API_BASE + "/login",{ method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  const data = await r.json();
  TOKEN = data.token;
  authOut.textContent = JSON.stringify(data, null, 2);
};

// Tevkil
const tevkilForm = document.getElementById("tevkilForm");
const tevkilOut = document.getElementById("tevkilOut");
const listTevkilBtn = document.getElementById("listTevkil");

tevkilForm.onsubmit = async (e) => {
  e.preventDefault();
  const body = {
    title: e.target.title.value,
    city: e.target.city.value,
    court: e.target.court.value,
    fee: parseFloat(e.target.fee.value),
    details: e.target.details.value
  };
  const r = await fetch(API_BASE + "/tevkil", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  tevkilOut.textContent = await r.text();
};

listTevkilBtn.onclick = async () => {
  const r = await fetch(API_BASE + "/tevkil");
  const data = await r.json();
  tevkilOut.textContent = JSON.stringify(data, null, 2);
};

// Templates & Render
const tplBtn = document.getElementById("listTpl");
const tplSelect = document.getElementById("tplSelect");
const fields = document.getElementById("fields");
const renderBtn = document.getElementById("renderBtn");
const renderOut = document.getElementById("renderOut");

tplBtn.onclick = async () => {
  const r = await fetch(API_BASE + "/templates");
  const data = await r.json();
  tplSelect.innerHTML = data.map(d => `<option value="${d.id}">${d.code} - ${d.title}</option>`).join("");
};

renderBtn.onclick = async () => {
  const payload = { template_id: parseInt(tplSelect.value), fields: {} };
  try { payload.fields = JSON.parse(fields.value || "{}"); } catch(e){ alert("JSON geçersiz"); return; }
  const r = await fetch(API_BASE + "/dilekce/render", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(payload)});
  renderOut.textContent = await r.text();
};

// Hearings
const hearForm = document.getElementById("hearForm");
const listHear = document.getElementById("listHear");
const hearOut = document.getElementById("hearOut");

hearForm.onsubmit = async (e) => {
  e.preventDefault();
  const body = {
    court: e.target.court.value,
    date: e.target.date.value,
    room: e.target.room.value,
    note: e.target.note.value
  };
  const r = await fetch(API_BASE + "/hearings", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  hearOut.textContent = await r.text();
};

listHear.onclick = async () => {
  const r = await fetch(API_BASE + "/hearings");
  const data = await r.json();
  hearOut.textContent = JSON.stringify(data, null, 2);
};
// ==== YargıNet typing animasyonu ====
document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("typeTarget");
  if(!el) return;

  const lines = [
    "Yargının Akıllı Yüzü",
    "Tevkil • Dilekçe • Takvim",
    "Hızlı • Basit • Güvenli"
  ];

  let i = 0, pos = 0, dir = 1; // dir: 1 yaz, -1 sil
  const typeSpeed = 55, eraseSpeed = 28, hold = 1200;

  function tick(){
    const text = lines[i];
    pos += dir;
    el.textContent = text.slice(0, pos);

    if (dir === 1 && pos === text.length){
      setTimeout(()=>{ dir = -1; tick(); }, hold);
    } else if (dir === -1 && pos === 0){
      i = (i + 1) % lines.length;
      dir = 1;
      setTimeout(tick, 250);
    } else {
      setTimeout(tick, dir === 1 ? typeSpeed : eraseSpeed);
    }
  }
  tick();
});
// Sayfa açıldığında pürüzsüz kayma efekti
window.addEventListener("load", () => {
  document.body.style.opacity = "1";
});
// ==== Dilekçe Şablonu (MVP) ====

// API kökü (sende zaten global bir API değişkeni varsa onu kullanır)
const API_BASE = window.API || "https://yarginet-mvp-api.onrender.com";

const tplSelect = document.getElementById("tplSelect");
const tplFields = document.getElementById("tplFields");
const tplPreview = document.getElementById("tplPreview");

async function loadTpls(){
  try{
    const r = await fetch(${API_BASE}/templates);
    const items = await r.json();
    // select'i doldur
    tplSelect.innerHTML = items.map(t => 
      `<option value="${t.code}" data-vars='${JSON.stringify(t.variables)}'>
        ${t.title}
      </option>`
    ).join("");
    buildTplFields();  // ilk seçili şablon için alanlar
  }catch(e){
    console.error(e);
    if (typeof toast === 'function') toast("Şablonlar yüklenemedi ❌","error");
  }
}

function buildTplFields(){
  tplFields.innerHTML = "";
  const opt = tplSelect.options[tplSelect.selectedIndex];
  if(!opt){ return; }
  const vars = JSON.parse(opt.dataset.vars || "[]");

  if(vars.length === 0){
    tplFields.innerHTML = <div class="out">Bu şablon değişken gerektirmiyor.</div>;
    return;
  }

  // Alanları üret
  vars.forEach(v=>{
    tplFields.insertAdjacentHTML("beforeend", `
      <label for="fld_${v}">${v}</label>
      <input id="fld_${v}" placeholder="${v} değeri" />
    `);
  });
}

tplSelect?.addEventListener("change", buildTplFields);

// Önizleme
document.getElementById("btnPreview")?.addEventListener("click", async ()=>{
  try{
    const code = tplSelect.value;
    const data = collectTplData();
    const r = await fetch(${API_BASE}/templates/render, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ code, data })
    });
    if(!r.ok) throw new Error("HTTP " + r.status);
    const j = await r.json();
    tplPreview.textContent = j.html || "";
    if (typeof toast === 'function') toast("Önizleme hazır ✅","success");
  }catch(e){
    console.error(e);
    if (typeof toast === 'function') toast("Önizleme başarısız ❌","error");
  }
});

// DOCX indir
document.getElementById("btnDocx")?.addEventListener("click", async ()=>{
  try{
    const code = tplSelect.value;
    const data = collectTplData();
    const r = await fetch(${API_BASE}/templates/docx, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ code, data })
    });
    if(!r.ok) throw new Error("HTTP " + r.status);
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = ${code}.docx;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
    if (typeof toast === 'function') toast("DOCX indirildi ✅","success");
  }catch(e){
    console.error(e);
    if (typeof toast === 'function') toast("DOCX oluşturulamadı ❌","error");
  }
});

function collectTplData(){
  const opt = tplSelect.options[tplSelect.selectedIndex];
  const vars = JSON.parse(opt.dataset.vars || "[]");
  const obj = {};
  vars.forEach(v=>{
    const el = document.getElementById(fld_${v});
    obj[v] = (el?.value || "").trim();
  });
  return obj;
}

// Başlangıçta yükle
loadTpls();
