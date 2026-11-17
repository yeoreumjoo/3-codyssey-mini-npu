def read_matrix(title, size=3):
    print(f"{title} ({size}줄 입력, 공백 구분)")
    matrix = []
    while len(matrix) < size:
        parts = input().split()
        if len(parts) != size:
            print(f"  ⚠ 숫자 {size}개를 띄어 써 주세요. (지금 {len(parts)}개) 이 줄을 다시 입력하세요.")
            continue
        try:
            row = [float(p) for p in parts]
        except ValueError:
            print("  ⚠ 숫자만 입력할 수 있어요. 이 줄을 다시 입력하세요.")
            continue
        matrix.append(row)
    return matrix


def main():
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = input("선택: ").strip()
    if choice == "1":
        filter_a = read_matrix("필터 A")
        print(filter_a)
    elif choice == "2":
        print("모드 2 준비 중")
    else:
        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()