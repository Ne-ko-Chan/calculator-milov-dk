import subprocess


def test_simple_int_math():
    res = subprocess.run(
        ["build/app.exe"], input="1 + 2 -3 * 4 / 5", text=True, capture_output=True
    )
    assert res.returncode == 0
    assert res.stdout == "1"


def test_simple_float_math():
    res = subprocess.run(
        ["build/app.exe", "--float"], input="10-9/2 + 5", text=True, capture_output=True
    )
    assert res.returncode == 0
    assert (float(res.stdout) - 10.5) < 10 ** (-4)


def test_ignore_space():
    res = subprocess.run(
        ["build/app.exe", "--float"],
        input="10                                                                                                  -9\t/\f\n2 + 5\r",
        text=True,
        capture_output=True,
    )
    assert res.returncode == 0
    assert (float(res.stdout) - 10.5) < 10 ** (-4)


def test_wrong_input_symbols():
    res = subprocess.run(
        ["build/app.exe", "--float"], input="10-x/@ + 5", text=True, capture_output=True
    )
    assert res.returncode != 0


def test_very_long():
    file = open("tests/integration/long_input.txt", "r")
    content = file.read()
    res = subprocess.run(
        ["build/app.exe", "--float"], input=content, text=True, capture_output=True
    )
    assert res.returncode == 0
    assert (float(res.stdout) - 98176) < 10 ** (-4)


def test_lots_of_braces():
    file = open("tests/integration/hell_lotta_braces.txt", "r")
    content = file.read()
    res = subprocess.run(
        ["build/app.exe", "--float"], input=content, text=True, capture_output=True
    )
    assert res.returncode == 0
    assert (float(res.stdout) - 25) < 10 ** (-4)


def test_mismatched_braces1():
    res = subprocess.run(
        ["build/app.exe", "--float"],
        input="10 + 5 - (6 * 9))",
        text=True,
        capture_output=True,
    )
    assert res.returncode != 0


def test_mismatched_braces2():
    res = subprocess.run(
        ["build/app.exe", "--float"],
        input="10 + 5 - ((6 * 9)",
        text=True,
        capture_output=True,
    )
    assert res.returncode != 0


def test_double_op():
    res = subprocess.run(
        ["build/app.exe", "--float"],
        input="10 + 5 -- (6 * 9)",
        text=True,
        capture_output=True,
    )
    assert res.returncode != 0
    res = subprocess.run(
        ["build/app.exe", "--float"],
        input="10 ++ 5 - (6 * 9)",
        text=True,
        capture_output=True,
    )
    assert res.returncode != 0
    res = subprocess.run(
        ["build/app.exe", "--float"],
        input="10 + 5 - (6 ** 9)",
        text=True,
        capture_output=True,
    )
    assert res.returncode != 0
    res = subprocess.run(
        ["build/app.exe", "--float"],
        input="10 + 5 - (6 * 9) //3",
        text=True,
        capture_output=True,
    )
    assert res.returncode != 0


def test_wrong_operand_operator_amount():
    res = subprocess.run(
        ["build/app.exe", "--float"], input="3 0", text=True, capture_output=True
    )
    assert res.returncode != 0

def test_operation_order():
    res = subprocess.run(
        ["build/app.exe", "--float"], input="+ 3 0", text=True, capture_output=True
    )
    assert res.returncode != 0

    res = subprocess.run(
        ["build/app.exe", "--float"], input="3 0 +", text=True, capture_output=True
    )
    assert res.returncode != 0

    res = subprocess.run(
        ["build/app.exe", "--float"], input="3 0 + 0 *", text=True, capture_output=True
    )
    assert res.returncode != 0

def test_tricky_operation_order():
    res = subprocess.run(
        ["build/app.exe", "--float"], input="(3) (0)+", text=True, capture_output=True
    )
    assert res.returncode != 0

def test_braces():
    res = subprocess.run(
        ["build/app.exe", "--float"], input="3) + (0", text=True, capture_output=True
    )
    assert res.returncode != 0
