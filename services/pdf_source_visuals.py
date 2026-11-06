"""Crop original PDF question regions without mixing equal numbers across parts."""
import base64
import hashlib
import re


def extract_pdf_question_visuals(file_bytes, max_pages=150, max_regions=100):
    import pymupdf
    if len(file_bytes) > 30 * 1024 * 1024:
        raise ValueError("Tệp PDF vượt giới hạn 30 MB cho quét hình một lượt.")
    images, regions, ambiguous = {}, {}, set()
    numbers = {}
    section = "p1"
    signature = hashlib.sha256(file_bytes).hexdigest()
    header = re.compile(r"(?:PHẦN|PHAN)\s*(III|II|I|[123])\b", re.I)
    question = re.compile(r"(?:Câu|Cau|Bài|Bai)\s*(\d+)\s*[.:)]", re.I)
    with pymupdf.open(stream=file_bytes, filetype="pdf") as document:
        for page_no, page in enumerate(document):
            if page_no >= max_pages or len(images) >= max_regions:
                break
            markers = []
            for block in sorted(page.get_text("blocks"), key=lambda b: (b[1], b[0])):
                text = block[4]
                found_header = header.search(text)
                if found_header:
                    section = {"I": "p1", "II": "p2", "III": "p3", "1": "p1", "2": "p2", "3": "p3"}[found_header[1].upper()]
                    markers.append((block[1], "header", section, None, block[0]))
                found_questions = list(question.finditer(text))
                if len(found_questions) != 1:
                    continue  # No reliable per-question boundary in a merged text block.
                number = int(found_questions[0][1])
                markers.append((block[1], "question", section, number, block[0]))
            q_markers = [m for m in markers if m[1] == "question"]
            if q_markers and max(m[4] for m in q_markers) - min(m[4] for m in q_markers) > page.rect.width * .25:
                continue  # Two-column ambiguity must not crop another question's figure.
            markers.sort(key=lambda m: m[0])
            drawings = [d["rect"] for d in page.get_drawings()]
            embedded = [rect for image in page.get_images() for rect in page.get_image_rects(image[0])]
            for index, marker in enumerate(markers):
                y0, kind, part, number, _ = marker
                if kind != "question":
                    continue
                key = f"{part}_q_{number}"
                numbers.setdefault(number, []).append(key)
                if key in regions or key in ambiguous:
                    ambiguous.add(key); images.pop(key, None); regions.pop(key, None)
                    continue
                y_end = markers[index + 1][0] if index + 1 < len(markers) else page.rect.height
                rect = pymupdf.Rect(0, max(0, y0 - 2), page.rect.width, min(page.rect.height, y_end - 2))
                if rect.height < 20:
                    continue
                text = page.get_text("text", clip=rect).lower()
                cue = any(term in text for term in ("hình", "hinh", "đồ thị", "do thi", "sơ đồ", "so do", "biểu đồ"))
                if not cue or not any(rect.intersects(shape) for shape in drawings + embedded):
                    continue
                pixmap = page.get_pixmap(matrix=pymupdf.Matrix(1.7, 1.7), clip=rect)
                images[key] = "data:image/png;base64," + base64.b64encode(pixmap.tobytes("png")).decode("ascii")
                regions[key] = {"source_sha256": signature, "page": page_no + 1, "bbox": list(rect), "part": part, "question_number": number,
                                "method": "original_pdf_region_not_generated", "mapping_requires_review": True}
        truncated = len(document) > max_pages or len(images) >= max_regions
    for number, keys in numbers.items():
        if len(keys) == 1 and keys[0] in images:
            images[f"q_{number}"] = images[keys[0]]  # Backward compatibility only when unambiguous.
    images["_regions"] = regions
    images["_ambiguous"] = sorted(ambiguous)
    images["_truncated"] = truncated
    return images
