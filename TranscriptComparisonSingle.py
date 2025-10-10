#This script was created to do 1:1 testing of AI speech-to-text programs. Idea is to put in a text file of an edited transcript, put in a text file of raw output from your program of choice, use the jiwer module to test the things, and then put the numbers out to a CSV.

import jiwer
from pathlib import Path
import pandas as pd
import os

#This gets the things to test using pathlib
reference = Path("C:/Users/ct524/Documents/Transcripts/ComparisonTesting/reference/mssa_hvt_16_p1of1_transcript_control.txt").read_text()
hypothesis = Path("C:/Users/ct524/Documents/Transcripts/ComparisonTesting/generated/mssa_hvt_16_p1of1_sonix.txt").read_text()

#This does the processing stats thing using jiwer
output = jiwer.process_words(reference, hypothesis)
wer = output.wer
mer = output.mer
wil = output.wil
error = jiwer.cer(reference, hypothesis)

#This allows me to see the results in the terminal
print("word error rate:",wer)
print("match error rate:",mer)
print("word information rate:",wil)
print("charecter error rate:",error)

#This identifies the filenames of the things I tested for the output CSV using os. This is probably way more clunky than it needs to be, but #teamMetadataJanktress
identify_control = "C:/Users/ct524/Documents/Transcripts/ComparisonTesting/reference/mssa_hvt_16_p1of1_transcript_control.txt"
control = os.path.basename(identify_control)
identify_test = "C:/Users/ct524/Documents/Transcripts/ComparisonTesting/generated/mssa_hvt_16_p1of1_sonix.txt"
test = os.path.basename(identify_test)

#This makes the CSV output using pandas!
analysis = {'control file': [control],
            'test file': [test],
            'word error rate': [wer],
            'match error rate': [mer],
            'word information rate': [wil],
            'charecter error rate': [error]}
df = pd.DataFrame(analysis)
df.to_csv('C:/Users/ct524/Documents/Transcripts/ComparisonTesting/analysis.csv')
print('Done')

#Congrats, it did a thing!


