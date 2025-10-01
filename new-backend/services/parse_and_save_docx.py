import os, zipfile
from lxml import etree # type: ignore
import json

DATA_DIR = os.getenv("MCP_DATA_DIR", "/data")
DOCS_PARSED_DIR = os.path.join(DATA_DIR, "docs/parsed")
os.makedirs(DOCS_PARSED_DIR, exist_ok=True)

def parse_and_save_docx(file_path):
    parsed = _parse_docx(file_path)
    saved_path = _save_parsed_docx(parsed)
    return saved_path

def _parse_docx(file_path):
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")

    parts_to_read = [
        "word/document.xml",
        "word/styles.xml",
        "word/numbering.xml",
        "word/comments.xml",
        "word/_rels/document.xml.rels",
        "word/footnotes.xml",
        "word/endnotes.xml"
    ]

    out = {"source_path": file_path, "parts": {}}

    with zipfile.ZipFile(file_path) as zf:
        zip_names = set(zf.namelist())

        for part in parts_to_read:
            if part not in zip_names:
                continue
            raw = zf.read(part)
            
            try: 
                root = etree.fromstring(raw)
            except etree.XMLSyntaxError as e:
                out["parts"][part] = {"error": f"XML parse error: {str(e)}"}
                continue
            
            out["parts"][part] = _xml_to_dict(root)
    
    return out

def _xml_to_dict(element):
    qname = etree.QName(element.tag)
    out = {
        "tag": qname.localname,
        "attrib": {etree.QName(k).localname: v for k, v in element.attrib.items()},
    }

    text = (element.text or "").strip()
    if text:
        out["text"] = text

    children = []
    for child in element:
        children.append(_xml_to_dict(child))

    if children:
        out["children"] = children

    return out

def _save_parsed_docx(parsed):
    if "source_path" not in parsed or not isinstance(parsed["source_path"], str):
        raise ValueError("Parsed data must include 'source_path' as a string")

    path = parsed["source_path"]
    base_name = os.path.splitext(os.path.basename(path))[0]
    file_path = os.path.join(DOCS_PARSED_DIR, f"{base_name}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)

    return file_path