def main():
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = input("선택: ").strip()
    if choice == "1":
        print("모드 1 준비 중")
    elif choice == "2":
        print("모드 2 준비 중")
    else:
        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()
