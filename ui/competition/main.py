from competition.api import ResultOperation
from datetime import datetime
import pandas as pd
import requests
import streamlit as st
from competition.api import EventResultOperation
from country.api import GameOperation
# form athlete.api import AthleteOperation
from rest_framework import status

def competitionResult():
    st.title("Competition")

    tab1, tab2 = st.tabs(['Result Profile', 'Results'])

    with tab1:
        response = ResultOperation.search()
        if response:
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                    st.write(df)
                else:
                    st.write('No country has been created yet')
            else:
                st.write('An error occurs. Please try again')

    with tab2:
        with st.expander("Create new result", expanded=True):
            with st.form(key='my_form'):
                # result_id = st.text_input("Enter result id:")
                event_title = st.text_input("Enter event title:")
                sport = st.text_input("Enter sport:")
                sport_url = st.text_input("Enter sport url")
                result_location = st.text_input("Enter result location")
                # result_participants = st.text_input(
                    #"Enter result participants")
                # result_countries = st.text_input("Enter result countries")
                start_date = st.date_input("Enter start date")
                end_date = st.date_input("Enter end date")
                result_format = st.text_input("Enter result format")
                result_detail = st.text_input("Enter result detail")
                result_description = st.text_input("Enter result description")
                
                games = GameOperation.search().json()
                game_options = [f"{game['edition_id']} - {game['edition']}" for game in games]  # Lấy danh sách mã quốc gia
                selected_game = st.selectbox("Select edition", game_options)
                edition_id = selected_game.split(' - ')[0]
                submit_button = st.form_submit_button(label='Submit')

                if submit_button:
                    form_data = {
                        'result_id': '',
                        'event_title': event_title,
                        'sport': sport,
                        'sport_url': sport_url,
                        'result_location': result_location,
                        'result_participants': 0,
                        'result_countries': 0,
                        'start_date': str(start_date),
                        'end_date': str(end_date),
                        'result_format': result_format,
                        'result_detail': result_detail,
                        'result_description': result_description,
                        'edition_id': edition_id
                    }

                    response = ResultOperation.create(form_data)
                    if response.status_code == 200 or response.status_code == 201:
                        st.success(response.json()['message'])
                    else:
                        st.error(response.json()['message'])

        # Hiển thị DataFrame
        response = ResultOperation.search()
        if response:
            if response.status_code == 200:  # Assuming successful status code is 200
                data = response.json()
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                    edited_df = st.data_editor(df)
                    if st.button("Update Data"):
                        updated_rows = edited_df.compare(df)
                        for index, _ in updated_rows.iterrows():
                            for col in updated_rows.columns.levels[0]:
                                if (col, 'self') in updated_rows.columns:
                                    new_value = edited_df.loc[index]
                                    new_value_dict = new_value.to_dict()
                                    response = ResultOperation.update(
                                        new_value_dict['result_id'], new_value_dict)
                                    if response.status_code == 201:
                                        st.success(response.json()['message'])
                                    else:
                                        st.error(response.json()['message'])

                    # for index, row in df.iterrows():
                    #     st.subheader(f"Update Game - Edition: {row['edition']}")  # Hiển thị tiêu đề
                    #     with st.form(key=f'update_form_{index}'):
                    #         edition = st.text_input("Edition", value=row['edition'])
                    #         year = st.number_input("Year", value=row['year'], min_value=1896, max_value=2100)
                    #         city = st.text_input("City", value=row['city'])
                    #         edition_url = st.text_input("Edition URL", value=row['edition_url'])
                    #         country_flag_url = st.text_input("Country Flag URL", value=row['country_flag_url'])

                    #         # Kiểm tra và chuyển đổi giá trị ngày tháng
                    #         start_date = row['start_date'] if row['start_date'] else None
                    #         end_date = row['end_date'] if row['end_date'] else None

                    #         start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if isinstance(start_date, str) else start_date
                    #         end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if isinstance(end_date, str) else end_date

                    #         start_date = st.date_input("Start Date", value=start_date)
                    #         end_date = st.date_input("End Date", value=end_date)

                    #         is_held = st.checkbox("Is Held", value=row['is_held'])
                    #         competition_start_date = st.date_input("Competition Start Date", value=row['competition_start_date'])
                    #         competition_end_date = st.date_input("Competition End Date", value=row['competition_end_date'])

                    #         submit_button = st.form_submit_button(label='Update Game')

                    #         if submit_button:
                    #             # Thực hiện cập nhật
                    #             edition_id = row['edition_id']  # Giả sử có trường 'edition_id' trong DataFrame
                    #             updated_data = {
                    #                 'edition': edition,
                    #                 'year': year,
                    #                 'city': city,
                    #                 'edition_url': edition_url,
                    #                 'country_flag_url': country_flag_url,
                    #                 'start_date': start_date,
                    #                 'end_date': end_date,
                    #                 'is_held': is_held,
                    #                 'competition_start_date': competition_start_date,
                    #                 'competition_end_date': competition_end_date,
                    #             }
                    #             update_response = GameOperation.update(edition_id, updated_data)

                    #             if update_response.status_code == 200:
                    #                 st.success("Game updated successfully!")
                    #             else:
                    #                 st.error("Failed to update game.")

                else:
                    st.write('No game has been created yet')
            else:
                st.write('An error occurred. Please try again.')
        # uploaded_file = st.file_uploader("Country", type="csv")

        # if uploaded_file is not None:
        #     df = pd.read_csv(uploaded_file)
        #     st.subheader("Data Preview")
        #     st.write(df.head())

        #     if st.button("Upload country games"):
        #         api_url = 'http://localhost:8000/upload_games/'

        #         files = {'file': uploaded_file.getvalue()}

        #         response = requests.post(api_url, files=files)

        #         if response.status_code == 201:
        #             st.success("CSV uploaded and processed successfully!")
        #         else:
        #             st.error(f"Error: {response.status_code}, {response.text}")



