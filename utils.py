def input_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt).strip())

            if min_val is not None and val < min_val:
                print(f"❌ Value must be >= {min_val}")
                continue

            if max_val is not None and val > max_val:
                print(f"❌ Value must be <= {max_val}")
                continue

            return val

        except ValueError:
            print("❌ Enter a valid integer.")


def input_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt).strip())

            if min_val is not None and val < min_val:
                print(f"❌ Value must be >= {min_val}")
                continue

            if max_val is not None and val > max_val:
                print(f"❌ Value must be <= {max_val}")
                continue

            return val

        except ValueError:
            print("❌ Enter a valid number.")
