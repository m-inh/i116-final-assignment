# -*- coding: utf-8 -*-
"""1st-method.ipynb

Student name: NGUYEN, Tien Minh
Student ID  : s1810445
Student mail: minh.nguyen@jaist.ac.jp
"""

import multiprocessing
from joblib import Parallel, delayed
import time

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

  f = 1

  for i in range(1, n+1):
    f = f * i

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
  if n == 0: 
    return 0

  return int(fact(n) / (fact(k) * fact(n-k)))



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
  combination = []

  nck = calculate_nck(n, k)

  # m can be uniquely represented by a sum of binomials:
  #   (c_1 k) + (c_2 k-1) + ... + (c_k 1)
  # where 0 <= c_i < n.
  m = nck-1-index

  # guess cannot exceed n-1, otherwise (guess k) exceeds the index range.
  guess = n-1

  for i in range(k):
    ri = k-i
    take = calculate_nck(guess, ri)
    while (take > m):
      guess = guess-1
      take = calculate_nck(guess, ri)
    
    m = m-take
    combination.append(n-guess)

  return combination



def generate_combinations(n, k, num_cores):
  nck    = calculate_nck(n, k)
  inputs = range(nck)

  # Generate all combinations in Parallel
  Parallel(n_jobs=num_cores)(delayed(generate_combination)(n, k, i) for i in inputs)



def search_a_combination(n, k, index):
  return generate_combination(n, k, index)



def conduct_experiments(n, k, num_cores):
  nck = calculate_nck(n, k)

  # generate
  start_gen = time.time()
  generate_combinations(n, k, num_cores)
  end_gen   = time.time()
  total_gen = end_gen - start_gen

  print("--------------------------")
  print("1st_method: generate")
  print("n:            ", n)
  print("k:            ", k)
  print("combinations: ", nck)
  print("num_cores:    ", num_cores)
  print("total time:   ", total_gen)

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
  - generate_combinations
  - search_a_combination
"""

# nks   = [(36, 8), (45, 9), (55, 10), (66, 11), (78, 12)]
nks = [(20,8),(21,8),(22,8),(23,8),(24,8),(25,8),(26,8),(27,8),(28,8),(29,8),(30,8),(31,8),(32,8),(33,8),(34,8),(35,8),(36,8)]
cores = [8, 16, 32]

for nk in nks:
  for core in cores:
    conduct_experiments(nk[0], nk[1], core)

print("------------------------------")
print("DONE!")