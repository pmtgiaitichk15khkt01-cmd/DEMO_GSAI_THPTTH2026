"""Deterministic lesson exports: preserve source text and typeset formulas offline."""
import base64
import hashlib
import html
import json
import re
from functools import lru_cache
from pathlib import Path

from markdown_it import MarkdownIt
from services.academic_context import academic_context

ROOT = Path(__file__).resolve().parents[1]
T1_CONTEXT_REVISION = 2026110510
_TOKENS = re.compile(r"(```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`|(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|\\\[[\s\S]*?\\\]|\\\([^\n]*?\\\)|(?<!\\)\$(?!\$)[^\n$]+?(?<!\\)\$)")


@lru_cache(maxsize=1)
def renderer_assets():
    vendor = ROOT / "assets/vendor/katex/dist"
    css = (vendor / "katex.min.css").read_text(encoding="utf-8")
    # Keep only the WOFF2 source, embedded; no CDN or fonts/ URL is needed.
    def font_source(match):
        block = match[0]
        font = re.search(r"url\([^)]*?fonts/([^/()]+\.woff2)\)", block)
        if not font:
            raise ValueError("KaTeX font face has no packaged WOFF2 source")
        encoded = base64.b64encode((vendor / "fonts" / font[1]).read_bytes()).decode()
        return re.sub(r"src:[^;}]+", 'src:url("data:font/woff2;base64,' + encoded + '") format("woff2")', block)
    css = re.sub(r"@font-face\{[^}]+\}", font_source, css)
    notebook = base64.b64encode((ROOT / "assets/fonts/PatrickHand-Regular.ttf").read_bytes()).decode()
    js = "\n".join((vendor / name).read_text(encoding="utf-8") for name in ("katex.min.js", "contrib/mhchem.min.js"))
    license_text = (ROOT / "assets/fonts/PatrickHand-OFL.txt").read_text(encoding="utf-8") + "\n" + (ROOT / "assets/vendor/katex/LICENSE").read_text(encoding="utf-8")
    css += "\n/* " + license_text.replace("*/", "* /") + " */"
    return css, notebook, js.replace("</script", r"<\/script")


def lesson_body_html(lesson):
    """Protect math/code separately; never convert formulas to approximate Unicode."""
    from services.text_boundaries import wrap_naked_chemistry, polya_display_markdown
    lesson = polya_display_markdown(wrap_naked_chemistry(lesson))
    # Separate explicit teaching steps and inline bullets; protect formulas/code.
    from services.text_boundaries import preserve_math_and_code
    def teaching_lines(value):
        value = re.sub(r"(?<!\n)[ \t]+(?=(?:\*\*)?Bước[ \t]+\d+[ \t]*:)", "\n\n", value)
        value = re.sub(r"(?<=\S)[ \t]+\*[ \t]+(?=[A-ZĐÀ-Ỹ])", "\n\n- ", value)
        value = re.sub(r"(?<=\S)[ \t]+(?=[a-d]\)[ \t]+[A-ZĐÀ-Ỹ])", "\n\n", value)
        return value
    lesson = preserve_math_and_code(lesson, teaching_lines)
    # A table emitted directly after a numbered-list item is otherwise parsed
    # as literal pipes by CommonMark. Separate real pipe-row blocks from prose,
    # while preserving code examples and every source cell.
    def separate_tables(prose):
        return re.sub(r"(?m)(?:^[ \t]{0,3}\|[^\n]+\|[ \t]*(?:\r?\n|$))+",
                      lambda match: "\n\n" + match[0].strip() + "\n\n", prose)
    blocks = re.split(r"(```[\s\S]*?```|~~~[\s\S]*?~~~)", lesson)
    lesson = ''.join(block if index % 2 else separate_tables(block)
                     for index, block in enumerate(blocks))
    replacements = {}
    nonce = hashlib.sha256(lesson.encode()).hexdigest()[:12]

    def protect(match):
        raw = match[0]
        if raw.startswith(("`", "~~~")):
            return raw
        display = raw.startswith(("$$", r"\["))
        width = 2 if raw.startswith(("$$", r"\[", r"\(")) else 1
        tex = raw[width:-width]
        token = f"GSAIMATH{nonce}N{len(replacements)}END"
        replacements[token] = ('<span class="lesson-math" data-display="' + str(display).lower() +
                               '" data-tex="' + html.escape(tex, quote=True) + '">' + html.escape(raw) + '</span>')
        return token

    protected = _TOKENS.sub(protect, lesson)
    outside_code = re.sub(r"```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`", "", protected)
    naked_math = re.search(r"\\(?:frac|dfrac|sqrt|begin|ce|pu|omega|alpha|int|sum|vec)\b", outside_code)
    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    # Remote images are not evidence of the selected lesson. Preserve their alt
    # description, without loading arbitrary image hosts from generated text.
    md.renderer.rules["image"] = lambda tokens, idx, options, env: html.escape(tokens[idx].content)
    # Preserve a discontinuity marker inside one Markdown cell.
    code_blocks = re.split(r'(```[\s\S]*?```|~~~[\s\S]*?~~~)', protected)
    protected = ''.join(block if index % 2 else re.sub(
        r'(?m)^([ \t]*\|[^\n]+)$', lambda m: m[0].replace('||', r'\|\|'), block)
        for index, block in enumerate(code_blocks))
    body = md.render(protected)
    for token, value in replacements.items():
        body = body.replace(token, value)
    if naked_math:
        body = '<p class="notice" data-source-issue="math-delimiter">Có lệnh công thức chưa nằm trong dấu phân cách toán học; cần sửa nội dung trước khi in.</p>' + body
    return body


