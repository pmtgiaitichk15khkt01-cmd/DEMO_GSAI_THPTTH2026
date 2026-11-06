"""Escape printable source text while retaining fenced code verbatim."""
import html
import re

FENCES = re.compile(r'(```[^\n]*\n[\s\S]*?```|~~~[^\n]*\n[\s\S]*?~~~)')


def code_body(block):
    return block.split('\n', 1)[1][:-3].rstrip('\r\n')


def source_text_html(value):
    chunks = FENCES.split(str(value or ''))
    return ''.join('<code class="exam-source-code" style="display:block;white-space:pre-wrap;'
                   'font:12px/1.4 monospace;overflow-wrap:anywhere;margin:6px 0">'
                   + html.escape(code_body(chunk)) + '</code>' if index % 2
                   else html.escape(chunk) for index, chunk in enumerate(chunks))


def code_text_latex(block):
    replacements = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}",
                    "&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#",
                    "$": r"\$", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
                    " ": r"\ "}
    lines = [''.join(replacements.get(c,c) for c in line) for line in code_body(block).splitlines()]
    return r"\par\begingroup\ttfamily\small " + r"\\ ".join(lines) + r"\par\endgroup "
