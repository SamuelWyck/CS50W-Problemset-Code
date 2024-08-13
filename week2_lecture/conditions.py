while True:
    try:
        number = int(input("Number: "))
        break
    except ValueError:
        pass

if number > 0:
    print("Number is positive")
elif number == 0:
    print("Number equals zero")
else:
    print("Number is negative")