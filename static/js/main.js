// ─── NAV ──────────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

if (hamburger) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}

// Dropdown touch toggle
document.querySelectorAll('.dropdown > button, .dropdown > a').forEach(el => {
  el.addEventListener('click', (e) => {
    if (window.innerWidth <= 900) {
      e.preventDefault();
      el.parentElement.classList.toggle('open');
    }
  });
});

// Color theme switch: IEEE blue & white is the default; the switch turns on
// the secondary "classic" COINS navy & gold theme. The saved choice is
// applied before first paint by an inline script in base.html's <head>.
const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
  const root = document.documentElement;
  const sync = () => themeToggle.setAttribute('aria-checked', root.dataset.theme === 'classic');
  sync();
  themeToggle.addEventListener('click', () => {
    const classic = root.dataset.theme !== 'classic';
    if (classic) root.dataset.theme = 'classic'; else delete root.dataset.theme;
    try { localStorage.setItem('coins-theme', classic ? 'classic' : 'default'); } catch (e) {}
    sync();
  });
}

// Active nav link
const currentPage = location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.getAttribute('href') === currentPage || a.getAttribute('href') === './' + currentPage) {
    a.classList.add('active');
  }
});

// ─── COUNTDOWN ─────────────────────────────────────────────
// Target date comes from conference.yml (dates.countdown_iso), passed via
// the data-countdown attribute on this script's own <script> tag in base.html.
const countdownScript = document.currentScript;
const COUNTDOWN_TARGET = countdownScript ? countdownScript.dataset.countdown : null;

function updateCountdown() {
  if (!COUNTDOWN_TARGET) return;
  const target = new Date(COUNTDOWN_TARGET);
  const now = new Date();
  const diff = target - now;
  if (diff <= 0) return;

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const secs = Math.floor((diff % (1000 * 60)) / 1000);

  const d = document.getElementById('cd-days');
  const h = document.getElementById('cd-hours');
  const m = document.getElementById('cd-mins');
  const s = document.getElementById('cd-secs');

  if (d) d.textContent = String(days).padStart(2, '0');
  if (h) h.textContent = String(hours).padStart(2, '0');
  if (m) m.textContent = String(mins).padStart(2, '0');
  if (s) s.textContent = String(secs).padStart(2, '0');
}
updateCountdown();
setInterval(updateCountdown, 1000);

// ─── PROGRAM TABS ──────────────────────────────────────────
document.querySelectorAll('.day-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.day-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.day-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    const target = document.getElementById(tab.dataset.target);
    if (target) target.classList.add('active');
  });
});

// ─── SMOOTH SCROLL ─────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ─── SCROLL FADE-IN ────────────────────────────────────────
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.track-card, .person-card, .reg-card, .date-row, .stat-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(12px)';
    el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    observer.observe(el);
  });
}
