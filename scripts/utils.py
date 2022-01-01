import csv 

def file_generator_csv(filename):
    with open(filename) as fh:
        read_data = csv.reader(fh)
        for row in read_data:
            yield(row)
    