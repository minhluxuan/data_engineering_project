import pandas as pd
import streamlit as st
from athlete.api import AthleteOperations
from country.api import CountryOperation
from rest_framework import status


def main():
    st.title("Athelete Biography")

    if "option" not in st.session_state:
            st.session_state.option = ''  # Mặc định là rỗng

    option = st.selectbox(
        label='Choose option',
        options=['','Create athlete', 'Athelete Biography Info','Update Biography Info'],
        key="option"  # Liên kết giá trị với session_state
    )

    # tab1, tab2, tab3, tab4 = st.tabs(['Athelete Biography Info', 'Create athlete', 'Update athlete', 'Delete athlete'])
    if "countries" not in st.session_state:
        st.session_state.countries = CountryOperation.search().json() # Giả sử bạn đã import Country model

    if option == 'Athelete Biography Info':
        response = None
        response_data = None
        if "page" not in st.session_state:
            st.session_state.page = 1

        country_options = [f"{country['noc']} - {country['country']}" for country in st.session_state.countries]  # Lấy danh sách mã quốc gia
        country_noc = st.selectbox("Select country noc", country_options)
        selected_country = country_noc.split(' - ')[0]
        
        condition_query = st.selectbox("Select view option", ['ALL', 'GOLD', 'SILVER', 'BRONZE'])
        
        viewOption = {
            'ALL': 0,
            'GOLD': 1,
            'SILVER': 2,
            'BRONZE': 3
        }

        response = AthleteOperations.search(1, selected_country, viewOption[condition_query], st.session_state.page)

        if response.status_code == status.HTTP_200_OK:
            response_data = response.json()
            print(response_data['data'])

        # Hiển thị dữ liệu
        if response_data and "data" in response_data:
            st.write(f"Trang {response_data['data']['page']} / {response_data['data']['total_pages']}")

            # Chuyển dữ liệu bệnh nhân thành một danh sách các từ điển
            patients_data = []
            for item in response_data["data"]["data"]:
                print(item)
                patients_data.append({
                    "athlete_id": str(item['athlete_id']),
                    "name": item['name'],
                    "sex": item['sex'],
                    "born": item['born'],
                    "height": item['height'],
                    "weight": item['weight'],
                    'description': item['description'],
                    'special_notes': item['special_notes'],
                    'gold': item['gold'],
                    'silver': item['silver'],
                    'bronze': item['bronze'],
                })

            # Hiển thị bảng dữ liệu bệnh nhân
            st.dataframe(patients_data)

            # Các nút điều hướng trang
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("<< Trang trước", disabled=st.session_state.page == 1):
                    st.session_state.page -= 1
                    st.rerun()
            with col3:
                if st.button("Trang tiếp >>", disabled=st.session_state.page == response_data["data"]["total_pages"]):
                    st.session_state.page += 1
                    st.rerun()

    if option == 'Update Biography Info':
        response = None
        data = None

        country_options = [f"{country['noc']} - {country['country']}" for country in st.session_state.countries]  # Lấy danh sách mã quốc gia
        country_noc = st.selectbox("Select country noc", country_options)
        selected_country = country_noc.split(' - ')[0]
        name = st.text_input("Input athlete name: ", value="")

        if st.button('Search Update Athlete'):
            if "df_selections" in st.session_state:
                del st.session_state.df_selections
                del st.session_state.df_data

            response = AthleteOperations.searchOne(0, str(name), selected_country)
            print(response)
            
            if response.status_code == status.HTTP_200_OK:
                data = response.json()['data']

                if isinstance(data, list):
                    df = pd.DataFrame(data)

                    if "df_selections" not in st.session_state:
                        st.session_state.df_selections = len(df) * [False]
                        st.session_state.df_data = df

            elif response.status_code == status.HTTP_404_NOT_FOUND:
                st.error(response.json()['message'])
            else:
                st.error("An error occurs. Please try again")
                


# Render the data editor if data is available
        if  "df_data" in st.session_state:
            df_with_selections = st.session_state.df_data.copy()
            df_with_selections["Select"] = st.session_state.df_selections
              # Chuyển cột "Select" lên đầu bằng phương pháp insert
            select_column = df_with_selections.pop("Select")  # Xóa cột "Select" tạm thời
            df_with_selections.insert(0, "Select", select_column)  # Chèn cột vào vị trí đầu tiên

            edited_df = st.data_editor(
                df_with_selections,
                hide_index=True,
                column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            )

            # Sync checkbox selections with session state
            st.session_state.df_selections = edited_df["Select"].tolist()

            born_updated = st.text_input("Input born year: ")
            weight_updated = st.number_input("Input weight (kg): ")
            height_updated = st.number_input("Input height (cm): ")
            special_notes_updated = st.text_input(" Input special notes: ")

            # Button to update data
            if st.button("Update Data"):
                selected_rows = edited_df[edited_df["Select"]]
                for _, row in selected_rows.iterrows():
                    row_dict = row.to_dict()
                    temp = row_dict

                    row_dict['born'] = born_updated if born_updated != None else temp['born']
                    row_dict['weight'] = weight_updated if weight_updated != 0 else temp['weight']
                    row_dict['height'] = height_updated if height_updated != 0 else temp['height']
                    row_dict['special_notes'] = special_notes_updated if special_notes_updated != '' else temp['special_notes']
                    

                    response_update = AthleteOperations.update(row_dict['athlete_id'], row_dict)
                    if response_update.status_code == 200:
                        st.success(f"Athlete {row_dict['athlete_id']} updated successfully.")
                    else:
                        st.error(f"Failed to update athlete {row_dict['athlete_id']}.")

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

    if option == 'Create athlete':
      with st.expander("Create new athlete", expanded=True):
          with st.form(key='my_form'):
            name = st.text_input("Enter athlete name: ")
            year_born = st.text_input("Enter year born: ")
            sex = st.radio(label='Gender', options=['Male', 'Female'])
            height = st.text_input("Enter athlete height: ")
            weight = st.text_input("Enter athlete weight: ")
            
            country_options = [f"{country['noc']} - {country['country']}" for country in st.session_state.countries]  # Lấy danh sách mã quốc gia
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
            

  