def saved_markdown_html(payload, subject, grade, topic, style="handwritten"):
    """Reopen an explicitly uploaded saved lesson, without AI or session replay."""
    if not isinstance(payload, bytes) or len(payload) > 1_000_000:
        raise ValueError("Bản lưu phải là tệp Markdown UTF-8 không quá 1 MB.")
    try:
        lesson = payload.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError("Không đọc được bản lưu UTF-8; hãy chọn đúng tệp Markdown đã tải.") from error
    if not str(topic or "").strip():
        raise ValueError("Nhập đúng tên bài của bản lưu trước khi mở phiếu.")
    from services.curriculum_policy import correct_reviewed_english_family_guidance
    lesson = correct_reviewed_english_family_guidance(lesson, subject, grade, topic)
    return build_lesson_html(subject, grade, topic, lesson, style)


def build_lesson_html(subject, grade, topic, lesson, style="handwritten"):
    subject, grade = academic_context(subject, grade)
    if not isinstance(lesson, str) or not lesson.strip():
        raise ValueError("Chưa có nội dung bài học để xuất.")
    if len(lesson) > 250000:
        raise ValueError("Bài học quá dài để xuất trong một lượt.")
    from services.curriculum_policy import validate_lesson_policy
    validate_lesson_policy(lesson, subject, grade)
    from services.lesson_sources import lesson_source_review_html, reviewed_lesson_sources
    source_review_html = lesson_source_review_html(subject, grade, topic)
    if style not in {"handwritten", "color", "monochrome"}:
        raise ValueError("Kiểu bản in không hợp lệ.")
    css, font, js = renderer_assets()
    digest = hashlib.sha256(lesson.encode()).hexdigest()
    metadata = json.dumps({"subject": subject, "grade": grade, "topic": topic, "source_sha256": digest,
                           "reference_review": reviewed_lesson_sources(subject, grade, topic)}, ensure_ascii=False).replace("<", "\\u003c")
    title = html.escape(str(topic or subject))
    body = lesson_body_html(lesson)
    if subject == 'Toán học':
        from services.function_visuals import with_function_visuals
        body = with_function_visuals(body, topic, lesson)
    return r'''<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>''' + title + r'''</title>
<style>''' + css + r'''
@font-face{font-family:GSAIHand;src:url(data:font/ttf;base64,''' + font + r''') format('truetype');font-style:normal;font-weight:400;font-display:swap}
*{box-sizing:border-box}body{margin:0;background:#e8e3d8;color:#182c73;font-family:Arial,'Segoe UI',sans-serif}
.toolbar{padding:12px;background:#fff;position:sticky;top:0;z-index:5;font:14px system-ui;color:#334155}.toolbar button{padding:8px 18px;margin-right:12px;cursor:pointer}
.paper{max-width:820px;margin:20px auto;padding:32px 35px 40px 66px;background:#f5eedc;min-height:1120px;overflow-wrap:anywhere;position:relative}
.handwritten .paper{padding:30px 34px 40px 76px;background-color:#f5eedc;background-image:linear-gradient(#aea18a30 1px,transparent 1px),linear-gradient(90deg,#aea18a30 1px,transparent 1px),linear-gradient(90deg,#e1d3b9,transparent 10%,#fff5 55%,transparent);background-size:24px 24px,24px 24px,100% 100%;box-shadow:0 6px 24px #36280c26;border-radius:2px}
.handwritten .paper:before{content:"";position:absolute;top:0;bottom:0;left:0;width:37px;background:radial-gradient(ellipse 8px 7px at 27px 24px,#332e27 65%,#b0a18a 72%,transparent 82%) 0 0/37px 48px repeat-y;pointer-events:none}
.handwritten .paper:after{content:"";position:absolute;top:0;bottom:0;left:-5px;width:36px;background:repeating-linear-gradient(180deg,transparent 0 18px,#222 18px 21px,#8a8983 21px 24px,#252521 24px 28px,transparent 28px 48px);border-radius:5px;pointer-events:none}
.handwritten{font-family:GSAIHand,cursive;font-synthesis:none}.handwritten article{font:26px/1.48 GSAIHand,cursive;font-weight:400}.handwritten h1,.handwritten h2,.handwritten h3,.handwritten h4{font-family:GSAIHand,cursive}
.notebook-header{display:none}.handwritten .notebook-header{display:grid;grid-template-columns:minmax(140px,1fr) minmax(0,2fr);gap:18px;align-items:start;border-bottom:2px solid #a72b36;padding-bottom:15px;margin-bottom:24px;font:24px/1.2 GSAIHand,cursive}
.notebook-identity{text-align:center;padding-top:3px}.notebook-identity strong{display:block;font-weight:600}.notebook-identity span{display:inline-block;border-bottom:1px solid #a72b36;padding-bottom:6px;margin-top:6px;font-size:20px}.notebook-heading h1{margin:0 0 7px;font-size:30px;text-align:center}.notebook-heading .context{font:24px/1.25 GSAIHand,cursive;margin:0;color:#182c73}
.handwritten>.toolbar{border-bottom:1px solid #d6c6aa}.handwritten .plain-header{display:none}.handwritten article h1,.handwritten article h2,.handwritten article h3,.handwritten article h4{color:#a82332;font-weight:650;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:5px;text-align:left;margin:22px 0 12px}.handwritten article h1{font-size:1.25em}.handwritten article h2{font-size:1.15em}.handwritten article h3,.handwritten article h4{font-size:1.07em}
.handwritten article strong{font-weight:650}.handwritten article li::marker{color:#a82332;font-weight:650}.handwritten article blockquote{margin:16px 0;padding:1px 0 1px 18px;border-left:2px solid #a82332}.handwritten article table{background:#fff3}.handwritten article th{color:#a82332}.handwritten .source-note{font:18px/1.35 GSAIHand,cursive;color:#655842}
.handwritten .katex{font-size:.88em}.handwritten .katex-display{margin:.6em 0}.handwritten .lesson-end{display:flex;align-items:center;gap:12px;color:#a82332;font:23px GSAIHand,cursive;justify-content:center;margin:24px 0 14px}.lesson-end{display:none}.lesson-end:before,.lesson-end:after{content:"";border-top:1px dashed currentColor;flex:1;max-width:160px}
h1{font-size:30px;line-height:1.2;color:#b51e35;text-align:center;margin:10px 0 20px}h2,h3,h4{color:#b51e35;line-height:1.25;break-after:avoid}h2{font-size:1.2em}h3{font-size:1.1em}
.context{text-align:center;font:15px system-ui;margin-bottom:20px;color:#334155}.source-note{font:13px system-ui;border-top:1px solid #bcae94;padding-top:12px;margin-top:24px;color:#475569}
article{font-size:17px;line-height:1.6}article p{margin:0 0 .75em}article li{margin:.25em 0}article table{border-collapse:collapse;width:100%;font-size:.85em}td,th{border:1px solid #9e998e;padding:6px;vertical-align:top}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#ffffff80;padding:10px;font:14px/1.4 monospace}code{font-family:monospace;font-size:.8em}.katex{font-size:1.02em}.katex-display{overflow-x:auto;overflow-y:hidden;margin:.7em 0}
.formula-error{outline:2px solid #b91c1c;color:#991b1b;white-space:pre-wrap;font-family:monospace}.monochrome,.monochrome h1,.monochrome h2,.monochrome h3,.monochrome h4{color:#111}.monochrome .paper{background:#fff}
.color .paper{background:#fff}.color h2{border-left:4px solid #0891b2;padding-left:10px}.notice{color:#b91c1c}
.monochrome .verified-function-visuals polyline{stroke:#111}
article .verified-function-visuals svg{background:transparent!important}article .verified-function-visuals svg rect[fill="white"],article .verified-function-visuals svg circle[fill="white"]{fill:none}
.lesson-source-review{margin-top:18px;padding-top:12px;border-top:1px solid #94a3b8;font:14px/1.5 Arial,'Segoe UI',sans-serif;color:#334155}.monochrome .lesson-source-review{color:#111}
.handwritten .lesson-source-review{font-family:GSAIHand,cursive;font-size:18px;line-height:1.4}
@media(max-width:600px){.paper{margin:10px 8px;padding:20px}.handwritten .paper{padding:24px 18px 28px 48px}.handwritten article{font-size:22px}.handwritten .notebook-header{grid-template-columns:1fr;gap:14px}.notebook-identity span{margin-top:2px}.notebook-heading h1{font-size:28px}}
@page{size:A4;margin:10mm}@media print{body{background:#fff}.toolbar{display:none}.paper{margin:0;max-width:none;min-height:0;padding:10mm 7mm 10mm 12mm;box-shadow:none}.handwritten .paper{padding:5mm 5mm 7mm 16mm;box-shadow:none;print-color-adjust:exact;-webkit-print-color-adjust:exact;box-decoration-break:clone;-webkit-box-decoration-break:clone}.handwritten .notebook-header{grid-template-columns:minmax(120px,1fr) minmax(0,2fr);break-inside:avoid}.handwritten article{font-size:23px}.handwritten .source-note{font-size:16px}article{orphans:3;widows:3}p,li{break-inside:avoid}pre{break-inside:auto}thead{display:table-header-group}tr{break-inside:avoid}.katex-display{overflow:visible}a{color:inherit;text-decoration:none}}
</style></head><body class="''' + style + r'''">
<div class="toolbar"><button id="print" disabled>In / Lưu PDF</button><span id="render-status">Đang dựng công thức…</span></div>
<main class="paper"><header class="notebook-header"><div class="notebook-identity"><strong>SỔ TAY HỌC TẬP</strong><span>KẾT NỐI TRI THỨC</span></div><div class="notebook-heading"><h1>''' + title + r'''</h1><div class="context">''' + html.escape(subject) + f" · Lớp {grade}" + r'''</div></div></header>
<header class="plain-header"><h1>''' + title + r'''</h1><div class="context">''' + html.escape(subject) + f" · Lớp {grade}" + r'''</div></header>
<article id="lesson">''' + body + r'''</article>
<div class="lesson-end" aria-hidden="true">Hết bài</div>
''' + source_review_html + r'''
<p class="source-note">Bản trình bày giữ nội dung bài học AI, không bổ sung công thức hoặc ví dụ mẫu. Cần giáo viên duyệt tính đúng đắn học thuật trước khi sử dụng chính thức. Nội dung dài được in thành nhiều trang.</p></main>
<script type="application/json" id="lesson-context">''' + metadata + r'''</script>
<script>''' + js + r'''</script><script>
(async function(){let errors=document.querySelectorAll('[data-source-issue]').length;const status=document.getElementById('render-status');
for(const el of document.querySelectorAll('.lesson-math')){try{katex.render(el.dataset.tex,el,{displayMode:el.dataset.display==='true',throwOnError:true,trust:false,strict:'warn',maxExpand:1000,maxSize:20});}catch(error){errors++;el.textContent=el.dataset.tex;el.classList.add('formula-error');el.title='Công thức chưa dựng được; cần kiểm tra cú pháp.';}}
// Variation tables: source-bound labels, split one-sided limits, large interval arrows.
for(const table of document.querySelectorAll('article table')){
 const rows=Array.from(table.rows);
 const plain=cell=>{const c=cell.cloneNode(true);for(const m of c.querySelectorAll('.lesson-math'))m.replaceWith(m.dataset.tex);return c.textContent.trim().replace(/\\prime/g,'′').replace(/\\infty/g,'∞').replace(/[$ {}]/g,'').replace(/−/g,'-');};
 if(rows.length!==3)continue;
 const data=rows.map(r=>Array.from(r.cells).map(plain));
 if(!data[0][0]||!/[′']/.test(data[1][0])||data[1][0].replace(/\^?[′']/g,'')!==data[2][0])continue;
 if(!data.every(r=>r.length===data[0].length))continue;
 const points=[];for(let i=1;i<data[0].length;i++)if(data[0][i])points.push(i);
 if(points.length<2||points.length>8)continue;
 const dirs=[];for(let k=0;k<points.length-1;k++){const a=points[k],b=points[k+1];const sign=data[1].slice(a+1,b).join('');const arrow=data[2].slice(a+1,b).join('');dirs.push(sign==='+'?'up':sign==='-'?'down':arrow.includes('↗')?'up':arrow.includes('↘')?'down':null);}
 if(dirs.some(d=>!d))continue;
 const values=points.map(i=>data[2][i].split('||'));
 // Never manufacture a missing one-sided limit or turn an ordinary table into a BBT.
 const numeric=v=>/^[-+]?([0-9]+([.,][0-9]+)?|∞)$/.test(v);
 if(values.some((v,k)=>v.length>2||v.some(x=>!numeric(x))||(data[1][points[k]]==='||'&&v.length!==2)||(v.length===2&&(k===0||k===points.length-1))))continue;
 const num=v=>v==='-∞'?-Infinity:v==='+∞'||v==='∞'?Infinity:Number(v.replace(',','.'));
 if(dirs.some((d,k)=>{const a=num(values[k].at(-1)),b=num(values[k+1][0]);return d==='up'?a>=b:a<=b;}))continue;
 const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');
 const width=Math.max(900,points.length*200),height=310;
 svg.setAttribute('viewBox',`0 0 ${width} ${height}`);svg.setAttribute('role','img');svg.setAttribute('data-variation-card','2026110507');svg.setAttribute('aria-label',table.innerText);svg.style.cssText='display:block;width:100%;height:auto;min-width:650px;background:transparent;break-inside:avoid;font:20px Times New Roman,serif';
 const mono=document.body.classList.contains('monochrome'),up=mono?'#111':'#16a34a',down=mono?'#111':'#dc2626';
 const add=(tag,attrs,text,parent=svg)=>{const el=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))el.setAttribute(k,v);if(text!==undefined)el.textContent=text;parent.append(el);return el;};
 add('rect',{x:1,y:1,width:width-2,height:height-2,rx:7,fill:'none',stroke:'#0f172a'});
 add('rect',{x:1,y:1,width:width-2,height:32,fill:'#0f172a'});
 add('text',{x:16,y:22,fill:'white','font-size':14,'font-family':'Arial,sans-serif','font-weight':700},'BẢNG BIẾN THIÊN');
 for(const y of [90,144])add('line',{x1:1,y1:y,x2:width-1,y2:y,stroke:'#0f172a','stroke-width':1.6});
 add('line',{x1:82,y1:33,x2:82,y2:height-1,stroke:'#0f172a','stroke-width':1.6});
 const label=(x,y,t,color='#0f172a')=>add('text',{x,y,fill:color,'text-anchor':'middle','dominant-baseline':'middle'},t.replace(/-/g,'−'));
 label(42,61,data[0][0]);label(42,117,data[1][0]);label(42,225,data[2][0]);
 const xs=points.map((_,k)=>125+k*(width-175)/(points.length-1));
 const level=(v,k,side)=>v.includes('∞')?(v.startsWith('-')?282:168):((side==='left'?dirs[k-1]==='up':dirs[k]==='down')?180:270);
 points.forEach((i,k)=>{label(xs[k],61,data[0][i]);if(values[k].length===2){for(const offset of [-3,3])add('line',{x1:xs[k]+offset,y1:91,x2:xs[k]+offset,y2:height-2,stroke:down,'stroke-width':1.4});label(xs[k]-28,level(values[k][0],k,'left'),values[k][0]);label(xs[k]+28,level(values[k][1],k,'right'),values[k][1]);}else{label(xs[k],117,data[1][i]);const y=values[k][0].includes('∞')?level(values[k][0],k,'right'):(dirs[k]==='down'||dirs[k-1]==='up'?180:270);label(xs[k],y,values[k][0]);}});
 dirs.forEach((d,k)=>{const color=d==='up'?up:down;label((xs[k]+xs[k+1])/2,117,data[1].slice(points[k]+1,points[k+1]).join(''),color);const x1=xs[k]+45,x2=xs[k+1]-45,y1=d==='up'?270:180,y2=d==='up'?180:270;add('line',{x1,y1,x2,y2,stroke:color,'stroke-width':2.8});const a=Math.atan2(y2-y1,x2-x1),size=16;add('path',{d:`M ${x2-size*Math.cos(a-.5)} ${y2-size*Math.sin(a-.5)} L ${x2} ${y2} L ${x2-size*Math.cos(a+.5)} ${y2-size*Math.sin(a+.5)} Z`,fill:color,stroke:color});});
 const wrapper=document.createElement('div');wrapper.style.cssText='overflow-x:auto;margin:16px 0;break-inside:avoid';wrapper.append(svg);table.replaceWith(wrapper);
}
await document.fonts.ready;status.textContent=errors?'Có '+errors+' công thức cần kiểm tra; chưa cho in.':'Đã dựng công thức. Có thể in hoặc lưu PDF.';status.className=errors?'notice':'';
const print=document.getElementById('print');print.disabled=errors>0;print.onclick=()=>window.print();document.documentElement.dataset.renderErrors=String(errors);document.documentElement.dataset.renderReady='true';
})();</script></body></html>'''


