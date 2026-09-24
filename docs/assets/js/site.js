const toggle = document.querySelector('.mobile-toggle');
const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.nav-overlay');
function closeNavigation() {
  sidebar.classList.remove('open');
  overlay.classList.remove('open');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', 'Open navigation');
}
toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  sidebar.classList.toggle('open', open);
  overlay.classList.toggle('open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  if (open) sidebar.querySelector('a').focus();
});
overlay.addEventListener('click', closeNavigation);
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && sidebar.classList.contains('open')) { closeNavigation(); toggle.focus(); }
});
sidebar.querySelectorAll('a').forEach(link => link.addEventListener('click', closeNavigation));
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
  }), { threshold: .1 });
  reveals.forEach(item => observer.observe(item));
} else reveals.forEach(item => item.classList.add('visible'));
