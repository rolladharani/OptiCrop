/* ===================================================
   OptiCrop – Main JavaScript
   Smart Agricultural Production Optimization Engine
   =================================================== */

/* ─── NAVBAR SCROLL EFFECT ─── */
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('mainNavbar');
  if (navbar) {
    if (window.scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }
});

/* ─── AUTO-DISMISS FLASH MESSAGES ─── */
document.addEventListener('DOMContentLoaded', () => {
  const flashContainer = document.getElementById('flashContainer');
  if (flashContainer) {
    setTimeout(() => {
      flashContainer.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      flashContainer.style.opacity = '0';
      flashContainer.style.transform = 'translateX(20px)';
      setTimeout(() => flashContainer.remove(), 500);
    }, 4000);
  }

  /* ─── INTERSECTION OBSERVER for scroll animations ─── */
  const animateEls = document.querySelectorAll(
    '.feature-card, .scenario-card, .card, .stat-card, .chart-wrapper'
  );

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, idx) => {
      if (entry.isIntersecting) {
        entry.target.style.animationDelay = `${idx * 0.05}s`;
        entry.target.classList.add('animate-fade-up');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  animateEls.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });

  /* ─── ANIMATE OBSERVED ELEMENTS ─── */
  const style = document.createElement('style');
  style.textContent = `.animate-fade-up { opacity: 1 !important; transform: translateY(0) !important; }`;
  document.head.appendChild(style);

  /* ─── COUNTER ANIMATIONS for stat values ─── */
  const counters = document.querySelectorAll('.stat-value, .stat-card-value');
  counters.forEach(counter => {
    const target = parseFloat(counter.textContent.replace(/[^0-9.]/g, ''));
    const suffix = counter.textContent.replace(/[0-9.]/g, '');
    if (!isNaN(target) && target > 0) {
      let current = 0;
      const increment = target / 50;
      const timer = setInterval(() => {
        current = Math.min(current + increment, target);
        const isFloat = target % 1 !== 0;
        counter.textContent = (isFloat ? current.toFixed(1) : Math.round(current)) + suffix;
        if (current >= target) clearInterval(timer);
      }, 30);
    }
  });
});

/* ─── TOOLTIP HOVER SUPPORT ─── */
function addTooltip(el, text) {
  const tooltip = document.createElement('div');
  tooltip.className = 'tooltip';
  tooltip.textContent = text;
  tooltip.style.cssText = `
    position:absolute; background:rgba(8,14,20,0.95); color:#e8f5e9;
    padding:0.4rem 0.8rem; border-radius:6px; font-size:0.75rem;
    pointer-events:none; z-index:9999; white-space:nowrap;
    border:1px solid rgba(255,255,255,0.08); box-shadow:0 4px 12px rgba(0,0,0,0.4);
  `;
  document.body.appendChild(tooltip);

  el.addEventListener('mousemove', (e) => {
    tooltip.style.left = (e.clientX + 12) + 'px';
    tooltip.style.top = (e.clientY - 30) + 'px';
    tooltip.style.display = 'block';
  });
  el.addEventListener('mouseleave', () => {
    tooltip.style.display = 'none';
  });
}

/* ─── MOBILE NAVBAR TOGGLE (graceful degradation) ─── */
const navbarToggle = document.getElementById('navToggle');
if (navbarToggle) {
  navbarToggle.addEventListener('click', () => {
    const navMenu = document.querySelector('.navbar-nav');
    if (navMenu) {
      navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
    }
  });
}

/* ─── PRINT / EXPORT ─── */
function exportResults() {
  window.print();
}
