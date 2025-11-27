import streamlit as st
import time
import random


st.set_page_config(page_title="F1 Reaction Time", page_icon="🏎️", layout="centered")

CIRCLE_STYLE = """
<style>
.light-row{
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 20px 0;
}
.light {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: #300000;
    box-shadow: 0 0 10px #000;
}
.red-on {
    background: red;
    box-shadow: 0 0 25px red;
}
.green-on{
    background: #00ff00;
    box-shadow: 0 0 25px #00ff00;
}
</style>
"""

st.markdown(CIRCLE_STYLE, unsafe_allow_html=True)

def show_lights(red_count=0, green=False):
    html = "<div class='light-row'>"

    for i in range(5):
        if green:
            html += "<div class='light green-on'></div>"
        elif i < red_count:
            html += "<div class='light red-on'></div>"
        else:
            html += "<div class='light'></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

st.title("F1 Reaction Time Test")
st.write("Wait for all 5 lights to turn **green**, then hit the button as quick as you can!")

if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if not st.session_state.running:
    if st.button("Start Sequence"):
        st.session_state.running = True
        st.rerun()

if st.session_state.running:
    for i in range(1, 6):
        show_lights(red_count=i)
        time.sleep(0.6)
        st.rerun()

    delay = random.uniform(1.0, 1.35)
    time.sleep(delay)

    show_lights(green=True)
    st.write("### LIGHTS OUT, CLICK NOW")
    st. session_state.start_time = time.time()

    if st.button("STOP"):
        reaction = (time.time() - st.session_state.start_time) * 1000
        st.session_state.running = False
        st.success(f"**Your Reaction time: `{reaction:.0f} ms`**")