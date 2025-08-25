from flask import Flask, render_template, request, send_file, make_response
from fpdf import FPDF
import qrcode
from io import BytesIO
import os
from database import init_db, insert_ticket, get_ticket
import random

app = Flask(__name__)

# Initialize database once at startup
init_db()

app.config['EVENT_POSTER_PATH'] = 'static/triwizard_poster.png'


def draw_ticket(pdf, name, ticket_no, event, email, date, time, venue, event_img_path):
    pdf.add_page(format=(260, 110))
    pdf.set_fill_color(245, 240, 230)
    pdf.rect(0, 0, 260, 110, 'F')

    pdf.set_xy(10, 20)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(40, 10, "TRIWIZARD ID", ln=2)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(40, 10, ticket_no, ln=2)
    pdf.set_font("Arial", "", 12)
    pdf.cell(40, 10, name, ln=2)
    pdf.cell(40, 10, email, ln=2)

    qr_data = f"{name}|{ticket_no}|{event}|{email}"
    qr_img = qrcode.make(qr_data)
    qr_io = BytesIO()
    qr_img.save(qr_io)
    qr_io.seek(0)
    pdf.image(qr_io, x=15, y=50, w=40, h=40)

    pdf.set_xy(70, 16)
    pdf.set_font("Arial", "B", 17)
    pdf.cell(0, 10, "YOUR TICKET")

    pdf.set_font("Arial", "B", 12)
    pdf.set_xy(70, 36)
    pdf.cell(0, 8, "EVENT:", ln=0)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f" {event}", ln=1)

    pdf.set_font("Arial", "B", 12)
    pdf.set_xy(70, 44)
    pdf.cell(20, 8, "DATE:")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f" {date}", ln=1)

    pdf.set_font("Arial", "B", 12)
    pdf.set_xy(70, 52)
    pdf.cell(20, 8, "TIME:")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f" {time}", ln=1)

    pdf.set_font("Arial", "B", 12)
    pdf.set_xy(70, 60)
    pdf.cell(20, 8, "VENUE:")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f" {venue}", ln=1)

    if os.path.exists(event_img_path):
        pdf.image(event_img_path, x=75, y=72, w=38, h=30)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/triwizard')
def triwizard():
    return render_template('triwizard.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name', 'Unknown')
        ticket_no = request.form.get('ticket_no', 'N/A')
        event = request.form.get('event', 'N/A')
        email = request.form.get('email', 'N/A')
        date = "10th - 11th September, 2025"
        time = "09:00 AM"
        venue = "SRM Vadapalani Auditorium"
        event_img = app.config['EVENT_POSTER_PATH']

        ticket_data = {
            'ticket_no': ticket_no,
            'name': name,
            'event': event,
            'email': email,
            'date': date,
            'time': time,
            'venue': venue,
        }
        insert_ticket(ticket_data)

        pdf = FPDF()
        draw_ticket(pdf, name, ticket_no, event, email, date, time, venue, event_img)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response = make_response(pdf_output.read())
            response.headers['Content-Type'] = 'application/pdf'
            return response
        else:
            return send_file(pdf_output, mimetype='application/pdf',
                             download_name=f'Triwizard_Ticket_{ticket_no}.pdf',
                             as_attachment=True)

    event_prefill = request.args.get('event', '')
    ticket_no_generated = random.randint(1000, 9999)
    return render_template('form.html', event_prefill=event_prefill, ticket_no_generated=ticket_no_generated)
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    ticket_info = None
    error = None
    if request.method == 'POST':
        ticket_no = request.form.get('ticket_no')
        ticket_info = get_ticket(ticket_no)
        if not ticket_info:
            error = "Invalid or not found ticket ID"
    return render_template('verify.html', ticket=ticket_info, error=error)



if __name__ == '__main__':
    app.run(debug=True)
