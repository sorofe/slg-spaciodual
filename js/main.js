// SpacioDual.com clone — shared header behavior
document.addEventListener('DOMContentLoaded', function () {
  var header = document.querySelector('.site-header');

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

  // Static booking / store forms: prevent submission, show inline confirmation
  document.querySelectorAll('.form-mock').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('.form-mock-note');
      if (note) {
        note.textContent = 'Este es un formulario de demostración estática — no se envía ningún dato. En el sitio real esto enviaría tu solicitud.';
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

  // Two-step checkout: payment -> date/time (both static demo panels)
  var checkoutForm = document.querySelector('.checkout-form');
  if (checkoutForm) {
    var panels = checkoutForm.querySelectorAll('.checkout-panel');
    var indicators = document.querySelectorAll('.checkout-step-indicator');

    function goToStep(step) {
      panels.forEach(function (panel) {
        panel.classList.toggle('is-active', panel.dataset.step === String(step));
      });
      indicators.forEach(function (ind) {
        ind.classList.toggle('is-active', ind.dataset.stepIndicator === String(step));
      });
    }

    var nextBtn = checkoutForm.querySelector('.checkout-next');
    if (nextBtn) {
      nextBtn.addEventListener('click', function () { goToStep(2); });
    }
    var backBtn = checkoutForm.querySelector('.checkout-back');
    if (backBtn) {
      backBtn.addEventListener('click', function () { goToStep(1); });
    }
  }

  document.querySelectorAll('.time-slot').forEach(function (slot) {
    slot.addEventListener('click', function () {
      slot.parentElement.querySelectorAll('.time-slot').forEach(function (s) {
        s.classList.remove('is-selected');
      });
      slot.classList.add('is-selected');
    });
  });
});
