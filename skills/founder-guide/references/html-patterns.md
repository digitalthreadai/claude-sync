# HTML Component Library

Reusable patterns for generating self-contained HTML documentation pages. All pages share these foundations.

## Shared CSS Foundation

Every HTML file starts with this CSS custom properties block. Replace `--primary` and `--secondary` with the project's brand colors.

```css
:root {
  --bg: #0A0A0F;
  --surface: #12121A;
  --surface-hover: #1E1E2E;
  --terminal-bg: #1A1A2E;
  --terminal-border: #2A2A3E;
  --text: #E8E8ED;
  --muted: #8888A0;
  --muted-fg: #6E6E88;
  --primary: #FFD600;       /* Main accent — customize per project */
  --primary-rgb: 255, 214, 0;  /* rgba() companion — update when changing --primary */
  --primary-light: #FFFDE7;
  --secondary: #E87040;     /* Secondary accent — customize per project */
  --secondary-rgb: 232, 112, 64; /* rgba() companion — update when changing --secondary */
  --green: #4ADE80;
  --blue: #60A5FA;
  --purple: #A78BFA;
  --red: #F87171;
}
```

### Google Fonts Import

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Base Styles

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.6;
}
code, pre, .mono { font-family: 'JetBrains Mono', monospace; }
```

---

## Components

---

#### Layout & Typography

### 1. Gradient Text

```css
.gradient-text {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
```

### 2. Section Layout

```html
<section id="section-id">
  <div class="section-label">CATEGORY</div>
  <h2 class="section-title">Section Title</h2>
  <p class="section-desc">Description text here.</p>
  <!-- content -->
</section>
```

```css
section { padding: 5rem 1.5rem; max-width: 1200px; margin: 0 auto; }
.section-label {
  display: inline-block; font-size: 0.75rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--primary); margin-bottom: 0.75rem;
}
.section-title { font-size: clamp(1.75rem, 3vw, 2.5rem); font-weight: 800; margin-bottom: 0.5rem; }
.section-desc { color: var(--muted); font-size: 1rem; margin-bottom: 3rem; max-width: 600px; }
```

---

#### Code & Terminal

### 3. Terminal / Code Block

```html
<div class="terminal">
  <div class="terminal-bar">
    <span class="terminal-dot red"></span>
    <span class="terminal-dot yellow"></span>
    <span class="terminal-dot green"></span>
    <span class="terminal-title">title</span>
  </div>
  <button class="terminal-copy" onclick="copyCode(this)">Copy</button>
  <div class="terminal-body">
    <div><span class="prompt">$</span> <span class="cmd">npm install</span></div>
    <div><span class="comment"># comment</span></div>
  </div>
</div>
```

```css
.terminal {
  position: relative; background: var(--terminal-bg);
  border: 1px solid var(--terminal-border); border-radius: 12px;
  overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.terminal-bar {
  display: flex; align-items: center; gap: 6px;
  padding: 0.75rem 1rem; background: rgba(0,0,0,0.3);
  border-bottom: 1px solid var(--terminal-border);
}
.terminal-dot { width: 10px; height: 10px; border-radius: 50%; }
.terminal-dot.red { background: #FF5F57; }
.terminal-dot.yellow { background: #FEBC2E; }
.terminal-dot.green { background: #28C840; }
.terminal-body { padding: 1rem 1.25rem; font-size: 0.85rem; line-height: 1.8; }
.terminal-body .prompt { color: var(--green); }
.terminal-body .cmd { color: var(--text); }
.terminal-body .comment { color: var(--muted-fg); }
.terminal-copy {
  position: absolute; top: 0.6rem; right: 0.75rem;
  background: transparent; border: 1px solid var(--terminal-border);
  color: var(--muted); padding: 0.25rem 0.5rem; border-radius: 4px;
  font-size: 0.7rem; cursor: pointer; transition: all 0.2s;
}
.terminal-copy:hover { border-color: var(--primary); color: var(--primary); }
```

### 4. Copy Button JavaScript

```javascript
function copyCode(btn) {
  const block = btn.closest('.terminal') || btn.closest('.code-block');
  const code = block.querySelector('.terminal-body, .code-body').textContent;
  navigator.clipboard.writeText(code).then(() => {
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 2000);
  });
}
```

---

#### UI Components

### 5. Card Grid

```css
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1rem; }
.card {
  background: var(--surface); border: 1px solid var(--terminal-border);
  border-radius: 12px; padding: 1.25rem; transition: all 0.2s;
}
.card:hover { border-color: rgba(var(--primary-rgb), 0.3); transform: translateY(-2px); }
.card .label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted-fg); }
.card h3 { font-size: 1rem; font-weight: 700; }
.card .version {
  display: inline-block; font-size: 0.7rem; font-weight: 600;
  background: rgba(var(--primary-rgb), 0.1); color: var(--primary);
  padding: 0.15rem 0.5rem; border-radius: 4px;
}
.card p { font-size: 0.85rem; color: var(--muted); }
```

### 6. Sidebar Navigation (for strategy.html and setup.html)

```css
.sidebar {
  position: fixed; top: 0; left: 0; bottom: 0; width: 260px;
  background: var(--surface); border-right: 1px solid var(--terminal-border);
  padding: 1.5rem 0; overflow-y: auto; z-index: 100;
}
.sidebar nav a {
  display: block; padding: 0.45rem 1.25rem;
  color: var(--muted); text-decoration: none; font-size: 0.85rem;
  border-left: 2px solid transparent; transition: all 0.15s;
}
.sidebar nav a.active { color: var(--primary); border-left-color: var(--primary); background: rgba(var(--primary-rgb), 0.05); }
.main { margin-left: 260px; }

