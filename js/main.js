// Spaciodual.us clone — shared header/nav behavior
document.addEventListener('DOMContentLoaded', function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var body = document.body;

  function updateSolid() {
    if (!header || header.dataset.alwaysSolid === 'true') return;
    if (window.scrollY > 60) {
      header.classList.add('is-solid');
    } else {
      header.classList.remove('is-solid');
    }
  }
  updateSolid();
  window.addEventListener('scroll', updateSolid, { passive: true });

  if (toggle) {
    toggle.addEventListener('click', function () {
      body.classList.toggle('nav-open');
    });
  }

  // Close mobile menu when a plain nav link is tapped
  document.querySelectorAll('.main-nav > .nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      body.classList.remove('nav-open');
    });
  });

  // Tap-to-open dropdown on touch/mobile widths (hover has no effect there)
  document.querySelectorAll('.nav-item-dropdown > .nav-link').forEach(function (trigger) {
    trigger.addEventListener('click', function (e) {
      if (window.innerWidth > 900) return;
      e.preventDefault();
      trigger.closest('.nav-item-dropdown').classList.toggle('is-open');
    });
  });

  // Static booking / store forms: prevent submission, show inline confirmation
  document.querySelectorAll('.form-mock').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('.form-mock-note');
      if (note) {
        note.textContent = 'This is a static demo form — no data is sent. In the real site this would submit your request.';
        note.style.display = 'block';
      }
    });
  });

  document.querySelectorAll('.mock-add-to-cart').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var original = btn.textContent;
      btn.textContent = 'Demo only';
      setTimeout(function () { btn.textContent = original; }, 1400);
    });
  });
});
