# utils.py
def input_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"❌ Enter a value between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("❌ Invalid input. Enter a number.")

def input_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"❌ Enter a value between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("❌ Invalid input. Enter a number.")

def confirm(prompt="Are you sure? (y/n): "):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ['y', 'yes']:
            return True
        elif ans in ['n', 'no']:
            return False
        else:
            print("❌ Invalid input. Type 'y' or 'n'.")
