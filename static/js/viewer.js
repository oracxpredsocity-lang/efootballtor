// Viewer script: récupère /api/data toutes les 2s et reconstruit le bracket
const container = document.getElementById('bracket-container');
let lastData = null;

function fetchData(){
  fetch('/api/data')
    .then(r => r.json())
    .then(data => {
      const jsonStr = JSON.stringify(data);
      if (jsonStr !== lastData){
        lastData = jsonStr;
        renderBracket(data);
      }
    })
    .catch(err => console.error('fetch error', err));
}

function getPlayer(players, id){
  if (id === null || id === undefined) return null;
  return players.find(x => x.id === id) || { id: id, name: '#'+id, controller: '-', team: '-' };
}

function formatLabel(p){
  if (!p) return '—';
  const controller = p.controller || p.name || '—';
  const team = p.team || '—';
  return `${escapeHtml(controller)} — ${escapeHtml(team)}`;
}

function renderBracket(data){
  container.innerHTML = '';
  const players = data.players || [];
  const rounds = data.rounds || [];

  rounds.forEach((round, rIdx) => {
    const col = document.createElement('div');
    col.className = 'bracket-column';
    const title = document.createElement('h3');
    title.style.marginTop = '4px';
    title.style.marginBottom = '6px';
    title.style.color = 'var(--muted)';
    title.textContent = rIdx === rounds.length-1 ? 'Finale' : `Round ${rIdx+1}`;
    col.appendChild(title);

    round.forEach(match => {
      const matchEl = document.createElement('div');
      matchEl.className = 'match';

      const p1 = getPlayer(players, match.p1);
      const p2 = getPlayer(players, match.p2);
      const p1Label = formatLabel(p1);
      const p2Label = formatLabel(p2);

      let score1 = Number(match.score1) || 0;
      let score2 = Number(match.score2) || 0;
      let total = score1 + score2;
      let ratio1 = total === 0 ? 0.5 : (score1 / (total));
      let ratio2 = total === 0 ? 0.5 : (score2 / (total));
      if (match.winner){
        ratio1 = match.winner === match.p1 ? 1 : 0;
        ratio2 = match.winner === match.p2 ? 1 : 0;
      }

      matchEl.innerHTML = `
        <div class="player-line">
          <div class="player-name">${p1 ? escapeHtml(p1.name) : '—'}</div>
          <div class="score">${score1}</div>
        </div>
        <div class="sub-label">${p1Label}</div>
        <div class="progress"><div class="bar" style="width:${Math.round(ratio1*100)}%"></div></div>

        <div style="height:6px"></div>

        <div class="player-line">
          <div class="player-name">${p2 ? escapeHtml(p2.name) : '—'}</div>
          <div class="score">${score2}</div>
        </div>
        <div class="sub-label">${p2Label}</div>
        <div class="progress"><div class="bar" style="width:${Math.round(ratio2*100)}%"></div></div>
      `;
      col.appendChild(matchEl);
    });

    container.appendChild(col);
  });
}

function escapeHtml(str){
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// initial fetch + polling
fetchData();
setInterval(fetchData, 2000);
