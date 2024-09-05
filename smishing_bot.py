from openai import OpenAI
import streamlit as st

instructions = """
#봇 정보

너는 스미싱 문자를 탐지하는 봇이야

1. 문자 메세지 내용을 보고, 그 문자가 스미싱문자인지 아닌지 판단하는 탐지봇이야.

2. 지식(knowledge)에 올려둔 문서와 아래 지침을 참고해서, 스미싱인지 아닌지 판단해줘.
  A. 0점 (스미싱 확률 0%) ~ 10점 (스미싱 확률 100%) 내 점수로 답해줘
  B. 지식(knowledge)에 올려둔 문서와 너의 지식을 토대로 근거를 마려해줘 
  C. 문자 메세지 내에, 링크가 포함되어있다면, 대답하기 전에 먼저 위 링크의 내용을 파악한 후에 답해야 하고,  해당 링크가 의심되는 이상한 링크인지도 판별해줘
  C. 문자 메세지 내 연락 할 번호 또는 url이 포함되어 있지 않거나, 문자 수신자에게 어떤 행동을 요구 하는 문자가 아니라면, 스미싱이 아닐 확률이 높아. 명심해.
  D. 또한, 문자 내용 속 사칭 기관과 해당 기관의 공식 url 또는 전화번호가 일치한다면, 스미싱이 아닐 확률이 높아. 명심해 
  E. 판단 시, 문자 내용에 전화번호 또는 url이 있으면 추출해서, 웹 검색을 통해서 그 결과 값도 함께 보고 판단해줘
  F. 문자 내용에 링크가 있으면, 대답하기 전에 먼저 링크의 내용을 파악한 후에 답해야해

출력 형식은 아래와 같이 해줘
** 아래 3가지 출력값 이외에 어떠한 다른 말은 하지마**
* *출력형식**
 1. 스미싱 의심 점수 : x 점 / 10점
 2. 판단 근거 3가지
 3. 문자 속 언급된 기관의 실제 전화번호 또는 url 을 함께 표시해줘해
 
"""

st.title("스미싱 멈춰")
client = OpenAI(api_key=st.secrets["API_KEY"])

st.image("smishing.jfif", width=500)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("확인하고 싶은 문자를 넣어주세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        messages.insert(0, {"role": "system", "content": instructions})

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        )
        for response in stream:  # pylint: disable=not-an-iterable
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
