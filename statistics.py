# procedure definitions

import math

def mean(a):
    return float(sum(a)) / len(a)

def median(a):
    n = len(a)
    if n%2 is not 0: return quick_select(int(n/2+1),a)
    else: return (quick_select(int(n/2),a)+quick_select(int(n/2+1),a))/2.

def dev(a, m):
    return [x-m for x in a]

def adev(a, m):
    return [abs(x-m) for x in a]

def population_variance(a):
    return sum(map(lambda x: x**2, dev(a, mean(a)))) / len(a)

def sample_variance(a):
    return sum(map(lambda x: x**2, dev(a, mean(a)))) / (len(a) - 1)

def population_standard_deviation(a):
    return math.sqrt(population_variance(a))

def sample_standard_deviation(a):
    return math.sqrt(sample_variance(a))

def quick_select(k, a):
    n = len(a)
    if n <= 0 or k <= 0 or k > n: return None
    k -= 1
    left = 0
    right = n - 1
    idx = []
    for i in range(0, n): idx.append(i)
    while left < right:
        pivot = a[idx[k]]
        i = left
        j = right
        while True:
            while a[idx[i]] < pivot: i += 1
            while pivot < a[idx[j]]: j -= 1
            if i <= j:
                tmp = idx[i]
                idx[i] = idx[j]
                idx[j] = tmp
                i += 1
                j -= 1
            if i > j: break
        if j < k: left = i
        if k < i: right = j
    return a[idx[k]]

def median_deviation(a):
    return median(adev(a, median(a)))

def mean_deviation(a):
    return mean(adev(a, mean(a)))

def skewness(a):
    return sum(map(lambda x: x**3, dev(a, mean(a)))) / ((len(a) - 1) * sample_standard_deviation(a)**3)

def dot_product(x, y):
    return sum( map(lambda i, j: i*j, x, y) )
    
def covariance(x, y):
    n = min(len(x), len(y))
    dx = dev(x, mean(x))
    dy = dev(y, mean(y))
    return dot_product(dx, dy) / (n - 1)

def correlation_coefficient(x, y):
    return covariance(x, y) / (sample_standard_deviation(x) * sample_standard_deviation(y))
