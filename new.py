import streamlit as st
import os
import docx
import pdfplumber
import re
import zipfile
import tempfile
from io import BytesIO

new_a2u = {
    'Dç': 'अ', 'Kç': 'ख', 'kç': 'क',
    'yç': 'ब', 's': 'छ', 'mç': 'स', 'hç': 'प',
    'Lç': 'थ', '³ç': 'य', '@æ[': 'ड़', 'lç': 'त',
    ']pç': 'ज़', 'Çþ': 'ठ', '~': '।', ',': ',',
    'çÆ': 'ि', 'çÇ': 'ी', 'á': 'ु', 'Ó': 'ू',
    'ô': 'ॆ', '@': 'ॉ'
}

vowel_a2u = {
    'ç': 'ा', 'çÆ': 'ि', 'çÇ': 'ी', 'á': 'ु', 'Ó': 'ू',
    'ô': 'ॆ', '@': 'ॉ'
}

vowel = [u'ा', u'ि', u'ी', u'ु', u'ू',
         u'ृ', u'ॄ', u'ॅ', u'ॆ', u'े', u'ै', u'ॉ', u'ॊ', u'ो', u'ौ', u'्']


def convert_akruti_to_unicode(akruti_text):
    arr = []
    i = 0
    unicode_text = ''
    for char in akruti_text:
        arr.append(char)

        # FOR CONSONANTS
        for key, value in new_a2u.items():

            if char == ' ':
                unicode_text += ' '
                break

            if char == '\n':
                unicode_text += '\n'
                break

            if i > 1:
                if arr[i-2] + arr[i-1] + arr[i] == key:
                    unicode_text += new_a2u.get(key, value)
                elif arr[i-1] + arr[i] == key:
                    unicode_text += new_a2u.get(key, value)
                elif arr[i] == key:
                    unicode_text += new_a2u.get(key, value)

        # FOR VOWELS
        for key, value in vowel_a2u.items():
            for key_cons, value_cons in new_a2u.items():
                if i > 1:
                    if arr[i-1] + arr[i] == key and (arr[i-4] + arr[i-3] + arr[i-2] == key_cons or arr[i-3] + arr[i-2] == key_cons):
                        unicode_text += new_a2u.get(key, value)
                    elif arr[i] == key and (arr[i-3] + arr[i-2] + arr[i-1] == key_cons or arr[i-2] + arr[i-1] == key_cons):
                        unicode_text += new_a2u.get(key, value)

        i = i + 1

    arr = []
    i = 0

    for char in unicode_text:
        arr.append(char)
        for key_cons, value_cons in new_a2u.items():
            for key, value in vowel_a2u.items():
                if i > 1:
                    if arr[i-2] != 'त' and arr[i-1] == value and arr[i] == value_cons:
                        unicode_text = unicode_text.replace(
                            value + value_cons, value_cons + value)
        i = i + 1

    return unicode_text


def process_input_file(input):
    if isinstance(input, str):  # Check if input is a string (manual input)
        input_text = input
    else:  # Otherwise, input is a file object
        _, file_extension = os.path.splitext(input.name)

        if file_extension == '.txt':
            input_text = input.getvalue().decode('utf-8')
        elif file_extension == '.docx':
            doc = docx.Document(input)
            input_text = '\n'.join(
                [paragraph.text for paragraph in doc.paragraphs])
        elif file_extension == '.pdf':
            input_text = ''
            with pdfplumber.open(input) as pdf:
                for page in pdf.pages:
                    input_text += page.extract_text()

    output_text = convert_akruti_to_unicode(input_text)
    return input_text, output_text


def process_manual_input(input_text):
    output_text = convert_akruti_to_unicode(input_text)
    return output_text


def process_folder(input_folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith(('.txt', '.docx', '.pdf')):
            input_file_path = os.path.join(input_folder_path, filename)
            input_text, output_text = process_input_file(input_file_path)
            # Display the processed input and output text
            st.write(f"### File: {filename}")
            st.write("#### Input Text:")
            st.text_area("Input", value=input_text, height=300, max_chars=None)
            st.write("#### Converted Text:")
            st.text_area("Output", value=output_text,
                         height=300, max_chars=None)
            st.markdown("---")  # Add a horizontal line between files


def main():

    st.title("Akruti to Unicode Converter")
    # st.title("Select input method")
    input_method = st.sidebar.radio(
        "Select input method:", ('Upload a file', 'Select a folder', 'Enter text manually'))

    if input_method == 'Upload a file':
        uploaded_file = st.file_uploader(
            "Upload a file", type=['txt', 'docx', 'pdf'])

        if uploaded_file is not None:
            input_text, output_text = process_input_file(uploaded_file)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Input Text")
                st.write(
                    '<style>textarea{width:900px !important;height:300px;}</style>',
                    unsafe_allow_html=True
                )
                st.text_area("Input", value=input_text)

            with col2:
                st.subheader("Converted Text")
                st.write(
                    '<style>textarea{width:900px !important;height:300px;}</style>',
                    unsafe_allow_html=True
                )
                st.text_area("Output", value=output_text)

            download_button = st.button("Download Converted Text")
            if download_button:
                st.download_button(
                    label="Click to Download",
                    data=output_text,
                    file_name="converted_text.txt",
                    mime="text/plain"
                )

    elif input_method == 'Select a folder':
        st.write("Please upload a folder containing files.")
        uploaded_zip = st.file_uploader("Upload zip file", type=[
                                        "zip"], accept_multiple_files=False)
        if uploaded_zip is not None:
            # Create a temporary directory to extract the uploaded zip file
            temp_dir = tempfile.TemporaryDirectory()
            zip_file_path = os.path.join(temp_dir.name, uploaded_zip.name)
            with open(zip_file_path, "wb") as f:
                f.write(uploaded_zip.read())

            # Extract the zip file
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir.name)

            # Process files in the extracted folder
            process_folder(temp_dir.name)

    elif input_method == 'Enter text manually':
        input_text_manual = st.text_area("Enter Text Manually:", height=300)

        if st.button("Convert"):
            if input_text_manual.strip() != "":
                output_text_manual = process_manual_input(input_text_manual)
                st.write("### Output Text")
                st.text_area("Output", value=output_text_manual.decode(
                    'utf-8'), height=300)

                st.download_button(
                    label="Download Converted Text",
                    data=output_text_manual,
                    file_name="converted_text_manual.txt",
                    mime="text/plain",
                    key="download_button_manual"
                )


if __name__ == '__main__':
    main()
