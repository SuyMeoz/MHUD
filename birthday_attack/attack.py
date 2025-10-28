import random
import time
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SHA1.sha1 import sha1

def fingerprint_k_bits(data_bytes, k):
    digest = sha1(data_bytes)
    int_digest = int.from_bytes(digest,'big')
    return int_digest >> (160 - k)

def birthday_trial(k, max_attempts=2000000):
    seen = dict()
    for i in range(max_attempts):
        s = random.randbytes(8)
        fp = fingerprint_k_bits(s, k)
        if fp in seen:
            return i + 1, seen[fp], s
        seen[fp] = s
    return None, None, None

def estimate_average_samples(k, trials=5):
    total = 0
    count = 0
    sample_list = []
    for _ in range(trials):
        t0 = time.time()
        res = birthday_trial(k)
        t1 = time.time()
        if res[0] is None:
            continue
        total += res[0]
        count += 1
        sample_list.append(res[0])
    return total / count if count > 0 else None, sample_list

ks = [16,18,20,22,24]
averages = []
for k in ks:
    print("Running trials for k =", k)
    avg, times = estimate_average_samples(k, trials=6)
    averages.append(avg)
    print("k = ", k, "avg samples to collision:", avg)

plt.figure(figsize=(8,5))
plt.plot(ks, averages, marker='o')
plt.yscale('log')
plt.xlabel('k (bits of fingerprint)')
plt.ylabel('Average samples to collision (log scale)')
plt.title('Birthday paradox: k-bit fingerprint vs samples to collision')
plt.grid(True)
plt.show()
