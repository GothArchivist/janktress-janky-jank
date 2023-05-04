import os
import pandas as pd


#with os.scandir('C:\Users\ct524\Documents\Transcripts\NewUpload_2023-05-02\Transcripts\converted') as directory:
#    for item in directory:
#        df2 = df.iloc[:, [1,0,2]]
#        print(df2)

directory = 'C:/Users/ct524/Documents/Transcripts/NewUpload_2023-05-02/Transcripts/converted'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        if f.endswith('.txt'):
#            print(f)
#            col_names = ['speaker', 'timestamp', 'text']
            df = pd.read_table(f, sep='\t', skiprows=[0,1])
#            df = pd.read_table(f)
            print(df)
            columnsTitles = ['timestamp', 'speaker', 'text']
            df2 = df.reindex(columns=columnsTitles)
            print(df2)
            nd = 'C:/Users/ct524/Documents/Transcripts/NewUpload_2023-05-02/Transcripts/reformatted'
            nf = os.path.join(nd, filename)
            df2.to_csv(nf, sep='\t', index=False)
