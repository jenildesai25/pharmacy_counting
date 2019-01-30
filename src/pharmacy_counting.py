import sys

import sys
import csv
import os
from argparse import ArgumentParser
import math
import numbers

# Set up Global Variables
# Set up the static columns
columns_input = ['id', 'prescriber_last_name', 'prescriber_first_name', 'drug_name', 'drug_cost']
columns_output = ['drug_name', 'num_prescriber', 'total_cost']

# Set up the empty dict
drug_Cost_Dict = {}


# Read in the file line by line as dictionary labeled type
def csvRows(filename):
    with open(filename, 'r', newline='') as fi:
        reader = csv.DictReader(fi)
        for row in reader:
            yield row


# Check if the line is in proper format and take action if necessary. Look for outliers
def check_line(line):
    # Discovered one outliner with extra ',' in between
    # Check for outliner PANCRELIPASE 5,000
    # if line['drug_name'] == "PANCRELIPASE 5,000":
    #     print(line)
    #     print("Outlier!!! - Found PANCRELIPASE 5,000")
    #     sys.exit(1)

    # Check for missing value
    if len(set(columns_input) - line.keys()) != 0:
        print("Outlier!!! - There are missing fields in this line")
        sys.exit(1)

    if ('drug_name' not in line) or (not isinstance(line['drug_name'], str)):
        print("Outlier!!! - Missing drug_name or drug_name is not a string ")
        sys.exit(1)

    if ('prescriber_last_name' not in line) or (not isinstance(line['prescriber_last_name'], str)):
        print("Outlier!!! - Missing prescriber_last_name or prescriber_last_name is not a string ")
        sys.exit(1)

    if ('prescriber_first_name' not in line) or (not isinstance(line['prescriber_first_name'], str)):
        print("Outlier!!! - Missing prescriber_first_name or prescriber_first_name is not a string ")
        sys.exit(1)

    if ('drug_cost' not in line) or (not isinstance(float(line['drug_cost']), numbers.Number)):
        print("Outlier!!! - Missing drug_cost or drug_cost is not a number ")
        sys.exit(1)


def extract_line(line):
    return line['drug_name'], str(line['prescriber_last_name'] + " " + line['prescriber_first_name']), line['drug_cost']


def map_to_dict(dict, drug_name, prescriber, drug_cost):
    if drug_name in dict:
        dict[drug_name][1].add(prescriber)
        dict[drug_name][2] += math.ceil(float(drug_cost))

    else:
        dict.setdefault(drug_name, []).append(drug_name)
        dict.setdefault(drug_name, []).append({prescriber})
        dict.setdefault(drug_name, []).append(math.ceil(float(drug_cost)))


def write_outputFile(dict, outputFile):
    drug_Cost_List = dict.values()

    # Sorted the values by drug_cost(index 2) in descending order and drug_name(index 0) in alphabetical order
    sorted_drug_Cost_List = sorted(drug_Cost_List, key=lambda k: (-k[2], k[0]))

    with open(outputFile, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(columns_output)
        for line in sorted_drug_Cost_List:
            writer.writerow([line[0], str(len(line[1])), str(line[2])])

            # Output Row number should be 2750


# A wrapper function to run all the functions listed above
def output_top_cost_drug(inputFile, outputfile, dict):
    try:
        # input_file_directory = os.listdir("../input")
        # output_file_directory = os.listdir("../output")
        inputFile = os.path.abspath("{0}".format(inputFile))
        outputfile = os.path.abspath("{0}".format(outputfile))
        for line in csvRows(inputFile):
            check_line(line)
            drug_name, prescriber, drug_cost = extract_line(line)

            map_to_dict(dict, drug_name, prescriber, drug_cost)

        write_outputFile(dict, outputfile)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # input_file = input('please input file name that is in the input folder')
    # output_file = input('please output file name that is in the input folder')
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        output_top_cost_drug(input_file, output_file, drug_Cost_Dict)
    except Exception as e:
        print(e)