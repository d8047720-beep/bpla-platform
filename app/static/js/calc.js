(async function () {
  const res = await fetch('/api/drones');
  const drones = await res.json();
  const sel = document.getElementById('modelSel');
  drones.forEach(d => { const o = document.createElement('option'); o.value = d.slug; o.textContent = d.name; o.dataset.json = JSON.stringify(d); sel.appendChild(o); });
  const btn = document.getElementById('calcBtn');
  const out = document.getElementById('calcRes');
  btn.addEventListener('click', () => {
    const d = drones.find(x => x.slug === sel.value);
    if (!d) { out.innerHTML = '<p style="color:#ff6b6b">Выберите модель</p>'; return; }
    const dist = +document.getElementById('dist').value || 0;
    const payload = +document.getElementById('payload').value || 0;
    const flights = +document.getElementById('flights').value || 1;
    const payloadPenalty = Math.min(0.4, payload / (d.payload_kg || 1) * 0.3);
    const range = d.range_km * (1 - payloadPenalty);
    const timePerFlight = Math.min(d.endurance_min, (dist / Math.max(d.speed,1)) * 60);
    const costPerFlight = 1500 + (dist * 120) + (payload * 300);
    out.innerHTML = `
      <p><b>«${d.name}</b></p>
      <p>Макс. дальность с грузом: <b>${range.toFixed(1)} км</b></p>
      <p>Время полёта (в одну сторону): <b>${timePerFlight.toFixed(0)} мин</b></p>
      <p>Вылетов: <b>${flights}</b> · Примерная стоимость: <b>${(costPerFlight * flights).toLocaleString()} ₽</b></p>`;
  });
})();
