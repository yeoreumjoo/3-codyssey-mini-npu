import time

EPSILON = 1e-9
REPEAT = 10


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
        print("모드 2 준비 중")
    else:
        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()
