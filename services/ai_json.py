"""Bounded JSON syntax recovery without inventing missing exam content."""
import json
import re


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON có khóa trùng; chưa sử dụng vì có thể làm mất câu hỏi.")
        result[key] = value
    return result


def _trailing_commas(text):
    result = []
    quoted = escaped = False
    for index, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == ',':
            following = index + 1
            while following < len(text) and text[following].isspace():
                following += 1
            if following < len(text) and text[following] in '}]':
                continue
        result.append(char)
    return ''.join(result)


def _inner_quotes(text):
    # A single linear scan instead of slicing both halves of the full response
    # for every quote. Keep delimiters; escape prose quotes only as a candidate.
    following = [len(text)] * (len(text) + 1)
    for index in range(len(text) - 1, -1, -1):
        following[index] = index if not text[index].isspace() else following[index + 1]
    result = []
    quoted = escaped = False
    for index, char in enumerate(text):
        if escaped:
            result.append(char)
            escaped = False
            continue
        if char == '\\' and quoted:
            result.append(char)
            escaped = True
            continue
        if char == '"':
            if not quoted:
                quoted = True
            else:
                next_index = following[index + 1]
                next_char = text[next_index] if next_index < len(text) else ''
                if not next_char or next_char in '},]:"{[':
                    quoted = False
                else:
                    result.append('\\')
        result.append(char)
    return ''.join(result)


def _decode_with_commas(text):
    text = _trailing_commas(text)
    for attempt in range(9):
        try:
            return json.loads(text, strict=False, object_pairs_hook=_unique_object)
        except json.JSONDecodeError as error:
            if error.msg == "Extra data":
                candidate = text.lstrip()
                value, end = json.JSONDecoder(
                    strict=False, object_pairs_hook=_unique_object).raw_decode(candidate)
                suffix = ''.join(candidate[end:].split())
                closer = {'{': '}', '[': ']'}.get(candidate[:1])
                # Observed local response: complete exam object + one extra }.
                # Only discard up to three matching closing tokens, never any
                # answer/question text, another root, or a missing root closer.
                if closer and 1 <= len(suffix) <= 3 and suffix == closer * len(suffix):
                    return value
            # The decoder has already recognized a complete value. Inserting a
            # separator here does not create a key, an answer or a closing brace.
            if (attempt == 8 or error.msg != "Expecting ',' delimiter"
                    or error.pos >= len(text) or text[error.pos] not in '"{['):
                raise
            text = text[:error.pos] + ',' + text[error.pos:]


def parse_ai_json(raw, prepare=lambda value: value):
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("AI không trả nội dung JSON.")
    if len(raw) > 2_000_000:
        raise ValueError("Phản hồi JSON quá lớn; chưa đưa vào đề.")
    text = raw.strip().lstrip('\ufeff')
    # Treat a short prose preamble followed by a JSON code fence exactly like
    # a fence at the start. Do not trim arbitrary text after the root or invent
    # closing braces; the full remaining candidate must still decode.
    if not text.startswith(('{', '[', '```')):
        fence = re.search(r'```(?:json)?[ \t]*\r?\n', text, flags=re.I)
        if fence and not any(char in text[:fence.start()] for char in '{}[]'):
            text = text[fence.start():]
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*', '', text, count=1, flags=re.I)
        text = re.sub(r'\s*```\s*$', '', text, count=1)
    if not text.startswith(('{', '[')):
        start = text.find('{')
        if start >= 0:
            text = text[start:]
    text = prepare(text)
    try:
        return _decode_with_commas(text)
    except RecursionError as error:
        raise ValueError("JSON lồng quá sâu; chưa sử dụng bản nháp.") from error
    except json.JSONDecodeError:
        pass
    try:
        return _decode_with_commas(_inner_quotes(text))
    except json.JSONDecodeError as error:
        raise ValueError(
            f"JSON của AI chưa hợp lệ tại dòng {error.lineno}, cột {error.colno}. "
            "Chưa dùng bản nháp này; không tự đóng nội dung bị cắt hoặc tự bù đáp án."
        ) from error
    except RecursionError as error:
        raise ValueError("JSON lồng quá sâu; chưa sử dụng bản nháp.") from error
