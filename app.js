'use strict';

// Mobile navigation: keyboard dismissal and no stale open menu after resizing.
const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('.main-nav');
if (menuButton && menu) {
  const closeMenu = () => {
    menuButton.setAttribute('aria-expanded', 'false');
    menu.classList.remove('is-open');
  };
  menuButton.addEventListener('click', () => {
    const opening = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(opening));
    menu.classList.toggle('is-open', opening);
  });
  menu.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menuButton.focus();
    }
  });
  window.matchMedia('(min-width: 961px)').addEventListener('change', closeMenu);
}

// The full directory remains visible when JavaScript is unavailable.
const filters = [...document.querySelectorAll('[data-filter]')];
const programs = [...document.querySelectorAll('[data-program]')];
const filterCount = document.querySelector('.filter-count');
filters.forEach(button => {
  button.addEventListener('click', () => {
    const selected = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    programs.forEach(program => {
      const visible = selected === 'all' || program.dataset.filters.split(' ').includes(selected);
      program.hidden = !visible;
      if (visible) count += 1;
    });
    if (filterCount) filterCount.textContent = `${count} ${count === 1 ? 'program' : 'programs'}`;
  });
});

const copyButton = document.querySelector('[data-copy-email]');
if (copyButton) {
  copyButton.addEventListener('click', async () => {
    const status = document.querySelector('.copy-status');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(copyButton.dataset.copyEmail);
      status.textContent = 'Email address copied.';
    } catch {
      const address = document.querySelector('.contact-email');
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(address);
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Email address selected. Press Ctrl+C or Command+C to copy.';
    }
  });
}

// Analytic solution to a fall from rest with F_drag = 0.5*rho*Cd*A*v^2.
// Exported only in Node so the physical model can be checked without a browser.
function parachuteModel(diameter, mass, height = 20) {
  if (!(diameter > 0 && mass > 0 && height >= 0)) throw new RangeError('Use positive size and mass, and nonnegative height.');
  const g = 9.81;
  const area = Math.PI * (diameter / 2) ** 2;
  const terminal = Math.sqrt((2 * mass * g) / (1.225 * 1.5 * area));
  const x = g * height / terminal ** 2;
  // acosh(exp(x)), rearranged to avoid overflow for large x.
  const fallTime = terminal / g * (x + Math.log1p(Math.sqrt(-Math.expm1(-2 * x))));
  const distanceAt = time => {
    const z = Math.max(0, time) * g / terminal;
    const logCosh = z + Math.log1p(Math.exp(-2 * z)) - Math.LN2;
    return Math.max(0, Math.min(height, terminal ** 2 / g * logCosh));
  };
  return { area, terminal, fallTime, distanceAt };
}

if (typeof module !== 'undefined' && module.exports) module.exports = { parachuteModel };

const lab = document.querySelector('[data-parachute-lab]');
if (lab) {
  const canopy = lab.querySelector('#canopy');
  const payload = lab.querySelector('#payload');
  const canopyValue = lab.querySelector('#canopy-value');
  const payloadValue = lab.querySelector('#payload-value');
  const terminalValue = lab.querySelector('[data-terminal]');
  const timeValue = lab.querySelector('[data-time]');
  const altitude = lab.querySelector('[data-height]');
  const drop = lab.querySelector('[data-drop]');
  const reset = lab.querySelector('[data-reset]');
  const parachute = lab.querySelector('.parachute-drop');
  const stage = lab.querySelector('.lab-stage');
  const status = lab.querySelector('.lab-status');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;
  let model;
  let running = false;
  let started = 0;
  let pausedAt = 0;

  const setInputs = disabled => {
    canopy.disabled = disabled;
    payload.disabled = disabled;
    drop.disabled = disabled;
  };
  const showDistance = distance => {
    const travel = Math.max(0, stage.clientHeight - 65 - 32 - 109);
    parachute.style.transform = `translateY(${travel * distance / 20}px)`;
    altitude.textContent = Math.max(0, 20 - distance).toFixed(1);
  };
  const stop = () => {
    cancelAnimationFrame(frame);
    running = false;
    pausedAt = 0;
    setInputs(false);
  };
  const update = () => {
    stop();
    model = parachuteModel(Number(canopy.value), Number(payload.value));
    canopyValue.textContent = `${Number(canopy.value).toFixed(2)} m`;
    payloadValue.textContent = `${Number(payload.value).toFixed(2)} kg`;
    canopy.setAttribute('aria-valuetext', `${Number(canopy.value).toFixed(2)} metres`);
    payload.setAttribute('aria-valuetext', `${Number(payload.value).toFixed(2)} kilograms`);
    terminalValue.innerHTML = `${model.terminal.toFixed(2)} <span class="readout-unit">m/s</span>`;
    timeValue.innerHTML = `${model.fallTime.toFixed(1)} <span class="readout-unit">s</span>`;
    const scale = .68 + (Number(canopy.value) - .3) / 1 * .5;
    lab.querySelector('[data-canopy]').setAttribute('transform', `translate(${50 * (1 - scale)} ${42 * (1 - scale)}) scale(${scale})`);
    // Keep suspension lines attached when the canopy diameter changes.
    const lines = parachute.querySelector('svg > path');
    const anchor = [5, 27.5, 50, 72.5, 95].map(x => 50 + (x - 50) * scale);
    lines.setAttribute('d', `M${anchor[0]} 42 47 95M${anchor[1]} 42 47 95M50 42v53M${anchor[3]} 42 53 95M${anchor[4]} 42 53 95`);
    showDistance(0);
    status.textContent = 'Set the canopy diameter and payload mass, then drop the parachute.';
  };
  const landed = () => {
    stop();
    showDistance(20);
    status.textContent = `The parachute landed in ${model.fallTime.toFixed(1)} seconds. Change a setting to compare the next drop.`;
  };
  const animate = now => {
    if (!running) return;
    const elapsed = Math.max(0, (now - started) / 1000);
    if (elapsed >= model.fallTime) { landed(); return; }
    showDistance(model.distanceAt(elapsed));
    frame = requestAnimationFrame(animate);
  };
  drop.addEventListener('click', () => {
    showDistance(0);
    if (reduceMotion.matches) { landed(); return; }
    running = true;
    setInputs(true);
    status.textContent = 'The parachute is falling; watch how the speed changes.';
    started = performance.now();
    frame = requestAnimationFrame(animate);
  });
  reset.addEventListener('click', update);
  canopy.addEventListener('input', update);
  payload.addEventListener('input', update);
  reduceMotion.addEventListener('change', () => { if (running && reduceMotion.matches) landed(); });
  // Pause elapsed time when the tab is hidden, so the experiment remains observable.
  document.addEventListener('visibilitychange', () => {
    if (!running) return;
    if (document.hidden) { pausedAt = performance.now(); cancelAnimationFrame(frame); }
    else if (pausedAt) { started += performance.now() - pausedAt; pausedAt = 0; frame = requestAnimationFrame(animate); }
  });
  window.addEventListener('resize', () => {
    if (!running) showDistance(Number(altitude.textContent) === 0 ? 20 : 0);
  });
  update();
}
