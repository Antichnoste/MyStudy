from collections import Counter
from scipy.stats import chi2
from decimal import Decimal, getcontext


def pi_digits_after_decimal(count: int) -> str:
	"""Return `count` digits of pi after the decimal point."""
	if count <= 0:
		return ""

	# Keep a small safety margin in precision to avoid rounding artifacts.
	getcontext().prec = count + 20

	c = 426880 * Decimal(10005).sqrt()
	s = Decimal(0)

	m = 1
	l = 13591409
	x = 1
	k = 6

	# Number of terms required by Chudnovsky formula.
	terms = count // 14 + 2
	for n in range(terms):
		if n > 0:
			m = (m * (k**3 - 16 * k)) // (n**3)
			l += 545140134
			x *= -262537412640768000
			k += 12

		s += Decimal(m * l) / Decimal(x)

	pi_value = c / s
	pi_str = format(pi_value, "f")

	if "." not in pi_str:
		return "0" * count

	fractional = pi_str.split(".", maxsplit=1)[1]
	return fractional[:count].ljust(count, "0")


def count_pi_digits(count: int = 10_000) -> dict[str, int]:
	digits = pi_digits_after_decimal(count)
	freq = Counter(digits)
	return {str(d): freq.get(str(d), 0) for d in range(10)}


if __name__ == "__main__":
	n = 10_000_000
	result = count_pi_digits(n)

	print(f"Первые {n} цифр после запятой в числе pi:")
	for d, cnt in result.items():
		print(f"{d}: {cnt}")
	print(f"Итого: {sum(result.values())}")

	sum_hi = 0
	for d, cnt in result.items():
		sum_hi += ((cnt - n * 0.1)**2 / (n * 0.1))

	print(f"Сумма для критерия хи-квадрат: {sum_hi}")
	
	print(f"Лучшее альфа для нашей задачи: {chi2.sf(sum_hi, df=9)}")


