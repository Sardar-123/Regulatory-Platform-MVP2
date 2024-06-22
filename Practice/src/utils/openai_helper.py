import openai


def set_openai_api_key():
    openai.api_key = st.text_input("Enter your OpenAI API key", type="password")
    if not openai.api_key:
        st.error("Please enter your OpenAI API key")
        return False
    return True
