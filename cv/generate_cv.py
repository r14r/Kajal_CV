"""Generate the editable HTML CV, vector diagrams and matching A4 PDF.

Run from any directory: python cv/generate_cv.py
Dependencies for PDF: reportlab. No dependencies for the HTML/SVG output.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
REPO = "https://github.com/r14r/Kajal_CV"
PROJECTS = [
    {
        "slug": "animated-portfolio", "name": "Animated Portfolio", "stack": "HTML / CSS / JavaScript", "port": "Open index.html locally",
        "intro": "A responsive concept site for a fictional studio. Semantic sections, CSS artwork and lightweight JavaScript create a navigable portfolio without a build step.",
        "files": [("index.html", "Semantic sections and navigation"), ("styles.css", "Layout, artwork and animations"), ("script.js", "Menu and scroll reveal behavior")],
        "structure": ["Browser", "HTML sections", "CSS artwork", "JavaScript"],
        "flow": ["Open index.html", "Browser builds the document", "CSS renders responsive layout", "JS handles menu and scroll", "Updated sections appear"],
        "features": "Responsive navigation, accessible keyboard flow, reveal animations and reduced-motion styling.",
        "detail": "The browser loads three local files directly. HTML defines landmarks and section anchors; CSS handles both the artwork and responsive breakpoints. JavaScript changes navigation state on small screens and reveals sections as they enter the viewport. A reduced-motion media query removes unnecessary movement for users who request it.",
        "scenario": "A visitor selects Work in the menu; the page moves to the case studies and the relevant content becomes visible.",
        "limits": "Fictional content and demonstration contact address; replace these before public use.",
    },
    {
        "slug": "django-htmx-taskboard", "name": "Django Task Board", "stack": "Django / HTMX / SQLite", "port": "python manage.py migrate; python manage.py runserver 127.0.0.1:8000",
        "intro": "A local task manager with server-rendered updates. Django owns validation and persistence; HTMX swaps a task-list fragment after actions.",
        "files": [("board/models.py", "Task model and database fields"), ("board/forms.py", "Input validation"), ("board/views.py", "Requests and partial responses"), ("board/templates/", "Page and task-list fragments")],
        "structure": ["Browser + HTMX", "Django views", "Forms + models", "SQLite"],
        "flow": ["Submit task action", "Django validates form + CSRF", "Model reads or writes SQLite", "View renders task-list fragment", "HTMX swaps #task-list"],
        "features": "Create, filter, complete and delete tasks; local HTMX asset; CSRF checks and escaped templates.",
        "detail": "The page submits actions to Django views. A Django form validates incoming fields before the model writes tasks to SQLite. For HTMX requests, the view renders only the task-list template; the browser replaces that fragment while leaving the rest of the page in place. Mutating requests include Django's CSRF token.",
        "scenario": "When a task is marked complete, Django updates its row and returns the refreshed list fragment without a full page reload.",
        "limits": "Single-user development example. Needs authentication and production settings before deployment.",
    },
    {
        "slug": "fastapi-rag-chat", "name": "Notebook Chat", "stack": "FastAPI / SQLite / lexical RAG / optional Ollama", "port": "uvicorn app:app --host 127.0.0.1 --port 8001",
        "intro": "A local knowledge-base chat that retrieves passages from Markdown or text notes and shows citations. Optional Ollama generation uses retrieved context.",
        "files": [("index.html + client.js", "Chat and knowledge library UI"), ("app.py", "API, chat and persistence"), ("retrieval.py", "Chunking and TF-IDF ranking"), ("knowledge/", "Bundled example notes")],
        "structure": ["Browser UI", "FastAPI", "Retrieval + SQLite", "Optional Ollama"],
        "flow": ["Add notes; split into chunks", "Ask a question", "Rank chunks using lexical TF-IDF", "Show cited excerpts or call Ollama", "Save answer and citations"],
        "features": "Local document ingestion, passage ranking, saved conversations and citations; useful without a model.",
        "detail": "The backend splits notes into passages and scores them with lexical TF-IDF. A question selects the strongest passages, which become cited excerpts in the fallback response. When configured, the backend sends those passages to a local Ollama server for an optional answer. SQLite retains documents, conversations and citation records.",
        "scenario": "Ask a question about a stored note; the response points back to the passages used, so the reader can inspect the evidence.",
        "limits": "Lexical search may miss synonyms. Model output needs verification; no login or multi-user isolation.",
    },
    {
        "slug": "job-application-tracker", "name": "Job Application Tracker", "stack": "Streamlit / SQLite", "port": "streamlit run app.py --server.port 8501",
        "intro": "A local dashboard for managing applications and interview notes. Streamlit renders the interface and SQLite retains records between sessions.",
        "files": [("app.py", "Forms, filters, tabs and metrics"), ("application_store.py", "Validation and SQLite queries"), ("tests/test_storage.py", "Temporary-database lifecycle check")],
        "structure": ["Browser", "Streamlit app", "Storage module", "SQLite"],
        "flow": ["Enter company, role and status", "Validate required fields", "Write parameterized SQLite query", "Re-read application list", "Filter, edit or delete in UI"],
        "features": "Add, update, delete, search and status-filter records; metrics for interviews and offers.",
        "detail": "Streamlit forms gather a company, role, status and optional notes. The storage module trims and validates input, then uses parameterized SQL to insert or update a row. On rerun, the app reads the database again and computes metrics and filtered lists from those records. Each app has its own database file next to its source.",
        "scenario": "After an interview, change an application status to Interview and see the dashboard count update.",
        "limits": "Local single-user learning app. Database file should be backed up and kept out of Git.",
    },
    {
        "slug": "study-planner", "name": "Study Planner", "stack": "Streamlit / SQLite", "port": "streamlit run app.py --server.port 8502",
        "intro": "A local coursework planner with status counts. A small storage module encapsulates validation and persistent task operations.",
        "files": [("app.py", "Task forms, filters and metrics"), ("planner_store.py", "Task validation and SQLite"), ("tests/test_storage.py", "Create, edit and delete checks")],
        "structure": ["Browser", "Streamlit app", "Storage module", "SQLite"],
        "flow": ["Enter title, course and status", "Validate required fields", "Save task in SQLite", "Re-read task list", "Search, edit or complete task"],
        "features": "Create and edit coursework, track progress, search notes and filter by task status.",
        "detail": "The UI separates task review, creation and editing into tabs. The storage module requires a title, course and supported status, and persists data using parameterized SQLite statements. Search checks task titles, course names and notes; progress metrics are calculated from the current database rows after each interaction.",
        "scenario": "Add a coursework task, then change it from To do to Done and verify the progress count.",
        "limits": "Single-user local demo, without accounts or shared access.",
    },
    {
        "slug": "data-cleaning-studio", "name": "Data Cleaning Studio", "stack": "Streamlit / Pandas / public APIs", "port": "streamlit run app.py --server.port 8503",
        "intro": "An interactive data workflow with a fictional offline sample, CSV upload and fixed public sources for weather, currency rates and economic indicators.",
        "files": [("app.py", "Source selection and cleaning controls"), ("sources.py", "Open-Meteo, ECB, World Bank clients"), ("cleaning.py", "Pure Pandas transformations"), ("samples/", "Offline demonstration dataset")],
        "structure": ["CSV or fixed API", "Streamlit app", "Pandas cleaning", "CSV export"],
        "flow": ["Load sample, upload or fetch", "Preview original table", "Select cleaning options", "Profile and chart transformed copy", "Download full cleaned CSV"],
        "features": "Trim text, deduplicate, parse dates and numbers, handle missing values and inspect before/after metrics.",
        "detail": "A source adapter turns each supported API response or CSV input into a Pandas table. A pure cleaning function copies the original table before applying selected transformations, so previewing alternatives does not alter the source. Column profiles expose types, missing values and unique counts; the final table is serialized to CSV for download.",
        "scenario": "Load the fictional sales sample, convert revenue to numbers, fill numeric medians and compare missing-cell counts before exporting.",
        "limits": "Public APIs need internet access; previews show 500 rows while the download retains all rows.",
    },
]

NAVY = "#142d3d"
BLUE = "#0d7896"
PALE = "#eaf5f6"
INK = "#233c4b"
MUTED = "#526b78"


def svg_structure(p):
    nodes = p["structure"]
    width, height = 900, 132
    blocks = []
    for i, label in enumerate(nodes):
        x = 24 + i * 220
        blocks.append(f'<rect x="{x}" y="30" width="180" height="70" rx="13" fill="{PALE}" stroke="{BLUE}" stroke-width="2"/>')
        blocks.append(f'<text x="{x+90}" y="71" text-anchor="middle" fill="{NAVY}" font-family="Arial,sans-serif" font-size="17" font-weight="700">{xml_escape(label)}</text>')
        if i < len(nodes)-1:
            blocks.append(f'<path d="M{x+185},65 L{x+215},65 M{x+206},57 L{x+215},65 L{x+206},73" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Structure of {xml_escape(p["name"])}">' + ''.join(blocks) + '</svg>'


def svg_flow(p):
    steps = p["flow"]
    height = 54 + len(steps)*62
    blocks = []
    for i, label in enumerate(steps):
        y = 18+i*62
        blocks.append(f'<rect x="46" y="{y}" width="808" height="44" rx="11" fill="{PALE if i % 2 == 0 else "#f3f7f9"}" stroke="#b5d8df"/>')
        blocks.append(f'<circle cx="72" cy="{y+22}" r="15" fill="{BLUE}"/>')
        blocks.append(f'<text x="72" y="{y+27}" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="15">{i+1}</text>')
        blocks.append(f'<text x="100" y="{y+28}" fill="{NAVY}" font-family="Arial,sans-serif" font-size="16">{xml_escape(label)}</text>')
        if i < len(steps)-1:
            blocks.append(f'<path d="M450,{y+44} V{y+62} M444,{y+56} L450,{y+62} L456,{y+56}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {height}" role="img" aria-label="Data flow of {xml_escape(p["name"])}">' + ''.join(blocks) + '</svg>'


def generate_html():
    cards = []
    for i, p in enumerate(PROJECTS, 1):
        slug = p['slug']
        files = ''.join(f'<li><code>{escape(path)}</code><span>{escape(why)}</span></li>' for path, why in p['files'])
        cards.append(f'''<section class="project page" id="{slug}"><div class="topline">SECTION 2 / PROJECT TECHNICAL NOTES <span>{i:02d} / 06</span></div>
<h2>{escape(p['name'])}</h2><p class="stack">{escape(p['stack'])}</p><p class="intro">{escape(p['intro'])}</p>
<div class="panel"><h3>Project structure</h3><ul class="filelist">{files}</ul></div>
<div class="panel"><h3>Architecture image</h3><img src="diagrams/{slug}-structure.svg" alt="Architecture: {' to '.join(p['structure'])}"></div>
<div class="panel"><h3>Data flow image</h3><img class="flow" src="diagrams/{slug}-flow.svg" alt="Data flow: {'; '.join(p['flow'])}"></div>
<div class="panel"><h3>Implementation</h3><p>{escape(p['detail'])}</p><p class="note"><strong>Example:</strong> {escape(p['scenario'])}</p></div>
<div class="two"><div><h3>Key features</h3><p>{escape(p['features'])}</p></div><div><h3>Scope and limits</h3><p>{escape(p['limits'])}</p></div></div>
<p class="run"><strong>Run:</strong> <code>{escape(p['port'])}</code> &nbsp; <a href="{REPO}/tree/main/projects/{slug}">Source and setup guide ↗</a></p>
<footer>Prepared learning example • Review and personalize before presenting as your own work</footer></section>''')
    listing = ''.join(f'<li><a href="#{p["slug"]}">{escape(p["name"])}</a><span>{escape(p["stack"])}</span></li>' for p in PROJECTS)
    html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kajal Raju Kale - CV and project portfolio draft</title>
<style>''' + '''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#e8eff2;color:#233c4b;font:15px/1.48 system-ui,Arial,sans-serif}.page{max-width:850px;min-height:1100px;margin:22px auto;padding:48px 58px;background:white;box-shadow:0 12px 30px #142d3d18}h1,h2,h3,p{margin-top:0}h1{font-size:39px;line-height:1.1;letter-spacing:-.03em;color:#142d3d;margin:18px 0 5px}h2{font-size:30px;letter-spacing:-.02em;color:#142d3d;margin:17px 0 3px}h3{font-size:13px;letter-spacing:.10em;text-transform:uppercase;color:#0d7896;margin:0 0 10px}.topline{display:flex;justify-content:space-between;border-bottom:2px solid #0d7896;padding-bottom:9px;letter-spacing:.1em;color:#0d7896;font-size:11px;font-weight:800}.draft{display:inline-block;background:#fff0e7;color:#944321;font-size:11px;font-weight:800;letter-spacing:.08em;padding:7px 10px;margin-top:22px}.subtitle{font-size:19px;color:#0d7896}.muted,.note{color:#526b78}.note{font-size:13px}.cv-block{margin:26px 0}.cv-block p{margin:6px 0}.project-index{list-style:none;padding:0}.project-index li{display:flex;justify-content:space-between;gap:15px;border-bottom:1px solid #d7e5e8;padding:9px 0}.project-index span{color:#526b78;font-size:12px}.project-index a,a{color:#0d7896}.project-index a{text-decoration:none;font-weight:650}.stack{font-size:16px;color:#0d7896;font-weight:600}.intro{font-size:16px;margin:18px 0}.panel{background:#f7fafb;border:1px solid #d8e7eb;border-radius:12px;padding:14px 18px;margin:15px 0}.panel img{display:block;width:100%;height:auto}.panel img.flow{width:75%;margin:0 auto}.filelist{list-style:none;padding:0;margin:0}.filelist li{display:flex;gap:20px;padding:4px 0}.filelist code{width:215px;flex:none;color:#142d3d}.two{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:20px}.two p{font-size:13px}.run{font-size:12px;border-top:1px solid #d7e5e8;padding-top:12px}.run code{overflow-wrap:anywhere}footer{color:#526b78;font-size:11px;margin-top:24px}nav a{margin-right:18px}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}@media(max-width:680px){.page{min-height:0;margin:0 0 12px;padding:26px 20px}.project-index li,.filelist li{display:block}.two{grid-template-columns:1fr;gap:5px}.panel img.flow{width:100%}h1{font-size:31px}}@media print{@page{size:A4;margin:0}body{background:white}.page{page-break-after:always;break-after:page;width:210mm;height:297mm;min-height:0;max-width:none;margin:0;padding:14mm 16mm;box-shadow:none}.page:last-child{page-break-after:auto}.panel{break-inside:avoid;margin:10px 0;padding:10px 13px}.panel img.flow{width:68%}.intro{font-size:13px;margin:9px 0}.filelist li{padding:2px 0}.two{margin-top:10px}footer{margin-top:8px}}''' + '''</style></head><body><main>
<section class="page cv" id="cv"><div class="topline">SECTION 1 / CURRICULUM VITAE <span>01 / 07</span></div><div class="draft">DRAFT - VERIFY BEFORE APPLYING</div>
<h1>Kajal Raju Kale</h1><p class="subtitle">BCA student · Aspiring software developer</p><p class="muted">Contact details, college, graduation dates and public profile await Kajal's confirmation.</p>
<div class="cv-block"><h3>Profile</h3><p>BCA student preparing for an entry-level software development role. Studying practical frontend, backend, database and data workflows through runnable learning projects.</p></div>
<div class="cv-block"><h3>Education</h3><p><strong>Bachelor of Computer Applications (BCA)</strong><br>College and attendance dates: to be confirmed by Kajal.</p></div>
<div class="cv-block"><h3>Learning portfolio - project index</h3><ul class="project-index">''' + listing + '''</ul></div>
<div class="cv-block"><h3>Project ownership and next steps</h3><p class="note">These projects are prepared learning examples. Kajal should run, inspect and modify them, then identify only her own contributions and skills she can explain. Add verified contact information, education dates and a personal GitHub profile before applying.</p></div>
<nav><a href="#animated-portfolio">Read project pages ↓</a><a href="''' + REPO + '''">Repository ↗</a></nav><footer>CV draft • Page 1 of 7</footer></section>
''' + '\n'.join(cards) + '</main></body></html>'
    (ROOT / 'Kajal_Kale_CV.html').write_text(html, encoding='utf-8')


def fonts():
    base = Path('/usr/share/fonts/truetype/dejavu')
    for label, file in [('DejaVu', 'DejaVuSans.ttf'), ('DejaVu-Bold', 'DejaVuSans-Bold.ttf')]:
        pdfmetrics.registerFont(TTFont(label, str(base / file)))


def wrapped(c, string, x, top, width, size=9.3, leading=14, bold=False, color=INK):
    font = 'DejaVu-Bold' if bold else 'DejaVu'
    c.setFont(font, size); c.setFillColor(HexColor(color))
    words = string.split()
    lines, line = [], ''
    for word in words:
        candidate = (line + ' ' + word).strip()
        if pdfmetrics.stringWidth(candidate, font, size) > width and line:
            lines.append(line); line = word
        else:
            line = candidate
    if line: lines.append(line)
    for item in lines:
        c.drawString(x, top, item)
        top -= leading
    return top


def heading(c, label, x, y):
    c.setFillColor(HexColor(BLUE)); c.setFont('DejaVu-Bold', 9)
    c.drawString(x, y, label.upper())
    return y-15


def page_header(c, label, page):
    w,h=A4
    c.setStrokeColor(HexColor(BLUE)); c.setLineWidth(2)
    c.line(45,h-42,w-45,h-42)
    c.setFillColor(HexColor(BLUE)); c.setFont('DejaVu-Bold', 8)
    c.drawString(45,h-33,label.upper())
    c.drawRightString(w-45,h-33,f'{page:02d} / 07')
    c.setStrokeColor(HexColor('#d5e5e9')); c.setLineWidth(.5); c.line(45,48,w-45,48)
    c.setFillColor(HexColor(MUTED)); c.setFont('DejaVu',7)
    c.drawString(45,36,'Kajal Raju Kale  |  Prepared learning portfolio  |  Draft for review')


def architecture(c, p, y):
    x0, gap, boxw, boxh = 48, 10, 117, 55
    for i, label in enumerate(p['structure']):
        x=x0+i*(boxw+gap)
        c.setFillColor(HexColor(PALE)); c.setStrokeColor(HexColor(BLUE))
        c.roundRect(x,y,boxw,boxh,8,fill=1,stroke=1)
        # Labels always fit by wrapping in the box.
        words=label.split(); candidates=[label]
        if pdfmetrics.stringWidth(label,'DejaVu-Bold',8.4)>boxw-10:
            mid=max(1,len(words)//2);candidates=[' '.join(words[:mid]),' '.join(words[mid:])]
        for line_no, part in enumerate(candidates):
            c.setFillColor(HexColor(NAVY));c.setFont('DejaVu-Bold',8.3)
            c.drawCentredString(x+boxw/2,y+boxh/2+4-line_no*12,part)
        if i<3:
            c.setStrokeColor(HexColor(BLUE));c.setLineWidth(1.4)
            c.line(x+boxw+2,y+boxh/2,x+boxw+gap-2,y+boxh/2)
            c.line(x+boxw+gap-5,y+boxh/2+3,x+boxw+gap-2,y+boxh/2)
            c.line(x+boxw+gap-5,y+boxh/2-3,x+boxw+gap-2,y+boxh/2)


def flow(c,p,top):
    x,w,height,gap=73,449,34,7
    for i,step in enumerate(p['flow']):
        y=top-i*(height+gap)-height
        c.setFillColor(HexColor(PALE if i%2==0 else '#f4f8f9'))
        c.setStrokeColor(HexColor('#b5d8df'));c.roundRect(x,y,w,height,6,fill=1,stroke=1)
        c.setFillColor(HexColor(BLUE));c.circle(x+19,y+17,11,fill=1,stroke=0)
        c.setFillColor(HexColor('#ffffff'));c.setFont('DejaVu-Bold',8)
        c.drawCentredString(x+19,y+14,str(i+1))
        wrapped(c,step,x+39,y+14,w-49,size=8.5,leading=11)
        if i<len(p['flow'])-1:
            c.setStrokeColor(HexColor(BLUE));c.setLineWidth(1)
            c.line(x+w/2,y,x+w/2,y-gap+1)
    return top-len(p['flow'])*(height+gap)


def generate_pdf():
    fonts()
    target=ROOT/'Kajal_Kale_CV.pdf'; c=canvas.Canvas(str(target),pagesize=A4)
    c.setTitle('Kajal Raju Kale - CV and project portfolio draft')
    w,h=A4
    page_header(c,'Section 1 / Curriculum vitae',1)
    c.setFillColor(HexColor('#fff0e7'));c.roundRect(45,h-80,210,20,4,fill=1,stroke=0)
    wrapped(c,'DRAFT - VERIFY BEFORE APPLYING',52,h-73,200,size=8,bold=True,color='#944321')
    wrapped(c,'Kajal Raju Kale',45,h-125,w-90,size=23,leading=27,bold=True,color=NAVY)
    wrapped(c,'BCA student  |  Aspiring software developer',45,h-149,w-90,size=11,bold=True,color=BLUE)
    y=wrapped(c,"Contact details, college, graduation dates and public profile await Kajal's confirmation.",45,h-173,w-90,size=9,color=MUTED)-23
    y=heading(c,'Profile',45,y)
    y=wrapped(c,'BCA student preparing for an entry-level software development role. Studying practical frontend, backend, database and data workflows through runnable learning projects.',45,y,w-90)-25
    y=heading(c,'Education',45,y)
    y=wrapped(c,'Bachelor of Computer Applications (BCA)',45,y,w-90,bold=True)
    y=wrapped(c,'College and attendance dates: to be confirmed by Kajal.',45,y,w-90,color=MUTED)-24
    y=heading(c,'Learning portfolio - project index',45,y)
    for i,p in enumerate(PROJECTS,1):
        c.setFillColor(HexColor('#f4f9fa' if i%2 else '#ffffff'));c.rect(45,y-15,w-90,27,fill=1,stroke=0)
        wrapped(c,f'{i:02d}  {p["name"]}',53,y,w-200,size=9,bold=True)
        c.setFillColor(HexColor(MUTED));c.setFont('DejaVu',7.4)
        c.drawRightString(w-53,y,p['stack'])
        y-=32
    y-=15;y=heading(c,'Project ownership and next steps',45,y)
    y=wrapped(c,'These projects are prepared learning examples. Kajal should run, inspect and modify them, then identify only her own contributions and skills she can explain. Add verified contact information, education dates and a personal GitHub profile before applying.',45,y,w-90,size=8.7)
    c.showPage()
    for n,p in enumerate(PROJECTS,2):
        page_header(c,'Section 2 / Project technical notes',n)
        y=h-79
        y=wrapped(c,p['name'],45,y,w-90,size=19,leading=25,bold=True,color=NAVY)-1
        y=wrapped(c,p['stack'],45,y,w-90,size=9.5,bold=True,color=BLUE)-9
        y=wrapped(c,p['intro'],45,y,w-90,size=9.2,leading=13)-10
        y=heading(c,'Project structure',45,y)
        for path,description in p['files']:
            wrapped(c,path,47,y,175,size=8,bold=True)
            wrapped(c,description,226,y,310,size=8)
            y-=16
        y-=8
        y=heading(c,'Architecture image',45,y)
        architecture(c,p,y-65)
        y-=85
        y=heading(c,'Data flow image',45,y)
        y=flow(c,p,y-2)-7
        y=heading(c,'Implementation',45,y)
        y=wrapped(c,p['detail'],45,y,w-90,size=8.2,leading=11)-7
        y=wrapped(c,'Example: '+p['scenario'],45,y,w-90,size=8.1,leading=11,color=MUTED)-10
        y=heading(c,'Key features',45,y)
        y=wrapped(c,p['features'],45,y,w-90,size=8.3,leading=11)-10
        y=heading(c,'Scope and limits',45,y)
        y=wrapped(c,p['limits'],45,y,w-90,size=8.3,leading=11)-10
        y=heading(c,'Run locally',45,y)
        y=wrapped(c,p['port'],45,y,w-90,size=8.1,leading=11)-7
        c.setFont('DejaVu',7.5);c.setFillColor(HexColor(BLUE))
        url=f'{REPO}/tree/main/projects/{p["slug"]}'
        c.drawString(45,y,'Source code and full setup guide')
        c.linkURL(url,(45,y-2,290,y+10),relative=0)
        if y<55: raise RuntimeError(f'Page {n} content overlaps footer: {y}')
        c.showPage()
    c.save()


def main():
    diagrams=ROOT/'diagrams';diagrams.mkdir(exist_ok=True)
    for p in PROJECTS:
        (diagrams/(p['slug']+'-structure.svg')).write_text(svg_structure(p),encoding='utf-8')
        (diagrams/(p['slug']+'-flow.svg')).write_text(svg_flow(p),encoding='utf-8')
    generate_html();generate_pdf()
    print('Generated 7-page PDF, HTML, and',len(PROJECTS)*2,'SVG diagrams')


if __name__=='__main__':main()
