from openai import OpenAI
import re
import os
import replicate
import streamlit as st
from PIL import Image
from IFT import welcome_prompt_bot

os.environ['REPLICATE_API_TOKEN'] = st.secrets['REPLICATE_API_TOKEN']

st.set_page_config(
    page_title="FinnoSQLbot",  
    page_icon="💱",
    layout="wide"
)

logos = ['logo1.png', 'logo2.png']

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Workbench&display=swap');
        .pixel-font {
            font-family: "Pacifico", cursive, "Workbench", sans-serif;
            font-size: 37px;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
        """<div class="pixel-font">  FinnoSQLbot  </div>
    """,
        unsafe_allow_html=True,
    )
st.write("###### AI Asst. performs financial data exploration and answers questions executing SQL queries on Snowflake data, create a tabular response from the dynamic SQL")
            
# Set icons
icons = {"assistant": "💰", "user": "💭"}


with st.sidebar:
    st.write("Made in an AI hackathon inspired by SNOWFLAKE - May 2024 - Paul Biswa ")
    st.markdown("---")
    st.markdown("Powered by **Snowflake ARCTIC©** LLM\n\n" " Arctic Instruct is a 480B parameter foundation LLM. ")
   
    st.subheader("Adjust model parameters")
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.3, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_tokenlength', min_value=32, max_value=300, value=150, step=25)
    st.markdown("---")
    col1, _ = st.sidebar.columns(2)  # Creating two columns (use one for logos)
    for logo in logos:
        with col1:
            image = Image.open(logo)
            st.image(image,width=230)
    st.markdown("---")
    #st.markdown("replypaul@gmail.com\n")


# Function for generating Snowflake Arctic response
def generate_arctic_response():
    prompt = []
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            prompt.append("<|im_start|>user\n" + dict_message["content"] + "<|im_end|>")
        else:
            prompt.append("<|im_start|>assistant\n" + dict_message["content"] + "<|im_end|>")
    
    prompt.append("<|im_start|>assistant")
    prompt.append("")
    prompt_str = "\n".join(prompt)
    
    if get_num_tokens(prompt_str) >= 3072:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")
        st.button('Clear chat history', on_click=clear_chat_history, key="clear_chat_history")
        st.stop()

    for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                           input={"prompt": prompt_str,
                                  "prompt_template": r"{prompt}",
                                  "temperature": temperature,
                                  "top_p": top_p,
                                  }):
        yield str(event)


# Initialize the chat messages history
client = os.environ['REPLICATE_API_TOKEN']
client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    st.session_state.messages = [{"role": "system", "content": welcome_prompt_bot()}]


# Prompt for user input 
if prompt := st.chat_input(placeholder="✍️ Type prompt"):
    st.session_state.messages.append({"role": "user", "content": prompt})


# display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.write(message["content"])
        if "results" in message:
            st.dataframe(message["results"])


# If last message is not from the chat bot, we need to generate a new response for the assistant 
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        full_response = generate_arctic_response()
        st.write(" FinnoSQL: ")
        resp_container = st.empty()
        for delta in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            response = response + (delta.choices[0].delta.content or "")
            full_response = (delta.choices[0].delta.content or "")
            resp_container.markdown(response)

        message = {"role": "assistant", "content": response}
        # Parse the response for a SQL query and execute if available
        sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
        if sql_match:
            sql = sql_match.group(1)
            conn = st.connection("snowflake")
            message["results"] = conn.query(sql)
            st.dataframe(message["results"])
        st.session_state.messages.append(message)
