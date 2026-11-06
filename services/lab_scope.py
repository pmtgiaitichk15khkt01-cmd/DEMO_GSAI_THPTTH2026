"""Label the existing preset library without pretending it is the current lesson."""
import re
import math

from services.academic_context import academic_context, canonical_subject

T1_CONTEXT_REVISION = 2026110202


def is_proposition_request(command, subject):
    from services.academic_context import folded
    return canonical_subject(subject) == 'Toán học' and 'menh de' in folded(command)


def proposition_lab_request(command, subject):
    """Route a supported explicit predicate task by intent, not polynomial shape.

    Parse a limited numeric quadratic equality, never arbitrary Python/code.
    Unknown expressions are left unsupported rather than replaced by a sample.
    """
    from fractions import Fraction
    if not is_proposition_request(command, subject):
        return None
    compact = re.sub(r'\s+', ' ', str(command)).replace('−', '-').replace('²', '^2')
    compact = re.sub(r'\s*([+*/^=\-])\s*', r'\1', compact)
    number = r'\d+(?:\.\d+)?'
    match = re.search(r'(?<![\w./*^+\-])(?P<a>[+-]?(?:' + number + r'\*?)?)x\^2'
                      r'(?P<b>[+-](?:' + number + r'\*?)?)x'
                      r'(?P<c>[+-]' + number + r')=0', compact)
    if not match:
        return None
    def coefficient(value):
        value = value.replace('*', '')
        return str(Fraction({'': '1', '+': '1', '-': '-1'}.get(value, value)))
    return dict(type='proposition_quadratic', **{k: coefficient(match[k]) for k in ('a', 'b', 'c')})


def evaluate_proposition(data, value):
    """Exact rational substitution; a false proposition remains a proposition."""
    from fractions import Fraction
    if not re.fullmatch(r'[+-]?\d+(?:\.\d+|/\d+)?', str(value).strip()):
        raise ValueError('Nhập số nguyên, số thập phân hoặc phân số, ví dụ 1/2.')
    x = Fraction(str(value).strip())
    result = Fraction(data['a']) * x*x + Fraction(data['b']) * x + Fraction(data['c'])
    return result, result == 0


def function_formula_latex(numerator, denominator=None):
    """Format selected coefficients exactly, omitting zero terms and +- signs."""
    import sympy as sp
    x = sp.Symbol('x')
    def polynomial(coefficients):
        return sum(sp.Rational(str(value)) * x**power
                   for power, value in enumerate(reversed(coefficients)))
    top = sp.latex(polynomial(numerator))
    if denominator is None:
        return 'y = ' + top
    return r'y = \frac{' + top + '}{' + sp.latex(polynomial(denominator)) + '}'


def lesson_context_examples(subject, grade, topics):
    """Use selected-grade suggestions; never substitute senior-grade examples."""
    subject, grade = academic_context(subject, grade)
    examples = [re.sub(r'^Chuyên đề\s*\d+\s*:\s*', '', str(t)).strip() for t in topics[:2]]
    return 'Ví dụ: ' + '; '.join(examples) if examples else f'Nhập tên bài môn {subject} lớp {grade} và dữ kiện cần học.'


def ideal_ph(log_h):
    """Dilute ideal aqueous model at 25 C; activity approximated by c/c0."""
    value = float(log_h)
    if not math.isfinite(value) or not -14 <= value <= 0:
        raise ValueError('Mẫu pH hỗ trợ log10([H+]/c0) từ -14 đến 0.')
    return dict(ph=-value, log_h=value, log_oh=-14-value,
                h=10**value, oh=10**(-14-value))


def logarithm_model(base, coefficient, vertical_shift, natural=False):
    """Validate and describe y=k*log_a(x)+c without silently changing inputs."""
    base, coefficient, vertical_shift = map(float, (base, coefficient, vertical_shift))
    if not all(math.isfinite(value) for value in (base, coefficient, vertical_shift)):
        raise ValueError('Các tham số phải là số hữu hạn.')
    if natural:
        base = math.e
    elif base <= 0 or math.isclose(base, 1.0, abs_tol=1e-12):
        raise ValueError('Cơ số a phải dương và khác 1.')
    if coefficient == 0:
        behavior = 'constant'
    elif (coefficient > 0) == (base > 1):
        behavior = 'increasing'
    else:
        behavior = 'decreasing'
    return dict(base=base, coefficient=coefficient, vertical_shift=vertical_shift,
                behavior=behavior, has_vertical_asymptote=(coefficient != 0),
                constant_value=vertical_shift if coefficient == 0 else None)


