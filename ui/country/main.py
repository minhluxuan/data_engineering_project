from datetime import datetime
import pandas as pd
import requests
import streamlit as st
from country.api import CountryOperation, GameOperation
from rest_framework import status

def main():
    st.title("Country")

    tab1, tab2= st.tabs(['Country Profiles', 'Games'])

    with tab1:
        st.write("List of country and NOC")
        response = CountryOperation.search()
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
        with st.expander("Create new game", expanded=True):
            with st.form(key='my_form'):
                edition = st.text_input("Enter edition:")
                edition_url = st.text_input("Enter edition url:")
                year = st.text_input("Enter year")
                city = st.text_input("Enter city")
                country_flag_url = st.text_input("Enter country flag url")
                country_noc = st.text_input("Enter country noc")
                start_date = st.date_input("Enter start date")
                end_date = st.date_input("Enter end date")
                isHeld = st.radio(label='Held:', options=['Yes', 'No'])
                competition_start_date = st.date_input("Enter competition start date")
                competition_end_date = st.date_input("Enter competition end date")
                submit_button = st.form_submit_button(label='Submit')

                if submit_button:
                    isHeld_bool = True if isHeld == 'Yes' else False

                    form_data = {
                        'edition': edition,
                        'edition_url': edition_url,
                        'year': year,
                        'city': city,
                        'country_flag_url': country_flag_url,
                        'country_noc': country_noc,
                        'start_date': str(start_date),
                        'end_date': str(end_date),
                        'is_held': isHeld_bool,
                        'competition_start_date': str(competition_start_date),
                        'competition_end_date': str(competition_end_date)
                    }

                    response = GameOperation.create(form_data)
                    if response.status_code == 200 or response.status_code == 201:
                        st.success(response.json()['message'])
                    else:
                        st.error(response.json()['message'])

        # Hiển thị DataFrame
        response = GameOperation.search()
        if response:
            if response.status_code == 200:  # Assuming successful status code is 200
                data = response.json()
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                    # edited_df = st.data_editor(df, use_container_width=True)
                    df_with_selections = df.copy()
                    df_with_selections.insert(0, "Select", False)
                    edited_df = st.data_editor(
                        df_with_selections,
                        hide_index=True,
                        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                    )
                    if st.button("Update Data"):
                        updated_rows = edited_df.compare(df)
                        for index, _ in updated_rows.iterrows():
                            for col in updated_rows.columns.levels[0]:
                                if (col, 'self') in updated_rows.columns:
                                    new_value = edited_df.loc[index]
                                    new_value_dict = new_value.to_dict()
                                    response = GameOperation.update(new_value_dict['edition_id'], new_value_dict)
                                    if response.status_code == 201:
                                        st.success(response.json()['message'])
                                    else:
                                        st.error(response.json()['message'])
                    
                    if st.button("Delete selected row"):
                        selected_rows = edited_df[edited_df.Select]
                        
                        if not selected_rows.empty:
                            for index, row in selected_rows.iterrows():  # Dùng iterrows để duyệt qua từng hàng
                                    response = GameOperation.delete(row['edition_id'])
                                    if response.status_code == 200:
                                        st.success(response.json()['message'])
                                    else:
                                        st.error(response.json()['message'])
                            st.experimental_rerun()
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