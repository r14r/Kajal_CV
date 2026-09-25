"""Generate the editable HTML CV, vector diagrams and matching A4 PDF.

Run from any directory: python cv/generate_cv.py
Dependencies for PDF: reportlab. No dependencies for the HTML/SVG output.
"""
from __future__ import annotations

from html import escape
import re
import yaml
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "cv.yaml"


def load_cv(path=SOURCE):
    """Load the single editable source; fail before overwriting outputs on invalid data."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("cv.yaml must have schema_version: 1")
    cv = data.get("cv")
    if not isinstance(cv, dict) or not all(cv.get(k) for k in ("name", "subtitle", "profile", "ownership_note", "repository_url")):
        raise ValueError("cv.yaml needs cv.name, subtitle, profile, ownership_note and repository_url")
    if not isinstance(cv.get("contact"), dict) or not isinstance(cv.get("education"), dict):
        raise ValueError("cv.contact and cv.education must be mappings")
    projects = data.get("projects")
    if not isinstance(projects, list) or len(projects) != 6:
        raise ValueError("This seven-page layout requires six projects")
    slugs = set()
    for project in projects:
        required = ("slug", "name", "stack", "port", "intro", "features", "detail", "scenario", "limits", "icon", "category", "summary", "runtime", "number")
        if not isinstance(project, dict) or any(not isinstance(project.get(k), str) or not project[k] for k in required):
            raise ValueError("Every project needs all named text fields")
        slug = project["slug"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in slugs:
            raise ValueError(f"Invalid or duplicate project slug: {slug}")
        slugs.add(slug)
        if len(project.get("structure", [])) != 4 or len(project.get("flow", [])) != 5:
            raise ValueError(f"{slug}: diagrams need four structure nodes and five flow steps")
        if not isinstance(project.get("files"), list) or not (1 <= len(project["files"]) <= 4):
            raise ValueError(f"{slug}: provide one to four files")
        if any(not isinstance(f, dict) or not f.get("path") or not f.get("purpose") for f in project["files"]):
            raise ValueError(f"{slug}: every file needs a path and purpose")
    return data


DATA = load_cv()
CV = DATA["cv"]
PROJECTS = DATA["projects"]
REPO = CV["repository_url"].rstrip("/")

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


def contact_line():
    values = [CV["contact"].get(k, "") for k in ("email", "city", "github_url")]
    return "  |  ".join(value for value in values if value) or CV.get("contact_note", "Contact information to be confirmed")


def education_line():
    education = CV["education"]
    return "  |  ".join(value for value in (education.get("institution"), education.get("dates")) if value) or education.get("note", "Education details to be confirmed")


def generate_html():
    cards = []
    for i, p in enumerate(PROJECTS, 1):
        slug = p['slug']
        files = ''.join(f'<li><code>{escape(path)}</code><span>{escape(why)}</span></li>' for file in p['files'] for path, why in [(file['path'], file['purpose'])])
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
    html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(CV['name'])} - CV and project portfolio draft</title>
<style>''' + '''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#e8eff2;color:#233c4b;font:15px/1.48 system-ui,Arial,sans-serif}.page{max-width:850px;min-height:1100px;margin:22px auto;padding:48px 58px;background:white;box-shadow:0 12px 30px #142d3d18}h1,h2,h3,p{margin-top:0}h1{font-size:39px;line-height:1.1;letter-spacing:-.03em;color:#142d3d;margin:18px 0 5px}h2{font-size:30px;letter-spacing:-.02em;color:#142d3d;margin:17px 0 3px}h3{font-size:13px;letter-spacing:.10em;text-transform:uppercase;color:#0d7896;margin:0 0 10px}.topline{display:flex;justify-content:space-between;border-bottom:2px solid #0d7896;padding-bottom:9px;letter-spacing:.1em;color:#0d7896;font-size:11px;font-weight:800}.draft{display:inline-block;background:#fff0e7;color:#944321;font-size:11px;font-weight:800;letter-spacing:.08em;padding:7px 10px;margin-top:22px}.subtitle{font-size:19px;color:#0d7896}.muted,.note{color:#526b78}.note{font-size:13px}.cv-block{margin:26px 0}.cv-block p{margin:6px 0}.project-index{list-style:none;padding:0}.project-index li{display:flex;justify-content:space-between;gap:15px;border-bottom:1px solid #d7e5e8;padding:9px 0}.project-index span{color:#526b78;font-size:12px}.project-index a,a{color:#0d7896}.project-index a{text-decoration:none;font-weight:650}.stack{font-size:16px;color:#0d7896;font-weight:600}.intro{font-size:16px;margin:18px 0}.panel{background:#f7fafb;border:1px solid #d8e7eb;border-radius:12px;padding:14px 18px;margin:15px 0}.panel img{display:block;width:100%;height:auto}.panel img.flow{width:75%;margin:0 auto}.filelist{list-style:none;padding:0;margin:0}.filelist li{display:flex;gap:20px;padding:4px 0}.filelist code{width:215px;flex:none;color:#142d3d}.two{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:20px}.two p{font-size:13px}.run{font-size:12px;border-top:1px solid #d7e5e8;padding-top:12px}.run code{overflow-wrap:anywhere}footer{color:#526b78;font-size:11px;margin-top:24px}nav a{margin-right:18px}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}@media(max-width:680px){.page{min-height:0;margin:0 0 12px;padding:26px 20px}.project-index li,.filelist li{display:block}.two{grid-template-columns:1fr;gap:5px}.panel img.flow{width:100%}h1{font-size:31px}}@media print{@page{size:A4;margin:0}body{background:white}.page{page-break-after:always;break-after:page;width:210mm;height:297mm;min-height:0;max-width:none;margin:0;padding:14mm 16mm;box-shadow:none}.page:last-child{page-break-after:auto}.panel{break-inside:avoid;margin:10px 0;padding:10px 13px}.panel img.flow{width:68%}.intro{font-size:13px;margin:9px 0}.filelist li{padding:2px 0}.two{margin-top:10px}footer{margin-top:8px}}''' + '''</style></head><body><main>
<section class="page cv" id="cv"><div class="topline">SECTION 1 / CURRICULUM VITAE <span>01 / 07</span></div><div class="draft">DRAFT - VERIFY BEFORE APPLYING</div>
<h1>{escape(CV["name"])}</h1><p class="subtitle">{escape(CV["subtitle"])}</p><p class="muted">{escape(contact_line())}</p>
<div class="cv-block"><h3>Profile</h3><p>{escape(CV["profile"])}</p></div>
<div class="cv-block"><h3>Education</h3><p><strong>{escape(CV["education"]["degree"])}</strong><br>{escape(education_line())}</p></div>
<div class="cv-block"><h3>Learning portfolio - project index</h3><ul class="project-index">''' + listing + '''</ul></div>
<div class="cv-block"><h3>Project ownership and next steps</h3><p class="note">{escape(CV["ownership_note"])}</p></div>
<nav><a href="#animated-portfolio">Read project pages ↓</a><a href="''' + REPO + '''">Repository ↗</a></nav><footer>CV draft • Page 1 of 7</footer></section>
''' + '\n'.join(cards) + '</main></body></html>'
    substitutions = {
        "{escape(CV['name'])}": escape(CV['name']),
        '{escape(CV["name"])}': escape(CV['name']),
        '{escape(CV["subtitle"])}': escape(CV['subtitle']),
        '{escape(contact_line())}': escape(contact_line()),
        '{escape(CV["profile"])}': escape(CV['profile']),
        '{escape(CV["education"]["degree"])}': escape(CV['education']['degree']),
        '{escape(education_line())}': escape(education_line()),
        '{escape(CV["ownership_note"])}': escape(CV['ownership_note']),
    }
    for token, value in substitutions.items():
        html = html.replace(token, value)
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
    c.drawString(45,36,CV['name'] + '  |  Prepared learning portfolio  |  Draft for review')


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
    c.setTitle(CV['name'] + ' - CV and project portfolio draft')
    w,h=A4
    page_header(c,'Section 1 / Curriculum vitae',1)
    c.setFillColor(HexColor('#fff0e7'));c.roundRect(45,h-80,210,20,4,fill=1,stroke=0)
    wrapped(c,'DRAFT - VERIFY BEFORE APPLYING',52,h-73,200,size=8,bold=True,color='#944321')
    wrapped(c,CV['name'],45,h-125,w-90,size=23,leading=27,bold=True,color=NAVY)
    wrapped(c,CV['subtitle'],45,h-149,w-90,size=11,bold=True,color=BLUE)
    y=wrapped(c,contact_line(),45,h-173,w-90,size=9,color=MUTED)-23
    y=heading(c,'Profile',45,y)
    y=wrapped(c,CV['profile'],45,y,w-90)-25
    y=heading(c,'Education',45,y)
    y=wrapped(c,CV['education']['degree'],45,y,w-90,bold=True)
    y=wrapped(c,education_line(),45,y,w-90,color=MUTED)-24
    y=heading(c,'Learning portfolio - project index',45,y)
    for i,p in enumerate(PROJECTS,1):
        c.setFillColor(HexColor('#f4f9fa' if i%2 else '#ffffff'));c.rect(45,y-15,w-90,27,fill=1,stroke=0)
        wrapped(c,f'{i:02d}  {p["name"]}',53,y,w-200,size=9,bold=True)
        c.setFillColor(HexColor(MUTED));c.setFont('DejaVu',7.4)
        c.drawRightString(w-53,y,p['stack'])
        y-=32
    y-=15;y=heading(c,'Project ownership and next steps',45,y)
    y=wrapped(c,CV['ownership_note'],45,y,w-90,size=8.7)
    c.showPage()
    for n,p in enumerate(PROJECTS,2):
        page_header(c,'Section 2 / Project technical notes',n)
        y=h-79
        y=wrapped(c,p['name'],45,y,w-90,size=19,leading=25,bold=True,color=NAVY)-1
        y=wrapped(c,p['stack'],45,y,w-90,size=9.5,bold=True,color=BLUE)-9
        y=wrapped(c,p['intro'],45,y,w-90,size=9.2,leading=13)-10
        y=heading(c,'Project structure',45,y)
        for file in p['files']:
            path,description=file['path'],file['purpose']
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
