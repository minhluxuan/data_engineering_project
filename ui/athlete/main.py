import pandas as pd
import streamlit as st
from athlete.api import AthleteOperations
from country.api import CountryOperation
from rest_framework import status

def main():
    st.title("Athelete Biography")
    tab1, tab2, tab3, tab4 = st.tabs(['Athelete Biography Info', 'Create athlete', 'Update athlete', 'Delete athlete'])
    with tab1:
        athlete_id = st.text_input('Enter athlete Id: ')
        if athlete_id:
            response = AthleteOperations.searchOne(athlete_id)
        else:
            response = AthleteOperations.search()

        if response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR:
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
                if isinstance(data, list) :
                    df = pd.DataFrame(data)
                    st.write(df)
                elif isinstance(data, dict):
                    df = pd.DataFrame([data])
                    st.write(df)
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                st.write('No athlete found')
        else:
            st.write('An error occurs. Please try again')

    with tab2:
      with st.expander("Create new athlete", expanded=True):
          with st.form(key='my_form'):
            name = st.text_input("Enter athlete name: ")
            year_born = st.text_input("Enter year born: ")
            sex = st.radio(label='Gender', options=['Male', 'Female'])
            height = st.text_input("Enter athlete height: ")
            weight = st.text_input("Enter athlete weight: ")
            
            countries = CountryOperation.search().json() # Giả sử bạn đã import Country model
            country_options = [f"{country['noc']} - {country['country']}" for country in countries]  # Lấy danh sách mã quốc gia
            country_noc = st.selectbox("Select country noc", country_options)
            selected_country = country_noc.split(' - ')[0]
            
            description = st.text_input("Enter description ")
            special_notes = st.text_input("Enter notes ")
            submit_button = st.form_submit_button(label='Submit')
        
            if submit_button:
                form_data = {
                    'name': name.strip() if name else '',
                    'born': year_born.strip() if year_born else '',
                    'sex': sex,
                    'height': float(height) if height else 0,  # Chuyển sang float
                    'weight': float(weight) if weight else 0,  # Chuyển sang float
                    'country_noc': selected_country,
                    'description': description.strip() if description else '',
                    'special_notes': special_notes.strip() if special_notes else ''
                }
                if form_data['name'] == '':
                    st.error("Name of athlete is required") 
                else:
                    response = AthleteOperations.create(form_data)
                    if response.status_code == 200 or response.status_code == 201:
                        st.success("Create successfully")
                    else:
                        st.error("An error occurs. Please try again")
            

      # Hiển thị DataFrame
    with tab3:
        athlete_id = st.text_input("Enter update athlete id: ")
        if athlete_id:
            response = AthleteOperations.searchOne(athlete_id)
            if response.status_code != 500:
                if response.status_code == status.HTTP_200_OK:
                    data = response.json()
                    if isinstance(data, dict):
                        df = pd.DataFrame([data])
                        st.write(df)
                        df_with_selections = df.copy()
                        edited_df = st.data_editor(
                            df_with_selections,
                            hide_index = True,
                            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                        )
                        if st.button("Update Data"):
                            updated_rows = edited_df.compare(df)
                            for index, _ in updated_rows.iterrows():
                                for col in updated_rows.columns.levels[0]:
                                    if (col, 'self') in updated_rows.columns:
                                        new_value = edited_df.loc[index]
                                        new_value_dict = new_value.to_dict()
                                        print(new_value_dict)
                                        response1 = AthleteOperations.update(new_value_dict['athlete_id'], new_value_dict)
                                        #st.rerun()
                                        if response1.status_code == 200:
                                            st.success("Update successfully")
                                        else:
                                            st.error("Invalid input")
                elif response.status_code == status.HTTP_404_NOT_FOUND:
                    st.error('No athlete found') 
            else:
                st.error("An error occurs. Please try again")

    with tab4:
        athlete_id = st.text_input("Enter delete athlete id: ")
        if athlete_id:
            response = AthleteOperations.searchOne(athlete_id)
            if response.status_code != 500:
                if response.status_code == status.HTTP_200_OK:
                    data = response.json()
                    if isinstance(data, dict):
                        df = pd.DataFrame([data])
                        st.write(df)
                        df_with_selections = df.copy()
                        df_with_selections.insert(0, "Select", False)
                        edited_df = st.data_editor(
                            df_with_selections,
                            hide_index = True,
                            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                        )
                        
                        if st.button("Delete selected row"):
                            selected_rows = edited_df[edited_df.Select]
                            
                            if not selected_rows.empty:
                                for index, row in selected_rows.iterrows():  # Dùng iterrows để duyệt qua từng hàng
                                        response_delete = AthleteOperations.delete(row['athlete_id'])
                                        print(response_delete)
                                        if response_delete.status_code == 200:
                                            st.success(response_delete.json()['message'])
                                        else:
                                            st.error(response_delete.json()['message'])
                                st.rerun()

                elif response.status_code == status.HTTP_404_NOT_FOUND:
                    st.write('No athlete found') 
            else:
                st.write("An error occurs. Please try again")