import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from weasyprint import HTML
from db import db  # Import the db instance
from forms import ResumeForm
from models import Resume  # Import your model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key
app.config['WTF_CSRF_SECRET_KEY'] = 'your_csrf_secret_key_here'  # Replace with a strong CSRF key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}  # Allowed file types
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)  # Initialize the db with the app

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/preview')
def preview():
    return render_template('preview.html')

# Upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('upload_file'))
    
    return render_template('upload.html')

# Route for creating a resume
@app.route('/create_resume', methods=['GET', 'POST'])
def create_resume():
    form = ResumeForm()
    if form.validate_on_submit():
        resume = Resume(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            objective=form.objective.data,
            education=form.education.data,
            experience=form.experience.data,
            skills=form.skills.data
        )
        db.session.add(resume)
        db.session.commit()
        return redirect(url_for('resume', id=resume.id))
    return render_template('create_resume.html', form=form)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to view the resume
@app.route('/resume/<int:id>')
def resume(id):
    resume = Resume.query.get_or_404(id)
    return render_template('resume.html', resume=resume)

# New Route to generate resume PDF
@app.route('/generate_resume_pdf/<int:id>')
def generate_resume_pdf(id):
    # Fetch the resume from the database
    resume = Resume.query.get_or_404(id)
    
    # Prepare the context variables for rendering
    context_variables = {
        'name': resume.name,
        'email': resume.email,
        'phone': resume.phone,
        'objective': resume.objective,
        'education': resume.education,
        'experience': resume.experience,
        'skills': resume.skills.split(',')
    }

    # Render the resume template as an HTML string
    html_string = render_template('resume.html', **context_variables)
    
    # Generate PDF using WeasyPrint
    pdf = HTML(string=html_string).write_pdf()

    # Save the PDF file
    with open(f'resume_{id}.pdf', 'wb') as f:
        f.write(pdf)

    return "PDF generated successfully!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