def ammonia_equilibrium(temp_c, pressure_bar):
    """Ideal gas N2+3H2=2NH3; initial mole amounts 1:3:0; p0=1 bar.

    Shomate coefficients: NIST Chemistry WebBook, Chase (1998).
    https://webbook.nist.gov/cgi/cbook.cgi?ID=C7664417&Mask=1
    https://webbook.nist.gov/cgi/cbook.cgi?ID=C7727379&Mask=1
    https://webbook.nist.gov/cgi/cbook.cgi?ID=1333-74-0&cTG=on
    This is an ideal equilibrium model, not industrial yield or reaction rate.
    """
    temperature, pressure = float(temp_c)+273.15, float(pressure_bar)
    if not math.isfinite(temperature) or not 298.15 <= temperature <= 1000 or not math.isfinite(pressure) or pressure <= 0:
        raise ValueError('Ngoài miền nhiệt độ NIST hoặc áp suất không dương.')
    nh3 = (19.99563, 49.77119, -15.37599, 1.921168, .189174, -53.30667, 203.8591)
    h2 = (33.066178, -11.363417, 11.432816, -2.772874, -.158558, -9.980797, 172.707974)
    n2 = ((28.98641, 1.853978, -9.647459, 16.63537, .000117, -8.671914, 226.4168)
          if temperature < 500 else (19.50583, 19.88705, -8.598535, 1.369784, .527601, -4.935202, 212.3900))
    t = temperature/1000

    def hs(coefficients):
        a,b,c,d,e,f,g = coefficients
        # Formation enthalpy is included: Shomate (H-H298) + Hf298.
        h = 1000*(a*t + b*t*t/2 + c*t**3/3 + d*t**4/4 - e/t + f)
        s = a*math.log(t) + b*t + c*t*t/2 + d*t**3/3 - e/(2*t*t) + g
        return h, s

    properties = [hs(coefficients) for coefficients in (nh3, n2, h2)]
    dh, ds = [2*properties[0][i]-properties[1][i]-3*properties[2][i] for i in (0,1)]
    log_kp = -(dh-temperature*ds)/(8.31446261815324*temperature)
    lo, hi = 0.0, 1.0
    for _ in range(70):
        extent = (lo+hi)/2
        if extent >= 1:
            break
        log_q = math.log(4)+2*math.log(extent)+2*math.log(4-2*extent)-math.log(27)-4*math.log1p(-extent)-2*math.log(pressure)
        if log_q < log_kp:
            lo = extent
        else:
            hi = extent
    extent = (lo+hi)/2
    return dict(extent=extent, conversion=100*extent, nh3_mole_fraction=2*extent/(4-2*extent), kp=math.exp(log_kp))


def resolve_preset_lab(subject, label, payload):
    """Correct one mismatched preset; keep its menu identity and other payloads."""
    subject = canonical_subject(subject)
    if subject in ('Hóa học', 'Khoa học tự nhiên') and 'pH' in label:
        return {'type': 'chem_ph', 'log_h': -7.0}
    if (subject == 'Tin học'
            and label == 'Sơ đồ thuật toán & Cây nhị phân'
            and payload.get('type') == 'oxyz'):
        return {'type': 'mermaid', 'code': '''graph TD
R["Mẫu minh họa: tìm kiếm trên cây nhị phân tìm kiếm"] --> T["Cây mẫu"]
T --> N8["8"]
N8 --> N3["Nhánh trái: 3"]
N8 --> N10["Nhánh phải: 10"]
N3 --> N1["Nhánh trái: 1"]
N3 --> N6["Nhánh phải: 6"]
R --> A["Thuật toán: bắt đầu tại gốc, so sánh k với khóa nút"]
A --> E["Nút rỗng: kết luận không tìm thấy"]
A --> F["k bằng khóa: tìm thấy, dừng"]
A --> L["k nhỏ hơn khóa: sang con trái và lặp lại"]
A --> G["k lớn hơn khóa: sang con phải và lặp lại"]'''}
    return dict(payload)


def preset_lab_label(label, subject, grade):
    _, grade = academic_context(subject, grade)
    value = str(label)
    # Keep preset keys/payloads stable for saved sessions while correcting what
    # the rendered menu claims each generic visualization actually represents.
    honest_labels = {
        'Mã hóa dữ liệu (RSA)': 'Đồ thị hàm mũ minh họa (không mô phỏng mã hóa RSA)',
        'Mô hình mạng tinh thể': 'Điểm tọa độ Oxyz minh họa (không phải mô hình mạng tinh thể)',
        'Mạch điện xoay chiều RLC & Dao động': 'Mô hình dao động cơ (không mô phỏng mạch RLC)',
        'Tăng trưởng giới hạn': 'Đồ thị logarit cơ bản (không phải mô hình tăng trưởng giới hạn)',
        'Quy luật di truyền Mendel (KHTN)': 'Mô hình lai Aa × Aa (chỉ xét trội hoàn toàn)',
    }
    for misleading, accurate in honest_labels.items():
        if misleading in value:
            value = value.replace(misleading, accurate)
    if canonical_subject(subject) == 'Khoa học tự nhiên' and 'pH' in value:
        value = value.replace('(KHTN)', '(KNTT 8)')
    match = re.search(r'(?:KNTT|Vật l[íý]|Hóa học|Sinh học)\s*(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?', value, re.I)
    # Existing grade annotations are descriptions supplied with the preset,
    # not a verified curriculum map. Never invent a grade for untagged tools.
    if match:
        first, last = int(match[1]), int(match[2] or match[1])
        grades = f'{first}–{last}' if first != last else str(first)
        prefix = f'Mẫu tham khảo, nhãn lớp {grades}' if first <= grade <= last else f'Mở rộng, nhãn lớp {grades}'
    else:
        prefix = 'Công cụ minh họa'
    body = re.sub(r'\(\s*KNTT\s*\d{1,2}(?:\s*[-–]\s*\d{1,2})?\s*\)', '', value, flags=re.I).strip()
    return f'[{prefix}] {body}'


def preset_lab_note(subject, grade):
    subject, grade = academic_context(subject, grade)
    return (f'Thư viện mẫu minh họa độc lập với bài {subject} lớp {grade} đang học. '
            'Giữ các công cụ mở rộng; nhãn lớp lấy từ cấu hình mẫu, chưa phải đối chiếu SGK. '
            'Mẫu có sẵn không tự lấy hàm số hoặc dữ kiện từ bài học. '
            'Muốn mô phỏng theo bài, hãy nêu rõ dữ kiện trong lệnh mô phỏng bên dưới.')
