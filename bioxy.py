import streamlit as st
import pydna
from Bio import Entrez, SeqIO
import requests, sys #
from pydna.dseqrecord import Dseqrecord
from pydna.seqrecord import SeqRecord
from pydna import tm
from pydna.design import primer_design
#from pydna.gel import gel
from pydna.ladders import GeneRuler_1kb
from Bio.Seq import Seq
from Bio.Restriction import *
import itertools



# combine gene and prot_term_query
# create interactive functions' graph and list functions by appearance in code
# add search by identifier and read from xml more accurate source
# NCBI as uniprot alternative
# Work on entities' synonyms
# Work on variables' systematics, definitions, classes (tax,gene), (tax,protein)
#import json

# DMBT1 primers with HindIII and Acc65I (default 55 c and 4 overhang))
# DMBT1 restriction with HindIII and Acc65I

# DMBT1 cloning to pQM with HindIII and Acc65I

# Then demo complete, expand by remaining in Colab version, create Bioxy graph

WEBSITE_API = "https://rest.uniprot.org"

def get_url(url, **kwargs):
  response = requests.get(url, **kwargs);

  if not response.ok:
    print(response.text)
    response.raise_for_status()
    sys.exit()

  return response

def try_except(word,data):
  try:
    i = data.index(word)
  except ValueError:
    i = -1
  return i

def partial(n,i):
  d1 = ""
  d2 = ""
  if data[i-n].find("-") != -1:
    ss_text = data[i-n].split('-')
    n += 1
    for ss in ss_text:
      if ss.isdigit() == True:
        if d1 == "":
          d1 = ss
        elif d2 == "":
          d2 = ss
  return n,d1,d2

def gene_term_quiry(tax,gene):
    a_tax = [["Homo sapiens","human"], ["Oryctolagus cuniculus","rabbit"],["Mus musculus", "mouse"]]
    gene_term = ""
    for i in a_tax:
        if i[0] == tax or i[1] == tax:
            tax_term = '(%s [Organism] OR %s [All Fields]) AND ' % (i[0],i[1])
            tax_sci = i[0]
            gene_term = tax_term + gene + "[All Fields] AND gene[All Fields]"# complete[All Fields]" # AND cds[All Fields]"
    return gene_term,tax_sci  