@media (max-width: 900px) {
  .sidebar { display: none; }
  .main { margin-left: 0; }
}
```

### 7. Scroll Spy JavaScript

```javascript
const sidebarLinks = document.querySelectorAll('.sidebar nav a');
const allSections = document.querySelectorAll('section[id], [id].step-section');
window.addEventListener('scroll', () => {
  let current = '';
  allSections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 120) current = s.id;
  });
  sidebarLinks.forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === '#' + current);
  });
});
```

---

#### Interactive Components

### 8. Accordion

```html
<div class="accordion-header" onclick="toggleAccordion(this)">
  Title <span class="count">N items</span> <span class="arrow">&#9660;</span>
</div>
<div class="accordion-body">
  <!-- content -->
</div>
```

```javascript
function toggleAccordion(el) {
  el.classList.toggle('open');
  el.nextElementSibling.classList.toggle('open');
}
```

```css
.accordion-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 1.25rem; background: var(--surface);
  border: 1px solid var(--terminal-border); border-radius: 10px;
  cursor: pointer; font-weight: 700; margin-bottom: 0.5rem;
}
.accordion-header .arrow { transition: transform 0.2s; color: var(--muted); }
.accordion-header.open .arrow { transform: rotate(180deg); }
.accordion-body { display: none; }
.accordion-body.open { display: block; }
```

### 9. Collapsible File Tree

```html
<div class="file-tree">
  <div style="cursor:pointer;" onclick="this.nextElementSibling.classList.toggle('collapsed')">
    <span class="dir">src/</span>
  </div>
  <div class="tree-children">
    <div><span class="file">index.ts</span> <span class="comment">entry point</span></div>
  </div>
</div>
```

```css
.file-tree {
  background: var(--terminal-bg); border: 1px solid var(--terminal-border);
  border-radius: 12px; padding: 1.5rem; font-size: 0.85rem; line-height: 1.7;
}
.file-tree .dir { color: var(--primary); font-weight: 600; cursor: pointer; }
.file-tree .file { color: var(--text); }
.file-tree .comment { color: var(--muted-fg); margin-left: 0.75rem; }
.tree-children { padding-left: 1.25rem; }
.tree-children.collapsed { display: none; }
```

### 10. Styled Table

```css
.styled-table {
  width: 100%; border-collapse: collapse; background: var(--surface);
  border-radius: 12px; overflow: hidden; border: 1px solid var(--terminal-border);
}
.styled-table th {
  text-align: left; padding: 0.75rem 1rem; background: var(--terminal-bg);
  font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--muted); border-bottom: 1px solid var(--terminal-border);
}
.styled-table td { padding: 0.75rem 1rem; border-bottom: 1px solid rgba(42,42,62,0.5); font-size: 0.9rem; }
.styled-table tr:last-child td { border-bottom: none; }
.styled-table tr:hover td { background: var(--surface-hover); }
```

### 11. localStorage Checklist

```html
<div class="check-item" onclick="toggleCheck(this)" data-key="c1">
  <div class="check-box"></div>Step description
