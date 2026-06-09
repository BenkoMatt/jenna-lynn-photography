/* ═══════════════════════════════════════════════════════════
   [Photographer Name] — Scripts
   ═══════════════════════════════════════════════════════════ */

// ─── NAV SCROLL EFFECT ───
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 50);
});

// ─── MOBILE NAV TOGGLE ───
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  // Animate hamburger
  const spans = navToggle.querySelectorAll('span');
  if (navLinks.classList.contains('open')) {
    spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
    spans[1].style.opacity = '0';
    spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
  } else {
    spans[0].style.transform = '';
    spans[1].style.opacity = '';
    spans[2].style.transform = '';
  }
});

// Close mobile nav on link click
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    const spans = navToggle.querySelectorAll('span');
    spans[0].style.transform = '';
    spans[1].style.opacity = '';
    spans[2].style.transform = '';
  });
});

// ─── SMOOTH SCROLL (for older browsers) ───
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ─── FADE-IN ON SCROLL ───
const observerOptions = {
  root: null,
  rootMargin: '0px 0px -60px 0px',
  threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Add fade-in class to sections
document.querySelectorAll(
  '.about, .services, .gallery, .process, .kind-words, .faq, .contact, .instagram'
).forEach(section => {
  section.classList.add('fade-in');
  observer.observe(section);
});

// ─── CONTACT FORM (prevent default, show success) ───
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Replace form with success message
    const wrap = this.parentElement;
    wrap.innerHTML = `
      <div style="text-align:center; padding:60px 20px;">
        <p style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:#2c2c2c; margin-bottom:12px;">Yay!</p>
        <p style="font-size:1rem; color:#666; line-height:1.8;">
          Your inquiry is on its way! I'll get back to you within 24 hours.<br>
          Can't wait to hear more about you two! 💕
        </p>
      </div>
    `;
  });
}