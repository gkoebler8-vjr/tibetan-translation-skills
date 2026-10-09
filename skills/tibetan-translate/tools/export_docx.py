#!/usr/bin/env python3
"""
export_docx.py -- turn a tibetan-translate final.md into a Word document with real footnotes.

  python3 export_docx.py final.md [-o out.docx] [--notes] [--title "..."] [--no-headers]

Reads the per-unit blocks (### Uxx / HEADER: / TEXT: / FOOTNOTES: / NOTES:). The TEXT of each unit
becomes body paragraphs (verse lines as line breaks inside one paragraph; a blank line starts a new
paragraph). Each `FN(<anchor>): <text>` line becomes a Word footnote whose reference mark is placed
right after the first occurrence of <anchor> in that unit's text (at the end of the unit if the anchor
is not found, with a warning). `FN(): <text>` and `FN(*): <text>` are footnotes on the whole unit: the mark
goes after the last character of the unit's last paragraph (after the final punctuation), no warning. The CAT
app writes its edited final.md in this format. The editor NOTES are left out unless --notes, which appends them as an
"Editor's notes" section at the end, one paragraph per unit. A unit whose HEADER carries
`confidence: low` is shaded orange, `confidence: very low` red, with the Conf: reason in the header
line, so the reviser sees where to look first. Needs python-docx (pip install python-docx).
"""
import argparse, re, sys, copy
try:
    import docx
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.opc.part import Part
    from docx.opc.packuri import PackURI
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    sys.exit("python-docx is needed: pip install python-docx")

FOOTNOTES_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def parse(md):
    units, cur, field = [], None, None
    for line in md.splitlines():
        m = re.match(r"^### (U\d+|\S+)\s*$", line)
        if m:
            cur = {"id": m.group(1), "HEADER": "", "TEXT": [], "FOOTNOTES": [], "NOTES": []}
            units.append(cur); field = None; continue
        if cur is None:
            continue
        if line.startswith("## "):            # run summary etc.
            cur = None; field = None; continue
        m = re.match(r"^(HEADER|TEXT|FOOTNOTES|NOTES):\s*(.*)$", line)
        if m:
            field = m.group(1)
            if field == "HEADER":
                cur["HEADER"] = m.group(2).strip()
            elif m.group(2).strip():
                cur[field].append(m.group(2))
            continue
        if field in ("TEXT", "FOOTNOTES", "NOTES"):
            cur[field].append(line)
    for u in units:
        u["TEXT"] = [l.rstrip() for l in u["TEXT"]]
        while u["TEXT"] and not u["TEXT"][-1]: u["TEXT"].pop()
        while u["TEXT"] and not u["TEXT"][0]: u["TEXT"].pop(0)
        fns = []
        for l in u["FOOTNOTES"]:
            m = re.match(r"^\s*FN\((.*?)\):\s*(.*)$", l)
            if m:
                fns.append([m.group(1).strip(), m.group(2).strip()])
            elif fns and l.strip() and l.strip().lower() != "none":
                fns[-1][1] += " " + l.strip()
        u["FOOTNOTES"] = fns
        u["NOTES"] = [l for l in u["NOTES"] if l.strip() and l.strip().lower() != "none"]
    return units

