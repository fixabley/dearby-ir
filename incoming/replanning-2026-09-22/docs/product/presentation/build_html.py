"""Build the self-contained Dearby deck from its JSON manuscript and local template."""
import base64
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'dearby-presentation.json').read_text())


def esc(value):
    return html.escape(str(value), quote=True)


def lines(value):
    return esc(value).replace('\n', '<br>')


def heading(slide):
    first, second = slide['display_heading'].split('\n', 1)
    return f'{esc(first)}<br><em>{esc(second)}</em>'


def listing(values):
    return '<ul>' + ''.join(f'<li>{esc(v)}</li>' for v in values) + '</ul>'


def columns(slide):
    return ''.join(f'<div class="column"><h3>{esc(c["title"])}</h3>{listing(c["lines"])}</div>' for c in slide['columns'])


def items(slide):
    return ''.join(f'<div class="item"><h3>{esc(a)}</h3><p>{lines(b)}</p></div>' for a, b in slide['items'])


def steps(slide):
    return ''.join(f'<li><span class="step-index" aria-hidden="true">{i+1:02}</span><h3>{esc(a)}</h3><p>{lines(b)}</p></li>' for i, (a, b) in enumerate(slide['steps']))


def table(slide):
    head = ''.join(f'<th scope="col">{esc(h)}</th>' for h in slide['headers'])
    rows = ''.join('<tr>' + ''.join(f'<th scope="row">{esc(v)}</th>' if i == 0 else f'<td>{esc(v)}</td>' for i, v in enumerate(row)) + '</tr>' for row in slide['rows'])
    return f'<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'


sections = []
for s in DATA['slides']:
    n = s['id']
    layout = s['layout']
    topic = f'<header class="slide-heading"><p class="topic">{esc(s["title"])}</p><span class="wordmark" aria-hidden="true">Dearby</span></header>'
    if layout == 'cover':
        uri = 'data:image/png;base64,' + base64.b64encode((ROOT / s['image']).read_bytes()).decode()
        body = f'<div class="cover-copy"><p class="cover-category">{esc(s["caption"])}</p><h1>{esc(s["title"])}</h1><p class="cover-message">{lines(s["subtitle"])}</p></div><figure class="cover-image"><img src="{uri}" alt="대학생 협업 활동을 표현한 AI 생성 콘셉트 이미지" width="1536" height="1024"><figcaption>협업 활동을 표현한 AI 생성 이미지</figcaption></figure>'
        topic = ''
    elif layout in ('problem', 'closing'):
        body = f'<h2 class="statement">{lines(s["headline"])}</h2><div class="statement-details">{items(s)}</div>'
    elif layout == 'audience':
        body = f'<div class="audience-layout">{columns(s)}</div>'
    elif layout == 'criteria':
        summary = ''.join(f'<div><h3>{esc(a)}</h3><p>{lines(b)}</p></div>' for a, b in s['steps'][:2])
        body = f'<h2 class="main-message">{heading(s)}</h2><div class="profile-summary">{summary}</div>{table(s)}<p class="profile-priority">{esc(s["steps"][2][0])}: {esc(s["steps"][2][1])}</p>'
    elif layout == 'experience':
        body = f'<h2 class="main-message">{heading(s)}</h2>{table(s)}'
    elif layout == 'program':
        first, second = s['columns']
        body = f'<div class="program-layout"><div class="program-unit"><span class="unit-number">1</span><h2>{esc(first["title"])}</h2>{listing(first["lines"])}</div><div class="program-detail"><h3>{esc(second["title"])}</h3><div class="branch-list">'+''.join(f'<p>{esc(v)}</p>' for v in second['lines'])+'</div></div></div>'
    elif layout == 'ranking':
        priorities = s['priority'].split(' → ')
        body = '<div class="ranking-layout"><ol class="priority-order">'+''.join(f'<li><span>{i+1:02}</span><h2>{esc(v)}</h2></li>' for i, v in enumerate(priorities)) + f'</ol><div class="match-examples">{items(s)}</div></div>'
    elif layout == 'recovery':
        body = f'<h2 class="main-message">{heading(s)}</h2><ol class="recovery-flow">'+''.join(f'<li><span class="result-number" aria-hidden="true">{["0", "12", "→"][i]}</span><h3>{esc(a)}</h3><p>{lines(b)}</p>{"<span class=example-label>가상 예시</span>" if i == 1 else ""}</li>' for i, (a,b) in enumerate(s['steps']))+'</ol>'
    elif layout == 'saving':
        body = f'<h2 class="main-message">{heading(s)}</h2><div class="saving-layout">{columns(s)}</div>'
    elif layout == 'collection-scope':
        scope = ''.join(f'<div><h3>{esc(a)}</h3><p>{lines(b)}</p></div>' for a, b in s['collection_scope'])
        body = f'<h2 class="main-message">{heading(s)}</h2><p class="scope-note">{esc(s["scope_note"])}</p><div class="collection-scope">{scope}</div><div class="selection-criteria"><h3>{esc(s["selection_title"])}</h3>{listing(s["selection_criteria"])}</div>'
    elif layout == 'collection-method':
        body = f'<h2 class="main-message">{heading(s)}</h2><ol class="collection-flow">{steps(s)}</ol><div class="collection-quality">{columns(s)}</div>'
    elif layout == 'implementation':
        body = f'<div class="implementation-layout">{columns(s)}</div>'
    elif layout in ('search', 'technology'):
        body = f'<h2 class="appendix-title">{esc(s["title"].removeprefix("부록: "))}</h2>{table(s)}'
    else:
        body = f'<h2 class="appendix-title">{esc(s["title"].removeprefix("부록: "))}</h2><div class="remaining-layout">{columns(s)}</div>'
    footnote = s.get('footnote', DATA['date'].replace('-', '.'))
    folio = f'부록 {n-12:02} / 03' if s['appendix'] else f'{n:02} / 12'
    footer = f'<footer class="slide-footer"><p>{esc(footnote)}</p><span>{folio}</span></footer>'
    sections.append(f'<section class="slide layout-{esc(layout)}{" dark" if layout in ("problem","closing") else ""}" id="slide-{n}" aria-label="{n}. {esc(s["title"])}" tabindex="-1"{" hidden" if n != 1 else ""}>{topic}<div class="slide-body">{body}</div>{footer}</section>')

notes = json.dumps([{'title': s['title'], 'notes': s['notes'], 'status': s['status'], 'seconds': s['seconds']} for s in DATA['slides']], ensure_ascii=False).replace('<', '\\u003c')
options = ''.join(f'<option value="{i}">{s["id"]}. {esc(s["title"])}</option>' for i, s in enumerate(DATA['slides']))
page = (ROOT / 'presentation-template.html').read_text()
page = page.replace('__CSS__', (ROOT / 'presentation.css').read_text()).replace('__SLIDES__', '\n'.join(sections)).replace('__OPTIONS__', options).replace('__NOTES__', notes)
(ROOT / 'dearby-presentation.html').write_text(page)
print(f'Created self-contained presentation: {len(sections)} slides')