def eventResult():
    st.title("Event Results")

    tab1, tab2, tab3, tab4 = st.tabs(
        ['Event Result View', 'Event Result Creating', 'Event Result Updating', 'Event Result Deleting', ])
    with tab1:
        st.header("Searching the result of each athlete")
        st.write(
            "Please look up the result and athlete IDs before searching (empty = all).")

        # Tạo 4 hộp xổ xuống
        col1, col2 = st.columns(2)
        with col1:
            result_id = st.text_input(
                "Result ID:", placeholder="Enter number result ID")
        with col1:
            athlete_id = st.text_input(
                "Athlete ID:", placeholder="Enter number athlete ID")

        if st.button("Confirm Input"):
            if result_id == "":
                result_id = -793654029
            if athlete_id == "":
                athlete_id = -793654029

        response = EventResultOperation.search(
            result_id, athlete_id)
        if response is not None:
            if response.status_code == 200:  # Kiểm tra mã trạng thái HTTP
                data = response.json()
                if isinstance(data, list) and data:  # Kiểm tra xem có dữ liệu không
                    df = pd.DataFrame(data)
                    st.write(df)
                else:
                    st.write('No event result has been created yet.')
            else:
                st.write(f'An error occurred: {response.status_code}')
        else:
            st.write('No event result has been created yet.')

    with tab2:
        st.header("Creating the result of athlete")
        st.write(
            "Please look up the result and athlete IDs before creating.")

        with st.expander("Create new event result", expanded=True):
            with st.form(key='post_form'):
                result_id = st.text_input("Result ID")
                athlete_id = st.text_input("Athlete ID")
                pos = st.text_input("Position")
                isTeamSport = st.radio(
                    label='Is Team Sport?', options=['Yes', 'No'])
                medal = st.radio(label='Medal', options=[
                                 'Gold', 'Silver', 'Bronze', 'None'])
                submit_button = st.form_submit_button(label='Submit')

                if submit_button:
                    if not result_id or not athlete_id:
                        st.write(
                            "Result ID, Athelete ID cannot be empty. Please enter all values.")
                    else:
                        isTeamSport = True if isTeamSport == 'Yes' else False
                        if medal == 'None':
                            medal = None

                        form_data = {
                            'result_id': result_id,
                            'athlete_id': athlete_id,
                            'pos': pos,
                            'isTeamSport': isTeamSport,
                            'medal': medal
                        }
                        if form_data is not {}:
                            response = EventResultOperation.create(form_data)
                            if response.status_code == 200 or response.status_code == 201:
                                st.success(response.json()['message'])
                            else:
                                st.error(response.json()['message'])

        # Hiển thị các lựa chọn đã chọn
        # st.write(f"Selected Event: {edition_id}")
        # st.write(f"Selected Athlete: {result_id}")
        # st.write(f"Selected Gender: {athlete_id}")

    with tab3:
        st.header("Updating the result of athlete")
        st.write(
            "Please look up the result and athlete IDs before creating. (Not be empty)")

        col1, col2 = st.columns(2)
        with col1:
            result_id = st.text_input(
                "Result ID:", placeholder="Enter number result ID", key='u2')
        with col2:
            athlete_id = st.text_input(
                "Athlete ID:", placeholder="Enter number athlete ID", key='u3')

        # if st.button("Search"):
        if not result_id or not athlete_id:
            st.write("Cannot be empty. Please enter all values.")
        else:
            # Gọi API để tìm kiếm
            response = EventResultOperation.search(
                result_id, athlete_id)
            if response is not None and response.status_code == 200:
                data = response.json()
                row_count = len(data)
                # Kiểm tra nếu dữ liệu là list và không rỗng
                if isinstance(data, list) and data:
                    df = pd.DataFrame(data)  # Hiển thị dữ liệu dưới dạng bảng
                    st.write(df)

                # Lấy dữ liệu cũ
                    old_data = data[0]
                    print(old_data)

                    # Tạo form để người dùng cập nhật
                    st.write(
                        "Please update the information below. Leave blank if no changes are needed.")
                    with st.form(key=f'update_form1'):
                        result_id1 = st.text_input(
                            "Result ID", value=old_data.get("result_id", ""))
                        athlete_id1 = st.text_input(
                            "Athlete ID", value=old_data.get("athlete_id", ""))
                        pos1 = st.text_input(
                            "Position", value=old_data.get("pos", ""))
                        isTeamSport1 = st.radio("Is Team Sport?", options=[
                                                    "Yes", "No"], index=0 if old_data.get("isTeamSport") else 1)
                        medal1 = st.radio("Medal", options=["Gold", "Silver", "Bronze", "None"], index={
                                        "Gold": 0, "Silver": 1, "Bronze": 2, None: 3}[old_data.get("medal")])
                        submit_button1 = st.form_submit_button(label="Submit")

                        # So sánh và cập nhật khi người dùng nhấn nút Submit
                        if submit_button1:

                            isTeamSport1 = 1 if isTeamSport1 == "Yes" else 0
                            if medal1 == "None":
                                medal1 = None

                            # Tạo dict với dữ liệu mới nếu có sự thay đổi
                            updated_data = {}
                            #updated_data['id'] = (data[i])['id']
                            if result_id1 and result_id1 != old_data["result_id"]:
                                updated_data["result_id"] = result_id1
                            if athlete_id1 and athlete_id1 != old_data["athlete_id"]:
                                updated_data["athlete_id"] = athlete_id1
                            if pos1 and pos1 != old_data["pos"]:
                                updated_data["pos"] = pos1
                            if isTeamSport1 != old_data["isTeamSport"]:
                                updated_data["isTeamSport"] = isTeamSport1
                            if medal1 != old_data["medal"]:
                                updated_data["medal"] = medal1

                            print(updated_data)

                            # Gửi dữ liệu cập nhật nếu có thay đổi
                            if updated_data:
                                response = EventResultOperation.update(
                                    result_id, athlete_id, updated_data)
                                if response.status_code == 200:
                                    st.success(response.json()['message'])
                                else:
                                    st.write(f"An error occurred: {response.status_code}")
                            else:
                                st.write("No changes detected.")
                else:
                    st.write("No event result found.")
            else:
                st.write("No event result found.")

    with tab4:
        st.header("Deleting the result of athlete")
        st.write(
            "Please look up the result and athlete IDs before creating. (Not be empty)")

        col1, col2 = st.columns(2)
        with col1:
            result_id = st.text_input(
                "Result ID:", placeholder="Enter number result ID", key='u6')
        with col2:
            athlete_id = st.text_input(
                "Athlete ID:", placeholder="Enter number athlete ID", key='u7')

        # if st.button("Search"):
        if not result_id or not athlete_id:
            st.write("Cannot be empty, please enter all values.")
        else:
            # Gọi API để tìm kiếm
            response = EventResultOperation.search(
                result_id, athlete_id)
            if response is not None and response.status_code == 200:
                data = response.json()
                # Kiểm tra nếu dữ liệu là list và không rỗng
                if isinstance(data, list) and data:
                    df = pd.DataFrame(data)  # Hiển thị dữ liệu dưới dạng bảng
                    st.write(df)
                if st.button("Confirm Delete"):
                    response = EventResultOperation.delete(
                        result_id, athlete_id)
                    if response is not None and response.status_code == 204:
                        st.write("Delete successfully")
                    else:
                        st.write("An error occurred while deleting.")
            else:
                st.write("No event result found.")

