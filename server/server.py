import subprocess


def calculate(expr: str, isFloat: bool):
    if isFloat:
        res = subprocess.run(
            ["build/app.exe", "--float"], input=expr, text=True, capture_output=True
        )
    else:
        res = subprocess.run(
            ["build/app.exe"], input=expr, text=True, capture_output=True
        )

    if res.returncode != 0:
        print("ERROR!!!", res.returncode)
    try:
        if isFloat:
            return float(res.stdout)
        else:
            return int(res.stdout)
    except ValueError as e:
        raise e


def main():
    print(calculate("123+ 10", True))


if __name__ == "__main__":
    main()
