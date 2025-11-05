// === Ayarlar ===
const API_BASE = "https://yarginet-mvp-api.onrender.com";

// === Yardımcı ===
const $ = (id) => document.getElementById(id);

// === Alanları üret ===
function buildTplFields(){
  const sel = $("tplSelect");
  const host = $("tplFields");
  host.innerHTML = "";
  if (!sel) return;

  const opt  = sel.options[sel.selectedIndex];
  const vars = opt ? JSON.parse(opt.dataset.vars || "[]") : [];

  if (!vars.length){
    host.innerHTML = <div class="out">Bu şablon değişken gerektirmiyor.</div>;
    return;
  }
  vars.forEach(v=>{
    host.insertAdjacentHTML("beforeend", `
      <label for="fld_${v}">${v}</label>
      <input id="fld_${v}" placeholder="${v} değeri" />
    `);
  });
}

// Toplanan alanları json yap
function collectTplData(){
  const sel  = $("tplSelect");
  const opt  = sel.options[sel.selectedIndex];
  const vars = JSON.parse(opt.dataset.vars || "[]");
  const data = {};
  vars.forEach(v=>{
    data[v] = ($("fld_"+v)?.value || "").trim();
  });
  return data;
}

// Şablonları yükle ve select'i doldur
async function loadTpls(){
  console.log("loadTpls() çağrıldı");
  const r = await fetch(${API_BASE}/templates);
  if(!r.ok) throw new Error("HTTP "+r.status);
  const items = await r.json();

  const sel = $("tplSelect");
  sel.innerHTML = items.map(t =>
    <option value="${t.code}" data-vars='${JSON.stringify(t.variables || [])}'>${t.title}</option>
  ).join("");

  console.log("tplSelect dolduruldu, adet:", sel.options.length);
  buildTplFields();
}

// Önizleme
async function doPreview(){
  const code = $("tplSelect").value;
  const vars = collectTplData();

  // Önizlemeyi backend dönmüyorsa burada basit yer değiştirme yap:
  let text = "";
  try {
    const r = await fetch(${API_BASE}/templates/render, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ code, data: vars })
    });
    if(r.ok){
      const j = await r.json();
      text = j.html || j.content || "";
    }
  } catch(e){ console.warn("render api yok, client-side render"); }

  if(!text){
    // Fallback: şablon gövdesini alamıyorsak boş bırak
    text = "(Önizleme için sunucu cevabı yok)";
  }

  // NOT: regex YOK — güvenli replace
  Object.entries(vars).forEach(([k,v])=>{
    text = text.split("{{"+k+"}}").join(String(v));
  });

  $("tplPreview").textContent = text;
}

// DOCX indir
async function doDocx(){
  const code = $("tplSelect").value;
  const data = collectTplData();
  const r = await fetch(${API_BASE}/templates/docx, {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({ code, data })
  });
  if(!r.ok) throw new Error("HTTP "+r.status);
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = ${code}.docx;
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
}

// === Init ===
document.addEventListener("DOMContentLoaded", ()=>{
  console.log("YargiNet JS yüklendi");
  $("tplSelect").addEventListener("change", buildTplFields);
  $("btnPreview").addEventListener("click", ()=>doPreview().catch(console.error));
  $("btnDocx").addEventListener("click", ()=>doDocx().catch(console.error));
  window.buildTplFields = buildTplFields; // HTML'den çağrı yedeği

  loadTpls().catch(e=>{
    console.error(e);
    alert("Şablonlar yüklenemedi");
  });
});
    console.error(e);
    alert("Şablonlar yüklenemedi. API adresi doğru mu?");
  });
});
<script src="script.js" defer></script>
