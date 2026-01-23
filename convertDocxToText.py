#Created to convert .docx files to .txt files. Idea is you put in a CSV file that has a filepath column with the paths to the .docx file and a output column with the filepath down to the output file, including extensions. Example CSV will be in the repository
import pypandoc
from pathlib import Path
import csv

def opencsv():
    #This prompts you to put in the file path for the CSV file containing the filepaths for transcript files
    input_csv = input('Please enter path to CSV: ')
    file = open(input_csv, 'r', encoding='utf-8')
    csvin = csv.reader(file)
    next(csvin, None)
    return csvin

def convert():
    csvfile = opencsv()
    for row in csvfile:
        filepath = row[0]
        output = row[1] 
        input = Path(filepath)
        pypandoc.convert_file(input, 'plain', outputfile=output)
        print(input," done")

convert()
