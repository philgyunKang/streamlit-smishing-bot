import streamlit as st
import requests
import os

# API URL 및 키 설정
API_URL = os.environ.get("API_URL", "Your_url")  # 올바른 API URL로 설정
API_KEY = os.environ.get("API_KEY", "Your_key")

def predict_smishing(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)  # 올바른 메서드 사용
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        
        # 응답 내용 출력하여 확인
        print("응답 상태 코드:", response.status_code)
        print("응답 내용:", response.text)  # 응답 내용을 직접 출력
        
        result = response.json()  # JSON 파싱 시도
        return result.get("prediction", "결과를 가져올 수 없습니다.")
        
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP 에러 발생: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"에러 발생: {err}"
    except ValueError as val_err:
        # JSON 파싱 오류가 발생했을 때 처리
        return f"응답 파싱 에러: {val_err}. 응답 내용: {response.text}"

st.title("스미싱 탐지 봇")

user_input = st.text_input("문자 내용을 입력하세요:")
if user_input:
    result = predict_smishing(user_input)
    st.write("결과:", result)