def handwritten_prompt(subject, grade, topic, lesson):
    subject, grade = academic_context(subject, grade)
    return json.dumps({"purpose": "STYLE REFERENCE ONLY — use deterministic HTML/PDF for authoritative text and formulas",
                       "subject": subject, "grade": grade, "title": topic, "content": lesson,
                       "style": {"paper": "cream graph paper #F5EEDC", "binding": "black spiral on the left",
                                 "body_ink": "#182C73", "heading_ink": "#B51E35",
                                 "handwriting": "legible Vietnamese cursive, slight right slant, complete diacritics",
                                 "layout": "notebook page; two-part header; red underlined section headings; blue body; black spiral loops and punched holes on left; fine square grid",
                                 "reference_scope": "Use the supplied notebook image for visual style only; no exam year, ministry identity, questions, or official certification"},
                       "rules": ["Use only the supplied lesson content and context", "Never invent or alter formulas, facts, examples or figures", "All graph and variation-table panels inside the infographic must have transparent backgrounds, including label backdrops, so the parent infographic paper/grid shows through; never put them on an opaque white rectangle", "When the supplied lesson calls for a graph, draw the actual graph of its stated function; include projections of extrema and symmetry centers to both coordinate axes, exact irrational coordinates and axis intercept coordinates, with collision-free labels; never replace exact coordinates with rounded decimals or a verbal description",
                                 "Preserve chemical, physical, mathematical and language notation for this subject",
                                 "Use multiple pages instead of cutting or shrinking content", "Render variation tables as transparent panels over the infographic background; use large green rising/red falling arrows, aligned critical values and split one-sided limits at vertical discontinuities; never substitute tiny Unicode arrows in a flat grid", "Do not copy any subject matter or identity from a style reference"]}, ensure_ascii=False, indent=2)


def faithful_infographic_data(subject, grade, topic, lesson):
    academic_context(subject, grade)
    if not lesson or not lesson.strip():
        raise ValueError("Không có nội dung bài học để trích xuất infographic.")
    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    title, rows = str(topic or subject), []
    tokens = md.parse(lesson)
    for index, token in enumerate(tokens):
        if token.type == "inline" and index and tokens[index - 1].type == "heading_open":
            title = token.content
        elif token.type == "inline" and token.content.strip():
            rows.append((title, token.content, ""))
    # Legacy SVG is explicitly a short excerpt. Full, exact, multi-page content
    # is available in build_lesson_html; never pad excerpt slots with facts.
    return {"box1": rows[:4], "box2": rows[4:8], "box4": [],
            "example": {"title": "Nội dung trích từ bài học", "steps": [], "visual_svg": ""},
            "source_sha256": hashlib.sha256(lesson.encode()).hexdigest(), "is_excerpt": True}
