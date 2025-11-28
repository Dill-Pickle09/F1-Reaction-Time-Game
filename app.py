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

if "step" not in st.session_state:
    st.session_state.step = 0
if "red_count" not in st.session_state:
    st.session_state.red_count = 0
if "green_delay" not in st.session_state:
    st.session_state.green_delay = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None


st.title("F1 Reaction Time Test")
st.write("Wait for all 5 lights to turn **green**, then hit the button as quick as you can!")

if st.session_state.step == 0:
    if st.button("Start Sequence"):
        st.session_state.step = 1
        st.session_state.red_count = 1
        st.rerun()

elif st.session_state.step == 1:
    show_lights(red_count=st.session_state.red_count)

    if st.session_state.red_count < 5:
        if st.button("Next Light"):
            st.session_state.red_count += 1
            st.rerun()
    else:
        if st.session_state.green_delay is None:
            st.session_state.green_delay = time.time() + random.uniform(1.0, 1.35)
        if time.time() >= st.session_state.green_delay:
            st.session_state.step = 2
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.write("Get ready...")
            time.sleep(0.05)
            st.rerun()

elif st.session_state.step == 2:
    show_lights(green=True)
    st.write("### LIGHTS OUT. CLICK THE BUTTON")
    if st.button("STOP"):
        rt = (time.time() - st.session_state.start_time) * 1000
        st.session_state.reaction_time = rt

        st.session_state.step = 0
        st.session_state.green_delay = None

        st.success(f"**Your Reaction Time: `{rt:.0f} ms`**")