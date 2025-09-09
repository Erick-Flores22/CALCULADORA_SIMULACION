import math, statistics as stats
from scipy.stats import chi2

Z_CRIT = {0.10: 1.6448536269514722, 0.05: 1.959963984540054, 0.01: 2.5758293035489004}
KS_C = {0.10: 1.22, 0.05: 1.36, 0.01: 1.63}

def prueba_medias(samples, alpha=0.05):
    n = len(samples)
    if n == 0:
        return 'NO HAY DATOS'
    mu = sum(samples)/n
    z = (mu - 0.5) / math.sqrt(1/(12*n))
    zc = Z_CRIT.get(alpha, Z_CRIT[0.05])
    ok = abs(z) <= zc
    return f"Prueba de Medias: {'ACEPTA' if ok else 'RECHAZA'} | Z={z:.4f} | Zc={zc:.4f} | media={mu:.4f}"

def prueba_varianza(samples, alpha=0.05):
    n = len(samples)
    if n < 2:
        return 'NO HAY DATOS'
    s2 = stats.variance(samples)
    sigma2 = 1/12
    k = n-1
    chi = k * s2 / sigma2
    low = chi2.ppf(alpha/2, k)
    high = chi2.ppf(1-alpha/2, k)
    ok = low <= chi <= high
    return f"Prueba de Varianza: {'ACEPTA' if ok else 'RECHAZA'} | chi2={chi:.4f} | rango=[{low:.4f},{high:.4f}]"

def prueba_uniformidad(samples, alpha=0.05):
    n = len(samples)
    if n == 0:
        return 'NO HAY DATOS'
    xs = sorted(samples)
    d_plus = max((i+1)/n - x for i, x in enumerate(xs))
    d_minus = max(x - i/n for i, x in enumerate(xs))
    d = max(d_plus, d_minus)
    c = KS_C.get(alpha, KS_C[0.05])
    dcrit = c / math.sqrt(n)
    ok = d <= dcrit
    return f"Prueba K-S: {'ACEPTA' if ok else 'RECHAZA'} | D={d:.4f} | Dcrit={dcrit:.4f}"
