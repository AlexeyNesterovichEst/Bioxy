import streamlit as st

# make sidebar
# first
st.title("Documentation")
st.info("[compulsory] & (optional) parameters")
option = st.selectbox('Please choose the topic', ('Sequence', 'Primers', 'Restriction', 'Cloning'))

if option == "Sequence": # search by name, GenBank accession number
    c1 = st.container()
    c1.subheader("Gene sequence")
    c1.write("[taxon] [GENE NAME] (start-end) sequence")
    c1.markdown("*Example: human MAGEA10 1-10 sequence*")
    #c1.text("")
    #c1.write("[taxon] [Gene name] (start-end) gene sequence")
    #c1.markdown("*Example: human Dmbt1 1-100 gene sequence*")
    #c1.text("")
    c1.write("[GenBank accession number] (start-end) gene sequence")
    c1.markdown("*Example: NM_021048.5 1-10 gene sequence*")
    
 
    c2 = st.container()
    c2.subheader("Protein sequence")
    c2.write("[taxon] [Protein name] (start-end) protein sequence")
    c2.markdown("*Example: human Melanoma-associated antigen 10 1-10 protein sequence*")
    
    c2.write("[GenBank accession number] (start-end) protein sequence")
    c2.markdown("*Example: NP_066386.3 1-10 protein sequence*")
    
    
    #c3 = st.container()
    #c3.subheader("Gene coding sequence")
    #c3.write("[GenBank accession number] (start-end) gene coding sequence") # check start_end
    #c3.markdown("*Example: NM_021048.5 1-10 accession coding sequence*") 
    
    c4 = st.container()
    c4.subheader("Protein coding sequence")
    c4.write("[GenBank accession number] (start-end) protein coding sequence")
    c4.markdown("*Example: NP_066386.3 1-10 protein coding sequence*")

# develop [GenBank accession number] (start-end) primers
if option == "Primers":
    #c4 = st.container()
    #c4.subheader("Gene primers")
    #c4.write("[taxon] [GENE NAME] (start-end) primers")
    #c4.markdown("*Example: human DMBT1 1-100 primers*")
    
    c5 = st.container()
    c5.subheader("Protein coding sequence primers")
    c5.write("[GenBank accession number] (start-end) primers")
    c5.markdown("*Example: NP_066386.3 1-10 protein primers*")
    
    c6 = st.container()
    c6.subheader("Protein coding sequence primers with restriction sites")
    c6.write("[GenBank accession number] (start-end) primers with [restrictase 1] (and restrictase 2)")
    c6.markdown("*Example: NP_066386.3 1-10 protein primers with Acc65I and HindIII*")
    
if option == "Restriction":
    c7 = st.container()
    c7.subheader("Protein coding sequence all restrictases with sites")
    c7.write("[GenBank accession number] (start-end) protein restriction")
    c7.markdown("*Example: NP_066386.3 1-100 protein restriction*")
    
    c8 = st.container()
    c8.subheader("Protein coding sequence specific restrictases with sites")
    c8.write("[GenBank accession number] (start-end) protein restriction with (restrictase 1) , ... , (restrictase n)")
    c8.markdown("*Example: NP_066386.3 1-100 protein restriction with BseMII , UnbI*")
    
if option == "Cloning":
    st.info("In progress")
