#This script was created to do 1:1 testing of AI speech-to-text programs. Idea is to put in a CSV with the filepath information of transcript files to compare, use the jiwer module to test each pair of files, and then put the numbers out to a CSV.

import jiwer
from pathlib import Path
import pandas as pd
import os
import csv

def opencsv():
    #This prompts you to put in the file path for the CSV file containing the transcript files
    input_csv = input('Please enter path to CSV: ')
    file = open(input_csv, 'r', encoding='utf-8')
    csvin = csv.reader(file)
    next(csvin, None)
    return csvin

def compare_files():
    #This creates an empty dataframe to store the script output and open the CSV file you put in the file information for
    df_list = []
    csvfile = opencsv()
    for row in csvfile:
        fileR= row[0] #reference file
        fileH= row[1] #test file
        raw_reference = Path(fileR).read_text(encoding="utf-8")
        raw_hypothesis = Path(fileH).read_text(encoding="utf-8")

        #This does basic preprocessing for the reference transcripts.  
        strip_signal1 = jiwer.RemoveKaldiNonWords()(raw_reference) #removes any thing in brackets, as we use for things like actions or if something is inaudible
        strip_spaces1 = jiwer.RemoveMultipleSpaces()(strip_signal1) #removes any extra spaces
        strip_empty1 = jiwer.RemoveEmptyStrings()(strip_spaces1) #removes empty strings, but it's probably not necessary
        strip_newlines1 = jiwer.SubstituteRegexes({r"\n": r" "})(strip_empty1) #uses a regex pattern to remove new lines and replace with spaces
        strip_punc1 = jiwer.RemovePunctuation()(strip_newlines1) #removes punctuation
        reference = jiwer.ToLowerCase()(strip_punc1) #converts everything to lowercase. Note: note sure how that works with non-Latin scripts
        #next three functions are there in case you want to make it a list of words for some reason and make it a string again, but I didn't find a meaningful difference. Comment out the reference function above if you want to run the next three.
        #tolowercase1 = jiwer.ToLowerCase()(strip_punc1)
        #wordList1 = jiwer.ReduceToListOfListOfWords()(tolowercase1)
        #reference = str(wordList1)

        #This does the same basic preprocessing for the hypothesis transcripts. It doesn't include the bracket removal since raw transcripts won't have those.
        strip_spaces2 = jiwer.RemoveMultipleSpaces()(raw_hypothesis)
        strip_empty2 = jiwer.RemoveEmptyStrings()(strip_spaces2)
        strip_newlines2 = jiwer.SubstituteRegexes({r"\n": r" "})(strip_empty2)
        strip_punc2 = jiwer.RemovePunctuation()(strip_newlines2)
        hypothesis = jiwer.ToLowerCase()(strip_punc2)
        #tolowercase2 = jiwer.ToLowerCase()(strip_punc2)
        #wordList2 = jiwer.ReduceToListOfListOfWords()(tolowercase2)
        #hypothesis = str(wordList2)

        #This runs the jiwer processes for word error rate, match error rate, word information lost, and word information preserved    
        output = jiwer.process_words(reference, hypothesis)
        wer = output.wer
        mer = output.mer
        wil = output.wil
        wip = output.wip
        print(wer)
        print(mer)
        print(wil)
        print(wip)
      
        #This identifies the file names for the compared files using os, in order to populate the results csv
        identify_control = fileR
        control = os.path.basename(identify_control)
        identify_test = fileH
        test = os.path.basename(identify_test)

        #This makes the CSV output using pandas 
        analysis = {'control file': [control],
                    'test file': [test],
                    'word error rate': [wer],
                    'match error rate': [mer],
                    'word information loss': [wil],
                    'word preservation rate': [wip]}
        df = pd.DataFrame(analysis)
        df_list.append(df)
        result = pd.concat(df_list)
        result.to_csv('C:/Users/ct524/Documents/Transcripts/ComparisonTesting/generated/sonix_tested_2025-10-21_4.csv', encoding="utf-8")
        print(control,'Done!')

compare_files()
#Yay, it did a thing!