def gene_seq(gene_term,tax_sci,d1,d2,opt):
  Entrez.tool = 'Essequery'
  Entrez.email = ''
  h_search = Entrez.esearch(db="nucleotide", term=gene_term, retmax=20, sort = "relevance", api_key = "7c824eac4588c5996739d4a6c136c3f5d808")
  records = Entrez.read(h_search)
  h_search.close()
  identifiers = list(records['IdList'])
  #query_list = [] # (no synthetic-<synthetic) gene complete -> mRNA complete -> gene -> mRNA
  num = 0
  if len(identifiers) == 0:
      st.warning("NCBI first 20 results do not match")
      prot_plus = "+".join(prot)
      link = "https://www.ncbi.nlm.nih.gov/nuccore/?term=%s+%s" % (tax,prot_plus)
      html_string = '<a href="%s"><img alt="" src="https://serratus.io/ncbi.png" width="100" ></a>' % link
      st.markdown(html_string, unsafe_allow_html=True)
  for i in identifiers:
        percent = round(num/len(identifiers)*100)
        with st.spinner('Filtering NCBI nucleotide results (%s %%)' % percent):
            num += 1
            h_fetch = Entrez.efetch(db = 'nucleotide', id =i, rettype = 'gb', api_key = "7c824eac4588c5996739d4a6c136c3f5d808")
            recs = list(SeqIO.parse(h_fetch,'gb'))
            v = recs[0].description.lower()
            s = recs[0].seq
            source = "Genbank Accession no %s" % recs[0].id
            # (and ) or 
            # add d1 and d2 to expander names
            # add accession number to be easily copied or even added to input text area by button
            if opt == "seq":
                if v.find(tax_sci.lower()) != -1 and v.find(gene.lower()) != -1:
                      if d1 != "" and d2 != "":
                              s = s[int(d1):int(d2)+1]
                      with tab1:
                            with st.expander("%s (%s)" % (v,recs[0].id)):
                                html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                                st.markdown(html_string, unsafe_allow_html=True)
                                st.code(s)
                      with tab2:
                            with st.expander("%s (%s)" % (v,recs[0].id)):
                                html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                                st.markdown(html_string, unsafe_allow_html=True)
                                st.code(s)
                      with tab3:
                            exp_text = "%s %s sequence (%s)" % (tax_sci,data[seq_i-n],source)
                            with st.expander(exp_text):
                                st.code(s)     
                              # speed up by query_list[0] try to show up, more button
                              #query_list.append(recs)
            if opt == "cds":
                a_f = recs[0].features
                for f in a_f:
                    if f.type == "CDS":
                        s = f.location.extract(recs[0]).seq
                        if d1 != "" and d2 != "":
                              s = s[int(d1):int(d2)+1]
                        with tab1:
                              with st.expander("%s (%s)" % (v,recs[0].id)):
                                  html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                                  st.markdown(html_string, unsafe_allow_html=True)
                                  st.code(s)
                        with tab2:
                              with st.expander("%s (%s)" % (v,recs[0].id)):
                                  html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                                  st.markdown(html_string, unsafe_allow_html=True)
                                  st.code(s)
                        with tab3:
                              exp_text = "%s %s coding sequence (%s)" % (tax_sci,data[seq_i-n],source)
                              with st.expander(exp_text):
                                  st.code(s)   
                                # compare with "seq" opt if needed make one for both
                            #https://stackoverflow.com/questions/23333123/extracting-cds-sequences-in-biopython
            if opt == "acc":
                with tab1:
                      with st.expander("%s (%s)" % (v,recs[0].id)):
                          html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                          st.markdown(html_string, unsafe_allow_html=True)
                          st.code(s)
                with tab2:
                      with st.expander("%s (%s)" % (v,recs[0].id)):
                          html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                          st.markdown(html_string, unsafe_allow_html=True)
                          st.code(s)
                      with tab3:
                          exp_text = "%s %s sequence (%s)" % (tax_sci,data[seq_i-n],source)
                          with st.expander(exp_text):
                             st.code(s)  
            if opt == "prot_cds":
                a_f = recs[0].features
                for f in a_f:
                    if f.type == "CDS":
                        s = f.location.extract(recs[0]).seq
                        if d1 != "" and d2 != "":
                          if d1 == "1":
                             s = s[:(int(d2)*3)]
                          else:
                             s = s[((int(d1)-1)*3):(int(d2)*3)]
                        with tab1:
                              with st.expander("%s (%s)" % (v,recs[0].id)):
                                  html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                                  st.markdown(html_string, unsafe_allow_html=True)
                                  st.code(s)
                        with tab2:
                              with st.expander("%s (%s)" % (v,recs[0].id)):
                                  html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                                  st.markdown(html_string, unsafe_allow_html=True)
                                  st.code(s)
                        with tab3:
                              exp_text = "%s %s coding sequence (%s)" % (tax_sci,data[seq_i-n],source)
                              with st.expander(exp_text):
                                  st.code(s)
            if opt == "primer":
                a_f = recs[0].features
                for f in a_f:
                    if f.type == "CDS":
                        s = f.location.extract(recs[0]).seq
                        if d1 != "" and d2 != "":
                          if d1 == "1":
                             s = s[:(int(d2)*3)]
                          else:
                             s = s[((int(d1)-1)*3):(int(d2)*3)]
                        return s

def prot_term_query(tax,prot):
    a_tax = [["Homo sapiens","human"], ["Oryctolagus cuniculus","rabbit"],["Mus","Mus musculus", "mouse"]]
    prot_term = ""
    for i in a_tax:
        if i[0] == tax or i[1] == tax:
            #tax_term = '(%s [Organism] OR %s [All Fields]) AND ' % (i[0],i[1])
            tax_term = '(%s [Organism] OR %s [All Fields]) AND ' % (i[0],i[1])
            tax_sci = i[0]
            prot_term = tax_term + prot + "[Protein Name]"
    return prot_term,tax_sci  

def prot_gene():
    return

