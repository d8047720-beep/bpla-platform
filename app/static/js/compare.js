(async function () {
  const res = await fetch('/api/drones');
  const drones = await res.json();
  const grid = document.getElementById('compareGrid');
  const result = document.getElementById('compareResult');
  const boxes = document.querySelectorAll('.cmp-card');

  function render() {
    const sel = Array.from(document.querySelectorAll('.cmp:checked')).map(i => i.dataset.slug);
    const list = drones.filter(d => sel.includes(d.slug));
    if (!list.length) { result.innerHTML = ''; return; }
    result.innerHTML = '<table><thead><tr><th>Характеристика</th>' + list.map(d => '<th>' + d.name + '</th>').join('') + '</tr></thead><tbody>' +
      ['type','speed','range_km','endurance_min','payload_kg','ceiling_m','description'].map(f => {
        const labels = {type:'Тип',speed:'Скорость (км/ч)',range_km:'Дальность (км)',endurance_min:'Время (мин)',payload_kg:'Груз (кг)',ceiling_m:'Потолок (м)',description:'Описание'};
        return '<tr><td><b>'+labels[f]+'</b></td>' + list.map(d => '<td>'+d[f]+'</td>').join('') + '</tr>';
      }).join('') + '</tbody></table>';
  }
  boxes.forEach(b => b.addEventListener('click', () => {
    const inp = b.querySelector('input');
    if (inp.checked) inp.checked = false; else inp.checked = true;
    render();
  }));
  render();
})();
