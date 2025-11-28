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

if "state" not in st.session_state:
    st.session_state.state = "idle"
if "red_index" not in st.session_state:
    st.session_state.red_index = 0
if "green_time" not in st.session_state:
    st.session_state.green_time = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "reaction" not in st.session_state:
    st.session_state.reaction = None


st.title("F1 Reaction Time Test")
st.write("Wait for all 5 lights to turn **green**, then hit the button as quick as you can!")

if st.session_state.state == "idle":
    show_lights(0)
    if st.button("Start"):
        st.session_state.state = "red_sequence"
        st.session_state.red_index = 0
        st.rerun()

elif st.session_state.state == "red_sequence":
    show_lights(st.session_state.red_index)

    if st.button("STOP"):
        st.session_state.state = "done"
        st.session_state.reaction = None
        st.error("FALSE START!")
        st.rerun()
    
    if st.session_state.red_index < 5:
        time.sleep(0.6)
        st.session_state.red_index += 1
        st.rerun()
    else:
        st.session_state.state = "waiting_green"
        st.session_state.green_time = time.time() + random.uniform(1.0, 1.5)
        st.rerun()

elif st.session_state.state == "waiting_green":
    show_lights(5)

    if st.button("STOP"):
        st.session_state.state = "done"
        st.session_state.reaction = None
        st.error("FALSE START!")
        st.rerun()

    if time.time() >= st.session_state.green_time:
        st.session_state.state = "green"
        st.session_state.start_time = time.time()
        st.rerun()
    else:
        time.sleep(0.05)
        st.rerun()

elif st.session_state.state == "green":
    show_lights(green=True)
    st.write("### GO! STOP NOW")

    if st.button("STOP"):
        st.session_state.reaction = (time.time() - st.session_state.start_time) * 1000
        st.session_state.state = "done"
        st.rerun()

elif st.session_state.state == "done":
    if st.session_state.reaction is not None:
        st.success(f"**Your Reaction Time: `{st.session_state.reaction:.0f} ms`**")
    show_lights(0)

    if st.button("Try Again"):
        st.session_state.state = "idle"
        st.session_state.red_index = 0
        st.session_state.green_time = None
        st.session_state.start_time = None
        st.session_state.reaction = None
        st.rerun()