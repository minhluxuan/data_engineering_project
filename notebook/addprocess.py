import csv


def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read the header
        header = next(reader)
        # Remove the "edition" column (3rd column)
        header = header[:2] + header[3:]
        writer.writerow(header)

        # Process each row
        for row in reader:
            # Remove the "edition" column (3rd column)
            row = row[:2] + row[3:]
            # Change isTeamSport from 'False' to '0' and 'True' to '1'
            if row[-1].lower() == 'false':
                row[-1] = '0'
            elif row[-1].lower() == 'true':
                row[-1] = '1'
            writer.writerow(row)


# Define input and output file paths
input_file = 'E:\\data_engineering_project\\data\\processed\\Result.csv'
output_file = 'E:\\data_engineering_project\\data\\processed\\Result_processed.csv'

# Call the function to process the CSV
process_csv(input_file, output_file)
