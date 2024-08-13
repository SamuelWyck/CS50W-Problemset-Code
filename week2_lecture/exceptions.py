
while True:
    try:
        x = int(input("x: "))
    except ValueError:
        print("Error: x must be a number.")
        continue
    try:
        y = int(input("y: "))
    except ValueError:
        print("Error: y must be a number.")
        continue

    try:
        result = x / y
        break
    except ZeroDivisionError:
        print("Error: Cannot divide by 0.")
        continue

print(f"{x} / {y} = {result}")