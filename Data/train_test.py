import csv
import numpy as np
import random
import math

def split(csv_file, train, test):
    # set with all line numbers you pulled vs set with all lines
    lines = -1
    with open(csv_file) as csvfile:
        lines = len(csvfile.readlines())
    # stores train file lines
    train_lines = set()
    while train_lines.__len__() != int((lines * train)):
        with open(csv_file) as csvfile:
            data = csv.reader(csvfile)
            for line in range(1, lines):
                if train_lines.__len__() == int((lines * train)):
                    break
                choice = round(random.randint(0, 1))
                if choice == 1:
                    train_lines.add(line)
    test_lines = set(i for i in range(1, lines))
    test_lines.difference_update(train_lines)
    if test_lines.__len__() == math.floor(lines * test):
        writer_train = csv.writer(open('train.csv', 'w'))
        writer_test = csv.writer(open('test.csv', 'w'))
        with open(csv_file) as csvfile:
            writer_train.writerow(
                ['len', 'packet_id', 'flags', 'ttl', 'protocol', 'checksum', 'source_port', 'destination_port', 'test'])
            writer_test.writerow(
                ['len', 'packet_id', 'flags', 'ttl', 'protocol', 'checksum', 'source_port', 'destination_port', 'test'])
            data = csv.reader(csvfile)
            curr_line = 0
            for line in data:
                if train_lines.__contains__(curr_line):
                    writer_train.writerow(line)
                if test_lines.__contains__(curr_line):
                    writer_test.writerow(line)
                curr_line += 1
    else:
        print("created incorrectly")


def main():
    split('/Users/Laura/Desktop/IntelligentIDS/Data/combined_data_normalized.csv', 0.7, 0.3)

if __name__ == '__main__':
    main()