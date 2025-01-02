import streamlit as st
from PIL import Image
import pandas as pd
import country.main as country
from competition.medaltally.main import Dashboard
import athlete.main as athlete
import competition.main as competition

st.set_page_config(layout="wide")

# css_code = """
# <style>
#     body {
#         background-color: #f0f0f0; /* Thay màu nền tại đây */
#     }
#     .stApp {
#         background-color: #d9f2fa; /* Thay đổi màu nền ứng dụng */
#     }
# </style>
# """

# # Áp dụng CSS
# st.markdown(css_code, unsafe_allow_html=True)

st.sidebar.title("Menu")

menu_options = ['Homepage', 'Olympic Games', 'Olympic Competitions', 'Athletes',]

selected_options = st.sidebar.radio('Choose one', menu_options)

if selected_options == 'Homepage':
    st.title('WELCOME TO OLYMPIC PAGE')
    st.write('**"Faster, Higher, Stronger – Together."** - The official motto of the Olympics, reflecting the spirit of unity and relentless effort.')

    images = [
        "./image/olympic_1.jpg",
        "./image/olympic-flag.jpg",
        "./image/olympic_3.jpg",
    ]

    # Kích thước cố định cho tất cả ảnh (width, height)
    fixed_size = (300, 200)  # Bạn có thể thay đổi giá trị này tùy ý

    # Tạo các cột
    cols = st.columns(len(images))

    # Đọc và hiển thị từng ảnh trong cột
    for i, img_path in enumerate(images):
    # Chỉ hiển thị số lượng ảnh tương ứng số cột
        if i < len(cols):
            with cols[i]:  # Đảm bảo mỗi ảnh chỉ hiển thị trong một cột
                # Đọc ảnh bằng Pillow
                img = Image.open(img_path)
                # Thay đổi kích thước ảnh
                img_resized = img.resize(fixed_size)
                # Hiển thị ảnh đã thay đổi kích thước
                st.image(img_resized)

    # st.write('**Instructor**: Ms. Tran Thi Que Nguyet')
    # st.write('**Student:** ')
    # table_data = {
    #     'Student name': ['Lu Xuan Minh', 'Tran The Nhan', 'Ho Thanh Nhan', 'Nguyen Thanh Nhan', 'Nguyen Thanh Nhan'],
    #     'Student ID': ['2212051', '2212383', '2212352', '2212364', '2212366']
    # }

    # df = pd.DataFrame(table_data)

    # st.table(df)
    
    Dashboard.display()

    # Hiển thị mỗi hình ảnh trong một cột tương ứng
    # for col, img in zip(cols, images):
    #     col.image(img, use_container_width=True)

# if selected_options == 'Homepage':
#     st.title('Data engineering project')
#     st.header('**Topic:** 126 years of Historical Olympic')
#     images = [
#         "./image/olympic_1.jpg",
#         "./image/olympic_2.jpg",
#         "./image/olympic_3.jpg",
#     ]

#     # Tạo số lượng cột tùy ý (ở đây là 4 cột cho 4 hình ảnh)
#     cols = st.columns(len(images))

#     st.write('**Instructor**: Ms. Tran Thi Que Nguyet')
#     st.write('**Student:** ')
#     table_data = {
#         'Student name': ['Lu Xuan Minh', 'Tran The Nhan', 'Ho Thanh Nhan', 'Nguyen Thanh Nhan', 'Nguyen Thanh Nhan'],
#         'Student ID': ['2212051', '2212383', '2212352', '2212364', '2212366']
#     }

#     df = pd.DataFrame(table_data)

#     st.table(df)

#     # Hiển thị mỗi hình ảnh trong một cột tương ứng
#     for col, img in zip(cols, images):
#         col.image(img, use_container_width=True)

if selected_options == 'Olympic Games':
    country.main()

if selected_options == 'Olympic Competitions':
    competition.competitionResult()
    # competition.eventResult()

if selected_options == 'Athletes':
    athlete.main()