import csv

def parse(csv_file):
    csv_file2 = csv_file.split('.')[0]+'_2'+'.csv'
    writer = csv.writer(open(csv_file2, 'w'))
    with open(csv_file) as csvfile:
        normal1 = csv.reader(csvfile)
        for data in normal1:
            data = [d.lstrip('“').rstrip('”') for d in data]
            writer.writerow(data)

    csv_file3 = csv_file.split('.')[0]+'_3'+'.csv'
    writer = csv.writer(open(csv_file3, 'w'))
    with open(csv_file2) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        included_cols = [5, 6, 7, 9, 10, 11, 13, 14]
        for row in reader:
            content = list(row[i] for i in included_cols if i<len(row))
            writer.writerow(content)

    writer = csv.writer(open(csv_file.split('.')[0]+'_final'+'.csv', 'w'))
    with open(csv_file3) as csvfile:
        reader = csv.reader(csvfile)
        writer.writerow(['len', 'packet_id', 'flags', 'ttl', 'protocol', 'checksum', 'source_port', 'destination_port'])
        for row in reader:
            temp = []
            for i in range(8):
                if i < len(row):
                    if i == 2:
                        if ":" in row[i]:
                            x = -1
                        else:
                            y = row[i].split('=')
                            if 1 < len(y):
                                x = y[1]
                            else:
                                x = -1
                    elif i == 3:
                        if "ICMP" in row[i]:
                            x = -1
                        elif row[2] == -1:
                            x = -1
                        else:
                            y = row[i].split('=')
                            if 1 < len(y):
                                x = y[1]
                            else:
                                x = -1
                    elif i == 4:
                        if row[3] == -1:
                            x = -1
                        else:
                            y = row[i].split('=')
                            if 1 < len(y):
                                x = y[1]
                            else:
                                x = -1
                    elif i == 6:
                        y = row[i].split('=')
                        if 2 < len(y):
                            x = y[2]
                        else:
                            x = -1
                    elif i == 7:
                        if temp[3] == -1:
                            x = -1
                        else:
                            y = row[i].split('=')
                            if 1 < len(y):
                                x = y[1]
                            else:
                                x = -1
                    else:
                        y = row[i].split('=')
                        if 1 < len(y):
                            x = y[1]
                        else:
                            x = -1
                    temp.append(x)
            writer.writerow(temp)


def main():
    parse('normal_data/output1.csv')
    parse('normal_data/output2.csv')
    parse('normal_data/output3.csv')
    parse('normal_data/output4.csv')
    parse('normal_data/output5.csv')
    parse('attack_data/first_round.csv')
    parse('attack_data/second_round.csv')
    parse('attack_data/third_round.csv')


if __name__ == '__main__':
    main()
