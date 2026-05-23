// Contact form → Flask backend
async function sendMessage(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type="submit"]');
  const name    = document.getElementById('f-name').value.trim();
  const email   = document.getElementById('f-email').value.trim();
  const message = document.getElementById('f-msg').value.trim();

  btn.textContent = 'Sending...';
  btn.disabled = true;

  try {
    const res  = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message }),
    });
    const data = await res.json();

    if (data.ok) {
      btn.textContent = '✓ Message Sent!';
      btn.style.background = '#00e5ff';
      btn.style.color = '#000';
      e.target.reset();
    } else {
      btn.textContent = '✗ ' + (data.error || 'Error');
      btn.style.background = '#ff6b6b';
      btn.style.color = '#000';
    }
    setTimeout(() => {
      btn.textContent = 'Send Message →';
      btn.style.background = '';
      btn.style.color = '';
      btn.disabled = false;
    }, 3000);
  } catch {
    btn.textContent = '✗ Network error';
    btn.style.background = '#ff6b6b';
    btn.style.color = '#000';
    setTimeout(() => {
      btn.textContent = 'Send Message →';
      btn.style.background = '';
      btn.style.color = '';
      btn.disabled = false;
    }, 3000);
  }
}

// Scroll fade-in
const io = new IntersectionObserver(entries => {
  entries.forEach(el => {
    if (el.isIntersecting) {
      el.target.style.opacity = 1;
      el.target.style.transform = 'none';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.card, .skill-group, .stat-card').forEach(el => {
  el.style.opacity = 0;
  el.style.transform = 'translateY(18px)';
  el.style.transition = 'opacity .5s ease, transform .5s ease';
  io.observe(el);
});