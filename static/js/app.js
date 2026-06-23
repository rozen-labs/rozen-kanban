function getCookie(name) {
  return document.cookie.split('; ').reduce((acc, part) => {
    const [k, ...rest] = part.split('=');
    acc[decodeURIComponent(k)] = decodeURIComponent(rest.join('='));
    return acc;
  }, {})[name];
}

function initThemeToggle() {
  const stored = localStorage.getItem('theme');
  const preferred = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  const theme = stored || preferred;
  document.documentElement.dataset.theme = theme;
  document.querySelectorAll('[data-theme-toggle]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      localStorage.setItem('theme', next);
    });
  });
}

function initBoardDnD() {
  const cards = document.querySelectorAll('[data-task-id]');
  const columns = document.querySelectorAll('[data-column-id]');
  let draggingId = null;
  cards.forEach((card) => {
    card.addEventListener('dragstart', () => {
      draggingId = card.dataset.taskId;
      card.classList.add('dragging');
    });
    card.addEventListener('dragend', () => card.classList.remove('dragging'));
  });
  columns.forEach((column) => {
    column.addEventListener('dragover', (event) => event.preventDefault());
    column.addEventListener('drop', async (event) => {
      event.preventDefault();
      if (!draggingId) return;
      const response = await fetch(`/tasks/${draggingId}/move/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        body: new URLSearchParams({ column_id: column.dataset.columnId })
      });
      if (response.ok) window.location.reload();
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initBoardDnD();
});
