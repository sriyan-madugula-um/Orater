import streamlit as st

# Inject custom CSS for typing animation without blinking cursor and with center alignment
st.markdown("""
<style>
body {
    backgroundColor: #182121;   
    text-align: center;
}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

.mainTitle {
    font-size: 75px;
    color: #8eb1c7;
    font-family: 'Abolition', sans-serif;
    white-space: nowrap; /* Prevent text from wrapping */
    width: 0;
    overflow: hidden; /* Hide the text until it is revealed */
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 10; /* Remove default bottom margin */
    animation: typing 2.5s steps(40, end);
    animation-fill-mode: forwards; /* Keep the final state after animation ends */
    text-align: center;
}

.description {
    font-size: 25px;
    color: #c1bfb5;
    font-family: 'Abolition', sans-serif;
    white-space: nowrap;
    width: 0;
    overflow: hidden;
    margin-left: auto;
    margin-right: auto;
    animation: typing 3.5s steps(60, end);
    animation-delay: 2.5s; /* Delay description animation until title finishes */
    animation-fill-mode: forwards;
    text-align: center;
}
.button{
    background-color: #011638;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Display the main title and description with typing animation (no blinking cursor)
st.markdown('<p class="mainTitle">Welcome to Orater</p>', unsafe_allow_html=True)
st.markdown('<p class="description">The Best Place to Improve Public Speaking</p>', unsafe_allow_html=True)

# Input prompt with placeholder
user_input = st.text_input("", placeholder="Tell us your speech's prompt")

pressed = st.button("Start Recording")

if pressed:
    if user_input:
        st.success("Recording started!")
    else:
        st.error("Please enter your promp before proceeding.")
