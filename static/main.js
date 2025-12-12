document.addEventListener('DOMContentLoaded', () => {
  const getBtn = document.getElementById('getBtn');
  if (!getBtn) return;

  getBtn.addEventListener('click', async () => {
    const mood = document.getElementById('moodSelect').value;
    const resultsEl = document.getElementById('results');

    if (!mood) {
      alert('Please select a mood.');
      return;
    }

    resultsEl.innerHTML = '<p class="text-sm">Loading...</p>';

    try {
      const res = await fetch(`/api/recommend?mood=${encodeURIComponent(mood)}`);
      if (!res.ok) {
        const err = await res.json();
        resultsEl.innerHTML = `<p class="text-sm text-red-300">${err.error || 'Error'}</p>`;
        return;
      }
      const data = await res.json();
      if (!data.results || data.results.length === 0) {
        resultsEl.innerHTML = '<p class="text-sm">No movies found for this mood. Try another.</p>';
        return;
      }

      let html = '<div class="grid gap-4">';
      data.results.forEach(m => {
        html += `
          <div class="bg-white/5 p-4 rounded-lg flex items-center gap-4">
            <div class="w-20 h-28 bg-slate-700 rounded overflow-hidden">
              ${m.poster_url ? `<img src="${m.poster_url}" class="w-full h-full object-cover" />` : `<div class="flex items-center justify-center h-full text-sm">No poster</div>`}
            </div>
            <div>
              <div class="font-semibold">${m.title}</div>
              <div class="text-sm text-slate-200">${m.genre || ''} • ${m.rating ? '⭐ ' + m.rating : ''}</div>
            </div>
          </div>
        `;
      });
      html += '</div>';
      resultsEl.innerHTML = html;
    } catch (e) {
      resultsEl.innerHTML = '<p class="text-sm text-red-300">Network error.</p>';
      console.error(e);
    }
  });
});
