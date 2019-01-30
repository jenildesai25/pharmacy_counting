# Reference taken from https://github.com/heng2j/InsightDataScience_Data_Eng_Coding_Challenge_pharmacy_counting.
import sys
import csv
import os
import math
import numbers


class PharmacyCounting(object):
    # Read in the file line by line as dictionary labeled type
    def load_file(self, filename):
        with open(filename, 'r', newline='') as fi:
            reader = csv.DictReader(fi)
            for row in reader:
                yield row

    # Check if the line is in proper format and take action if necessary. Look for outliers
    def check_line(self, line):
        # Check for missing value
        if len(set(columns_input) - line.keys()) != 0:
            print("There are missing fields in this line")
            sys.exit(1)

        if ('drug_name' not in line) or (not isinstance(line['drug_name'], str)):
            print("Missing drug_name or drug_name is not a string ")
            sys.exit(1)

        if ('prescriber_last_name' not in line) or (not isinstance(line['prescriber_last_name'], str)):
            print("Missing prescriber_last_name or prescriber_last_name is not a string ")
            sys.exit(1)

        if ('prescriber_first_name' not in line) or (not isinstance(line['prescriber_first_name'], str)):
            print("Missing prescriber_first_name or prescriber_first_name is not a string ")
            sys.exit(1)

        if ('drug_cost' not in line) or (not isinstance(float(line['drug_cost']), numbers.Number)):
            print("Missing drug_cost or drug_cost is not a number ")
            sys.exit(1)

    def extract_line(self, line):
        return line['drug_name'], str(line['prescriber_last_name'] + " " + line['prescriber_first_name']), line['drug_cost']

    def map_to_dict(self, container_of_data, drug_name, prescriber, drug_cost):
        if drug_name in container_of_data:
            container_of_data[drug_name][1].add(prescriber)
            container_of_data[drug_name][2] += math.ceil(float(drug_cost))

        else:
            container_of_data.setdefault(drug_name, []).append(drug_name)
            container_of_data.setdefault(drug_name, []).append({prescriber})
            container_of_data.setdefault(drug_name, []).append(math.ceil(float(drug_cost)))

    def write_output_file(self, temporary_container, output_file_path):
        drug_cost_list = temporary_container.values()

        # Sorted the values by drug_cost(index 2) in descending order and drug_name(index 0) in alphabetical order
        sorted_drug_cost_list = sorted(drug_cost_list, key=lambda k: (-k[2], k[0]))

        with open(output_file_path, 'w', newline='') as output_file_:
            writer = csv.writer(output_file_)
            writer.writerow(columns_output)
            for line in sorted_drug_cost_list:
                writer.writerow([line[0], str(len(line[1])), str(line[2])])

    # A wrapper function to run all the functions listed above
    def output_top_cost_drug(self, input_file_name, output_file_name, container):
        try:
            # input_file_directory = os.listdir("../input")
            # output_file_directory = os.listdir("../output")
            input_file_user_path = os.path.abspath("{0}".format(input_file_name))
            output_file_user_path = os.path.abspath("{0}".format(output_file_name))
            for line in self.load_file(input_file_user_path):
                self.check_line(line)
                drug_name, prescriber, drug_cost = self.extract_line(line)

                self.map_to_dict(container, drug_name, prescriber, drug_cost)

            self.write_output_file(container, output_file_user_path)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # input_file = input('please input file name that is in the input folder')
    # output_file = input('please output file name that is in the input folder')
    try:
        # global variables
        # static column names
        columns_input = ['id', 'prescriber_last_name', 'prescriber_first_name', 'drug_name', 'drug_cost']
        columns_output = ['drug_name', 'num_prescriber', 'total_cost']

        # Set up the empty dict
        drug_cost_dict = {}

        input_file = sys.argv[1]
        output_file = sys.argv[2]
        pharmacy_counting_object = PharmacyCounting()
        pharmacy_counting_object.output_top_cost_drug(input_file, output_file, drug_cost_dict)
    except Exception as e:
        print(e)