def prot_name(i,n):
    # prot_name between tax and i_start
    i_start = i
    # delete human from name (check human appearance in names, if yes check if prot starts from upper case)
    r_data = data[::-1]
    r_start = r_data.index(i)
    r_current = r_start
    r_finish = None
    #st.success(r_data[r_start+1:])
    for i in r_data[r_start+1:]:
        if i[0].isupper() == True:
          r_finish = r_current
          #st.success(i)
        elif i[0].isupper() == False and r_finish != None:
          #st.error(i)
          break
        r_current += 1
    #st.success("r_i and r_x")
    #st.success(r_i)
    #st.success(r_x)
    if i_start == "sequence" or i_start == "primers":
        r_protein = r_data[r_start+1:r_start+1+r_finish+1]
    elif i_start == "protein":
        r_protein = r_data[r_start+1:r_start+r_finish+1]
    #st.success(r_protein)
    prot = r_protein[::-1]
    return prot

def uniprot_seq(protein,tax_id):
  r = get_url(f"{WEBSITE_API}/uniprotkb/search?query=(protein_name:{protein}) AND (taxonomy_id:{tax_id})&fields=protein_name,gene_names,accession&size=1", headers={"Accept": "text/plain; format=fasta"})
  return r.text

def ncbiprot_seq(prot_term,tax_sci,d1,d2,opt): #optimise
  Entrez.tool = 'Essequery'
  Entrez.email = ''
  h_search = Entrez.esearch(db="protein", term=prot_term, retmax=20,sort = "relevance")
  records = Entrez.read(h_search)
  h_search.close()
  identifiers = list(records['IdList'])
  num = 0
  if len(identifiers) == 0:
      st.warning("NCBI first 20 results do not match")
      prot_plus = "+".join(prot)
      link = "https://www.ncbi.nlm.nih.gov/protein/?term=%s+%s" % (tax,prot_plus)
      html_string = '<a href="%s"><img alt="" src="https://serratus.io/ncbi.png" width="100" ></a>' % link
  for i in identifiers:
        percent = round(num/len(identifiers)*100)
        with st.spinner('Filtering NCBI protein results (%s %%)' % percent):
            num += 1
            h_fetch = Entrez.efetch(db = 'protein', id =i, rettype = 'gb')
            recs = list(SeqIO.parse(h_fetch,'gb'))
            v = recs[0].description.lower()
            s = recs[0].seq
            source = "Genbank Accession no %s" % recs[0].id
            if opt == "seq":
                if (v.find(tax_sci.lower()) != -1 or v.find(tax.lower()) != -1) and v.find(protein.lower()) != -1:
                    if d1 != "" and d2 != "":
                         s = s[int(d1):int(d2)+1]
                    with tab1:
                          with st.expander("%s (%s)" % (v,recs[0].id)):
                              html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                              st.markdown(html_string, unsafe_allow_html=True)
                              st.code(s)
                              st.code(recs[0].id)
                    with tab2:
                          with st.expander("%s (%s)" % (v,recs[0].id)):
                              html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                              st.markdown(html_string, unsafe_allow_html=True)
                              st.code(s)
                              st.code(recs[0].id)
                    with tab3:
                          exp_text = "%s %s sequence (%s)" % (tax_sci,protein,source)
                          with st.expander(exp_text):
                              st.code(s)
                              st.code(recs[0].id)
            elif opt == "cds":
                st.success("cds")
            elif opt == "acc":
                if d1 != "" and d2 != "":
                         s = s[int(d1):int(d2)+1]
                with tab1:
                      with st.expander("%s (%s)" % (v,recs[0].id)):
                          html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                          st.markdown(html_string, unsafe_allow_html=True)
                          st.code(s)
                with tab2:
                      with st.expander("%s (%s)" % (v,recs[0].id)):
                          html_string = '<a href="https://www.ncbi.nlm.nih.gov/nuccore/%s"><img alt="%s" src="https://serratus.io/ncbi.png" width="100" ></a>' % (i,recs[0].id)
                          st.markdown(html_string, unsafe_allow_html=True)
                          st.code(s)
                with tab3:
                      exp_text = "%s %s sequence (%s)" % (tax_sci,protein,source)
                      with st.expander(exp_text):
                          st.code(s)
            elif opt == "acc_cds":
                handle = Entrez.efetch(db="protein", id=recs[0].id,rettype="gb")
                seq_record = SeqIO.read(handle, "genbank")
                seqAnn = seq_record.annotations
                gene_acc = seqAnn['db_source'] #test different proteins
                gene_acc_split = gene_acc.split()
                gene_acc = gene_acc_split[-1]
                #n,d1,d2 = partial(2)
                #if d1 != -1:
                    #acc = data[seq_i-n] 
                #else:
                    #acc = data[seq_i-n-3] 
                     #s = s[((int(d1)-1)*3):(int(d2)*3)]
                gene_seq(gene_acc,"",d1,d2,"prot_cds") #acc_cds # d1,d2
            elif opt == "primer":
                handle = Entrez.efetch(db="protein", id=recs[0].id,rettype="gb")
                seq_record = SeqIO.read(handle, "genbank")
                seqAnn = seq_record.annotations
                gene_acc = seqAnn['db_source'] #test different proteins
                gene_acc_split = gene_acc.split()
                gene_acc = gene_acc_split[-1]
                dna = gene_seq(gene_acc,"",d1,d2,"primer")
                t=Dseqrecord(dna)
                ampl = primer_design(t, target_tm=55.0)
                if d1 != "" and d2 != "":
                    d1_d2 = d1 + "-" + d2
                else:
                    d1_d2 = ""
                with tab1:
                    st.code(ampl.forward_primer.seq)
                    st.code(ampl.reverse_primer.seq)
                with tab2:
                    st.success("%s %s %s sequence " % (tax,protein,d1_d2))
                    st.code(s)
                    #coding sequence
                    st.success("forward primer of %s %s %s" % (tax,protein,d1_d2)) # add temperature
                    st.code(ampl.forward_primer.seq)
                    st.success("reverse primer of %s %s %s" % (tax,protein,d1_d2)) # add temperature
                    st.code(ampl.reverse_primer.seq)
                with tab3:
                    st.code(ampl.forward_primer.seq)
                    st.code(ampl.reverse_primer.seq)
                    #st.write("%s %s coding gene is %s with coding sequence %s (UniProt Consortium, 2021; NCBI Resource Coordinators ,2016)." % (tax.capitalize(),recs[0].description,gene,s))
                    #st.write("%s %s (NCBI Resource Coordinators, 2016) primers are %s and %s." 
                             #% (tax.capitalize(),gene, ampl.forward_primer.seq, ampl.reverse_primer.seq))
            elif opt == "res_primer":
                handle = Entrez.efetch(db="protein", id=recs[0].id,rettype="gb")
                seq_record = SeqIO.read(handle, "genbank")
                seqAnn = seq_record.annotations
                gene_acc = seqAnn['db_source'] #test different proteins
                gene_acc_split = gene_acc.split()
                gene_acc = gene_acc_split[-1]
                dna = gene_seq(gene_acc,"",d1,d2,"primer")
                t=Dseqrecord(dna)
                ampl = primer_design(t, target_tm=55.0)
                and_i = try_except("and",data)
                if and_i != -1:
                    e1 = data[and_i+1]
                    e2 = data[and_i-1]
                else:
                    e1 = data[pri_i+2]
                    e2 = e1
                re_s = eval(e1+ ".site")
                fe_s = eval(e2+".site")
                rp_e = re_s + ampl.reverse_primer.seq
                fp_e = fe_s + ampl.forward_primer.seq
                st.success("forward primer with %s site" % e2)
                st.code(fp_e)
                st.success("reverse primer with %s site" % e1)
                st.code(rp_e)
            elif opt == "over_primer":
                handle = Entrez.efetch(db="protein", id=recs[0].id,rettype="gb")
                seq_record = SeqIO.read(handle, "genbank")
                seqAnn = seq_record.annotations
                gene_acc = seqAnn['db_source'] #test different proteins
                gene_acc_split = gene_acc.split()
                gene_acc = gene_acc_split[-1]
                dna = gene_seq(gene_acc,"",d1,d2,"primer")
                t=Dseqrecord(dna)
                ampl = primer_design(t, target_tm=55.0)
                and_i = try_except("and",data)
                if and_i != -1:
                    e1 = data[and_i+1]
                    e2 = data[and_i-1]
                else:
                    e1 = data[pri_i+2]
                    e2 = e1
                re_s = eval(e1+ ".site")
                fe_s = eval(e2+".site")
                DNA = dna.upper()
                st.success(DNA)
                Reverse_DNA = DNA[::-1]
                overhang_size = 4 # take from text
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
                nucl_n = 0
                st.success(num_seq[0])
                rp_e = re_s + ampl.reverse_primer.seq
                fp_e = fe_s + ampl.forward_primer.seq
                # 4 different and 4th different from first of rp_e and fp_e
                for i in num_seq: 
                    st.success(i[1])
                    for nucl in overhang_parts:
                        nucl_c = i[1].count(nucl)
                        if nucl_c > nucl_n:
                            nucl_n = nucl_c
                            st.success(nucl_n)
                    if nucl_n == 1:
                        overhang = i[1]
                        orp_e = overhang + re_s + ampl.reverse_primer.seq
                        ofp_e = overhang + fe_s + ampl.forward_primer.seq
                        st.success("forward primer with %s site" % e2)
                        st.code(fp_e)
                        st.success("reverse primer with %s site" % e1)
                        st.code(rp_e)
                        break
                    nucl_n = 0
            elif opt == "res_all" or opt =="res" or opt == "res_seq" or "res_gel":
                handle = Entrez.efetch(db="protein", id=recs[0].id,rettype="gb")
                seq_record = SeqIO.read(handle, "genbank")
                seqAnn = seq_record.annotations
                gene_acc = seqAnn['db_source'] #test different proteins
                gene_acc_split = gene_acc.split()
                gene_acc = gene_acc_split[-1]
                dna = gene_seq(gene_acc,"",d1,d2,"primer")
                t= Seq(dna)
                #check len(t)
                a_site = []
                #st.success(opt)
                if opt == "res" or opt == "res_seq" or opt == "res_gel":
                    wit_i = try_except("with",data)
                    com_i = try_except(",",data)
                    if com_i == -1:
                        rb = RestrictionBatch([data[wit_i+1]])
                    else:
                        rb = RestrictionBatch(' '.join(data[wit_i+1:]).split(","))
                    test = rb.search(t)
                    for a,b in test.items():
                        if opt == "res":
                            st.success("%s %s" %(a,b))
                        if opt == "res_seq" or "res_gel":
                            a_site.append(b)
                if opt == "res_all":
                    rb = AllEnzymes.search(t)
                    for a,b in rb.items():
                        if len(b) != 0:
                            st.success("%s %s" %(a,b))
                if len(a_site) != 0 and opt != "res_all":
                    # if circular (add)
                    # ...
                    # if linear 
                    a_site = list(itertools.chain.from_iterable(a_site))
                    a_site.sort()
                    site_0 = 1
                    a_at = []
                    a_att = []
                    for site_1 in a_site:
                        at = t[site_0-1:site_1-1]
                        a_at.append(at)
                        site_0 = site_1
                        att = Dseqrecord(at)
                        a_att.append(att)
                        if opt != "res_gel":
                            st.success(at)
                    at = t[site_1-1:]
                    a_at.append(at)
                    att = Dseqrecord(at)
                    a_att.append(att)
                    if opt != "res_gel":
                        st.success(at)
                        st.success(len(att))
                    #else:
                        #st.image(gel([GeneRuler_1kb,a_att]))
                     
