import mysql.connector
import csv

# Connect to the database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='nhannt',
    database='doan'
)


# def import_first_data_row():
#     cursor = conn.cursor()
#     with open('C:\\Users\\ADMIN\\Documents\\CO3127\\data_engineering_project\\data\\processed\\Olympic_Event_Results.csv', 'r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         header = next(reader)  # Read the header row
#         first_row = next(reader)  # Read the first data row
#         print(first_row[12])

#         # Skip the "edition" column (3rd column)
#         first_row = first_row[:2] + first_row[3:]

#         # Validate and handle date columns
#         start_date = first_row[10] if first_row[10] else None
#         end_date = first_row[11] if first_row[11] else None

#         # Ensure the row has the correct number of elements
#         if len(first_row) != 12:
#             print(f"Skipping row with incorrect number of elements: {first_row}")
#         else:
#             try:
#                 cursor.execute(
#                     "INSERT INTO competition_result (result_id, event_title, edition_id_id, sport, sport_url, result_location, result_participants, result_format, result_detail, result_description, start_date, end_date, result_countries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                     (first_row[0], first_row[1], first_row[2], first_row[3], first_row[4], first_row[5], first_row[6],
#                      first_row[7], first_row[8], first_row[9], start_date, end_date, first_row[12])
#                 )
#             except mysql.connector.errors.IntegrityError as e:
#                 print(f"Error inserting row {first_row}: {e}")
#             except mysql.connector.errors.DataError as e:
#                 print(f"Data error in row {first_row}: {e}")

#     conn.commit()
#     cursor.close()


def import_data():
    cursor = conn.cursor()
    with open('C:\\Users\\ADMIN\\Documents\\CO3127\\data_engineering_project\\data\\processed\\Result_processed.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            # Skip the "edition" column (3rd column)
            # row = row[:2] + row[3:]

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

def import_data_EventResult():
    cursor = conn.cursor()

    with open('C:\\Users\\ADMIN\\Documents\\CO3127\\data_engineering_project\\data\\processed\\Olympic_Athlete_Event_Result_processed.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Bỏ qua dòng tiêu đề

        for row in reader:
            # Kiểm tra số lượng trường trong dòng dữ liệu
            if len(row) != 10:  # Nếu không có đủ 10 trường, bỏ qua dòng này
                print(f"Skipping row with incorrect number of elements: {row}")
                continue

            # Xử lý giá trị boolean cho trường 'isTeamSport'
            isTeamSport1 = 1 if row[9].strip().lower() == 'true' else 0

            # Lấy các giá trị từ dòng CSV
            edition_id = row[1]
            result_id = row[5]
            athlete_id = row[7]
            pos = row[8]
            is_team_sport = isTeamSport1

            try:
                # Kiểm tra xem result_id có tồn tại trong bảng 'competition_result'
                cursor.execute("SELECT COUNT(*) FROM competition_result WHERE result_id = %s", (result_id,))
                result_exists = cursor.fetchone()[0]

                # Nếu result_id không tồn tại, thêm mới vào bảng competition_result
                if result_exists == 0:
                    cursor.execute(
                        "INSERT INTO competition_result (result_id, event_title, sport, edition_id_id) VALUES (%s, %s, %s, %s)",
                        (result_id, row[3], row[2], edition_id),
                    )
                    print(f"Inserted new result record with result_id: {result_id}")

                    # Cập nhật trường result_participants cho result_id vừa thêm
                    cursor.execute(
                        "UPDATE competition_result SET result_participants = result_participants + 1 WHERE result_id = %s",
                        (result_id,)
                    )
                    print(f"Updated result_participants for result_id: {result_id}")
                
                cursor.execute("SELECT COUNT(*) FROM athlete_athlete_bio WHERE athlete_id = %s", (athlete_id,))
                athlete_exists = cursor.fetchone()[0]

                # Nếu athlete_id không tồn tại, bạn có thể thêm một bản ghi vào bảng athlete_bio
                if athlete_exists == 0:
                    cursor.execute("SELECT AVG(height) FROM athlete_athlete_bio WHERE country_noc_id = %s", (row[2],))
                    avg_height = cursor.fetchone()[0]
                    cursor.execute("SELECT AVG(weight) FROM athlete_athlete_bio WHERE country_noc_id = %s", (row[2],))
                    avg_weight = cursor.fetchone()[0]
                    cursor.execute(
                        "INSERT INTO athlete_athlete_bio (athlete_id, name, height, weight, country_noc_id) VALUES (%s, %s, %s, %s, %s)",
                        (athlete_id, row[6], avg_height, avg_weight, row[2],)
                    )
                    print(f"Inserted new athlete record with athlete_id: {athlete_id}")

                # Chèn dữ liệu vào bảng competition_eventresult
                cursor.execute(
                    """
                    INSERT INTO competition_eventresult (edition_id_id, result_id_id, athlete_id_id, pos, isTeamSport)
                    VALUES (%s, %s, %s, %s, %s)
                    """, 
                    (edition_id, result_id, athlete_id, pos, is_team_sport)
                )

            except mysql.connector.errors.IntegrityError as e:
                print(f"IntegrityError while inserting row {row}: {e}")
            except mysql.connector.errors.DataError as e:
                print(f"DataError in row {row}: {e}")
            except Exception as e:
                print(f"Unexpected error in row {row}: {e}")

    # Commit các thay đổi vào cơ sở dữ liệu và đóng kết nối
    conn.commit()
    cursor.close()
    
def import_data_MedalResult():
    cursor = conn.cursor()

    with open('C:\\Users\\ADMIN\\Documents\\CO3127\\data_engineering_project\\data\\processed\\Olympic_Athlete_Medal_Result_processed.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Bỏ qua dòng tiêu đề

        for row in reader:
            # Kiểm tra số lượng trường trong dòng dữ liệu
            if len(row) != 5:  # Nếu không có đủ 10 trường, bỏ qua dòng này
                print(f"Skipping row with incorrect number of elements: {row}")
                continue

            # Lấy các giá trị từ dòng CSV
            edition_id = row[0]
            result_id = row[2]
            athlete_id = row[3]
            medal = row[4]

            try:
                # Chèn dữ liệu vào bảng competition_medalresult
                cursor.execute(
                    """
                    INSERT INTO competition_medalresult (edition_id_id, result_id_id, athlete_id_id, medal)
                    VALUES (%s, %s, %s, %s)
                    """, 
                    (edition_id, result_id, athlete_id, medal)
                )

            except mysql.connector.errors.IntegrityError as e:
                print(f"IntegrityError while inserting row {row}: {e}")
            except mysql.connector.errors.DataError as e:
                print(f"DataError in row {row}: {e}")
            except Exception as e:
                print(f"Unexpected error in row {row}: {e}")

    # Commit các thay đổi vào cơ sở dữ liệu và đóng kết nối
    conn.commit()
    cursor.close()

# Call the function to import data
#import_data_EventResult()
import_data_MedalResult()

# Đóng kết nối sau khi hoàn thành
conn.close()

