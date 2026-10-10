"""Synthesise a soft 22 s wedding-ad bed: warm pad, bell arpeggio, whooshes on cuts. Writes a 44.1 kHz stereo WAV."""
import sys, wave, numpy as np
SR, DUR = 44100, 22.0
n = int(SR * DUR); t = np.arange(n) / SR
mix = np.zeros((n, 2))
def note(m): return 440 * 2 ** ((m - 69) / 12)
# progression: Fmaj7, Am7, Dm9, Bbmaj7 (2 bars each at 76 bpm -> ~3.16 s per bar)
bar = 60 / 76 * 4
chords = [[53, 57, 60, 64], [57, 60, 64, 67], [50, 57, 60, 64], [46, 53, 57, 62]]
for i in range(int(DUR / bar) + 1):
    ch = chords[i % 4]; s0 = int(i * bar * SR); s1 = min(n, int((i + 1) * bar * SR) + int(.8 * SR))
    if s0 >= n: break
    tt = np.arange(s1 - s0) / SR
    env = np.minimum(tt / 1.2, 1) * np.exp(-np.maximum(tt - bar, 0) * 3)
    for k, m in enumerate(ch):
        f = note(m)
        for det, pan in ((-.9, .3), (.9, .7)):
            w = np.sin(2 * np.pi * (f + det) * tt) + .25 * np.sin(2 * np.pi * 2 * (f + det) * tt)
            mix[s0:s1, 0] += w * env * .045 * (1 - pan); mix[s0:s1, 1] += w * env * .045 * pan
    # bass
    fb = note(ch[0] - 12); wb = np.sin(2 * np.pi * fb * tt) * env * .09
    mix[s0:s1] += wb[:, None]
# bell arpeggio on eighths from 3.2 s
eighth = 60 / 76 / 2
k = 0; tpos = 3.2
while tpos < DUR - .6:
    ch = chords[int(tpos / bar) % 4]; m = ch[[0, 2, 1, 3, 2, 1][k % 6]] + 12
    s0 = int(tpos * SR); L = int(1.6 * SR); s1 = min(n, s0 + L); tt = np.arange(s1 - s0) / SR
    f = note(m); env = np.exp(-tt * 3.2) * np.minimum(tt / .005, 1)
    w = (np.sin(2 * np.pi * f * tt) + .35 * np.sin(2 * np.pi * 2.01 * f * tt) * np.exp(-tt * 6) + .12 * np.sin(2 * np.pi * 3.0 * f * tt) * np.exp(-tt * 9))
    pan = .35 + .3 * ((k % 4) / 3)
    mix[s0:s1, 0] += w * env * .05 * (1 - pan); mix[s0:s1, 1] += w * env * .05 * pan
    k += 1; tpos += eighth
# whooshes on the product cuts and scene changes
rng = np.random.default_rng(3)
for c in [3.2, 6.4] + [6.4 + .83 * i for i in range(1, 6)] + [11.2, 16.2, 19.2]:
    s0 = int((c - .25) * SR); L = int(.5 * SR); tt = np.arange(L) / SR
    noise = rng.standard_normal(L)
    # crude band-pass via moving averages
    lp = np.convolve(noise, np.ones(12) / 12, mode='same'); bp = lp - np.convolve(lp, np.ones(60) / 60, mode='same')
    env = np.sin(np.pi * tt / .5) ** 2
    mix[s0:s0 + L] += (bp * env * .18)[:, None]
# end chime
s0 = int(19.3 * SR)
for m, g in ((77, .07), (81, .05), (84, .04)):
    tt = np.arange(n - s0) / SR; f = note(m)
    mix[s0:, :] += (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 1.4) * g)[:, None]
# simple stereo reverb: a few feedback delays
out = mix.copy()
for d, g in ((.031, .35), (.047, .3), (.071, .25), (.113, .2)):
    D = int(d * SR)
    for ch_ in (0, 1):
        y = out[:, ch_]
        for i in range(3):
            y[D * (i + 1):] += mix[:-D * (i + 1) or None, 1 - ch_] * g ** (i + 1)
# fades + normalise
fade = np.minimum(np.minimum(t / 1.0, 1), np.minimum((DUR - t) / 1.2, 1))
out *= fade[:, None]
out /= np.max(np.abs(out)) / .7
pcm = (out * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
