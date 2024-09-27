import streamlit as st
import pandas as pd
import country.main as country

st.sidebar.title("Menu")

menu_options = ['Homepage', 'Country', 'Competition', 'Athlete']

selected_options = st.sidebar.radio('Choose one', menu_options)

if selected_options == 'Homepage':
    st.title('Data engineering project')
    st.header('**Topic:** 126 years of Historical Olympic')
    images = [
        "./image/olympic_1.jpg",
        "./image/olympic_2.jpg",
        "./image/olympic_3.jpg",
    ]

    # Tạo số lượng cột tùy ý (ở đây là 4 cột cho 4 hình ảnh)
    cols = st.columns(len(images))

    st.write('**Instructor**: Ms. Tran Thi Que Nguyet')
    st.write('**Student:** ')
    table_data = {
        'Student name': ['Lu Xuan Minh', 'Tran The Nhan', 'Ho Thanh Nhan', 'Nguyen Thanh Nhan', 'Nguyen Thanh Nhan'],
        'Student ID': ['2212051', '', '', '', '']
    }

    df = pd.DataFrame(table_data)

    st.table(df)

    # Hiển thị mỗi hình ảnh trong một cột tương ứng
    for col, img in zip(cols, images):
        col.image(img, use_column_width=True)

if selected_options == 'Country':
    country.main()

if selected_options == 'Competition':
    pass

if selected_options == 'Athlete':
    pass
