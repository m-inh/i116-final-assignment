# -*- coding: utf-8 -*-
"""1st-method.ipynb

Student name: NGUYEN, Tien Minh
Student ID  : s1810445
Student mail: minh.nguyen@jaist.ac.jp
"""

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


class Combination:
  """Represent a combination object

  Attributes
  ----------
  n: Int
  k: Int
  data: List(Int)
  """
  def __init__(self, n, k):
    self.n = n
    self.k = k
    self.data = list(range(1, k+1))


  def next(self):
    n = self.n
    k = self.k

    # If current is the last element -> return None
    if (self.data[0] == n+1-k):
      return None

    successor = Combination(n, k)
    successor.data = list(self.data)
    
    # Increase right-most element in the current combination that doesn't exceed maximum value of its position
    for i in range(k):
      ri = k-1-i
      if (self.data[ri] < n-i):
        successor.data[ri] += 1
        if (ri < k-1):
          for j in range(ri+1, k):
            successor.data[j] = successor.data[ri] + j - ri
        break
      
    return successor


  def __str__(self):
    return str(self.data)



def generate_combinations(n, k):
  nck          = calculate_nck(n, k)
  combination  = Combination(n, k)
  # combinations = []

  # Generate all combinations
  for _ in range(nck):
    # combinations.append(combination)
    combination = combination.next()



def search_a_combination(n, k, index):
  combination = Combination(n, k)
  nck         = calculate_nck(n, k)

  for i in range(nck):
    combination = combination.next()
    if (i == index):
      return combination
  
  return None



def conduct_experiments(n, k):
  nck = calculate_nck(n, k)

  # generate
  start_gen = time.time()
  generate_combinations(n, k)
  end_gen   = time.time()
  total_gen = end_gen - start_gen

  print("--------------------------")
  print("1st_method: generate")
  print("n:            ", n)
  print("k:            ", k)
  print("combinations: ", nck)
  print("total time:   ", total_gen)

  # search
  result_se = []

  for i in range(nck):
    start_se = time.time()
    search_a_combination(n, k, i)
    end_se   = time.time()
    total_se = end_se - start_se
    result_se.append(total_se)

  print("--------------------------")
  print("1st_method: search")
  print("n:            ", n)
  print("k:            ", k)
  print("combinations: ", nck)
  print("average time: ", sum(result_se) / len(result_se))




"""This section is for experiment

  The functions are tested:
  - generate_combinations
  - search_a_combination
"""

# nks = [(36, 8), (45, 9), (55, 10), (66, 11), (78, 12)]
nks = [(10, 3), (20, 5)]

for nk in nks:
  conduct_experiments(nk[0], nk[1])

print("------------------------------")
print("DONE!")