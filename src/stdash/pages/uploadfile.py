import streamlit as st
import requests


# 새 페이지: 이미지 업로드 및 분류
def image_classification_page():
    st.title("Hotdog🌭 or Not Hotdog🐶")

    # 파일 업로드 컴포넌트
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # 업로드한 이미지 표시
        # 이미지를 FastAPI 서버로 전송
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://localhost:8000/uploadfile/", files=files)

        if response.status_code == 200:
            # FastAPI로부터 받은 분류 결과 출력
            result = response.json()
            label = result["label"]
            # 결과에 따라 비교 표시
            expected_label = "hot dog"  # 업로드한 이미지가 실제 hot dog인지 예측 결과와 비교
            result_image = ""
            if label == "hot dog":
                result_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxqqIG2n685k1AS3HyuhXLgMsySGTozbxNvQ&s"  # Hotdog 이미지
            else:
                result_image = "https://mblogthumb-phinf.pstatic.net/MjAyMjAyMDdfMjEy/MDAxNjQ0MTk0Mzk2MzY3.WAeeVCu2V3vqEz_98aWMOjK2RUKI_yHYbuZxrokf-0Ug.sV3LNWlROCJTkeS14PMu2UBl5zTkwK70aKX8B1w2oKQg.JPEG.41minit/1643900851960.jpg?type=w800"  # Not hotdog 이미지

            # 두 개의 열로 이미지를 나란히 배치
            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                st.image(uploaded_file, caption="Your Image", use_column_width=True)

            with col2:
                # 중간 위치에 = 또는 != 표시
                if label == expected_label:
                    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>=</h1>", unsafe_allow_html=True)
                else:
                    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>!=</h1>", unsafe_allow_html=True)

            with col3:
                st.image(result_image, caption="Result", use_column_width=True)
            st.success(f"결과: {result['label']} (신뢰도: 약 {result['score']:.2f})")
        else:
            st.error("이미지 분류 중 오류가 발생했습니다.")
    else:
        st.warning("이미지 파일을 업로드해주세요.")
image_classification_page()

