import csv
from utility.utility import empty_csv_file

def trim_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            trimmed_row = [field.strip() for field in row]
            writer.writerow(trimmed_row)


files = ['Project.csv','Teams.csv','Team Members.csv','Member Ratings.csv','DEI.csv','ESG.csv','Emails.csv']
for file in files:
    empty_csv_file('../TrimmedData/'+file)
    input_csv_file = '../RawData/'+file
    output_csv_file = '../TrimmedData/'+file
    trim_csv(input_csv_file, output_csv_file)
