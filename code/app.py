from PyPDF2.generic import NameObject
from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import io

# PermissionsFormsSimplifier created by @drxcu Vlad Prigoreanu for Bogdan Stefan at Uniper SE

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fill_pdf', methods=['POST'])
def fill_pdf():
    # Load the template PDF form
    with open('forms/template.pdf', 'rb') as template_file:
        template_pdf = PdfReader(template_file)

        # Get the user's information from the request
        userid = request.form['userid']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        # Get the reference user's information from the request
        firstnamelastname = request.form['firstnamelastname']
        emailadresse = request.form['emailadresse']
        kid = request.form['kid']

        # Get the dropdown value from the request
        dropdown_value1 = request.form['dropdown1']
        dropdown_value2 = request.form['dropdown2']

        # Get the comments from the request
        comments = request.form['comments']

        # Get all the checkboxes from the request
        permissions = []
        states = []

        for i in range(1, 32):
            permission = request.form.get(f'permission{i}')
            state = '/1' if permission == 'on' else '/Off'
            permissions.append(permission)
            states.append(state if state else '/Off')

        # Create a dictionary of the form field names and values
        fields = {'User ID': userid,
                  'EMail': email,
                  'First Name': firstname,
                  'Last Name': lastname,
                  'First Name  Last Name': firstnamelastname,
                  'EMailAdresse': emailadresse,
                  'KID': kid,
                  'Dropdown3': dropdown_value1,
                  'Dropdown4': dropdown_value2,
                  'Text7': comments,
                  'Check Box8': states[0],
                  'Check Box10': states[1],
                  'Check Box11': states[2],
                  'Check Box12': states[3],
                  'Check Box13': states[4],
                  'Check Box14': states[5],
                  'Check Box15': states[6],
                  'Check Box16': states[7],
                  'Check Box17': states[8],
                  'Check Box18': states[9],
                  'Check Box19': states[10],
                  'Check Box20': states[11],
                  'Check Box21': states[12],
                  'Check Box22': states[13],
                  'Check Box23': states[14],
                  'Check Box24': states[15],
                  'Check Box25': states[16],
                  'Check Box26': states[17],
                  'Check Box27': states[18],
                  'Check Box28': states[19],
                  'Check Box29': states[20],
                  'Check Box30': states[21],
                  'Check Box31': states[22],
                  'Check Box32': states[23],
                  'Check Box33': states[24],
                  'Check Box34': states[25],
                  'Check Box35': states[26],
                  'Check Box36': states[27],
                  'Check Box37': states[28],
                  'Check Box38': states[29],
                  'Check Box39': states[30],}

        # Save the filled-out PDF form as a new PDF file
        output_pdf = PdfWriter()
        output_pdf.add_page(template_pdf.pages[0])
        output_pdf.add_page(template_pdf.pages[1])
        output_pdf.update_page_form_field_values(output_pdf.pages[0], fields)
        output_pdf.update_page_form_field_values(output_pdf.pages[1], fields)
        updateCheckboxValues(output_pdf.pages[1], fields)

        output_stream = io.BytesIO()
        output_pdf.write(output_stream)
        output_stream.seek(0)

        # Return the filled-out PDF as a file
        return send_file(output_stream, as_attachment=True, mimetype='application/pdf', download_name='filled.pdf')

def updateCheckboxValues(page, fields):

    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].get_object()
        for field in fields:
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject("/V"): NameObject(fields[field]),
                    NameObject("/AS"): NameObject(fields[field])
                })

if __name__ == '__main__':
    app.run(debug=True)
