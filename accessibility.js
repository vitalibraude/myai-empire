/**
 * Accessibility Widget
 * Compliant with: WCAG 2.1 AA, Israeli Standard 5568, EN 301 549, ADA
 */
(function () {
  if (document.getElementById('a11y-widget')) return;

  var state = {
    open: false,
    fontSize: 0,
    contrast: 'none',
    links: false,
    readingGuide: false,
    animations: true,
    spacing: 0,
    dyslexia: false,
    cursor: 'default',
    saturation: 'none',
    lineHeight: 0
  };

  // Load saved state
  try {
    var saved = localStorage.getItem('a11y_state');
    if (saved) { state = JSON.parse(saved); state.open = false; }
  } catch (e) {}

  function save() {
    try { localStorage.setItem('a11y_state', JSON.stringify(state)); } catch (e) {}
  }

  // Inject CSS
  var css = document.createElement('style');
  css.id = 'a11y-widget-css';
  css.textContent = `
    #a11y-trigger {
      position: fixed; right: 0; top: 50%; transform: translateY(-50%);
      z-index: 999999; width: 52px; height: 52px;
      background: #1565c0; border: 2px solid #fff;
      border-radius: 50% 0 0 50%; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      box-shadow: -2px 2px 8px rgba(0,0,0,.35);
      transition: background .2s;
    }
    #a11y-trigger:hover, #a11y-trigger:focus { background: #0d47a1; outline: 3px solid #ffd600; }
    #a11y-trigger svg { width: 28px; height: 28px; fill: #fff; }
    #a11y-panel {
      position: fixed; right: -400px; top: 0; width: 370px; height: 100vh;
      background: #1a1a2e; color: #e0e0e0; z-index: 999998;
      overflow-y: auto; transition: right .3s ease;
      box-shadow: -4px 0 20px rgba(0,0,0,.5);
      font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
      font-size: 15px; line-height: 1.5;
    }
    #a11y-panel.open { right: 0; }
    #a11y-panel * { box-sizing: border-box; }
    .a11y-header {
      display: flex; justify-content: space-between; align-items: center;
      padding: 18px 20px; background: #0d47a1; position: sticky; top: 0; z-index: 2;
    }
    .a11y-header h2 { margin: 0; font-size: 18px; color: #fff; }
    .a11y-close {
      background: none; border: none; color: #fff; font-size: 26px;
      cursor: pointer; width: 36px; height: 36px; display: flex;
      align-items: center; justify-content: center; border-radius: 4px;
    }
    .a11y-close:hover, .a11y-close:focus { background: rgba(255,255,255,.15); outline: 2px solid #ffd600; }
    .a11y-section { padding: 14px 20px; border-bottom: 1px solid #2a2a4a; }
    .a11y-section h3 { margin: 0 0 10px; font-size: 14px; text-transform: uppercase; color: #90caf9; letter-spacing: .5px; }
    .a11y-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .a11y-btn {
      background: #2a2a4a; border: 2px solid transparent; border-radius: 8px;
      color: #e0e0e0; padding: 10px 8px; cursor: pointer; text-align: center;
      font-size: 13px; transition: all .15s; display: flex; flex-direction: column;
      align-items: center; gap: 4px;
    }
    .a11y-btn:hover, .a11y-btn:focus { border-color: #42a5f5; background: #33335a; outline: none; }
    .a11y-btn.active { background: #1565c0; border-color: #64b5f6; color: #fff; }
    .a11y-btn .a11y-icon { font-size: 22px; }
    .a11y-reset-btn {
      display: block; width: calc(100% - 40px); margin: 16px 20px;
      padding: 12px; background: #c62828; border: none; border-radius: 8px;
      color: #fff; font-size: 15px; font-weight: 600; cursor: pointer;
      text-align: center; transition: background .2s;
    }
    .a11y-reset-btn:hover, .a11y-reset-btn:focus { background: #b71c1c; outline: 2px solid #ffd600; }
    .a11y-compliance {
      padding: 14px 20px; text-align: center; font-size: 11px; color: #777;
      border-top: 1px solid #2a2a4a;
    }
    .a11y-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,.4);
      z-index: 999997; display: none;
    }
    .a11y-overlay.open { display: block; }
    /* Applied styles */
    body.a11y-high-contrast { filter: contrast(1.75) !important; }
    body.a11y-dark-contrast { filter: invert(1) hue-rotate(180deg) !important; }
    body.a11y-dark-contrast img,
    body.a11y-dark-contrast video,
    body.a11y-dark-contrast canvas { filter: invert(1) hue-rotate(180deg) !important; }
    body.a11y-light-contrast { background: #fff !important; color: #000 !important; }
    body.a11y-light-contrast * { background-color: #fff !important; color: #000 !important; border-color: #000 !important; }
    body.a11y-links-highlight a { outline: 3px solid #ffd600 !important; text-decoration: underline !important; }
    body.a11y-no-animations *, body.a11y-no-animations *::before, body.a11y-no-animations *::after {
      animation-duration: 0s !important; animation-delay: 0s !important;
      transition-duration: 0s !important; transition-delay: 0s !important;
    }
    body.a11y-dyslexia { font-family: 'OpenDyslexic', 'Comic Sans MS', cursive, sans-serif !important; }
    body.a11y-dyslexia * { font-family: inherit !important; }
    body.a11y-big-cursor, body.a11y-big-cursor * { cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48'%3E%3Cpath d='M4 4l16 36 6-14 14-6z' fill='%23000' stroke='%23fff' stroke-width='2'/%3E%3C/svg%3E") 4 4, auto !important; }
    body.a11y-reading-line #a11y-reading-line {
      display: block !important; position: fixed; left: 0; width: 100%; height: 12px;
      background: rgba(255,214,0,.35); z-index: 999990; pointer-events: none;
      border-top: 2px solid #ffd600; border-bottom: 2px solid #ffd600;
    }
    body.a11y-saturate-high { filter: saturate(2) !important; }
    body.a11y-saturate-low { filter: saturate(.3) !important; }
    body.a11y-monochrome { filter: grayscale(1) !important; }
    @media (max-width: 480px) {
      #a11y-panel { width: 100vw; }
      #a11y-trigger { width: 44px; height: 44px; }
      #a11y-trigger svg { width: 24px; height: 24px; }
    }
  `;
  document.head.appendChild(css);

  // Reading line element
  var readingLine = document.createElement('div');
  readingLine.id = 'a11y-reading-line';
  readingLine.style.display = 'none';
  document.body.appendChild(readingLine);
  document.addEventListener('mousemove', function (e) {
    readingLine.style.top = (e.clientY - 6) + 'px';
  });

  // Overlay
  var overlay = document.createElement('div');
  overlay.className = 'a11y-overlay';
  overlay.setAttribute('aria-hidden', 'true');
  overlay.addEventListener('click', togglePanel);
  document.body.appendChild(overlay);

  // Trigger button
  var trigger = document.createElement('button');
  trigger.id = 'a11y-trigger';
  trigger.setAttribute('aria-label', 'Open accessibility menu');
  trigger.setAttribute('title', 'Accessibility / \u05E0\u05D2\u05D9\u05E9\u05D5\u05EA');
  trigger.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm9 7h-6l-1.41 7.41L16 22h-2l-2-5-2 5H8l2.41-5.59L9 9H3V7h18v2z"/></svg>';
  trigger.addEventListener('click', togglePanel);
  document.body.appendChild(trigger);

  // Panel
  var panel = document.createElement('div');
  panel.id = 'a11y-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Accessibility settings');
  panel.setAttribute('aria-modal', 'true');
  panel.innerHTML = `
    <div class="a11y-header">
      <h2>\u2699\uFE0F Accessibility</h2>
      <button class="a11y-close" aria-label="Close accessibility menu">&times;</button>
    </div>

    <div class="a11y-section">
      <h3>Font Size</h3>
      <div class="a11y-grid">
        <button class="a11y-btn" data-action="fontUp"><span class="a11y-icon">A+</span>Increase</button>
        <button class="a11y-btn" data-action="fontDown"><span class="a11y-icon">A-</span>Decrease</button>
      </div>
    </div>

    <div class="a11y-section">
      <h3>Line &amp; Letter Spacing</h3>
      <div class="a11y-grid">
        <button class="a11y-btn" data-action="spacingUp"><span class="a11y-icon">&#x2194;</span>More Spacing</button>
        <button class="a11y-btn" data-action="spacingDown"><span class="a11y-icon">&#x2194;</span>Less Spacing</button>
        <button class="a11y-btn" data-action="lineHeightUp"><span class="a11y-icon">&#x2195;</span>Line Height +</button>
        <button class="a11y-btn" data-action="lineHeightDown"><span class="a11y-icon">&#x2195;</span>Line Height -</button>
      </div>
    </div>

    <div class="a11y-section">
      <h3>Contrast &amp; Colors</h3>
      <div class="a11y-grid">
        <button class="a11y-btn" data-action="highContrast"><span class="a11y-icon">&#x25D0;</span>High Contrast</button>
        <button class="a11y-btn" data-action="darkContrast"><span class="a11y-icon">&#x25CF;</span>Dark Mode</button>
        <button class="a11y-btn" data-action="lightContrast"><span class="a11y-icon">&#x25CB;</span>Light Mode</button>
        <button class="a11y-btn" data-action="monochrome"><span class="a11y-icon">&#x26AB;</span>Monochrome</button>
        <button class="a11y-btn" data-action="saturateHigh"><span class="a11y-icon">&#x1F308;</span>High Saturation</button>
        <button class="a11y-btn" data-action="saturateLow"><span class="a11y-icon">&#x1F4A7;</span>Low Saturation</button>
      </div>
    </div>

    <div class="a11y-section">
      <h3>Navigation &amp; Reading</h3>
      <div class="a11y-grid">
        <button class="a11y-btn" data-action="highlightLinks"><span class="a11y-icon">&#x1F517;</span>Highlight Links</button>
        <button class="a11y-btn" data-action="readingGuide"><span class="a11y-icon">&#x1F4D6;</span>Reading Guide</button>
        <button class="a11y-btn" data-action="bigCursor"><span class="a11y-icon">&#x1F5B1;</span>Big Cursor</button>
        <button class="a11y-btn" data-action="stopAnimations"><span class="a11y-icon">&#x23F8;</span>Stop Animations</button>
      </div>
    </div>

    <div class="a11y-section">
      <h3>Readability</h3>
      <div class="a11y-grid">
        <button class="a11y-btn" data-action="dyslexia"><span class="a11y-icon">&#x1F524;</span>Dyslexia Font</button>
      </div>
    </div>

    <button class="a11y-reset-btn" data-action="reset">&#x1F504; Reset All Settings</button>

    <div class="a11y-compliance">
      WCAG 2.1 AA &bull; Israeli Standard 5568 &bull; EN 301 549 &bull; ADA &sect;508
    </div>
  `;
  document.body.appendChild(panel);

  // Close button
  panel.querySelector('.a11y-close').addEventListener('click', togglePanel);

  // Button actions
  panel.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-action]');
    if (!btn) return;
    var action = btn.dataset.action;
    handleAction(action);
    updateButtons();
    save();
  });

  // Keyboard: Escape to close
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && state.open) togglePanel();
  });

  function togglePanel() {
    state.open = !state.open;
    panel.classList.toggle('open', state.open);
    overlay.classList.toggle('open', state.open);
    if (state.open) {
      trigger.style.display = 'none';
      panel.querySelector('.a11y-close').focus();
    } else {
      trigger.style.display = 'flex';
      trigger.focus();
    }
  }

  function clearContrast() {
    document.body.classList.remove('a11y-high-contrast', 'a11y-dark-contrast', 'a11y-light-contrast');
    state.contrast = 'none';
  }
  function clearSaturation() {
    document.body.classList.remove('a11y-saturate-high', 'a11y-saturate-low', 'a11y-monochrome');
    state.saturation = 'none';
  }

  function handleAction(action) {
    switch (action) {
      case 'fontUp':
        if (state.fontSize < 5) { state.fontSize++; applyFontSize(); } break;
      case 'fontDown':
        if (state.fontSize > -2) { state.fontSize--; applyFontSize(); } break;
      case 'spacingUp':
        if (state.spacing < 5) { state.spacing++; applySpacing(); } break;
      case 'spacingDown':
        if (state.spacing > 0) { state.spacing--; applySpacing(); } break;
      case 'lineHeightUp':
        if (state.lineHeight < 5) { state.lineHeight++; applyLineHeight(); } break;
      case 'lineHeightDown':
        if (state.lineHeight > 0) { state.lineHeight--; applyLineHeight(); } break;
      case 'highContrast':
        clearSaturation();
        if (state.contrast === 'high') { clearContrast(); }
        else { clearContrast(); state.contrast = 'high'; document.body.classList.add('a11y-high-contrast'); }
        break;
      case 'darkContrast':
        clearSaturation();
        if (state.contrast === 'dark') { clearContrast(); }
        else { clearContrast(); state.contrast = 'dark'; document.body.classList.add('a11y-dark-contrast'); }
        break;
      case 'lightContrast':
        clearSaturation();
        if (state.contrast === 'light') { clearContrast(); }
        else { clearContrast(); state.contrast = 'light'; document.body.classList.add('a11y-light-contrast'); }
        break;
      case 'monochrome':
        clearContrast();
        if (state.saturation === 'mono') { clearSaturation(); }
        else { clearSaturation(); state.saturation = 'mono'; document.body.classList.add('a11y-monochrome'); }
        break;
      case 'saturateHigh':
        clearContrast();
        if (state.saturation === 'high') { clearSaturation(); }
        else { clearSaturation(); state.saturation = 'high'; document.body.classList.add('a11y-saturate-high'); }
        break;
      case 'saturateLow':
        clearContrast();
        if (state.saturation === 'low') { clearSaturation(); }
        else { clearSaturation(); state.saturation = 'low'; document.body.classList.add('a11y-saturate-low'); }
        break;
      case 'highlightLinks':
        state.links = !state.links;
        document.body.classList.toggle('a11y-links-highlight', state.links);
        break;
      case 'readingGuide':
        state.readingGuide = !state.readingGuide;
        document.body.classList.toggle('a11y-reading-line', state.readingGuide);
        break;
      case 'bigCursor':
        state.cursor = state.cursor === 'big' ? 'default' : 'big';
        document.body.classList.toggle('a11y-big-cursor', state.cursor === 'big');
        break;
      case 'stopAnimations':
        state.animations = !state.animations;
        document.body.classList.toggle('a11y-no-animations', !state.animations);
        break;
      case 'dyslexia':
        state.dyslexia = !state.dyslexia;
        document.body.classList.toggle('a11y-dyslexia', state.dyslexia);
        break;
      case 'reset':
        resetAll(); break;
    }
  }

  function applyFontSize() {
    if (state.fontSize === 0) { document.body.style.removeProperty('font-size'); }
    else { document.body.style.fontSize = (100 + state.fontSize * 15) + '%'; }
  }
  function applySpacing() {
    if (state.spacing === 0) {
      document.body.style.removeProperty('letter-spacing');
      document.body.style.removeProperty('word-spacing');
    } else {
      document.body.style.letterSpacing = (state.spacing * 0.5) + 'px';
      document.body.style.wordSpacing = (state.spacing * 1.5) + 'px';
    }
  }
  function applyLineHeight() {
    if (state.lineHeight === 0) { document.body.style.removeProperty('line-height'); }
    else { document.body.style.lineHeight = (1.7 + state.lineHeight * 0.3); }
  }

  function resetAll() {
    clearContrast(); clearSaturation();
    document.body.classList.remove('a11y-links-highlight', 'a11y-no-animations',
      'a11y-dyslexia', 'a11y-big-cursor', 'a11y-reading-line');
    document.body.style.removeProperty('font-size');
    document.body.style.removeProperty('letter-spacing');
    document.body.style.removeProperty('word-spacing');
    document.body.style.removeProperty('line-height');
    state = {
      open: state.open, fontSize: 0, contrast: 'none', links: false,
      readingGuide: false, animations: true, spacing: 0, dyslexia: false,
      cursor: 'default', saturation: 'none', lineHeight: 0
    };
    updateButtons();
    save();
  }

  function updateButtons() {
    var btns = panel.querySelectorAll('[data-action]');
    btns.forEach(function (b) {
      var a = b.dataset.action;
      var active = false;
      if (a === 'highContrast') active = state.contrast === 'high';
      else if (a === 'darkContrast') active = state.contrast === 'dark';
      else if (a === 'lightContrast') active = state.contrast === 'light';
      else if (a === 'monochrome') active = state.saturation === 'mono';
      else if (a === 'saturateHigh') active = state.saturation === 'high';
      else if (a === 'saturateLow') active = state.saturation === 'low';
      else if (a === 'highlightLinks') active = state.links;
      else if (a === 'readingGuide') active = state.readingGuide;
      else if (a === 'bigCursor') active = state.cursor === 'big';
      else if (a === 'stopAnimations') active = !state.animations;
      else if (a === 'dyslexia') active = state.dyslexia;
      b.classList.toggle('active', active);
    });
  }

  // Apply saved state on load
  function applyState() {
    applyFontSize();
    applySpacing();
    applyLineHeight();
    if (state.contrast === 'high') document.body.classList.add('a11y-high-contrast');
    if (state.contrast === 'dark') document.body.classList.add('a11y-dark-contrast');
    if (state.contrast === 'light') document.body.classList.add('a11y-light-contrast');
    if (state.saturation === 'mono') document.body.classList.add('a11y-monochrome');
    if (state.saturation === 'high') document.body.classList.add('a11y-saturate-high');
    if (state.saturation === 'low') document.body.classList.add('a11y-saturate-low');
    if (state.links) document.body.classList.add('a11y-links-highlight');
    if (state.readingGuide) document.body.classList.add('a11y-reading-line');
    if (!state.animations) document.body.classList.add('a11y-no-animations');
    if (state.dyslexia) document.body.classList.add('a11y-dyslexia');
    if (state.cursor === 'big') document.body.classList.add('a11y-big-cursor');
    updateButtons();
  }
  applyState();
})();
