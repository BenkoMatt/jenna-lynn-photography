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
  '.about, .services, .gallery, .process, .faq, .contact, .instagram'
).forEach(section => {
  section.classList.add('fade-in');
  observer.observe(section);
});

// ─── CONTACT FORM — Formspree Integration ───
const contactForm = document.getElementById('contactForm');
const formSuccess = document.getElementById('formSuccess');
const formError = document.getElementById('formError');
const formLoading = document.getElementById('formLoading');
const submitBtn = document.getElementById('submitBtn');
const originalBtnText = submitBtn ? submitBtn.textContent : 'Send Inquiry';

function resetFormStates() {
  if (formSuccess) formSuccess.classList.remove('show');
  if (formError) formError.classList.remove('show');
  if (formLoading) formLoading.classList.remove('show');
  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.textContent = originalBtnText;
  }
}

if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();

    resetFormStates();

    if (formLoading) formLoading.classList.add('show');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';
    }

    var formData = new FormData(contactForm);

    fetch(contactForm.action, {
      method: 'POST',
      body: formData,
      headers: { 'Accept': 'application/json' }
    })
    .then(function(response) {
      if (response.ok) {
        if (formLoading) formLoading.classList.remove('show');
        if (formSuccess) formSuccess.classList.add('show');
        contactForm.reset();

        if (formSuccess) {
          formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        setTimeout(function() {
          if (formSuccess) formSuccess.classList.remove('show');
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
          }
        }, 8000);
      } else {
        throw new Error('Formspree returned ' + response.status);
      }
    })
    .catch(function(error) {
      if (formLoading) formLoading.classList.remove('show');
      if (formError) formError.classList.add('show');

      if (formError) {
        formError.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }

      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
      }

      setTimeout(function() {
        if (formError) formError.classList.remove('show');
      }, 10000);
    });
  });
}

// ─── PHONE FIELD — digits only, max 10 ───
var phoneInput = document.getElementById('phone');
if (phoneInput) {
  phoneInput.addEventListener('input', function(e) {
    var cleaned = e.target.value.replace(/\D/g, '');
    if (cleaned.length > 10) {
      cleaned = cleaned.substring(0, 10);
    }
    e.target.value = cleaned;
  });
}