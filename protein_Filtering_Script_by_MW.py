#import modules
import os
import time
import pandas as pd
import streamlit as st

initiating = time.process_time()

st.title("🧬FILTER PROTEIN SEQUENCES BY MOLECULAR WEIGHT🧬")
st.subheader('''
written_by: Zubair Hasan\n
**python_version: 3.10.12**\n
**script_version: 1.0.1**
''')

#input handling
st.sidebar.title('PARMETERS')
weight = st.sidebar.number_input('Enter Molecular Weight (e.g. 20000): ', 1,100000, step=1, value=20000, placeholder="Enter MW")
# length = st.sidebar.number_input('Enter Sequnce Length (e.g. 150): ', 0,1000000, step=1, value=150, placeholder="amino acid sequence length")
file_path = st.file_uploader("Enter file (e.g. .csv, .tsv or .txt files)", type=None)

clickRun = st.sidebar.button('Run', icon=":material/arrow_right:")

if clickRun == True and file_path is not None and weight != 0:
    #reading CSV file into dataframe
    seq_df = pd.read_csv(file_path, sep = '\t')
    #defining function for filtering SEQUENCES by MASS
    def filter_aaseq_MW(df_obj, weight_filter):
        #filtering operation
        filtered_col = df_obj.loc[df_obj["Mass"] < weight_filter, "Entry"]
        filtered_df = df_obj.loc[df_obj["Mass"] < weight_filter]
        #output screen and file handling
        st.write(f"Total Number of Filtered Proteins: {filtered_col.count()}\n")
        st.write(filtered_df[['Entry','Entry Name','Protein names','Organism','Length','Mass']])
        filtered_col.to_csv('output.txt', index = False, header = False)
        time.sleep(2)
        st.write("\nFile Exported!! ==>> output.txt\n")

    #datatype handling of the column Mass
    #check if Mass column is integer/float/string
    if (seq_df["Mass"].dtypes == int) or (seq_df["Mass"].dtypes == float):
        for mass_col in seq_df.columns:
            if mass_col in ["MASS", "mass", "Mass"]:
                st.info(f"\nDatatype of the {mass_col} Column: int/float")
                break
        #invoking the filter function
        filter_aaseq_MW(seq_df, weight)
    else:
        #converting Mass string data into integer
        seq_df["Mass"] = seq_df["Mass"].str.replace(",", "").astype(int)
        for mass_col in seq_df.columns:
            if mass_col in ["MASS", "mass", "Mass"]:
                st.info(f"\nDatatype of the {mass_col} Column: str ==>> converted into int")
                break
        filter_aaseq_MW(seq_df, weight)

    terminating = time.process_time()

    st.info(f"execution_time: {terminating - initiating} ms")

    with open("output.txt", "rb") as txt_file:
           st.download_button(
                 label="Download Output File",
                 data=txt_file,
                 file_name="output.txt",
                 mime="text/plain",
                 icon=":material/download:"
             )
elif clickRun == True and file_path is None:
    st.info("**Upload Your File Please!!**")
else:
    st.write("Filter Your Protein Sequences by Molecular Weight")
    
#invoking shell script to download fasta sequences
# os.system("bash retrieveUniProtSeq.sh")
# st.info("ran bash script successfully")
