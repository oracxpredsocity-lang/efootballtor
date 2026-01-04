// Admin JS: récupère /api/data, permet édition JSON et sauvegarde via /api/update
const rawJson = document.getElementById('raw-json');
const editor = document.getElementById('json-editor');
const btnEdit = document.getElementById('btn-edit-json');
const btnSave = document.getElementById('btn-save-json');
const btnRefresh = document.getElementById('btn-refresh');

let currentData = null;

function loadData(){
  fetch('/api/data')
    .then(r => r.json())
    .then(data => {
      currentData = data;
      rawJson.textContent = JSON.stringify(data, null, 2);
      editor.value = JSON.stringify(data, null, 2);
    })
    .catch(err => {
      rawJson.textContent = 'Erreur: ' + err;
    });
}

if (btnEdit) {
  btnEdit.addEventListener('click', () => {
    editor.style.display = editor.style.display === 'none' ? 'block' : 'none';
  });
}
if (btnSave) {
  btnSave.addEventListener('click', () => {
    let parsed;
    try {
      parsed = JSON.parse(editor.value);
    } catch (e){
      alert('JSON invalide: ' + e.message);
      return;
    }
    fetch('/api/update', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(parsed)
    })
      .then(r => {
        if (!r.ok) return r.json().then(j => Promise.reject(j));
        return r.json();
      })
      .then(resp => {
        alert('Sauvegardé');
        loadData();
      })
      .catch(err => {
        alert('Erreur sauvegarde: ' + (err.error || JSON.stringify(err)));
        console.error(err);
      });
  });
}
if (btnRefresh) {
  btnRefresh.addEventListener('click', () => loadData());
}

loadData();
