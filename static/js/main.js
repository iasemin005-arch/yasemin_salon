document.addEventListener('DOMContentLoaded', function () {

  // ── NAV scroll effect
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 30);
  });

  // ── Mobile menu
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggle) toggle.addEventListener('click', () => navLinks.classList.toggle('open'));

  // ── Service tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      this.classList.add('active');
      const panel = document.getElementById('tab-' + this.dataset.tab);
      if (panel) panel.classList.add('active');
    });
  });

  // ── Star rating (review modal)
  document.querySelectorAll('.star-btn').forEach((btn, i, all) => {
    btn.addEventListener('click', function () {
      const val = parseInt(this.dataset.val);
      document.getElementById('review-rating').value = val;
      all.forEach((b, j) => b.classList.toggle('active', j < val));
    });
    btn.addEventListener('mouseover', function () {
      const val = parseInt(this.dataset.val);
      document.querySelectorAll('.star-btn').forEach((b, j) => b.classList.toggle('active', j < val));
    });
  });
  const starsContainer = document.querySelector('.star-rating');
  if (starsContainer) starsContainer.addEventListener('mouseleave', () => {
    const val = parseInt(document.getElementById('review-rating').value || 0);
    document.querySelectorAll('.star-btn').forEach((b, j) => b.classList.toggle('active', j < val));
  });

  // ── Modals
  window.openModal = function (id) {
    document.getElementById(id).classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  window.closeModal = function (id) {
    document.getElementById(id).classList.remove('open');
    document.body.style.overflow = '';
  };
  document.querySelectorAll('.modal-overlay').forEach(m => {
    m.addEventListener('click', e => { if (e.target === m) closeModal(m.id); });
  });

  // ── Toast
  window.showToast = function (msg, type = 'success') {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = 'toast ' + type + ' show';
    setTimeout(() => t.classList.remove('show'), 4000);
  };

  // ── CSRF
  function getCsrf() {
    return document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='))?.split('=')[1] || '';
  }

  // ── Book appointment
  const bookForm = document.getElementById('book-form');
  if (bookForm) bookForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const data = {
      client_name: document.getElementById('b-name').value,
      client_phone: document.getElementById('b-phone').value,
      client_email: document.getElementById('b-email').value,
      service_id: document.getElementById('b-service').value,
      master_id: document.getElementById('b-master').value,
      date: document.getElementById('b-date').value,
      time: document.getElementById('b-time').value,
      comment: document.getElementById('b-comment').value,
      payment_method: document.querySelector('input[name="payment"]:checked')?.value || 'cash',
    };
    try {
      const res = await fetch('/api/book/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
        body: JSON.stringify(data),
      });
      const json = await res.json();
      showToast(json.message, json.success ? 'success' : 'error');
      if (json.success) bookForm.reset();
    } catch { showToast('Ошибка соединения', 'error'); }
  });

  // ── Review form
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) reviewForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const data = {
      client_name: document.getElementById('r-name').value,
      rating: document.getElementById('review-rating').value || 5,
      text: document.getElementById('r-text').value,
    };
    try {
      const res = await fetch('/api/review/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
        body: JSON.stringify(data),
      });
      const json = await res.json();
      showToast(json.message, json.success ? 'success' : 'error');
      if (json.success) { reviewForm.reset(); closeModal('review-modal'); }
    } catch { showToast('Ошибка соединения', 'error'); }
  });

  // ── Load services into booking select
  fetch('/api/services/').then(r => r.json()).then(data => {
    const sel = document.getElementById('b-service');
    if (!sel) return;
    data.services.forEach(s => {
      const o = document.createElement('option');
      o.value = s.id; o.textContent = s.name + ' — ' + s.price + ' сом';
      sel.appendChild(o);
    });
  });

  // ── Load masters into booking select
  fetch('/api/masters/').then(r => r.json()).then(data => {
    const sel = document.getElementById('b-master');
    if (!sel) return;
    data.masters.forEach(m => {
      const o = document.createElement('option');
      o.value = m.id; o.textContent = m.name + ' (' + m.specialty + ')';
      sel.appendChild(o);
    });
  });

  // ── Set min date to today
  const dateInput = document.getElementById('b-date');
  if (dateInput) dateInput.min = new Date().toISOString().split('T')[0];

});