</div>
```

```javascript
const STORAGE_KEY = 'project-setup-checklist';

function toggleCheck(item) {
  item.classList.toggle('checked');
  const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
  data[item.dataset.key] = item.classList.contains('checked');
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  updateProgress();
}

function updateProgress() {
  const items = document.querySelectorAll('.check-item');
  const checked = document.querySelectorAll('.check-item.checked').length;
  const pct = Math.round((checked / items.length) * 100);
  document.getElementById('progressBar').style.width = pct + '%';
  document.getElementById('progressCount').textContent = checked + ' / ' + items.length + ' completed';
}

// Restore on load
(function() {
  const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
  document.querySelectorAll('.check-item').forEach(item => {
    if (data[item.dataset.key]) item.classList.add('checked');
  });
  updateProgress();
})();
```

```css
.check-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.5rem 0; cursor: pointer; user-select: none;
  font-size: 0.88rem; color: var(--muted); transition: color 0.15s;
}
.check-item.checked { color: var(--muted-fg); text-decoration: line-through; }
.check-box {
  width: 20px; height: 20px; border-radius: 4px; flex-shrink: 0;
  border: 2px solid var(--terminal-border); display: flex;
  align-items: center; justify-content: center;
}
.check-item.checked .check-box { background: var(--primary); border-color: var(--primary); }
.check-item.checked .check-box::after { content: '\2713'; color: #000; font-size: 0.7rem; font-weight: 700; }
```

---

#### Styling & Utilities

### 12. Syntax Highlighting Classes (for SQL/code)

```css
.kw { color: var(--primary); }   /* SQL keywords: CREATE, SELECT, etc. */
.str { color: var(--green); }    /* String literals */
.cmt { color: var(--muted-fg); } /* Comments */
.fn { color: var(--blue); }      /* Function names */
.type { color: var(--purple); }  /* Type names */
```

### 13. Type Badges (for database schema)

```css
.type-badge {
  display: inline-block; font-size: 0.65rem; font-weight: 600;
  padding: 0.1rem 0.35rem; border-radius: 3px;
  font-family: 'JetBrains Mono', monospace;
}
.type-badge.text { background: rgba(96,165,250,0.15); color: var(--blue); }
.type-badge.bool { background: rgba(74,222,128,0.15); color: var(--green); }
.type-badge.int { background: rgba(167,139,250,0.15); color: var(--purple); }
.type-badge.json { background: rgba(232,112,64,0.15); color: var(--secondary); }

.rls-badge { display: inline-block; font-size: 0.65rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: 3px; }
.rls-badge.public { background: rgba(74,222,128,0.15); color: var(--green); }
.rls-badge.admin { background: rgba(248,113,113,0.15); color: var(--red); }
```

### 14. Button Styles

```css
.btn {
  display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.75rem 1.5rem; border-radius: 10px;
  font-weight: 600; font-size: 0.95rem; text-decoration: none;
  transition: all 0.2s; border: none; cursor: pointer;
}
.btn-primary { background: var(--primary); color: #000; }
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
.btn-secondary { background: transparent; color: var(--text); border: 1px solid var(--terminal-border); }
.btn-secondary:hover { border-color: var(--primary); color: var(--primary); }
```

### 15. Responsive Breakpoints

```css
@media (max-width: 900px) {
  .sidebar { display: none; }
  .main { margin-left: 0; }
  section { padding: 3rem 1rem; }
}
@media (max-width: 768px) {
  .card-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 480px) {
  .card-grid { grid-template-columns: 1fr; }
}
```

### 16. Timeline (for roadmap)

```css
.timeline { display: flex; gap: 0; position: relative; }
.timeline::before {
  content: ''; position: absolute; top: 24px; left: 0; right: 0;
  height: 3px; background: var(--terminal-border);
}
.timeline-node { flex: 1; text-align: center; position: relative; padding-top: 3.5rem; }
.timeline-node::before {
  content: ''; position: absolute; top: 16px; left: 50%;
  width: 16px; height: 16px; border-radius: 50%;
  background: var(--primary); transform: translateX(-50%);
  box-shadow: 0 0 12px rgba(var(--primary-rgb), 0.3);
}
```
