import mysql.connector
import csv

# Connect to the database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='do_an'
)


def import_first_data_row():
    cursor = conn.cursor()
    with open('E:\\data_engineering_project\\data\\processed\\Olympic_Event_Results.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        first_row = next(reader)  # Read the first data row
        print(first_row[12])

        # Skip the "edition" column (3rd column)
        first_row = first_row[:2] + first_row[3:]

        # Validate and handle date columns
        start_date = first_row[10] if first_row[10] else None
        end_date = first_row[11] if first_row[11] else None

        # Ensure the row has the correct number of elements
        if len(first_row) != 12:
            print(f"Skipping row with incorrect number of elements: {
                  first_row}")
        else:
            try:
                cursor.execute(
                    "INSERT INTO competition_result (result_id, event_title, edition_id_id, sport, sport_url, result_location, result_participants, result_format, result_detail, result_description, start_date, end_date, result_countries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (first_row[0], first_row[1], first_row[2], first_row[3], first_row[4], first_row[5], first_row[6],
                     first_row[7], first_row[8], first_row[9], start_date, end_date, first_row[12])
                )
            except mysql.connector.errors.IntegrityError as e:
                print(f"Error inserting row {first_row}: {e}")
            except mysql.connector.errors.DataError as e:
                print(f"Data error in row {first_row}: {e}")

    conn.commit()
    cursor.close()


def import_data():
    cursor = conn.cursor()
    with open('E:\\data_engineering_project\\data\\processed\\Olympic_Event_Results.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            # Skip the "edition" column (3rd column)
            row = row[:2] + row[3:]

            # Validate and handle date columns
            start_date = row[10] if row[10] else None
            end_date = row[11] if row[11] else None

            # Ensure the row has the correct number of elements
            if len(row) != 13:
                print(f"Skipping row with incorrect number of elements: {row}")
                continue

            try:
                cursor.execute(
                    "INSERT INTO competition_result (result_id, event_title, edition_id_id, sport, sport_url, result_location, result_participants, result_format, result_detail, result_description, start_date, end_date, result_countries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                     row[7], row[8], row[9], start_date, end_date, row[12])
                )
            except mysql.connector.errors.IntegrityError as e:
                print(f"Error inserting row {row}: {e}")
            except mysql.connector.errors.DataError as e:
                print(f"Data error in row {row}: {e}")
    conn.commit()
    cursor.close()


# Call the function to import data
import_first_data_row()

# Close the connection
conn.close()
