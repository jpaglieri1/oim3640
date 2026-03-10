#Here is the work from session 14, practicing with data dictionaries

prices = {}

prices['APPL'] = 178.5
prices['GOOG'] = 141.8
prices['MSFT'] = 405.63

print(prices)


def histogram(s):
    d = {}
    for c in s:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1
    return d

print(histogram("jackie paglieri"))