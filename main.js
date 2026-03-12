/* ══════════════════════════════════════════
   MONEY TREE GANG BANGERS — main.js
══════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── CUSTOM CURSOR ────────────────── */
  const cursor     = document.querySelector('.cursor');
  const cursorRing = document.querySelector('.cursor-ring');
  let mouseX = 0, mouseY = 0;
  let ringX = 0, ringY = 0;

  document.addEventListener('mousemove', e => {
    mouseX = e.clientX; mouseY = e.clientY;
    cursor.style.left = mouseX + 'px';
    cursor.style.top  = mouseY + 'px';
  });

  // Smooth ring follow
  function animateRing() {
    ringX += (mouseX - ringX) * 0.12;
    ringY += (mouseY - ringY) * 0.12;
    cursorRing.style.left = ringX + 'px';
    cursorRing.style.top  = ringY + 'px';
    requestAnimationFrame(animateRing);
  }
  animateRing();

  document.querySelectorAll('a, button, .member-card, .album-card, .concert-row, .track-item').forEach(el => {
    el.addEventListener('mouseenter', () => { cursor.classList.add('hover'); cursorRing.classList.add('hover'); });
    el.addEventListener('mouseleave', () => { cursor.classList.remove('hover'); cursorRing.classList.remove('hover'); });
  });

  /* ── NAV SCROLL ───────────────────── */
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  });

  /* ── SCROLL REVEAL ────────────────── */
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        revealObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

  /* ── HOURS HIGHLIGHT TODAY ─────────── */
  const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const today = days[new Date().getDay()];
  document.querySelectorAll('.concert-row[data-day]').forEach(row => {
    if (row.dataset.day === today) row.classList.add('today');
  });

  /* ── TRACK PLAY BUTTON ────────────── */
  let currentPlaying = null;
  document.querySelectorAll('.track-item').forEach(item => {
    item.addEventListener('click', () => {
      const btn  = item.querySelector('.track-play');
      const name = item.querySelector('.track-name').textContent;

      if (currentPlaying && currentPlaying !== item) {
        currentPlaying.querySelector('.track-play').innerHTML = '▶';
        currentPlaying.querySelector('.track-play').style.background = 'var(--green)';
        currentPlaying.classList.remove('playing');
      }

      if (currentPlaying === item) {
        btn.innerHTML = '▶';
        btn.style.background = 'var(--green)';
        item.classList.remove('playing');
        currentPlaying = null;
      } else {
        btn.innerHTML = '■';
        btn.style.background = 'var(--gold)';
        item.classList.add('playing');
        currentPlaying = item;
        // Pulse animation
        item.style.borderColor = 'rgba(0,255,135,.4)';
        setTimeout(() => item.style.borderColor = '', 2000);
      }
    });
  });

  /* ── NEWSLETTER FORM ──────────────── */
  const nlForm    = document.getElementById('nl-form');
  const nlSuccess = document.getElementById('nl-success');
  const nlInput   = document.getElementById('nl-email');

  if (nlForm) {
    nlForm.addEventListener('submit', async e => {
      e.preventDefault();
      const email = nlInput.value.trim();
      if (!email || !email.includes('@')) {
        nlInput.style.borderBottom = '2px solid var(--red)';
        return;
      }
      nlInput.style.borderBottom = '';

      // Simulate submission
      const btn = nlForm.querySelector('button');
      btn.textContent = 'Signing you up…';
      btn.disabled = true;

      await new Promise(r => setTimeout(r, 1200));

      nlForm.style.opacity = '0';
      nlForm.style.transform = 'translateY(-10px)';
      nlForm.style.transition = 'all .4s';

      setTimeout(() => {
        nlForm.style.display = 'none';
        nlSuccess.style.display = 'block';
        nlSuccess.textContent = `🎤 Welcome to the Money Tree, ${email.split('@')[0]}! You're in.`;
        nlSuccess.style.animation = 'fadeUp .5s ease both';
      }, 400);
    });
  }

  /* ── CONCERT TICKET BUTTONS ───────── */
  document.querySelectorAll('.concert-btn:not(.sold)').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const row  = btn.closest('.concert-row');
      const show = row.querySelector('h3').textContent;
      const city = row.querySelector('.concert-city').textContent;
      alert(`🎟️ Redirecting to tickets for:\n"${show}"\n📍 ${city}\n\nLink would open here in production.`);
    });
  });

  /* ── ALBUM CARD HOVER TILT ─────────── */
  document.querySelectorAll('.album-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width  - .5;
      const y = (e.clientY - rect.top)  / rect.height - .5;
      card.style.transform = `perspective(600px) rotateX(${-y*6}deg) rotateY(${x*6}deg) translateY(-4px)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });

  /* ── TICKER DUPLICATE ─────────────── */
  const track = document.querySelector('.ticker-track');
  if (track) {
    track.innerHTML += track.innerHTML; // seamless loop
  }

  /* ── SMOOTH HASH SCROLL ───────────── */
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