def prot_gene_seq(protein,tax_id,tax):
  r = get_url(f"{WEBSITE_API}/uniprotkb/search?query=(protein_name:{protein}) AND (taxonomy_id:{tax_id})&fields=gene_names", headers={"Accept": "text/plain; format=tsv"})
  entities = r.text
  a_entity = entities.split('\n')
  a_gene = a_entity[1].split(' ')
  gene = a_gene[0] #optimize
  return gene

def primers():
    return

st.title('Essequery')
st.subheader('bioinformatics virtual assistant')

# Text Input
# save the input text in the variable 'name'
# first argument shows the title of the text input box
# second argument displays a default text inside the text input area
result = ""
task = st.text_input("Please enter the task", result)
 
# display the name when the submit button is clicked
# .title() is used to get the input text string
if(st.button('Submit')):
    #st.clean() find right word
    data = task.split()
    # list of words for try_except, logic, three first
    a_try_except = ['human','sequence','primers','for','restriction','gel', 'with']
    hum_i = try_except('human',data)  # find/create antology of uniprot taxonomies
    seq_i = try_except('sequence',data) 
    pri_i = try_except('primers',data) #add primers -> cloning (look pydna)
    for_i = try_except('for',data)
    res_i = try_except('restriction',data)
    gel_i = try_except('gel',data)
    wit_i = try_except('with',data)
    global tab1,tab2,tab3
    tab1, tab2, tab3 = st.tabs(["Result-only", "Step-by-step", "Article"])
    
    if hum_i != -1:
        tax = data[hum_i]
        if tax == 'human':
            tax_id = 9606
    else:
        tax = 'human'
        tax_id = 9606
    if seq_i != -1 and res_i == -1:
        n,d1,d2 = partial(1,seq_i)
        if data[seq_i-n] == "gene":
            if hum_i == -1:
                n,d1,d2 = partial(2,seq_i)
                if d1 != -1:
                    acc = data[seq_i-n] 
                else:
                    acc = data[seq_i-n-3] 
                gene = ""
                gene_seq(acc,"",d1,d2,"acc")
            else:
               st.success("gene sequence")
               #look below and apply
        if data[seq_i-n].isupper() == True: #  
            gene = data[seq_i-n]
            gene_term,tax_sci = gene_term_quiry(tax,gene)
            gene_seq(gene_term,tax_sci,d1,d2,"seq")
        elif data[seq_i-1] == "coding":
            n,d1,d2 = partial(3,seq_i)
            if data[seq_i-2] == "gene":
                gene = ""
                gene_seq(data[seq_i-n],"",d1,d2,"cds")
            elif data[seq_i-2] == "protein": 
                protein = data[0]
                ncbiprot_seq(protein,"",d1,d2,"acc_cds")
                
        elif data[seq_i-n] == "product":
            n,d1,d2 = partial(2)
            st.success('gene_prot_seq')
            
        elif data[seq_i-1] == "plasmid":
            n,d1,d2 = partial(2,seq_i)
            st.success('plasmid_seq')
            
        else: # check d1 to be [0] instead of [1] if 1
            n,d1,d2 = partial(2,seq_i)
            if hum_i == -1:
                protein = data[0] 
                ncbiprot_seq(protein,"",d1,d2,"acc")  
            else:
                #combine prot_name and prot_term_query
                prot = prot_name("protein",3)
                prot_s = ' '.join(prot)
                if d1 != "" and d2 != "":
                  prot = prot[:-1]
                protein = ' '.join(prot)
                prot_term,tax_sci = prot_term_query(tax,protein)
                ncbiprot_seq(prot_term,tax_sci,d1,d2,"seq")
    elif pri_i != -1: 
        n,d1,d2 = partial(2,seq_i)
        if  data[pri_i-1] == "protein":
            protein = data[0]
            if data[pri_i] == data[-1]:
                ncbiprot_seq(protein,"",d1,d2,"primer") 
            elif data[-1] == "overhang":
                # option of custom size and custom aminoacids
                ncbiprot_seq(protein,"",d1,d2,"over_primer")
                # work on over_primer
            elif data[pri_i+1] == "with":
                ncbiprot_seq(protein,"",d1,d2,"res_primer")
        # add overhang    
        elif data[pri_i-1] == "gene":
            st.success("gene primers")
    elif res_i != -1:
        n,d1,d2 = partial(2,res_i)
        if data[res_i-1] == "protein":
            protein = data[0]
        if seq_i == -1:
            #if gel_i != -1:
                #if wit_i == -1 or wit_i == len(data) -1:
                    #st.warning("please add restrictases")
                #else:
                    #ncbiprot_seq(protein,"",d1,d2,"res_gel")
            else:
                if res_i == len(data)-1:
                    ncbiprot_seq(protein,"",d1,d2,"res_all") #make in alphabetic order
                else:
                    ncbiprot_seq(protein,"",d1,d2,"res")
        elif seq_i != -1:
            if wit_i == -1 or wit_i == len(data) -1:
                st.warning("please add restrictases")
            else:
                ncbiprot_seq(protein,"",d1,d2,"res_seq")
    else:
        st.error("No result")