class Footnotes:
    """Adds a /word/footnotes.xml part to a python-docx Document and hands out footnote ids."""
    def __init__(self, document):
        self.doc = document
        self.part = None
        self.root = None
        self.next_id = 1
        self._ensure_part()

    def _ensure_part(self):
        dp = self.doc.part
        for rel in dp.rels.values():
            if rel.reltype == RT.FOOTNOTES:
                self.part = rel.target_part
                from lxml import etree
                self.root = etree.fromstring(self.part.blob)
                ids = [int(f.get(qn("w:id"))) for f in self.root.findall(qn("w:footnote"))]
                self.next_id = max([0] + ids) + 1
                self.part._element = self.root
                return
        xml = ('<w:footnotes xmlns:w="%s">'
               '<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>'
               '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>'
               '</w:footnotes>') % W
        from lxml import etree
        self.root = etree.fromstring(xml.encode())
        self.part = Part(PackURI("/word/footnotes.xml"), FOOTNOTES_CT, b"", dp.package)
        dp.relate_to(self.part, RT.FOOTNOTES)
        # settings: tell Word which footnotes are the separators
        settings = self.doc.settings.element
        if settings.find(qn("w:footnotePr")) is None:
            fp = OxmlElement("w:footnotePr")
            for i in ("-1", "0"):
                fn = OxmlElement("w:footnote"); fn.set(qn("w:id"), i); fp.append(fn)
            later = ("endnotePr compat docVars rsids mathPr attachedSchema themeFontLang clrSchemeMapping doNotIncludeSubdocsInStats "
                     "doNotAutoCompressPictures forceUpgrade captions readModeInkLockDown smartTagType schemaLibrary shapeDefaults "
                     "doNotEmbedSmartTags decimalSymbol listSeparator").split()
            for child in list(settings):
                if child.tag.split('}')[-1] in later:
                    child.addprevious(fp); break
            else:
                settings.append(fp)

    def add(self, text):
        fid = self.next_id; self.next_id += 1
        fn = OxmlElement("w:footnote"); fn.set(qn("w:id"), str(fid))
        p = OxmlElement("w:p")
        ppr = OxmlElement("w:pPr"); sp = OxmlElement("w:spacing"); sp.set(qn("w:after"), "0"); ppr.append(sp); p.append(ppr)
        rpr0 = OxmlElement("w:rPr"); sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "20"); rpr0.append(sz)
        r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr"); va = OxmlElement("w:vertAlign"); va.set(qn("w:val"), "superscript"); rpr.append(va); r.append(rpr)
        ref = OxmlElement("w:footnoteRef"); r.append(ref); p.append(r)
        r2 = OxmlElement("w:r"); r2.append(rpr0); t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = " " + text; r2.append(t); p.append(r2)
        fn.append(p); self.root.append(fn)
        return fid

    def reference(self, paragraph, fid):
        r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr"); va = OxmlElement("w:vertAlign"); va.set(qn("w:val"), "superscript"); rpr.append(va); r.append(rpr)
        fr = OxmlElement("w:footnoteReference"); fr.set(qn("w:id"), str(fid)); r.append(fr)
        paragraph._p.append(r)

    def save_into(self):
        from lxml import etree
        self.part._blob = etree.tostring(self.root, xml_declaration=True, encoding="UTF-8", standalone=True)

def confidence_of(header):
    m = re.search(r"confidence:\s*(very low|low|medium|high)", header, re.I)
    return m.group(1).lower() if m else None

SHADE = {"low": "FFD8A8", "very low": "F4A6A6"}   # orange, red

PPR_AFTER_SHD = ("tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi "
                 "adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection "
                 "textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange").split()

def insert_in_order(parent, el, later_tags):
    """Insert EL before the first child whose local tag is in LATER_TAGS (schema order), else append."""
    for child in list(parent):
        if child.tag.split('}')[-1] in later_tags:
            child.addprevious(el); return
    parent.append(el)

def shade_ppr(ppr, fill):
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
    insert_in_order(ppr, shd, PPR_AFTER_SHD)

def shade(paragraph, grade):
    fill = SHADE.get(grade)
    if not fill:
        return
    shade_ppr(paragraph._p.get_or_add_pPr(), fill)

def add_text_with_breaks(paragraph, lines):
    for i, l in enumerate(lines):
        if i:
            paragraph.add_run().add_break()
        paragraph.add_run(l)

