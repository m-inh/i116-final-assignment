# -*- coding: utf-8 -*-
"""1st-method.ipynb

Student name: NGUYEN, Tien Minh
Student ID  : s1810445
Student mail: minh.nguyen@jaist.ac.jp
"""

import multiprocessing
from multiprocessing import Pool
import time
import math
import os

cache_fact = []

# Initialize cache_fact
for i in range(1000):
  cache_fact.append(-1)


def fact(n):
  """Calculate the factorial of a given number n

  Parameters
  ----------
  n: Int

  Returns
  -------
  factorial: Int
  """
  if n == 0:
    return 1

  if (cache_fact[n] != -1):
    return cache_fact[n]

  f = 1

  for i in range(1, n+1):
    f = f * i

  cache_fact[n] = f

  return f


def calculate_nck(n, k):
  """Calculate the total number of combinations of a given number n, k

  Parameters
  ----------
  n: Int

  k: Int

  Returns
  -------
  number_of_combinations: Int
  """
  if (n < k):
    return 0
  
  if n == 0: 
    return 0

  numerator = 1

  for i in range(n-k+1, n+1):
    numerator = numerator*i

  denominator = fact(k)

  return int(numerator / denominator)
  # return int(fact(n) / (fact(k) * fact(n-k)))



"""This section is for testing the utility functions
  
  The functions are tested:
  - fact
  - calculate_nck
"""
assert fact(4) == 24 
assert fact(1) == 1 
assert fact(0) == 1 

assert calculate_nck(5, 3) == 10
assert calculate_nck(5, 1) == 5
assert calculate_nck(5, 4) == 5
assert calculate_nck(0, 4) == 0

print("---------------------")
print("All tests are passed!")



def generate_combination(n, k, index):
  """Generate a combination of a given number n, k at given index

  Parameters
  ----------
  n: Int
  k: Int
  index: Int

  Returns
  -------
  combination: list(Int)
  """
  combination = list(range(k))

  # nck = calculate_nck(n, k)

  # m can be uniquely represented by a sum of binomials:
  #   (c_1 k) + (c_2 k-1) + ... + (c_k 1)
  # where 0 <= c_i < n.
  m = index

  # guess cannot exceed n-1, otherwise (guess k) exceeds the index range.
  guess = n-1

  for i in range(k):
    ri = k-i
    take = calculate_nck(guess, ri)
    while (take > m):
      guess = guess-1
      take = calculate_nck(guess, ri)
    
    m = m-take
    combination[i] = n-guess

  return combination



def generate_combinations_by_inteval(start_i, end_i, n, k):
  start = time.time()
  
  for i in range(start_i, end_i):
    generate_combination(n, k, i)
    # comb = generate_combination(n, k, i)
    # print(comb)
  
  end = time.time()
  print("time per core: ", end - start, "start_i: ", start_i, "end_i: ", end_i, "jobs: ", end_i - start_i)
  return (end - start, start_i, end_i, end_i - start_i)



def generate_combinations(n, k, cores):
  nck  = calculate_nck(n, k)
  jobs = nck

  jobs_per_core = math.floor(jobs/cores)

  inteval = []

  for i in range(cores):
    start = jobs_per_core * i
    end   = jobs_per_core * (i+1)
    inteval.append((start, end))

  last_inteval = inteval.pop()
  inteval.append((last_inteval[0], last_inteval[1] + (jobs%cores)))

  # Generate all combinations in Parallel
  pool = Pool(processes=cores)
  multiple_results = [pool.apply_async(generate_combinations_by_inteval, (i[0], i[1], n, k)) for i in inteval]
  
  return [res.get() for res in multiple_results]



def search_a_combination(n, k, index):
  return generate_combination(n, k, index)



def conduct_experiments(n, k, num_cores):
  nck = calculate_nck(n, k)

  # experiment generate-function
  start_gen = time.time()
  generate_combinations(n, k, num_cores)
  end_gen   = time.time()
  total_gen = end_gen - start_gen

  print("--------------------------")
  print("2nd_method: generate")
  print("n:            ", n)
  print("k:            ", k)
  print("combinations: ", nck)
  print("num_cores:    ", num_cores)
  print("total time:   ", total_gen)
  print("--------------------------")

  return total_gen

  # search
  # result_se = []
  
  # for i in range(nck):
  #   start_se = time.time()
  #   search_a_combination(n, k, i)
  #   end_se   = time.time()
    
  #   total_se = end_se - start_se
  #   result_se.append(total_se)

  # print("--------------------------")
  # print("1st_method: search")
  # print("n:            ", n)
  # print("k:            ", k)
  # print("combinations: ", nck)
  # print("num_cores:    ", num_cores)
  # print("average time: ", sum(result_se) / len(result_se))



"""This section is for experiment

  The functions are tested:
  - conduct_experiments
  - generate_combinations
"""

# For experiment
# nks   = [(36, 8), (45, 9), (55, 10), (66, 11), (78, 12)]
# nks = [(28, 8), (29, 8), (30, 8), (31, 8), (32, 8), (33, 8), (34, 8), (35, 8), (36, 8), (37, 8)]
# cores = [8, 16, 30]


# For test only
nks = [(5,3), (6,3), (7,3)]
cores = [1, 2, 4, 8]

max_cores = multiprocessing.cpu_count()

results = []

for nk in nks:
  for core in cores:
    if core <= max_cores:
      total_time = conduct_experiments(nk[0], nk[1], core)
      results.append([nk[0], nk[1], calculate_nck(nk[0], nk[1]), core, total_time])

# Print csv
headers = ["n", "k", "combinations", "cores", "total_time"]
print(",".join(headers))

for r in results:
  rs = []
  # Stringify
  for i in r:
    rs.append(str(i))
  print(",".join(rs))

print("------------------------------")
print("DONE!")