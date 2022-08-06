import streamlit as st

def try_except(word,data):
  try:
    i = data.index(word)
  except ValueError:
    i = -1
  return i

def partial(n):
  d1 = ""
  d2 = ""
  if data[seq_i-n].find("-") != -1:
    ss_text = data[seq_i-n].split('-')
    n += 1
    for ss in ss_text:
      if ss.isdigit() == True:
        if d1 == "":
          d1 = ss
        elif d2 == "":
          d2 = ss
  return n,d1,d2

st.title('Bioxy')

# Text Input
# save the input text in the variable 'name'
# first argument shows the title of the text input box
# second argument displays a default text inside the text input area
result = ""
task = st.text_input("Enter Your Task", result)
 
# display the name when the submit button is clicked
# .title() is used to get the input text string
if(st.button('Submit')):
    data = task.split()
    hum_i = try_except('human',data)  # find/create antology of uniprot taxonomies
    seq_i = try_except('sequence',data) 
    prim_i = try_except('primers',data) #add primers -> cloning (look pydna)
    if hum_i != -1:
        tax = data[hum_i]
        if tax == 'human':
            tax_id = 9606
    if seq_i != -1:
        n,d1,d2 = partial(1)
        if data[seq_i-n].isupper() == True:
            st.success('gene_sequence')
