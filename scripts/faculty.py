"""Build faculty/index.html from the presenter deck: faculty speaker notes, presenter guide, learning links."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'build' / 'general.html').read_text()

def rep(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new)

def L(href, text):
    return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'

LINKS = {
 'rename': L('https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/', 'Google: NotebookLM is now Gemini Notebook'),
 'app': L('https://notebook.google.com/', 'notebook.google.com'),
 'help': L('https://support.google.com/notebooklm', 'Gemini Notebook (NotebookLM) Help Center'),
 'classroom': L('https://workspaceupdates.googleblog.com/2026/04/students-can-now-create-personal-class-notebooks-with-NotebookLM-in-Google-Classroom.html', 'Workspace Updates: student class notebooks'),
 'ewu': L('https://support.ewu.edu/support/solutions/articles/10000097642-What-AI-Options-Are-Available-to-EWU-Accounts-', 'EWU IT: AI options for EWU accounts'),
 'bastani': L('https://doi.org/10.1073/pnas.2422633122', 'Bastani et al., PNAS 2025'),
 'bastani_ssrn': L('https://papers.ssrn.com/abstract=4895486', 'free preprint (SSRN)'),
 'wharton': L('https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education/', 'Wharton summary'),
 'kestin': L('https://news.harvard.edu/gazette/story/2025/10/what-if-ai-could-help-students-learn-not-just-do-assignments-for-them/', 'Harvard Gazette on Kestin et al.'),
 'cycle': L('https://learningcenter.unc.edu/tips-and-tools/the-study-cycle/', 'UNC Learning Center: The Study Cycle'),
 'retrieval': L('https://www.retrievalpractice.org/', 'RetrievalPractice.org'),
 'ls': L('https://www.learningscientists.org/downloadable-materials', 'The Learning Scientists: six strategies'),
 'dunlosky': L('https://journals.sagepub.com/doi/10.1177/1529100612453266', 'Dunlosky et al. 2013, effective learning techniques'),
 'fortune': L('https://fortune.com/2026/10/02/meta-openai-ai-agent-mascots-jolly-dots-trust/', 'Fortune: AI agent mascots and trust'),
 'pets': L('https://penchan.co/en/ai/coding/codex-pets/', 'Codex pets guide'),
 'dots': L('https://designcompass.org/en/2026/09/30/openai-dots-always-on-ai-agents/', 'OpenAI Dots'),
 'jolly': L('https://www.avclub.com/jolly-ai-agent-subject-of-sexy-memes-meta', 'Meta Jolly'),
 'clawd': L('https://www.starkinsider.com/2025/10/clawd-ai-retro-mascot-command-line.html', 'Clawd'),
 'openstax': L('https://openstax.org/subjects', 'OpenStax: free, openly licensed textbooks'),
 'tutorial': L('https://claude.ai/artifact/NQ1SdRFPmvbp355UwoXMVJ', 'Build Your Study Notebook (step-by-step tutorial)'),
 'walkthrough': L('https://claude.ai/artifact/XgzXbB1abJcDm5dLf8bHwz', 'Brain First walk-through (self-paced version of this talk)'),
 'interactive': L('https://claude.ai/artifact/Ga9MWn5DB1hp4aYnJ1ReP7', 'Brain First Interactive (this deck with class activities)'),
}

def note(do=None, say=(), more=(), ask=None):
    out = []
    if do: out.append(f'<p class="cue"><b>Do</b> {do}</p>')
    out += [f'<p>{t}</p>' for t in say]
    if ask: out.append(f'<p class="ask"><b>If asked</b> {ask}</p>')
    if more: out.append('<p class="more"><b>Learn more</b> ' + ' · '.join(LINKS[k] for k in more) + '</p>')
    return out

NOTES = {
's1': note(do='Projector window: press F. Your window: press N for these notes and G for the presenter guide. Advancing either window moves both.',
  say=["Hi everyone. In this course you'll read, take notes and study a lot. Today I'll show you how to use Gemini Notebook so it helps you actually learn the material, not just get through it.",
       "Three things: why AI helps some students and hurts others, one 20-minute study routine, and a few rules. Then your questions."]),
's2': note(do='Ask for a show of hands. If the room is quiet, click a mascot for a one-liner.',
  say=["Quick show of hands. Who has seen one of these?",
       "The pixel crab is Clawd. It greets you every time you open Claude Code. The blue robot with the little prompt on its face is a Codex pet. Since May it floats on your desktop and pings you when the AI needs you.",
       "The fuzzy ones are newer. OpenAI launched Dots on September 29. Meta launched its Muse agent and gave it Jolly, a plush character with rosy cheeks. Every company decided, at about the same time, that its AI needed a face."],
  more=('clawd','pets','dots','jolly')),
's3': note(say=["Here's a secret about these mascots. They exist to make you trust the AI. <i>Fortune</i> ran a piece in October on exactly this: a character makes people treat AI less like software and more like a companion.",
       "That's great for these companies. It can be bad for your learning. When AI feels like a friend, you stop checking it. And a friend will happily do your homework.",
       "So today's question is simple: who is doing the thinking? You, or the bot?"],
  more=('fortune',)),
's4': note(do='Optional: show where your course posts readings, and point to the AI policy in your syllabus.',
  say=["Every course already hands you study material: readings, slides, your own notes, problem sets. Gemini Notebook turns that material into a study partner.",
       "The rule is simple: AI should support your learning, not replace it. Every course sets its own AI rules, so check the syllabus. The rest of this talk is how to follow that rule."],
  ask="“Can I upload anything?” Upload only what you have the right to use: your notes, materials your instructor provides, open textbooks. Never other people's work or personal information.",
  more=('openstax',)),
's5': note(do='Live demo. Before class, build a notebook with one reading or set of slides from your course. In class, type one question into the chat and click the [1] at the end of the answer.',
  say=["If you've heard of NotebookLM, this is the same tool with a new name. Google renamed it Gemini Notebook in July.",
       "Here's what makes it different from a regular chatbot. You hand it sources, like a reading or your lecture slides, and it answers from those sources. Answers in the chat end with numbered citations that jump to the exact sentence. The Studio panel turns a chapter into an audio overview, a mind map, flashcards or a quiz. Those Studio items don't show citations, so check them in the chat.",
       "Two practical notes. Upload only what you have the right to use: your notes, materials your instructor provides, open textbooks. And sign in with your EWU account, which has data protections a personal account doesn't."],
  ask="“Can I use my personal Gmail?” Use your EWU account. It carries data protections a personal account doesn't.",
  more=('rename','app','help','ewu','classroom')),
's6': note(say=["Two studies. In the first, about a thousand high school students practiced math with AI. The ones using a regular chatbot to get answers did 48 percent better while practicing. Then the AI was taken away for the test, and they did 17 percent worse than students who never used it. They let the bot do the thinking.",
       "Another group used an AI tutor that only gave hints. They did 127 percent better while practicing, and their test scores didn't drop.",
       "In the second study, Harvard physics students learned more than twice as much with an AI tutor that made them do the thinking, in less time than a regular class.",
       "Same technology. Opposite results. The tool doesn't decide. How you use it decides."],
  ask="“Was it ChatGPT?” Study A used GPT-4 in a ChatGPT-style chat window. The tutor version used the same model with instructions to give hints instead of answers.",
  more=('bastani','bastani_ssrn','wharton','kestin')),
's7': note(say=["Saundra McGuire's Study Cycle gives us a shared language: preview, attend, review, study, assess.",
       "Two ideas sit underneath it. First, retrieval beats rereading. Pulling an idea out of your own head is what makes it stick, even when you get it wrong.",
       "Second, fluency fools you. A clean, smooth summary feels like knowing. An AI summary is the smoothest text you'll ever read. So if you catch yourself thinking “I read the summary, I've got it,” translate that to “I haven't tested myself yet.”"],
  more=('cycle','retrieval','ls','dunlosky')),
's8': note(do='Click through the four status states and finish on “Needs input.”',
  say=["Here's the one rule I want you to leave with: brain first, bot second. Generate, then check, then fix.",
       "The Codex pet helps explain it. Its status bubble has four states: running, needs input, ready and blocked. For learning, the state you want is “needs input.” The AI should spend most of its time waiting for you to think. If the bot never waits, you never think."]),
's9': note(do='Click each stage in order. Read the “Try” prompt aloud.',
  say=["Here's how the notebook tools fit the Study Cycle.",
       "Preview is where summaries and audio overviews belong. They're a trailer for the chapter, not a replacement. Attend: bring a question the notebook couldn't answer.",
       "Review and Study are where quizzes and flashcards shine, because they make you retrieve. Assess: take a quiz without looking, then check the citations for what you missed.",
       "Notice where the summary sits: at the start, never at the end."],
  more=('cycle',)),
's10': note(do='Read a card aloud, ask “with or for?”, let the room vote by hand, then tap to reveal. Use Reveal all if time is short.',
  say=["You don't need to be a prompt expert. You need a few good sentences.",
       "“With you” prompts put you to work: the notebook asks, waits and critiques. “For you” prompts hand the work to the bot. My favorite: write your own explanation first, then ask what you missed, with a citation.",
       "The yellow ones depend on you. Flashcards only help if you actually quiz yourself."]),
's11': note(do='Decide before class: run the sprint now (20 minutes, students need laptops or phones and one reading from your course) or assign it for homework. The timer chimes between steps.',
  say=["Here's a routine for any reading or unit. Twenty minutes.",
       "Start with your screen down and write what you remember. That's “brain first.” Then build a notebook and let it quiz you.",
       "Then check the receipts: click two citations and see whether the page really says that. Finish with a partner: what did you miss, and what did the notebook miss? The exit line goes in your notes."]),
's12': note(do='If you skipped the demo on slide 5, show a citation now.',
  say=["Receipts are the little numbered citations at the end of the notebook's chat answers. Click one and it jumps to the exact sentence in your source. Flashcards and Studio quizzes don't show them, so if a flashcard seems off, ask in the chat: “Where in my sources does this come from?”",
       "Even with receipts, it still makes mistakes. It pulls a sentence out of context. It flattens a nuance. It skips what your class focused on. So click the citation, read the sentence it points to, and name one thing it got wrong or left out. Catching the AI's mistake is a win."],
  more=('help',)),
's13': note(say=["Five rules. Use your EWU account. Upload course materials, never other people's information. Say when you used AI and how; one sentence is enough.",
       "Your reflections stay yours, so write them in your own words. And every course sets its own AI rules, so if you're not sure what's allowed, ask before you submit."],
  ask="“Can I use AI in my other classes?” Each class sets its own rules. Check the syllabus or ask that instructor.",
  more=('ewu',)),
's14': note(say=["Here's how this plays out across your term. At the start, try things. Early on, learn the method: do the sprint once, on purpose. Through the middle, you choose the tool that fits each task, and you know why. That's thinking about your own learning, which is exactly what McGuire's cycle asks for.",
       "At the end of the term, look back: what helped, and what didn't, before finals."]),
's15': note(do='Open the floor. Leave this slide up during questions.',
  say=["Three moves. Today, build a notebook for one course and try three prompts from today. This week, do the 20-minute sprint before your next class. Every week, ask yourself: what did AI help with, and what didn't it?",
       "The mascots will keep getting cuter. You'll be fine if you keep one habit: brain first, bot second. Thanks. What questions do you have?"]),
}

for sid, paras in NOTES.items():
    start = s.index(f'id="{sid}"')
    a = s.index('<div class="say" hidden>', start)
    b = s.index('</div>\n</section>', a)
    s = s[:a] + '<div class="say" hidden>\n' + '\n'.join('    ' + p for p in paras) + '\n  ' + s[b:]

# title + byline
rep('<title>Brain First, Bot Second</title>', '<title>Brain First Faculty Deck</title>')
rep('<p class="byline">Travis Masingale · Design, EWU · October 2026</p>',
    '<p class="byline"><span id="presenterOut">Your instructor</span> · <span id="courseOut">Your course</span></p>')

# HUD guide button
rep('<button class="hbtn" type="button" id="notesBtn" aria-pressed="false" aria-controls="notes">Notes</button>',
    '<button class="hbtn" type="button" id="guideBtn" aria-controls="guide">Guide</button>\n    <button class="hbtn" type="button" id="notesBtn" aria-pressed="false" aria-controls="notes">Notes</button>')

GUIDE = f'''
<div class="guide" id="guide" hidden role="dialog" aria-modal="true" aria-labelledby="guideTitle">
  <div class="guide-inner">
    <div class="guide-top">
      <p class="meta"><span class="badge b-yellow">Presenter guide</span><span>Press G or Esc to close</span></p>
      <button class="hbtn" type="button" id="guideClose">Close</button>
    </div>
    <h2 id="guideTitle">Present <span class="hl hl-red">Brain First, Bot Second.</span></h2>
    <p class="body">A 15-slide talk for students in any course or discipline, about 17 minutes plus questions, or about 37 with the in-class sprint. The slides speak to students. These notes and this guide are for you.</p>
    <div class="guide-grid">
      <section class="card card-top-cyan">
        <h3>Name and course on slide 1</h3>
        <label class="label" for="presenterName">Presenter name</label>
        <input id="presenterName" type="text" placeholder="Your instructor" autocomplete="name">
        <label class="label" for="courseName">Course</label>
        <input id="courseName" type="text" placeholder="Your course">
        <p class="small">Saved in this browser only.</p>
      </section>
      <section class="card card-top-green">
        <h3>Two screens</h3>
        <ol class="glist">
          <li>Open this page in two windows.</li>
          <li>Projector window: press <kbd>F</kbd>.</li>
          <li>Laptop window: press <kbd>N</kbd> for notes.</li>
          <li>Advance either window. Both move.</li>
        </ol>
        <p class="small"><kbd>→</kbd> next · <kbd>←</kbd> back · <kbd>G</kbd> this guide · click a mascot for a line</p>
      </section>
      <section class="card card-top-yellow">
        <h3>Before class</h3>
        <ul class="checks">
          <li><input type="checkbox" id="pc1"><label for="pc1">Sign in at {LINKS['app']} with your @ewu.edu account.</label></li>
          <li><input type="checkbox" id="pc2"><label for="pc2">Add one reading or set of slides from your course to a new notebook.</label></li>
          <li><input type="checkbox" id="pc3"><label for="pc3">Ask the chat one question and find the [1] citation for the slide 5 demo.</label></li>
          <li><input type="checkbox" id="pc4"><label for="pc4">Make a set of flashcards in Studio so you know where Studio lives.</label></li>
          <li><input type="checkbox" id="pc5"><label for="pc5">Decide: run the 20-minute sprint in class or assign it.</label></li>
        </ul>
      </section>
      <section class="card card-top-red">
        <h3>Check before you promise</h3>
        <p>Some students are under 18. Google's April 2026 Classroom notebook feature requires students 18 or older. Ask EWU IT what under-18 students can use, and have a non-AI version of the sprint ready: brain dump, then self-quiz from the reading's headings.</p>
        <p class="small">EWU's own list: {LINKS['ewu']}</p>
      </section>
    </div>
    <div class="guide-grid two-up">
      <section class="card">
        <h3>Learn the tech</h3>
        <ul class="links">
          <li>{LINKS['rename']}</li>
          <li>{LINKS['help']}</li>
          <li>{LINKS['classroom']}</li>
          <li>{LINKS['ewu']}</li>
          <li>{LINKS['openstax']}</li>
        </ul>
      </section>
      <section class="card">
        <h3>Learn the study methods</h3>
        <ul class="links">
          <li>{LINKS['cycle']} (Saundra McGuire)</li>
          <li>{LINKS['retrieval']} (retrieval practice for teachers)</li>
          <li>{LINKS['ls']}</li>
          <li>{LINKS['dunlosky']}</li>
        </ul>
      </section>
      <section class="card">
        <h3>The research on slide 6</h3>
        <ul class="links">
          <li>{LINKS['bastani']} · {LINKS['bastani_ssrn']} · {LINKS['wharton']}</li>
          <li>{LINKS['kestin']}</li>
        </ul>
      </section>
      <section class="card card-top-green">
        <h3>Share with students</h3>
        <ul class="links">
          <li>{LINKS['tutorial']}</li>
          <li>{LINKS['walkthrough']}</li>
          <li>{LINKS['interactive']}</li>
        </ul>
        <p class="small">Each link opens only for people you share it with. Use the Share menu on each page.</p>
      </section>
      <section class="card">
        <h3>The mascots</h3>
        <ul class="links">
          <li>{LINKS['fortune']}</li>
          <li>{LINKS['clawd']} · {LINKS['pets']} · {LINKS['dots']} · {LINKS['jolly']}</li>
        </ul>
      </section>
    </div>
  </div>
</div>
'''
rep('<aside class="notes" id="notes"', GUIDE + '\n<aside class="notes" id="notes"')

CSS = '''
/* ---------- faculty: notes structure + presenter guide ---------- */
.notes .cue { font: 500 0.9rem/1.5 var(--font-mono); color: var(--cyan-text); }
.notes .ask { font-size: 0.95rem; color: var(--yellow); }
.notes .more { font: 400 0.85rem/1.6 var(--font-mono); color: var(--muted); }
.notes b { font-family: var(--font-pixel); font-weight: 400; font-size: 0.75rem; letter-spacing: .06em; margin-right: 0.4rem; text-transform: uppercase; }
.notes a, .guide a { color: var(--cyan-text); }
.guide { position: fixed; inset: 0; z-index: 40; overflow-y: auto; background: var(--bg); padding: calc(env(safe-area-inset-top, 0px) + 1.5rem) clamp(16px, 4vw, 3.5rem) 3rem; }
.guide-inner { max-width: 75rem; margin-inline: auto; display: grid; gap: 1.25rem; }
.guide-top { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.guide h2 { font-size: clamp(1.8rem, 3.6vw, 3rem); }
.guide-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; }
.guide-grid.two-up { grid-template-columns: repeat(2, minmax(0, 1fr)); }
@media (max-width: 1000px) { .guide-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 640px) { .guide-grid, .guide-grid.two-up { grid-template-columns: minmax(0, 1fr); } }
.guide .card { display: grid; gap: 0.6rem; align-content: start; }
.guide .card p, .guide li { font-size: 0.95rem; line-height: 1.5; }
.guide input[type="text"] { width: 100%; padding: 0.6rem 0.7rem; background: var(--inset); color: var(--fg); border: 1px solid var(--line); font: 500 1rem/1.2 var(--font-sans); }
.glist { list-style: decimal; padding-left: 1.2rem; display: grid; gap: 0.3rem; }
.checks { display: grid; gap: 0.5rem; }
.checks li { display: grid; grid-template-columns: 1.4rem minmax(0, 1fr); gap: 0.5rem; align-items: start; }
.checks input { width: 1.1rem; height: 1.1rem; margin-top: 0.2rem; accent-color: var(--yellow); }
.links { display: grid; gap: 0.5rem; }
.links li::before { content: "› "; color: var(--green); font-family: var(--font-mono); }
.guide kbd { font: 500 0.75rem/1 var(--font-mono); padding: 3px 0.35rem; border: 1px solid var(--line); border-bottom-width: 3px; background: var(--card); }
'''
rep('@media (prefers-reduced-motion: reduce) {', CSS + '\n@media (prefers-reduced-motion: reduce) {')

JS = '''
  /* presenter guide */
  const guide = document.getElementById('guide');
  const guideBtn = document.getElementById('guideBtn');
  function toggleGuide(force) {
    const open = typeof force === 'boolean' ? force : guide.hidden;
    guide.hidden = !open;
    if (open) document.getElementById('guideClose').focus(); else guideBtn.focus();
  }
  guideBtn.addEventListener('click', () => toggleGuide());
  document.getElementById('guideClose').addEventListener('click', () => toggleGuide(false));
  const nameIn = document.getElementById('presenterName'), nameOut = document.getElementById('presenterOut');
  try { const v = localStorage.getItem('bfbs-presenter'); if (v) { nameIn.value = v; nameOut.textContent = v; } } catch (e) {}
  const courseIn = document.getElementById('courseName'), courseOut = document.getElementById('courseOut');
  try { const c = localStorage.getItem('bfbs-course'); if (c) { courseIn.value = c; courseOut.textContent = c; } } catch (e) {}
  courseIn.addEventListener('input', () => {
    courseOut.textContent = courseIn.value.trim() || 'Your course';
    try { localStorage.setItem('bfbs-course', courseIn.value.trim()); } catch (e) {}
  });
  nameIn.addEventListener('input', () => {
    nameOut.textContent = nameIn.value.trim() || 'Your instructor';
    try { localStorage.setItem('bfbs-presenter', nameIn.value.trim()); } catch (e) {}
  });
  guide.querySelectorAll('.checks input').forEach(c => {
    try { c.checked = localStorage.getItem('bfbs-' + c.id) === '1'; } catch (e) {}
    c.addEventListener('change', () => { try { localStorage.setItem('bfbs-' + c.id, c.checked ? '1' : '0'); } catch (e) {} });
  });
'''
rep('  /* keyboard */', JS + '\n  /* keyboard */')
# keyboard: G toggles guide, Esc closes; ignore deck keys while guide is open
rep("""    if (t.closest && t.closest('input, textarea, select, [contenteditable]')) return;""",
    """    if (e.key === 'Escape' && !guide.hidden) { toggleGuide(false); return; }
    if (t.closest && t.closest('input, textarea, select, [contenteditable]')) return;
    if (e.key === 'g' || e.key === 'G') { toggleGuide(); return; }
    if (!guide.hidden) return;""")
rep('<kbd>N</kbd> speaker notes · <kbd>F</kbd> full screen · click a mascot</p>',
    '<kbd>N</kbd> speaker notes · <kbd>G</kbd> presenter guide · <kbd>F</kbd> full screen</p>')
rep("let bc = null, remote = false, bcTimer;\n  try { bc = new BroadcastChannel('brain-first-deck'); }",
    "let bc = null, remote = false, bcTimer;\n  try { bc = new BroadcastChannel('brain-first-faculty-deck'); }")

out = root / 'src' / 'faculty' / 'index.html'
out.write_text(s)
print('wrote', out, len(s))
