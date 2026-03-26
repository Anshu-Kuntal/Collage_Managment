def input_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if (min_val is not None and val < min_val) or \
               (max_val is not None and val > max_val):
                print("❌ Out of range.")
                continue
            return val
        except ValueError:
            print("❌ Enter a valid integer.")


def input_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt))
            if (min_val is not None and val < min_val) or \
               (max_val is not None and val > max_val):
                print("❌ Out of range.")
                continue
            return val
        except ValueError:
            print("❌ Enter a valid number.")
