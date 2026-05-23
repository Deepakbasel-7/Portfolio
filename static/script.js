// Contact form submission
function send(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button');
  btn.textContent = '✓ Sent!';
  btn.style.background = '#00e5ff';
  btn.style.color = '#000';
  setTimeout(() => {
    btn.textContent = 'Send Message →';
    btn.style.background = '';
    btn.style.color = '';
    e.target.reset();
  }, 2500);
}

// Scroll fade-in animation
const observer = new IntersectionObserver((entries) => {
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
  observer.observe(el);
});