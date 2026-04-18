// === FIREWORKS & SPARKLES ENGINE — shared across all pages ===
(function() {
    // Create fireworks canvas
    const fc = document.createElement('canvas');
    fc.id = 'fireworks-global';
    fc.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;';
    document.body.prepend(fc);
    const ctx = fc.getContext('2d');
    fc.width = innerWidth; fc.height = innerHeight;
    window.addEventListener('resize', () => { fc.width = innerWidth; fc.height = innerHeight; });

    const sparks = [];
    const colors = ['#00d4ff','#7b2ff7','#f472b6','#fbbf24','#34d399','#ff6b6b','#a78bfa'];

    // === ANIMATED FAVICON WITH FIREWORKS ===
    const favSize = 32;
    const favCanvas = document.createElement('canvas');
    favCanvas.width = favSize; favCanvas.height = favSize;
    const favCtx = favCanvas.getContext('2d');
    let favLink = document.querySelector("link[rel*='icon']");
    if (!favLink) { favLink = document.createElement('link'); favLink.rel = 'icon'; document.head.appendChild(favLink); }
    const favSparks = [];
    const favAmbient = [];
    for (let i = 0; i < 8; i++) {
        favAmbient.push({
            x: Math.random() * favSize, y: Math.random() * favSize,
            size: Math.random() * 1.5 + 0.5, alpha: Math.random(),
            speed: Math.random() * 0.3 + 0.1,
            color: colors[Math.floor(Math.random() * colors.length)],
            phase: Math.random() * Math.PI * 2
        });
    }
    function favBurst() {
        const cx = 8 + Math.random() * 16, cy = 6 + Math.random() * 14;
        for (let i = 0; i < 12; i++) {
            const a = Math.random() * Math.PI * 2, sp = Math.random() * 1.5 + 0.5;
            favSparks.push({ x: cx, y: cy, vx: Math.cos(a)*sp, vy: Math.sin(a)*sp,
                life: 1, decay: Math.random()*0.04+0.02,
                color: colors[Math.floor(Math.random()*colors.length)], size: Math.random()*1.5+0.5 });
        }
    }
    let gradAngle = 0;
    function drawFavicon() {
        favCtx.clearRect(0, 0, favSize, favSize);
        // Animated gradient background
        gradAngle += 0.02;
        const grd = favCtx.createLinearGradient(
            favSize/2 + Math.cos(gradAngle)*favSize/2, 0,
            favSize/2 + Math.sin(gradAngle)*favSize/2, favSize);
        grd.addColorStop(0, '#00d4ff'); grd.addColorStop(0.5, '#7b2ff7'); grd.addColorStop(1, '#f472b6');
        favCtx.fillStyle = grd;
        favCtx.beginPath();
        // Rounded square
        const r = 6; const s = favSize;
        favCtx.moveTo(r, 0); favCtx.lineTo(s-r, 0); favCtx.quadraticCurveTo(s, 0, s, r);
        favCtx.lineTo(s, s-r); favCtx.quadraticCurveTo(s, s, s-r, s);
        favCtx.lineTo(r, s); favCtx.quadraticCurveTo(0, s, 0, s-r);
        favCtx.lineTo(0, r); favCtx.quadraticCurveTo(0, 0, r, 0);
        favCtx.fill();
        // "mA" text with subtle wobble
        const wobble = Math.sin(performance.now() * 0.003) * 1;
        favCtx.fillStyle = '#fff';
        favCtx.font = 'bold 16px sans-serif';
        favCtx.textAlign = 'center'; favCtx.textBaseline = 'middle';
        favCtx.fillText('mA', favSize/2 + wobble, favSize/2 + 1);
        // Ambient sparkles on favicon
        const t = performance.now() * 0.001;
        favAmbient.forEach(sp => {
            sp.y -= sp.speed;
            if (sp.y < -2) { sp.y = favSize + 2; sp.x = Math.random() * favSize; }
            const fl = Math.sin(t * 4 + sp.phase) * 0.5 + 0.5;
            favCtx.beginPath();
            favCtx.arc(sp.x, sp.y, sp.size, 0, Math.PI * 2);
            favCtx.fillStyle = sp.color;
            favCtx.globalAlpha = sp.alpha * fl;
            favCtx.fill();
        });
        favCtx.globalAlpha = 1;
        // Burst sparks on favicon
        for (let i = favSparks.length - 1; i >= 0; i--) {
            const p = favSparks[i];
            p.x += p.vx; p.y += p.vy; p.vy += 0.05; p.life -= p.decay;
            if (p.life <= 0) { favSparks.splice(i, 1); continue; }
            favCtx.beginPath();
            favCtx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
            favCtx.fillStyle = p.color;
            favCtx.globalAlpha = p.life;
            favCtx.fill();
        }
        favCtx.globalAlpha = 1;
        // Update favicon (throttled to ~10fps to save CPU)
        favLink.type = 'image/png';
        favLink.href = favCanvas.toDataURL('image/png');
    }
    setInterval(drawFavicon, 100);
    setInterval(favBurst, 2000);
    favBurst(); // initial burst

    function spawnBurst(x, y, count) {
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 3 + 1;
            sparks.push({
                x, y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 1,
                decay: Math.random() * 0.015 + 0.008,
                color: colors[Math.floor(Math.random() * colors.length)],
                size: Math.random() * 3 + 1
            });
        }
    }

    // Ambient sparkles
    const ambient = [];
    for (let i = 0; i < 40; i++) {
        ambient.push({
            x: Math.random() * innerWidth,
            y: Math.random() * innerHeight,
            size: Math.random() * 2.5 + 0.5,
            alpha: Math.random(),
            speed: Math.random() * 0.5 + 0.1,
            color: colors[Math.floor(Math.random() * colors.length)],
            phase: Math.random() * Math.PI * 2
        });
    }

    function draw() {
        ctx.clearRect(0, 0, fc.width, fc.height);
        const t = performance.now() * 0.001;
        // Ambient sparkles
        ambient.forEach(s => {
            s.y -= s.speed;
            if (s.y < -10) { s.y = fc.height + 10; s.x = Math.random() * fc.width; }
            const flicker = Math.sin(t * 3 + s.phase) * 0.4 + 0.6;
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
            ctx.fillStyle = s.color;
            ctx.globalAlpha = s.alpha * flicker;
            ctx.shadowColor = s.color;
            ctx.shadowBlur = 10;
            ctx.fill();
            ctx.shadowBlur = 0;
        });
        ctx.globalAlpha = 1;
        // Burst sparks
        for (let i = sparks.length - 1; i >= 0; i--) {
            const s = sparks[i];
            s.x += s.vx; s.y += s.vy; s.vy += 0.03;
            s.life -= s.decay;
            if (s.life <= 0) { sparks.splice(i, 1); continue; }
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.size * s.life, 0, Math.PI * 2);
            ctx.fillStyle = s.color;
            ctx.globalAlpha = s.life;
            ctx.shadowColor = s.color;
            ctx.shadowBlur = 15;
            ctx.fill();
            ctx.shadowBlur = 0;
        }
        ctx.globalAlpha = 1;
        requestAnimationFrame(draw);
    }
    draw();
    setInterval(() => {
        spawnBurst(Math.random() * fc.width, Math.random() * fc.height * 0.7,
            Math.floor(Math.random() * 20) + 15);
    }, 2500);
    document.addEventListener('click', e => spawnBurst(e.clientX, e.clientY, 30));
})();