def build(units, out, notes=False, title=None, headers=True):
    document = docx.Document()
    fns = Footnotes(document)
    if title:
        document.add_heading(title, level=1)
    warnings = []
    grades = [confidence_of(u["HEADER"]) for u in units]
    if any(g in ("low", "very low") for g in grades):
        lg = document.add_paragraph(); r = lg.add_run("Confidence: units shaded orange are graded low, red very low (reason in the unit's header line); unshaded units are medium or high."); r.italic = True; r.font.size = docx.shared.Pt(8)
    for u, grade in zip(units, grades):
        if headers and u["HEADER"]:
            h = document.add_paragraph(); r = h.add_run(u["id"] + " · " + u["HEADER"]); r.italic = True; r.font.size = docx.shared.Pt(8)
            conf = [n for n in u["NOTES"] if n.strip().startswith("Conf:")]
            if grade in ("low", "very low") and conf:
                r2 = h.add_run("  [" + conf[0].strip() + "]"); r2.italic = True; r2.font.size = docx.shared.Pt(8)
            shade(h, grade)
        # paragraphs: split TEXT on blank lines; a verse block (several short lines) becomes one paragraph with line breaks
        paras, buf = [], []
        for l in u["TEXT"] + [""]:
            if l.strip():
                buf.append(l)
            elif buf:
                paras.append(buf); buf = []
        unit_end = [fn for fn in u["FOOTNOTES"] if fn[0] in ("", "*")]       # FN(): / FN(*): belong to the whole unit
        pending = [fn for fn in u["FOOTNOTES"] if fn[0] not in ("", "*")]
        last_p = None
        for lines in paras:
            text = " ".join(lines) if len(lines) == 1 else None
            p = document.add_paragraph(); shade(p, grade); last_p = p
            if text is not None:
                # place footnote references after their anchors
                pos_fns = []
                for anchor, body in list(pending):
                    k = text.find(anchor)
                    if k >= 0:
                        pos_fns.append((k + len(anchor), anchor, body)); pending.remove([anchor, body])
                pos_fns.sort()
                last = 0
                for pos, anchor, body in pos_fns:
                    p.add_run(text[last:pos]); fns.reference(p, fns.add(body)); last = pos
                p.add_run(text[last:])
            else:
                # verse: one run per line with breaks; anchors matched per line
                for i, l in enumerate(lines):
                    if i:
                        p.add_run().add_break()
                    hits = [(l.find(a) + len(a), a, b) for a, b in pending if l.find(a) >= 0]
                    hits.sort(); last = 0
                    for pos, a, b in hits:
                        p.add_run(l[last:pos]); fns.reference(p, fns.add(b)); pending.remove([a, b]); last = pos
                    p.add_run(l[last:])
        for anchor, body in pending:
            warnings.append(f"{u['id']}: anchor not found: {anchor!r}; footnote placed at the unit's end")
            p = last_p or document.paragraphs[-1]; fns.reference(p, fns.add(body))
        for anchor, body in unit_end:
            if last_p is None:
                last_p = document.add_paragraph(); shade(last_p, grade)
            fns.reference(last_p, fns.add(body))
    if notes and any(u["NOTES"] for u in units):
        document.add_page_break(); document.add_heading("Editor's notes", level=1)
        for u in units:
            if u["NOTES"]:
                document.add_paragraph(u["id"], style="Heading 3")
                for n in u["NOTES"]:
                    document.add_paragraph(n)
    fns.save_into()
    document.save(out)
    return warnings

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("final_md"); ap.add_argument("-o", "--out"); ap.add_argument("--notes", action="store_true", help="append the editor notes as a final section")
    ap.add_argument("--title"); ap.add_argument("--no-headers", action="store_true", help="omit the per-unit header lines")
    a = ap.parse_args()
    units = parse(open(a.final_md, encoding="utf-8").read())
    if not units:
        sys.exit("no ### Uxx blocks found")
    out = a.out or re.sub(r"\.md$", "", a.final_md) + ".docx"
    warnings = build(units, out, notes=a.notes, title=a.title, headers=not a.no_headers)
    nf = sum(len(u["FOOTNOTES"]) for u in units)
    print(f"wrote {out}: {len(units)} units, {nf} footnotes" + (f", {len(warnings)} warning(s)" if warnings else ""))
    for w in warnings:
        print("  " + w)

if __name__ == "__main__":
    main()
