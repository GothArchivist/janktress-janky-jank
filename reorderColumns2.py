# created for reordering columns in .tsv files. This is part of a workflow to fix transcriptth formatting in .docx documents. If you're wondering where .tsv files come into this...it's a long story.

import os
import pandas as pd

directory = '' #insert filepath
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):  # checking if it is a file
        if f.endswith('.txt'): #I left the extension on these as .txt, but you could do .tsv as well. Or even make this work for .csv!
            print(f) #Only have this here in case you want to check things.
            df = pd.read_table(f, sep='\t') #if you want to use a csv, leave off the sep='\t'. 
            print(df) #Same deal with checking things
            columnsTitles = ['timestamp', 'speaker', 'text'] #I'm using the names of the columns in the original document but in the order I want them to be in here. 
            df2 = df.reindex(columns=columnsTitles) #does the reorder
            print(df2) #same deal with checking things
            nd = '' #filepath of wherever the new documents should live
            nf = os.path.join(nd, filename)
            df2.to_csv(nf, sep='\t', index=False)
