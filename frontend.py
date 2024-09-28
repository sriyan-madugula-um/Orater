import streamlit as st
import pandas as pd

st.markdown("""
<style>
@keyframes example {
  0%   { color: 81bec7; }
  25%  { color: 011638; }
  50%  { color: 364158; }
  75%  { color: c1b5b5; }
  100% { color: 81bec7; }
}
.mainTitle {
    font-size: 70px !important;
    text-align: center;
    animation-name: example;
    animation-duration: 4s;
    animation-iteration-count: infinite;
    
}
</style>
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="mainTitle">Welcome</p>', unsafe_allow_html=True)
user_input = st.text_input("Enter prompt:", placeholder="Tell your speech's purpose")