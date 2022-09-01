import streamlit as st

import itertools

dna = "atgactgctaacccttccttggtgttgaacaagatcgacgacatttcgttcgaaacttacgatg"
DNA = dna.upper()
Reverse_DNA = DNA[::-1]
overhang_size = 4
overhang_parts = ["A","T", "G", "C"]
perm = itertools.product(overhang_parts, repeat=4)
num_seq = []

for i in list(perm):
    j = "".join(i)
    n = DNA.count(j)
    n_r = Reverse_DNA.count(j)
    a = [n+n_r,j]
    num_seq.append(a)
    #print(j,":",n+n_r,"(",n,"+",n_r,")")

num_seq.sort(key=lambda x: int(x[0]))
st.success(num_seq)

i = 0
r_min = 4
o_min = ""
while n == num_seq[0][0]:
  n = num_seq[i][0]
  m = num_seq[i][1]
  r0 = 0
  for o in overhang_parts:
    r = m.count(o)
    if r > r0:
      r0 = r
  if r_min > r0:
    r_min = r0
    o_min = num_seq[i][1]
  i += 1
