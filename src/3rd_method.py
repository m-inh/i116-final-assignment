# -*- coding: utf-8 -*-
"""1st-method.ipynb

Student name: NGUYEN, Tien Minh
Student ID  : s1810445
Student mail: minh.nguyen@jaist.ac.jp
"""

from multiprocessing import Pool
import time
import math
import os

# cache_fact = []

# Initialize cache_fact
# for i in range(1000):
#   cache_fact.append(-1)


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

  # if (cache_fact[n] != -1):
  #   return cache_fact[n]

  f = 1

  for i in range(1, n+1):
    f = f * i

  # cache_fact[n] = f

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


def test_print():
  id = os.getpid()

  for i in range(100):
    print('test_print', i, id)


def generate_combinations_by_inteval(start_i, end_i, n, k):
  start = time.time()
  
  for i in range(start_i, end_i):
    comb = generate_combination(n, k, i)
    # print(comb)
  
  end = time.time()

  print("time per core: ", end - start, "start_i: ", start_i, "end_i: ", end_i, "jobs: ", end_i - start_i)

pool = Pool(processes=4)

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
  # Parallel(n_jobs=cores, 
  # # prefer="threads", 
  # # require='sharedmem'
  # )(delayed(generate_combinations_by_inteval)(i[0], i[1], n, k) for i in inteval)
  
  # for i in inteval:
  #   rs = pool.apply_async(generate_combinations_by_inteval, [i[0], i[1], n, k])
  #   chunk_combinations = rs.get()
    # print("chunk_combinations", chunk_combinations)
  multiple_results = [pool.apply_async(generate_combinations_by_inteval, (i[0], i[1], n, k)) for i in inteval]
  print([res.get() for res in multiple_results])
  # multiple_results = [pool.apply_async(test_print, []) for i in range(4)]
  # print([res.get(timeout=1) for res in multiple_results])



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
  print("--------------------------")

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
# cores = [8, 16, 32]

# nks = [(5,3)]
cores = [1, 2, 4, 8]

for nk in nks:
  for core in cores:
    conduct_experiments(nk[0], nk[1], core)

print("------------------------------")
print("DONE!")