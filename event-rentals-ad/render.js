// Renders ad.html to frames and pipes them to ffmpeg.
// Usage: node render.js <out.mp4> [fps]            full video
//        node render.js --stills <dir> t1 t2 ...    preview PNGs at given seconds
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const { chromium } = require(process.env.PW || '/opt/node-tools/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'ad.html'));
  await page.waitForFunction(() => window.READY === true, null, { timeout: 30000 });
  const grab = async t => {
    const url = await page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.93); }, t);
    return Buffer.from(url.split(',')[1], 'base64');
  };

  if (process.argv[2] === '--stills') {
    const dir = process.argv[3]; fs.mkdirSync(dir, { recursive: true });
    for (const t of process.argv.slice(4)) fs.writeFileSync(path.join(dir, `still-${t}.jpg`), await grab(+t));
  } else {
    const out = process.argv[2], fps = +(process.argv[3] || 30);
    const dur = await page.evaluate(() => window.DUR);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(dur * fps);
    for (let i = 0; i < n; i++) {
      const buf = await grab(i / fps);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 60 === 0) process.stdout.write(`frame ${i}/${n}\n`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
