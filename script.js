/* ==========================================================
   DBA TECHSTORE - COMPORTAMIENTO INTERACTIVO JS
   ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const toggleSlicesBtn = document.getElementById('toggleSlicesBtn');
  const cartButton = document.getElementById('cartButton');
  const cartCount = document.getElementById('cartCount');
  const toast = document.getElementById('toast');
  const buyHeroBtn = document.getElementById('buyHeroBtn');
  const specsBtn = document.getElementById('specsBtn');
  const couponForm = document.getElementById('couponForm');
  const emailInput = document.getElementById('emailInput');
  const catPills = document.querySelectorAll('.cat-pill');
  const productCards = document.querySelectorAll('.product-card');
  const addCartBtns = document.querySelectorAll('.add-cart-btn');

  let currentCartCount = 3;

  // 1. Toast Notification Helper
  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }

  // 2. Toggle Photoshop Slices (Sectores de exportación)
  let slicesActive = false;
  if (toggleSlicesBtn) {
    toggleSlicesBtn.addEventListener('click', () => {
      slicesActive = !slicesActive;
      document.body.classList.toggle('show-slices', slicesActive);
      if (slicesActive) {
        showToast('📐 Sectores de Photoshop (Slices) ACTIVADOS: Modo inspección');
      } else {
        showToast('👁️ Modo Normal Web ACTIVADO');
      }
    });
  }

  // 3. Hero CTA Interactivity
  if (buyHeroBtn) {
    buyHeroBtn.addEventListener('click', () => {
      currentCartCount++;
      cartCount.textContent = currentCartCount;
      showToast('🎉 ¡Audio Pro Ultra ($249.99) añadido a tu pedido!');
    });
  }

  if (specsBtn) {
    specsBtn.addEventListener('click', () => {
      showToast('📋 Especificaciones: Drivers 50mm Titanio, Bluetooth 5.4, Batería 48h, Cancelación ANC 45dB.');
    });
  }

  // 4. Products "Añadir al Carrito" Interactivity
  addCartBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const name = btn.getAttribute('data-name');
      const price = btn.getAttribute('data-price');
      currentCartCount++;
      cartCount.textContent = currentCartCount;
      btn.textContent = '✓ ¡Añadido!';
      btn.style.background = '#10b981';
      setTimeout(() => {
        btn.textContent = 'Añadir al Carrito';
        btn.style.background = '';
      }, 1800);
      showToast(`🛒 ${name} ($${price}) sumado al carrito.`);
    });
  });

  // 5. Category Tabs Filter
  catPills.forEach(pill => {
    pill.addEventListener('click', () => {
      catPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const filter = pill.getAttribute('data-filter');

      productCards.forEach(card => {
        const cat = card.getAttribute('data-category');
        if (filter === 'all' || cat === filter) {
          card.style.display = 'block';
          card.style.animation = 'fadeIn 0.3s ease';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // 6. Interactive Countdown Timer
  let hours = 8;
  let mins = 42;
  let secs = 19;

  const hoursEl = document.getElementById('hoursVal');
  const minsEl = document.getElementById('minsVal');
  const secsEl = document.getElementById('secsVal');

  setInterval(() => {
    if (secs > 0) {
      secs--;
    } else {
      secs = 59;
      if (mins > 0) {
        mins--;
      } else {
        mins = 59;
        if (hours > 0) {
          hours--;
        }
      }
    }

    if (hoursEl) hoursEl.textContent = String(hours).padStart(2, '0');
    if (minsEl) minsEl.textContent = String(mins).padStart(2, '0');
    if (secsEl) secsEl.textContent = String(secs).padStart(2, '0');
  }, 1000);

  // 7. Coupon Form Submit
  if (couponForm) {
    couponForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = emailInput.value.trim();
      if (email) {
        showToast(`🎁 ¡Cupón desbloqueado para ${email}! Código: TECH40OFF`);
        emailInput.value = '';
      }
    });
  }

  // 8. Navigation active tab on click
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');
    });
  });
});
