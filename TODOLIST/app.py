import streamlit as st

# 페이지 제목 설정
st.title("할 일 목록 (TODO List)")

# 할 일 목록을 저장할 리스트
todo_list = []

# 할 일 추가 함수
def add_todo():
    todo = st.session_state["new_todo"]  # 입력된 새로운 할 일 가져오기
    if todo:
        todo_list.append(todo)  # 리스트에 추가
        st.session_state["new_todo"] = ""  # 입력 필드 초기화

# 할 일 삭제 함수
def delete_todo(index):
    if 0 <= index < len(todo_list):
        del todo_list[index]  # 해당 인덱스의 할 일 삭제

# 할 일 입력 필드와 추가 버튼
st.text_input("새로운 할 일을 입력하세요:", key="new_todo", on_change=add_todo)

# 할 일 목록 출력
st.subheader("할 일 목록")
if todo_list:
    for i, todo in enumerate(todo_list):
        col1, col2 = st.columns([4, 1])
        col1.write(f"{i + 1}. {todo}")  # 할 일 출력
        if col2.button("삭제", key=f"delete_{i}"):
            delete_todo(i)  # 삭제 버튼 클릭 시 해당 할 일 삭제
else:
    st.write("할 일이 없습니다.")