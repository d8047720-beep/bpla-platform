(function () {
  const grid = document.getElementById('droneGrid');
  const search = document.getElementById('droneSearch');
  const typeFilter = document.getElementById('typeFilter');
  const priceFilter = document.getElementById('priceFilter');
  const sortPill = document.getElementById('sortPill');

  const featuredGrid = document.getElementById('featuredGrid');
  const featuredMsg = document.getElementById('featuredMsg');

  if (!grid || !search || !typeFilter) return;

  // Types
  const types = [...new Set(Array.from(document.querySelectorAll('.drone-card')).map(c => c.dataset.type))];
  types.forEach(t => { const o = document.createElement('option'); o.value = t; o.textContent = t; typeFilter.appendChild(o); });

  // Read all cards once
  const cards = Array.from(document.querySelectorAll('.drone-card'));

  function priceRangeMatch(card, val) {
    if (!val) return true;
    const p = +card.dataset.price || 0;
    const [lo, hi] = val.split('-').map(Number);
    if (hi === undefined) return p >= lo;
    return p >= lo && p <= hi;
  }

  function sortCards(list) {
    const mode = sortPill.textContent;
    if (mode.includes('цене')) {
      const asc = mode.includes('▲');
      list.sort((a, b) => asc ? (+a.dataset.price - +b.dataset.price) : (+b.dataset.price - +a.dataset.price));
    } else if (mode.includes('по названию')) {
      const asc = mode.includes('▲');
      list.sort((a, b) => asc ? a.dataset.name.localeCompare(b.dataset.name) : b.dataset.name.localeCompare(a.dataset.name));
    }
    return list;
  }

  function render(list) {
    grid.innerHTML = '';
    if (!list.length) {
      grid.innerHTML = '<div class="empty-state" style="grid-column:1/-1"><div class="icon">🔍</div><h3>Ничего не найдено</h3><p>Попробуйте изменить поисковый запрос или фильтры.</p><a class="btn" href="{{ url_for(\'main.drones\') }}">Сбросить фильтры</a></div>';
      return;
    }
    grid.append(...list);
  }

  function apply() {
    const q = (search.value || '').toLowerCase();
    const t = typeFilter.value || '';
    const pr = priceFilter.value || '';
    const filtered = cards.filter(c => {
      const nameOk = !q || c.dataset.name.includes(q) || c.dataset.type.includes(q);
      const typeOk = !t || c.dataset.type === t;
      return nameOk && typeOk && priceRangeMatch(c, pr);
    });
    render(sortCards(filtered.slice()));
  }

  search.addEventListener('input', apply);
  typeFilter.addEventListener('change', apply);
  priceFilter.addEventListener('change', apply);

  let sortMode = 0; // 0: default, 1: price asc, 2: price desc, 3: name asc, 4: name desc
  sortPill.addEventListener('click', () => {
    sortMode = (sortMode + 1) % 5;
    const labels = ['Сортировка: по умолчанию ▲', 'Сортировка: цене ▲', 'Сортировка: цене ▼', 'Сортировка: названию ▲', 'Сортировка: названию ▼'];
    sortPill.textContent = labels[sortMode];
    apply();
  });

  apply();

  // Add to Hangar (all pages)
  document.querySelectorAll('.btn-hangar').forEach(btn => {
    btn.addEventListener('click', function () {
      const slug = this.dataset.slug;
      let hangar = JSON.parse(localStorage.getItem('hangar') || '[]');
      if (!hangar.includes(slug)) {
        hangar.push(slug);
        localStorage.setItem('hangar', JSON.stringify(hangar));
        this.textContent = 'В ангаре';
        this.classList.add('btn-hangar-added');
      }
    });
  });
})();
