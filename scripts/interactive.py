"""Build interactive/index.html: classroom-interaction deck, no speaker notes, sprint as optional final slide."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'build' / 'general.html').read_text()

def rep(old, new, src=None):
    global s
    target = s if src is None else src
    assert old in target, old[:70]
    if src is None:
        s = s.replace(old, new); return s
    return target.replace(old, new)

# ---------- split sections ----------
first = s.index('<!-- 1 · Title -->')
end = s.index('</main>')
head, body, tail = s[:first], s[first:end], s[end:]
secs = re.findall(r'<!-- [^\n]*-->\n<section class="slide.*?</section>\n', body, re.S)
assert len(secs) == 15, len(secs)
S = {}
for sec in secs:
    sid = re.search(r'id="(s\d+)"', sec).group(1)
    sec = re.sub(r'\n  <div class="say" hidden>.*?</div>\n(?=</section>)', '\n', sec, flags=re.S)
    S[sid] = sec

def act(tag, text, timer=None, extra=''):
    t = f'<span class="mini" data-sec="{timer}"><button class="btn" type="button">Start {timer // 60}:{timer % 60:02d}</button><span class="t" aria-live="polite">{timer // 60}:{timer % 60:02d}</span></span>' if timer else ''
    return f'<div class="act"><span class="tag">{tag}</span><p>{text}</p>{t}{extra}</div>'

def tallies(labels):
    btns = ''.join(f'<button class="tally" type="button"><span>{l}</span><b>0</b></button>' for l in labels)
    return f'<div class="tallies" aria-label="Hand count">{btns}<button class="tally-reset" type="button">Reset</button></div>'

# 1 title
S['s1'] = S['s1'].replace(' · <kbd>N</kbd> speaker notes', '').replace('Travis Masingale · Design, EWU · October 2026', 'Bring a phone or laptop')
# 2 faces: hand-count tallies
S['s2'] = rep('<p class="ask">Hands up if you\'ve met one of these.</p>',
  '<p class="ask">Hands up: who has met each one?</p>' + tallies(['Clawd', 'Codex pet', 'Dots', 'Jolly', 'None']), S['s2'])
# 3 cute: turn and talk
S['s3'] = rep('<p class="thinker"><span class="pixel">Q:</span> So who is doing the thinking?</p>',
  act('Turn + talk', 'Has an app ever felt like a friend? Did you check it less because of that?', 60) +
  '\n        <p class="thinker"><span class="pixel">Q:</span> So who is doing the thinking?</p>', S['s3'])
# 4 class: poll
S['s4'] = rep('<div class="host-row">',
  act('Poll', 'How do you study now? Hands up for each one you do.') + tallies(['Reread', 'Highlight', 'Quiz myself', 'Ask AI']) + '\n        <div class="host-row">', S['s4'])
# 5 notebook: phones out
S['s5'] = rep('<p class="demo">Live demo › ask the chat a question, click the [1]</p>',
  act('Phones out', 'Open notebook.google.com and sign in with your @ewu.edu account. Thumbs up when you\'re in.') +
  '\n    <p class="demo">Watch › ask the chat a question, click the [1]</p>', S['s5'])
# 6 results: predict, then reveal the test column
S['s6'] = rep('<span class="res-num bad">17%<small>worse</small></span>',
  '<button class="cover" type="button" aria-label="Reveal result"><span class="res-num bad">17%<small>worse</small></span><span class="q">?</span></button>', S['s6'])
S['s6'] = rep('<span class="res-num gold">No drop<small>held steady</small></span>',
  '<button class="cover" type="button" aria-label="Reveal result"><span class="res-num gold">No drop<small>held steady</small></span><span class="q">?</span></button>', S['s6'])
S['s6'] = rep('<div class="studies">',
  act('Predict', 'When the AI was taken away for the test, how did each group do? Thumbs up for better, down for worse.', extra='<button class="btn btn-primary reveal-covers" type="button">Reveal</button>') + '\n    <div class="studies">', S['s6'])
# 7 learning: retrieval demo
S['s7'] = rep('<div class="host-row">',
  act('Try it', 'Retrieval, right now: without scrolling back, write the names of all four mascots from the start.', 30,
      '<button class="btn" type="button" data-reveal="mascotAns">Show answer</button>') +
  '<p class="answer" id="mascotAns" hidden>Clawd · Codex pet · Dots · Jolly. That little struggle to remember is what makes it stick.</p>\n    <div class="host-row">', S['s7'])
# 8 brain first: hand count
S['s8'] = rep('<p class="pet-caption">The best AI moment is when it waits for you.</p>',
  '<p class="pet-caption">The best AI moment is when it waits for you.</p>', S['s8'])
S['s8'] = rep('</ol>\n      </div>',
  '</ol>\n        ' + act('Hands up', 'Who has pasted an AI answer without checking it? No judgment.') + tallies(['Hands']) + '\n      </div>', S['s8'])
# 9 cycle: which stage do you skip
S['s9'] = rep('<p class="summary-note">Summaries live at the start of the cycle. Never at the end.</p>',
  act('Vote', 'Which stage do you skip most? Hands up as each one is called.') + tallies(['Preview', 'Attend', 'Review', 'Study', 'Assess']) +
  '\n    <p class="summary-note">Summaries live at the start of the cycle. Never at the end.</p>', S['s9'])
# 10 prompts: finger vote
S['s10'] = rep('<span>Quick poll: with or for?</span>', '<span>Vote on every card</span>', S['s10'])
S['s10'] = rep('<div class="flips" id="flips">',
  act('Vote', 'Fingers up: 1 = thinks with you, 2 = thinks for you, 3 = depends. Then tap the card.') + '\n    <div class="flips" id="flips">', S['s10'])
# 13 rules: thumbs
S['s13'] = rep('<span>Keep these</span>', '<span>Thumbs check</span>', S['s13'])
S['s13'] = rep('<div class="rails">',
  act('Thumbs', 'Which rule will be hardest for you to keep? Hold up 1 to 5 fingers.') + '\n    <div class="rails">', S['s13'])
# 14 ten weeks: you are here
# 15 your move: exit ticket
S['s15'] = rep('<div class="qa">',
  act('Exit ticket', 'Brain dump: write three things you remember from today. Then compare with a neighbor.', 120) + '\n    <div class="qa">', S['s15'])
S['s15'] = rep('<details class="sources">', '<p class="tut-link">Step-by-step tutorial: <a href="https://claude.ai/artifact/NQ1SdRFPmvbp355UwoXMVJ" target="_blank" rel="noopener">Build Your Study Notebook</a></p>\n    <details class="sources">', S['s15'])
S['s15'] = rep('<p>Do the 20-minute Notebook Sprint before your next class.</p>',
  '<p>Do the 20-minute Notebook Sprint before your next class. It\'s on the last slide.</p>', S['s15'])
# 11 sprint becomes optional final slide
S['s11'] = rep('<span class="badge b-yellow">Workshop</span><span>Any reading, slides or unit</span>',
  '<span class="badge b-yellow">Optional</span><span>If there\'s time · 20 minutes · any reading, slides or unit</span>', S['s11'])
S['s11'] = rep('<h2>Try it: the 20-minute <span class="hl hl-yellow">Notebook Sprint.</span></h2>',
  '<h2>Optional: the 20-minute <span class="hl hl-yellow">Notebook Sprint.</span></h2>', S['s11'])

# new slide: spot the AI's mistake
SPOT = '''<!-- Spot the mistake -->
<section class="slide" id="sX" data-title="Spot the AI's mistake">
  <div class="slide-inner">
    <div class="meta"><span class="num">00/16</span><span class="badge b-cyan">Check</span><span>Game</span></div>
    <h2>Spot the <span class="hl hl-cyan">AI's mistake.</span></h2>
    <div class="cols">
      <div class="slide-inner" style="gap:1rem">
        <p class="label">Example · a notebook summarized today's talk</p>
        <div class="ai-answer"><span class="ai-tag">Notebook</span><p>“In Study A, students who used a regular chatbot to get answers did 48% better on the test. <button class="cite-btn" type="button" data-reveal="srcBox" aria-label="Show source 1">1</button>”</p></div>
        <div class="source" id="srcBox" hidden><span class="label">Source 1 · slide 6</span><p>Used a regular AI chatbot to get answers: <b>48% better</b> while practicing with AI. <b>17% worse</b> on the test, with no AI.</p></div>
        ''' + act('Vote', 'Thumbs up if the summary is right. Thumbs down if something is off. Then click the [1].') + '''
        <button class="btn btn-primary" type="button" data-reveal="mistakeAns" style="justify-self:start">Reveal the mistake</button>
        <p class="answer" id="mistakeAns" hidden>It swapped <b>practice</b> and <b>test</b>. The chatbot group did 48% better while practicing and <b>17% worse on the test</b>. One click on the receipt caught it.</p>
      </div>
      <div class="jolly-stage">
        <p class="bubble">Looks right to me!</p>
        <figure class="sticker sh-yellow" style="--tilt:-3deg; margin:0; width:min(100%, 13rem)"><img src="img/jolly.jpg" alt="Jolly, Meta's plush mascot"></figure>
      </div>
    </div>
  </div>
</section>
'''
order = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s12','SPOT','s13','s14','s15','s11']
chunks = []
for i, k in enumerate(order, 1):
    c = SPOT if k == 'SPOT' else S[k]
    c = re.sub(r'id="s(\d+|X)"', f'id="s{i}"', c, count=1)
    c = re.sub(r'<span class="num">\d\d/1[56]</span>', f'<span class="num">{i:02d}/16</span>', c, count=1)
    chunks.append(c)
s = head + ''.join(chunks) + tail

# ---------- page-level edits ----------
rep('<title>Brain First, Bot Second</title>', '<title>Brain First Interactive</title>')
rep('    <button class="hbtn" type="button" id="notesBtn" aria-pressed="false" aria-controls="notes">Notes</button>\n', '')
rep("  notesBtn.addEventListener('click', () => toggleNotes());", "  if (notesBtn) notesBtn.addEventListener('click', () => toggleNotes());")
rep("      case 'n': case 'N': toggleNotes(); break;\n", '')
rep("try { bc = new BroadcastChannel('brain-first-deck'); }", "try { bc = new BroadcastChannel('brain-first-interactive'); }")

CSS = '''
/* ---------- interactive: activities, tallies, timers, reveals ---------- */
.act { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem 1rem; padding: 0.85rem 1rem; border: 2px dashed var(--yellow); background: var(--yellow-soft); min-width: 0; }
.act .tag { font: 400 0.75rem/1 var(--font-pixel); color: var(--on-accent); background: var(--yellow); padding: 0.45rem 0.55rem 0.4rem; letter-spacing: .05em; }
.act p { flex: 1 1 16rem; min-width: 0; font: 600 clamp(1rem, 1.35vw, 1.2rem)/1.35 var(--font-sans); }
.mini { display: inline-flex; align-items: center; gap: 0.6rem; }
.mini .t { font: 700 1.35rem/1 var(--font-pixel); font-variant-numeric: tabular-nums; min-width: 3.2em; }
.mini.done .t { color: var(--red); animation: pulse 0.6s steps(2) 4; }
.tallies { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }
.tally { cursor: pointer; display: inline-flex; align-items: center; gap: 0.7rem; padding: 0.55rem 0.8rem; border: 2px solid var(--fg); background: var(--card); color: var(--fg); font: 500 0.95rem/1 var(--font-mono); box-shadow: 3px 3px 0 var(--line); }
.tally:hover { border-color: var(--green); }
.tally:active { transform: translate(2px, 2px); box-shadow: 1px 1px 0 var(--line); }
.tally b { font: 700 1.15rem/1 var(--font-pixel); color: var(--green); min-width: 1.6em; text-align: right; }
.tally-reset { cursor: pointer; background: none; border: 0; color: var(--muted); font: 400 0.8rem/1 var(--font-mono); text-decoration: underline; padding: 0.4rem; }
.cover { position: relative; cursor: pointer; padding: 0; border: 0; background: none; text-align: left; }
.cover .q { position: absolute; inset: -0.2rem; display: grid; place-items: center; background: var(--inset); border: 2px dashed var(--yellow); color: var(--yellow); font: 700 2.2rem/1 var(--font-sans); }
.cover.open .q { display: none; }
.answer { padding: 0.85rem 1rem; border-left: 4px solid var(--green); background: var(--green-soft); font-size: clamp(1rem, 1.35vw, 1.2rem); }
.ai-answer { display: grid; gap: 0.6rem; padding: 1rem 1.1rem; background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--cyan); }
.ai-answer .ai-tag { font: 400 0.75rem/1 var(--font-pixel); color: var(--cyan-text); }
.ai-answer p { font-size: clamp(1.1rem, 1.6vw, 1.4rem); line-height: 1.45; }
.cite-btn { cursor: pointer; display: inline-grid; place-items: center; min-width: 1.6em; height: 1.6em; padding: 0 0.3em; margin-left: 0.2em; vertical-align: 0.15em; border: 0; background: var(--cyan); color: var(--on-accent); font: 700 0.8rem/1 var(--font-mono); }
.source { display: grid; gap: 0.4rem; padding: 0.9rem 1rem; background: var(--paper); color: var(--on-accent); box-shadow: 5px 5px 0 var(--cyan); }
.source .label { color: var(--on-accent); }
.tut-link { font: 500 1rem/1.4 var(--font-mono); color: var(--muted); }
.tut-link a { color: var(--cyan-text); }
'''
rep('@media (prefers-reduced-motion: reduce) {', CSS + '\n@media (prefers-reduced-motion: reduce) {')

JS = '''
  /* classroom activities: tallies, mini timers, reveals */
  document.querySelectorAll('.tallies').forEach(g => {
    const btns = [...g.querySelectorAll('.tally')];
    btns.forEach(b => {
      const n = b.querySelector('b');
      b.addEventListener('click', e => { n.textContent = Math.max(0, +n.textContent + (e.shiftKey ? -1 : 1)); });
      b.addEventListener('contextmenu', e => { e.preventDefault(); n.textContent = Math.max(0, +n.textContent - 1); });
    });
    g.querySelector('.tally-reset').addEventListener('click', () => btns.forEach(b => { b.querySelector('b').textContent = '0'; }));
  });
  document.querySelectorAll('.mini').forEach(m => {
    const total = +m.dataset.sec, btn = m.querySelector('button'), out = m.querySelector('.t');
    let left = total, run = false, last = 0, raf = 0;
    const show = () => { const sec = Math.ceil(left); out.textContent = `${Math.floor(sec / 60)}:${pad(sec % 60)}`; };
    const label = () => { btn.textContent = run ? 'Pause' : (left <= 0 ? 'Again' : (left < total ? 'Resume' : `Start ${Math.floor(total / 60)}:${pad(total % 60)}`)); };
    function tickMini(now) {
      left -= (now - last) / 1000; last = now;
      if (left <= 0) { left = 0; run = false; m.classList.add('done'); out.textContent = 'Time!'; label(); chime(); return; }
      show(); raf = requestAnimationFrame(tickMini);
    }
    btn.addEventListener('click', () => {
      if (left <= 0) { left = total; m.classList.remove('done'); }
      run = !run;
      if (run) { last = performance.now(); raf = requestAnimationFrame(tickMini); } else cancelAnimationFrame(raf);
      show(); label();
    });
  });
  document.querySelectorAll('[data-reveal]').forEach(b => {
    b.addEventListener('click', () => { const el = document.getElementById(b.dataset.reveal); if (el) el.hidden = false; });
  });
  document.querySelectorAll('.cover').forEach(c => c.addEventListener('click', () => c.classList.add('open')));
  document.querySelectorAll('.reveal-covers').forEach(b => b.addEventListener('click', () => {
    b.closest('.slide').querySelectorAll('.cover').forEach(c => c.classList.add('open'));
  }));
'''
rep('  /* start */', JS + '\n  /* start */')

out = root / 'src' / 'interactive' / 'index.html'
out.write_text(s)
print('wrote', out, len(s), 'slides', s.count('<section class="slide'))
