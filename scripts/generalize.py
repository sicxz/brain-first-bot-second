"""Derive build/general.html, a course- and discipline-agnostic deck, from the original ITGS talk deck (src/original/index.html).
See docs/GENERIC-SPEC.md. faculty.py and interactive.py build from general.html."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'src' / 'original' / 'index.html').read_text()

def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new)

CLAWD = '<svg class="clawd-svg" viewBox="0 0 18 10" shape-rendering="crispEdges"><path class="c-fill" d="M3 0h12v2H3zM3 2h2v2H3zM6 2h6v2H6zM13 2h2v2h-2zM1 4h16v2H1zM3 6h12v2H3z"/><path class="c-eyes" d="M5 2h1v2H5zM12 2h1v2h-1z"/><path class="c-fill c-legs-a" d="M4 8h1v2H4zM11 8h1v2h-1z"/><path class="c-fill c-legs-b" d="M6 8h1v2H6zM13 8h1v2h-1z"/></svg>'

# 1 title
rep('<span>ITGS 196 · First-Year Seminar</span>', '<span>For any course</span>')
# 2 faces
rep('data-title="This fall, AI got a face"', 'data-title="AI got a face"')
rep('<h2>This fall, AI got a <span class="hl hl-yellow">face.</span></h2>', '<h2>AI got a <span class="hl hl-yellow">face.</span></h2>')
# 4 rebuilt: your course is the source
a = s.index('<section class="slide" id="s4"'); b = s.index('<div class="host-row">', a)
s = s[:a] + '''<section class="slide" id="s4" data-title="Your course is the source" data-time="1:00">
  <div class="slide-inner">
    <div class="meta"><span class="num">04/15</span><span class="badge b-cyan">Context</span><span>Any course</span></div>
    <h2>Your course is <span class="hl hl-cyan">the source.</span></h2>
    <div class="cols" style="align-items:start">
      <div class="slide-inner" style="gap:16px">
        <p class="lede">Every course already hands you study material. Gemini Notebook turns it into a study partner.</p>
        <div class="chips" aria-label="Kinds of course material">
          <span class="chip">A reading</span><span class="chip">Lecture slides</span><span class="chip">Your notes</span><span class="chip">A lab manual</span><span class="chip">A problem set</span><span class="chip">A case study</span><span class="chip">An article</span><span class="chip">A study guide</span>
        </div>
        <div class="canvas-card">
          <div class="cc-head"><span>The rule</span><span>Every course</span></div>
          <div class="cc-body">
            <p class="cc-rule">AI should <span class="hl hl-red">support your learning, not replace it.</span></p>
          </div>
        </div>
      </div>
      <div class="slide-inner" style="gap:16px">
        <ul class="facts">
          <li class="fact"><span class="pixel">SYL</span><span>Check your syllabus. Every course sets its own AI rules.</span></li>
          <li class="fact"><span class="pixel">OK</span><span>Upload only what you have the right to use: your notes, materials your instructor provides, open textbooks.</span></li>
          <li class="fact"><span class="pixel">ASK</span><span>Not sure? Ask your instructor first.</span></li>
        </ul>
        ''' + s[b:]
# 5 notebook
rep('<p>It answers from the sources you add. Here, that\'s the OpenStax chapter.</p>', '<p>It answers only from the sources you add: your reading, slides or notes.</p>')
rep('Click one to jump to the exact sentence in the chapter.</p>', 'Click one to jump to the exact sentence in your source.</p>')
rep('<p>Upload the chapter PDF from Canvas. Add your own class notes too.</p>', '<p>Upload a reading or slides from your course. Add your own notes too.</p>')
rep('<p class="note"><span class="pixel">License</span><span>Your textbook, <i>College Success</i>, is openly licensed (CC BY 4.0), so uploading chapters is fine.</span></p>',
    '<p class="note"><span class="pixel">Rights</span><span>Upload only what you have the right to use. Never upload other people\'s work or personal information.</span></p>')
# 7 learning
rep('<span>Saundra McGuire, EWU, Sept 22</span>', '<span>Saundra McGuire\'s Study Cycle</span>')
# 9 cycle
rep('<p class="prompt" id="cdPrompt">Make a mind map of Chapter 4.</p>', '<p class="prompt" id="cdPrompt">Make a mind map of [this reading].</p>')
a = s.index('  const cycle = {'); b = s.index('  };', a) + 4
s = s[:a] + '''  const cycle = {
    preview: ['Preview', 'Play the audio overview on the walk to class. Skim the mind map.', 'Make a mind map of [this reading].', 'A trailer gives new ideas somewhere to land. It starts the cycle. It never replaces the reading.'],
    attend: ['Attend', 'Bring one question the notebook couldn\\u2019t answer.', 'List three questions [this reading] raises but doesn\\u2019t answer.', 'You arrive with a reason to listen and something to ask.'],
    review: ['Review', 'Right after class, quiz yourself on that day\\u2019s topic.', 'Quiz me on [topic], one question at a time. Wait for my answer before the next question.', 'McGuire\\u2019s cycle puts review as soon after class as possible. Retrieval does the work.'],
    study: ['Study', 'Flashcards first. Then explain a concept in your own words and ask what\\u2019s missing.', 'Here\\u2019s my explanation of [key idea]: [paste]. What did I miss? Cite my sources.', 'Explaining it yourself shows you what you actually know.'],
    assess: ['Assess', 'Take a practice quiz closed-book, then check citations on the ones you missed.', 'Make a 10-question quiz on [this unit]. After I finish, show which sources my misses came from.', 'Knowing what you know, and what you don\\u2019t, is metacognition.']
  };''' + s[b:]
# 10 flips
for old, new in [
    ('“Quiz me on Section 4.2, one question at a time. Wait for my answer.”', '“Quiz me on [topic], one question at a time. Wait for my answer before the next question.”'),
    ('“Summarize Chapter 4 so I don\'t have to read it.”', '“Summarize [this reading] so I don\'t have to read it.”'),
    ('“Here\'s my explanation of how to plan a degree path. What did I miss? Cite the chapter.”', '“Here\'s my explanation of [key idea]: [paste]. What did I miss? Cite my sources.”'),
    ('“Make me flashcards for Chapter 4.”', '“Make me flashcards for [this unit].”'),
    ('“Write my journal entry about time management.”', '“Write my reflection for me.”'),
    ('“Ask me three questions that connect this chapter to my major.”', '“Ask me three questions that connect [topic] to my major or my life.”'),
    ('“Which idea in this chapter do first-years usually misunderstand?”', '“Which idea in [this unit] do students usually misunderstand?”'),
    ('“Give me the answers to the quiz.”', '“Give me the answers to the homework.”'),
    ('<p>Retrieval, and the bot waits for the student.</p>', '<p>Retrieval, and the bot waits for you.</p>'),
    ('<p>The student generates first. The AI critiques, with receipts.</p>', '<p>You generate first. The AI critiques, with receipts.</p>'),
    ('<p>Great if they quiz themselves. Useless if they only read them.</p>', '<p>Great if you quiz yourself. Useless if you only read them.</p>'),
    ('<p>Ties new ideas to something the student cares about.</p>', '<p>Ties new ideas to something you care about.</p>'),
    ('<p>Useful as a pointer. The student still has to test it.</p>', '<p>Useful as a pointer. You still have to test it.</p>'),
]:
    rep(old, new)
# 11 sprint
rep('<span>This week · <i>College Success</i> Ch. 4</span>', '<span>Any reading, slides or unit</span>')
rep('List three things you remember from Ch. 4 and one question.', 'List three things you remember about your topic and one question.')
rep('New notebook. Add the Ch. 4 PDF from Canvas.', 'New notebook. Add your reading, slides or notes.')
rep('Does the page really say that?', 'Does the source really say that?')
rep('<span class="pixel">Exit line</span>For the journal: “AI helped me ___. It didn\'t help with ___.”', '<span class="pixel">Exit line</span>In your notes: “AI helped me ___. It didn\'t help with ___.”')
rep("tNow.textContent = 'Time! Exit line in the journal.';", "tNow.textContent = 'Time! Write your exit line.';")
# 12 receipts
rep('<p class="rc-sub">GEMINI NOTEBOOK · CH. 4 · ONE ANSWER</p>', '<p class="rc-sub">GEMINI NOTEBOOK · ONE ANSWER</p>')
rep('Ask in the chat: “Where in Ch. 4 does this come from?”', 'Ask in the chat: “Where in my sources does this come from?”')
rep('Click one and it jumps to the exact sentence in the chapter. Flashcards and Studio quizzes don\'t show them, so ask in the chat.',
    'Click one and it jumps to the exact sentence in your source. Flashcards and Studio quizzes don\'t show them, so ask in the chat.')
# 13 rules
rep('<h3>Reflection stays yours.</h3><p>The journal is already on paper.</p>', '<h3>Reflection stays yours.</h3><p>Write reflections in your own words.</p>')
rep('<p>Every class sets its own AI rules. Check the syllabus or ask your instructor.</p>', '<p>Every course sets its own AI rules. Check the syllabus or ask your instructor.</p>')
# 14 rebuilt: across your term
a = s.index('<!-- 14 · Ten weeks -->'); b = s.index('<div class="say" hidden>', a)
s = s[:a] + f'''<!-- 14 · Across your term -->
<section class="slide" id="s14" data-title="Across your term" data-time="1:00">
  <div class="slide-inner">
    <div class="meta"><span class="num">14/15</span><span class="badge b-green">Plan</span><span>Any course, any term</span></div>
    <h2>Across <span class="hl hl-green">your term.</span></h2>
    <div class="term">
      <div class="strip" aria-label="A term from start to end, colored by phase">
        <span class="walker" aria-hidden="true">{CLAWD}</span>
        <span class="c-try"></span><span class="c-try"></span><span class="c-teach"></span><span class="c-choose"></span><span class="c-choose"></span><span class="c-choose"></span><span class="c-choose"></span><span class="c-choose"></span><span class="c-choose"></span><span class="c-look"></span>
      </div>
      <p class="strip-ends"><span>Start of term</span><span>End of term</span></p>
      <div class="phases">
        <div class="phase ph-try"><span class="wk-range">Start of term</span><h3>Try it.</h3><p>Low stakes. One Studio tool a week.</p></div>
        <div class="phase ph-teach"><span class="wk-range">Early</span><h3>Learn the method.</h3><p>Do the Notebook Sprint once, on purpose.</p></div>
        <div class="phase ph-choose"><span class="wk-range">Middle</span><h3>You choose.</h3><p>Pick the tool that fits the task, and know why.</p></div>
        <div class="phase ph-look"><span class="wk-range">End of term</span><h3>Look back.</h3><p>What helped, what didn't, before finals.</p></div>
      </div>
    </div>
  </div>
  ''' + s[b:]
rep('.ph-try { color: var(--cyan-text); }', '.strip-ends { display: flex; justify-content: space-between; margin-top: -0.6rem; font: 400 0.75rem/1 var(--font-pixel); color: var(--muted); }\n.ph-try { color: var(--cyan-text); }')
# 15 your move
rep('<p>Build a notebook from Ch. 4. Try three prompts from today.</p>', '<p>Build a notebook for one course. Add this week\'s reading or notes. Try three prompts from today.</p>')
rep('<p>Do the 20-minute Notebook Sprint with Ch. 4.</p>', '<p>Do the 20-minute Notebook Sprint before your next class.</p>')
rep('<p>Answer one journal question: “What did AI help with, and what didn\'t it?”</p>', '<p>Ask yourself: “What did AI help with, and what didn\'t it?”</p>')
rep('data-lines="Partners, not answer keys!|Go try Chapter 4."', 'data-lines="Partners, not answer keys!|Go build a notebook."')
# sources
s = re.sub(r'\n\s*<li>ITGS 196 Canvas course: weekly Read pages and Learning Tools\.</li>', '', s)
s = re.sub(r'\n\s*<li><a href="https://openstax\.org/books/college-success/pages/preface"[^\n]*</li>', '', s)

leftover = re.findall(r'ITGS|Chapter 4|Ch\. 4|CH\. 4|Section 4|journal|College Success|degree path|first-year|this class|ten weeks|Sept 22', 
                      re.sub(r'<div class="say" hidden>.*?</div>\n(?=</section>)', '', s, flags=re.S))
print('leftover on-slide terms:', leftover)
(root / 'build').mkdir(exist_ok=True)
(root / 'build' / 'general.html').write_text(s)
print('wrote build/general.html', len(s))
