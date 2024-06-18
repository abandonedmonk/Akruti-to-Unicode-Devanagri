from flask import Flask, render_template, request, send_file
from akruti_to_unicode import convert_akruti_to_unicode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # Read the Akruti text from the file
        akruti_text = uploaded_file.read().decode('utf-8')

        # Convert to Unicode
        unicode_text = convert_akruti_to_unicode(akruti_text)

        # Create a new file with the converted text
        with open('converted_text.txt', 'w', encoding='utf-8') as file:
            file.write(unicode_text)

        # Return the converted file to the user
        return send_file('converted_text.txt', as_attachment=True, download_name='converted_text.txt')

    return 'No file uploaded'

if __name__ == '__main__':
    app.run(debug=True)
