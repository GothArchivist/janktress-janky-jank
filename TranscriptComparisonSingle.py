#This script was created to do 1:1 testing of AI speech-to-text programs. Idea is to put in a text file of an edited transcript, put in a text file of raw output from your program of choice, use the jiwer module to test the things, and then put the numbers out to a CSV.

import jiwer
from pathlib import Path
import pandas as pd
import os

#This gets the things to test using pathlib
def compareTranscripts():
    raw_reference = Path("/path/to/file").read_text(encoding="utf-8") #put the file paths in the quotation marks
    raw_hypothesis = Path("/path/to/file").read_text(encoding="utf-8")
    #This does preprocessing for the reference transcripts  
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

    #This does the same preprocessing for the hypothesis transcripts. It doesn't include the bracket removal since raw transcripts won't have those.
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
    
    #This prints that output in the terminal for those who like immediate gratification. Feel free to comment it out if you don't care
    print("word error rate:",wer)
    print("match error rate:",mer)
    print("word information loss:",wil)
    print("word information preserved:",wip)

    #This identifies the file names for the compared files using os, in order to populate the results csv. Use the same raw_reference path for control, raw_hypothesis for test
    identify_control = "/path/to/file"
    control = os.path.basename(identify_control)
    identify_test = "/path/to/file"
    test = os.path.basename(identify_test)

    #This makes the CSV output using pandas
    analysis = {'control file': [control],
                'test file': [test],
                'word error rate': [wer],
                'match error rate': [mer],
                'word information loss': [wil],
                'word information preserved': [wip]}
    df = pd.DataFrame(analysis)
    df.to_csv('/path/to/file') #input the file path for the CSV you're creating with the output.
    print('Done')

compareTranscripts()
    
#Congrats, it did a thing!

