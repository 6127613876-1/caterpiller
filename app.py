from flask import Flask, render_template, request, redirect, session, url_for
import pyrebase, dropbox, os, bcrypt, json
import google.generativeai as genai
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
import re
import subprocess
from flask import render_template_string
import pandas as pd
from flask import send_from_directory, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import docx
import openpyxl
from flask import jsonify, send_from_directory
from flask import render_template_string
from video_summarizer import video_data, summarize, TEMPLATE, SUMMARY_DIR





load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret_key'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
UPLOAD_FOLDER = 'uploads'
SUMMARY_FOLDER = 'summaries'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SUMMARY_FOLDER'] = SUMMARY_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Google OAuth setup
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to="google_auth",
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ]
)

app.register_blueprint(google_bp, url_prefix="/login")

# Firebase config
firebase_config = {
    "apiKey": "AIzaSyBCHKvaapkyDiYSPvIS-XYatw8_4oWUEBI",
    "authDomain": "caterpillar-fa475.firebaseapp.com",
    "databaseURL": "https://caterpillar-fa475-default-rtdb.firebaseio.com",
    "projectId": "caterpillar-fa475",
    "storageBucket": "caterpillar-fa475.appspot.com",
    "messagingSenderId": "1049817279301",
    "appId": "1:1049817279301:web:a270bd2145757e9a88ac2c",
    "measurementId": "G-CFJ41VV7M7"
}
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Dropbox and Gemini setup
dbx = dropbox.Dropbox(os.getenv("DROPBOX_ACCESS_TOKEN"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/text-bison-001')

def clean_department(dept):
    return re.sub(r'\s+', '_', dept.strip().lower())



@app.route('/')
def index():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        department = clean_department(request.form['department'])
        users = db.child("users").get()

        for user in users.each() if users.each() else []:
            if user.val().get('email') == email:
                return render_template('signup.html', status="Email already registered.", success=False)

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.child("users").push({
            "username": username,
            "email": email,
            "password": hashed_pw.decode('utf-8'),
            "role": "user",
            "department": department
        })

        return redirect('/login?status=Account created successfully&success=true')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    status = request.args.get("status")
    success = request.args.get("success") == "true"

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = db.child("users").get()

        for user in users.each() if users.each() else []:
            data = user.val()
            if data['email'] == email:
                if bcrypt.checkpw(password.encode('utf-8'), data['password'].encode('utf-8')):
                    session['user'] = email
                    session['username'] = data.get('username', 'User')
                    session['role'] = data.get('role', 'user')
                    session['department'] = data.get('department', '')
                    session['user_id'] = user.key()  # ✅ Store user_id here
                    return redirect('/admin' if session['role'] == 'admin' else '/dashboard')

                else:
                    return render_template('login.html', status="Invalid password.", success=False)

        return render_template('login.html', status="User not found.", success=False)

    return render_template('login.html', status=status, success=success)

@app.route('/google_auth')
def google_auth():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Failed to fetch user info from Google", 401

    user_info = resp.json()
    email = user_info["email"]
    username = user_info.get("name", "GoogleUser")

    users = db.child("users").order_by_child("email").equal_to(email).get()
    role = "user"
    department = "NotSet"

    if users.each():
        for user in users.each():
            role = user.val().get("role", "user")
            department = user.val().get("department", "NotSet")
            session['user_id'] = user.key()  # ✅ Store user ID from Firebase
            break
    else:
        new_user = db.child("users").push({
            "username": username,
            "email": email,
            "password": "",
            "role": role,
            "department": department
        })
        session['user_id'] = new_user['name']  # ✅ Store new user's Firebase key

    session['user'] = email
    session['username'] = username
    session['role'] = role
    session['department'] = department

    # Redirect to department selection if not set
    if department == "NotSet":
        return redirect('/select-department')

    return redirect('/admin' if role == 'admin' else '/dashboard')


@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    user_data = db.child("users").child(user_id).get().val()

    if user_data.get("department") == "NotSet":
        return redirect(url_for("select_department"))

    return render_template(
        "dashboard.html",
        name=user_data["username"],  # 👈 Add this line
        email=user_data["email"],
        department=user_data["department"]
    )




@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if session.get('role') != 'admin':
        return redirect('/login')

    users = db.child("users").get()
    user_list = []
    for user in users.each() if users.each() else []:
        data = user.val()
        user_list.append({
            "key": user.key(),
            "username": data.get("username", ""),
            "email": data.get("email", ""),
            "role": data.get("role", "user"),
            "department": data.get("department", "Unknown")
        })

    task_data = db.child("department_tasks").get().val() or {}
    selected_dept = clean_department(request.form.get("department")) if request.method == 'POST' else None
    task_text = "\n".join(task_data.get(selected_dept, [])) if selected_dept else ""

    return render_template("admin.html", users=user_list, task_data=task_data,
                           selected_dept=selected_dept, task_text=task_text)

@app.route('/update_tasks', methods=['POST'])
def update_tasks():
    if session.get('role') != 'admin':
        return redirect('/login')

    department = clean_department(request.form.get('department'))
    tasks_text = request.form.get('tasks')

    if not department or tasks_text is None:
        return "Invalid form submission", 400

    tasks = [t.strip() for t in tasks_text.splitlines() if t.strip()]
    db.child("department_tasks").child(department).set(tasks)

    return redirect('/admin')

@app.route('/update_user/<user_key>', methods=['POST'])
def update_user(user_key):
    if session.get('role') != 'admin':
        return redirect('/login')

    new_dept = clean_department(request.form.get('department'))
    if not new_dept:
        return "Invalid department", 400

    db.child("users").child(user_key).update({"department": new_dept})
    return redirect('/admin')

@app.route('/delete_user/<user_key>')
def delete_user(user_key):
    if session.get('role') == 'admin':
        db.child("users").child(user_key).remove()
    return redirect('/admin')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
@app.route("/select-department", methods=["GET", "POST"])
def select_department():
    if request.method == "POST":
        department = request.form.get("department")
        user_id = session.get("user_id")

        if user_id and department:
            db.child("users").child(user_id).update({"department": department})
            session['department'] = department  # Optional: update session immediately
            return redirect(url_for("dashboard"))

    return render_template("select_department.html")

@app.route('/simulate', methods=['POST'])
def simulate():
    return render_template('simulation.html')

@app.route('/calculate-time', methods=['POST'])
def calculate_time():
    return render_template('time.html')
def estimate_task_time(df):
    # Base Formula
    df['Estimated_Task_Time'] = (df['Load Cycles'] * 5) + df['Idling Time (min)'] + (df['Fuel Used (L)'] * 10)
    
    def adjust(row):
        factor = 1.0
        if row['Environmental Conditions'] in ['Foggy', 'Snowy', 'Rainy']:
            factor += 0.2
        if row['Safety Alert Triggered'].strip().lower() == 'yes':
            factor += 0.1
        return row['Estimated_Task_Time'] * factor

    df['Adjusted_Task_Time'] = df.apply(adjust, axis=1)
    df['Adjusted_Task_Time'] = df['Adjusted_Task_Time'].round(2)
    return df
@app.route('/manual', methods=['POST'])
def manual():
    try:
        # Get input values
        load_cycles = int(request.form['load_cycles'])
        idling_time = float(request.form['idling_time'])
        fuel_used = float(request.form['fuel_used'])
        env_conditions = request.form['environmental_conditions']
        safety_alert = request.form['safety_alert']

        df = pd.DataFrame([{
            'Load Cycles': load_cycles,
            'Idling Time (min)': idling_time,
            'Fuel Used (L)': fuel_used,
            'Environmental Conditions': env_conditions,
            'Safety Alert Triggered': safety_alert
        }])

        df = estimate_task_time(df)

        row = df.iloc[0].to_dict()

        result = f"""
            <b>Estimated Task Time:</b> {row['Estimated_Task_Time']:.2f} min<br>
            <b>Adjusted Task Time:</b> {row['Adjusted_Task_Time']:.2f} min
        """

        return render_template('time.html', result=result)
    except Exception as e:
        return f"Error: {e}", 400
def extract_text(filepath):
    if '.' not in filepath:
        raise ValueError(f"Invalid file path: '{filepath}' does not have an extension.")
    
    ext = filepath.rsplit('.', 1)[1].lower()
    text = ""

    if ext == 'pdf':
        reader = PdfReader(filepath)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    elif ext == 'docx':
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + '\n'
    elif ext == 'xlsx':
        wb = openpyxl.load_workbook(filepath)
        for sheet in wb:
            for row in sheet.iter_rows(values_only=True):
                text += ' '.join(str(cell) for cell in row if cell) + '\n'
    else:
        raise ValueError(f"Unsupported file type: '{ext}'")

    return text.strip()

def summarize_text(text):
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(f"Summarize the following:\n\n{text}")
        return response.text.strip()
    except Exception as e:
        print("Summarize error:", e)
        return "⚠️ Failed to summarize."

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file", 400
    file = request.files['file']
    if file.filename == '':
        return "No filename", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return redirect(url_for('dashboard'))  # or a new upload status page
    return "Invalid file type", 400

@app.route('/summarize/<filename>', methods=['POST'])
def summarize_document(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    text = extract_text(filepath)
    summary = summarize_text(text)
    
    summary_file = os.path.join(app.config['SUMMARY_FOLDER'], f"{filename}_summary.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    return jsonify({'summary': summary, 'download': f"/download/{filename}_summary.txt"})

@app.route('/ask/<filename>', methods=['POST'])
def ask_question(filename):
    try:
        question = request.json.get("question", "")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        document_text = extract_text(filepath)

        # Truncate if too long
        if len(document_text) > 12000:
            document_text = document_text[:12000]

        prompt = f"""
        Based on the document content below, answer the question in no more than 3 lines.

        Document:
        {document_text}

        Question:
        {question}

        Answer:
        """
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        answer = response.text.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        print("Ask error:", e)
        return jsonify({"answer": "⚠️ Failed to get an answer."}), 500

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(app.config['SUMMARY_FOLDER'], filename, as_attachment=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route('/ask-bot')
def ask_bot():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('doubt-bot.html', files=files)
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        summary_path = os.path.join(app.config['SUMMARY_FOLDER'], f"{filename}_summary.txt")

        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(summary_path):
            os.remove(summary_path)

        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Delete error: {e}")
        return jsonify({'status': 'error'}), 500
@app.route("/video-summary", methods=["GET", "POST"])
def video_summary():
    category = request.form.get("category", "wheel_tractor")
    action = request.form.get("action", "view")
    summary = summarize(category) if action == "summarize" else None
    return render_template_string(TEMPLATE, videos=video_data[category], category=category, summary=summary)
@app.route('/summarize/<filename>', methods=['POST'])
def summarize_file(filename):
    return summarize_document(filename)
@app.route('/contact')
def contact():
    return render_template('emailjs.html')


if __name__ == '__main__':
    app.run(debug=True)
