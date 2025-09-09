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

def productos_medios(seed1: int, seed2: int, n_dig: int, cantidad: int):
    x_prev, x = seed1, seed2
    rows = []
    for i in range(1, cantidad+1):
        y = x_prev * x
        x_next = middle_digits(y, n_dig)
        r = normalize(x_next, n_dig)
        rows.append((i, y, x_next, float(r)))
        x_prev, x = x, x_next
    return rows
