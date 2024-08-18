import streamlit as st
import pyperclip  # Ensure you have pyperclip installed
import io
import json
import pandas as pd

# Title of the app with an emoji and custom styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;600&display=swap');

    .title {
        text-align: center;
        color: #8000ff; /* Set your preferred color */
        font-size: 2em; /* Adjust size as needed */
        font-family: 'Kanit', sans-serif;
        animation: fadeIn 2s ease-in-out;
    }

    .subheader {
        font-family: 'Kanit', sans-serif;
        font-size: 1.8em;
        margin-bottom: 0.5em;
    }

    .label {
        font-family: 'Kanit', sans-serif;
        font-weight: 400;
    }

    .fixed-textarea {
        resize: none;
        overflow: auto;
        height: 300px;
        width: 100%;
        white-space: pre-wrap; /* Preserve whitespace */
        word-wrap: break-word; /* Ensure long words wrap correctly */
        font-family: 'Kanit', sans-serif;
        padding: 10px; /* Add padding for better appearance */
    }

    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #ffffff;
        font-family: 'Kanit', sans-serif;
    }

    .input-container {
        display: flex;
        flex-direction: column;
        font-family: 'Kanit', sans-serif;
    }

    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select {
        font-family: 'Kanit', sans-serif;
        font-size: 1em;
        padding: 0.5em;
    }

    .stTextInput input::placeholder {
        color: #888; /* Set your preferred placeholder color */
        font-family: 'Kanit', sans-serif;
        font-size: 1em;
    }

    </style>
    <h1 class="title">Text Repeater 📝</h1>
""", unsafe_allow_html=True)

# Layout for user text input at the top with default value
st.markdown('<h3 class="subheader">Text Input</h3>', unsafe_allow_html=True)
user_text = st.text_input("Enter text to repeat ✍️", value="Hello, World!", placeholder="Type your text here...", label_visibility="collapsed")

# Layout for repeat count and display options in a single row with default values
st.markdown('<h2 class="subheader">Options</h2>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="input-container"><label class="label">Repeat count 🔢</label></div>', unsafe_allow_html=True)
    repeat_count = st.number_input("", min_value=1, max_value=1_000_000, value=5, step=1, format="%d", key='repeat_count', help="Enter the number of times to repeat the text", label_visibility="collapsed")

with col2:
    st.markdown('<div class="input-container"><label class="label">Display Option 🛠️</label></div>', unsafe_allow_html=True)
    display_option = st.selectbox("", ["Default", "Separated by Spaces", "Concatenated Without Spaces"], index=0, key='display_option', label_visibility="collapsed")

st.markdown('<h3 class="subheader">Show Text</h3>', unsafe_allow_html=True)

# Add a line separator
st.markdown("---")

# Generate repeated text in real-time based on selected option
if user_text:
    if display_option == "Separated by Spaces":
        repeated_text = (' '.join([user_text] * repeat_count))
    elif display_option == "Concatenated Without Spaces":
        repeated_text = (user_text * repeat_count)
    else:
        repeated_text = (user_text + '\n') * repeat_count
else:
    repeated_text = ""

# Create a safe version of the repeated text for HTML
safe_repeated_text = repeated_text.replace("\n", "<br>")

# Display the repeated text in a non-editable, fixed-size text area using HTML
st.markdown(f"""
    <div class="fixed-textarea">{safe_repeated_text}</div>
""", unsafe_allow_html=True)

# Add a line separator
st.markdown("---")

# Format repeat count with commas
formatted_repeat_count = f"{repeat_count:,}"

# Display additional information below the line separator
st.markdown(f"""
    <p class="label">📝 Info: Text : '{user_text}' | 🔢 Count Repeat : {formatted_repeat_count} | 🛠️ Display Option : {display_option}</p>
""", unsafe_allow_html=True)

# Layout for buttons in a single row
col3, col4 = st.columns([1, 1])

with col3:
    # Copy functionality with additional options
    st.markdown('<h3 class="subheader">Copy Options</h3>', unsafe_allow_html=True)
    copy_format = st.selectbox("Copy Format", ["Plain Text", "HTML"], index=0, label_visibility="collapsed")

    if st.button("Copy Text 📋"):
        if repeated_text:
            if copy_format == "Plain Text":
                pyperclip.copy(repeated_text)
                st.success("Text copied to clipboard as plain text! 📋")
            elif copy_format == "HTML":
                # Create HTML-formatted text
                html_text = f"<html><body>{safe_repeated_text}</body></html>"
                pyperclip.copy(html_text)
                st.success("Text copied to clipboard as HTML! 📋")
        else:
            st.warning("No text to copy. Please enter some text and set the repeat count. ⚠️")

with col4:
    # File name and format input
    st.markdown('<h3 class="subheader">Save Options</h3>', unsafe_allow_html=True)
    file_name = st.text_input("File Name", value="repeated_text", placeholder="Enter file name...", label_visibility="collapsed")
    file_format = st.selectbox("File Format", [".txt", ".csv", ".json"], index=0, label_visibility="collapsed")

    # Save button
    if st.button("Save Text to File 💾"):
        if repeated_text:
            if file_format == ".txt":
                st.download_button(
                    label="Download",
                    data=repeated_text,
                    file_name=f"{file_name}.txt",
                    mime="text/plain"
                )
            elif file_format == ".csv":
                df = pd.DataFrame([repeated_text.split('\n')], columns=["Text"])
                buffer = io.StringIO()
                df.to_csv(buffer, index=False, header=False)
                st.download_button(
                    label="Download",
                    data=buffer.getvalue(),
                    file_name=f"{file_name}.csv",
                    mime="text/csv"
                )
            elif file_format == ".json":
                json_data = json.dumps({"text": repeated_text})
                st.download_button(
                    label="Download",
                    data=json_data,
                    file_name=f"{file_name}.json",
                    mime="application/json"
                )
        else:
            st.warning("No text to save. Please enter some text and set the repeat count. ⚠️")

# Footer with additional information
st.markdown("""
    <div class="footer">
        <p>Created by Merlinxz <a href="https://github.com/Merlinxz" target="_blank">My GitHub</a></p>
    </div>
""", unsafe_allow_html=True)