import json
import os
import time

EPSILON = 1e-9
REPEAT = 10
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
LABEL_MAP = {"+": "Cross", "cross": "Cross", "x": "X"}


def print_section(title):
    print()
    print("#" + "-" * 40)
    print(f"# {title}")
    print("#" + "-" * 40)


def read_matrix(title, size=3):
    print(f"{title} ({size}줄 입력, 공백 구분)")
    matrix = []
    while len(matrix) < size:
        parts = input().split()
        if len(parts) != size:
            print(f"  ⚠ 입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요. (지금 {len(parts)}개)")
            continue
        try:
            row = [float(p) for p in parts]
        except ValueError:
            print("  ⚠ 입력 형식 오류: 숫자만 입력할 수 있어요. 이 줄을 다시 입력하세요.")
            continue
        matrix.append(row)
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print("  " + " ".join(str(v) for v in row))


def mac(filter_grid, pattern_grid):
    total = 0.0
    n = len(filter_grid)
    for i in range(n):
        for j in range(n):
            total += filter_grid[i][j] * pattern_grid[i][j]
    return total


def judge(score_a, score_b, label_a, label_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    if score_a > score_b:
        return label_a
    return label_b


def measure_mac_ms(filter_grid, pattern_grid, repeat=REPEAT):
    total_time = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        mac(filter_grid, pattern_grid)
        end = time.perf_counter()
        total_time += end - start
    return total_time / repeat * 1000


def print_performance_table(rows):
    print("크기       평균 시간(ms)    연산 횟수")
    print("-" * 37)
    for n, avg_ms in rows:
        label = f"{n}×{n}"
        print(f"{label:<10}{avg_ms:>12.4f}{n * n:>12}")


def run_user_mode():
    print_section("[1] 필터 입력")
    filter_a = read_matrix("필터 A")
    print()
    filter_b = read_matrix("필터 B")

    print("\n✓ 필터 저장 완료")
    print("필터 A:")
    print_matrix(filter_a)
    print("필터 B:")
    print_matrix(filter_b)

    print_section("[2] 패턴 입력")
    pattern = read_matrix("패턴")

    score_a = mac(filter_a, pattern)
    score_b = mac(filter_b, pattern)
    avg_ms = measure_mac_ms(filter_a, pattern)
    result = judge(score_a, score_b, "A", "B")

    print_section("[3] MAC 결과")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/{REPEAT}회): {avg_ms:.4f} ms")
    if result == "UNDECIDED":
        print("판정: 판정 불가 (|A-B| < 1e-9)")
    else:
        print(f"판정: {result}")

    print_section(f"[4] 성능 분석 (평균/{REPEAT}회)")
    print_performance_table([(3, avg_ms)])


def normalize_label(raw):
    key = str(raw).strip().lower()
    return LABEL_MAP.get(key)


def is_square(matrix, n):
    if not isinstance(matrix, list) or len(matrix) != n:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return False
        for value in row:
            if not isinstance(value, (int, float)):
                return False
    return True


def load_data(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠ data.json 파일을 찾을 수 없어요. main.py와 같은 폴더에 두세요.")
    except json.JSONDecodeError as e:
        print(f"⚠ data.json 형식이 잘못됐어요: {e}")
    return None


def load_filters(data):
    filters = {}
    raw_filters = data.get("filters", {})
    for size_key, pair in raw_filters.items():
        try:
            n = int(size_key.split("_")[1])
        except (IndexError, ValueError):
            print(f"✗ {size_key}: 필터 키 이름이 size_N 형식이 아니에요")
            continue
        loaded = {}
        for raw_label, matrix in pair.items():
            label = normalize_label(raw_label)
            if label is None:
                print(f"✗ {size_key}: 알 수 없는 필터 이름 '{raw_label}'")
            elif not is_square(matrix, n):
                print(f"✗ {size_key}: {raw_label} 필터가 {n}×{n}이 아니에요")
            else:
                loaded[label] = matrix
        if "Cross" in loaded and "X" in loaded:
            filters[n] = loaded
            print(f"✓ {size_key:<8} 필터 로드 완료 (Cross, X)")
        else:
            print(f"✗ {size_key:<8} 필터 로드 실패 (Cross와 X가 모두 필요)")
    return filters


def analyze_pattern(key, item, filters):
    try:
        n = int(key.split("_")[1])
    except (IndexError, ValueError):
        return None, "키 이름이 size_N_idx 형식이 아님"
    if n not in filters:
        return None, f"size_{n} 필터가 없음"
    if not isinstance(item, dict):
        return None, "패턴 항목 형식 오류"
    expected = normalize_label(item.get("expected", ""))
    if expected is None:
        return None, f"expected 라벨을 알 수 없음 ({item.get('expected')})"
    pattern = item.get("input")
    if not is_square(pattern, n):
        return None, f"패턴 크기가 {n}×{n}이 아님 (필터와 크기 불일치)"

    score_cross = mac(filters[n]["Cross"], pattern)
    score_x = mac(filters[n]["X"], pattern)
    result = judge(score_cross, score_x, "Cross", "X")
    return (score_cross, score_x, result, expected), None


def make_cross(n):
    mid = n // 2
    return [[1.0 if (i == mid or j == mid) else 0.0 for j in range(n)] for i in range(n)]


def run_json_mode():
    print_section("[1] 필터 로드")
    data = load_data(DATA_FILE)
    if not isinstance(data, dict):
        print("data.json을 읽지 못해서 분석을 멈춰요.")
        return
    filters = load_filters(data)

    print_section("[2] 패턴 분석 (라벨 정규화 적용)")
    total = 0
    passed = 0
    failures = []
    for key, item in data.get("patterns", {}).items():
        total += 1
        print(f"--- {key} ---")
        outcome, error = analyze_pattern(key, item, filters)
        if error:
            print(f"FAIL ({error})")
            failures.append((key, error))
            continue
        score_cross, score_x, result, expected = outcome
        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        if result == expected:
            passed += 1
            print(f"판정: {result} | expected: {expected} | PASS")
        else:
            if result == "UNDECIDED":
                reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL (|Cross-X| < 1e-9)"
            else:
                reason = f"판정 {result}이(가) expected {expected}와 다름"
            print(f"판정: {result} | expected: {expected} | FAIL")
            failures.append((key, reason))

    print_section(f"[3] 성능 분석 (평균/{REPEAT}회)")
    rows = []
    cross3 = make_cross(3)
    rows.append((3, measure_mac_ms(cross3, cross3)))
    for n in sorted(filters):
        f = filters[n]["Cross"]
        rows.append((n, measure_mac_ms(f, f)))
    print_performance_table(rows)

    print_section("[4] 결과 요약")
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {len(failures)}개")
    if failures:
        print()
        print("실패 케이스:")
        for key, reason in failures:
            print(f"- {key}: {reason}")


def main():
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = input("선택: ").strip()
    if choice == "1":
        run_user_mode()
    elif choice == "2":
        run_json_mode()
    else:
        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()
