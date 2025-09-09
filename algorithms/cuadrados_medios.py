def pad_to_even(s: str) -> str:
    return s if len(s) % 2 == 0 else '0' + s

def middle_digits(value: int, n: int) -> int:
    s = str(value)
    s = pad_to_even(s)
    target = 2 * n
    if len(s) < target:
        s = s.zfill(target)
    start = (len(s) - n) // 2
    return int(s[start:start+n])

def normalize(x: int, n: int) -> float:
    return x / (10 ** n)

def cuadrados_medios(seed: int, n_dig: int, cantidad: int):
    x = seed
    rows = []
    for i in range(1, cantidad+1):
        y = x * x
        x = middle_digits(y, n_dig)
        r = normalize(x, n_dig)
        rows.append((i, y, x, float(r)))
    return rows
