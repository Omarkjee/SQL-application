from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup and initialization
def init_db():
    conn = sqlite3.connect('doctoral.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PHDSTUDENT (
            StudentId TEXT PRIMARY KEY,
            FName TEXT,
            LName TEXT,
            StSem TEXT,
            StYear INTEGER,
            Supervisor TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SCHOLARSHIP (
            ScholarshipID TEXT PRIMARY KEY,
            Type TEXT,
            Source TEXT,
            FundingCountry TEXT,
            FundingOrganization TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SCHOLARSHIPSUPPORT (
            StudentId TEXT,
            ScholarshipId TEXT,
            MonthlyStipend REAL,
            Category TEXT,
            FOREIGN KEY(StudentId) REFERENCES PHDSTUDENT(StudentId),
            FOREIGN KEY(ScholarshipId) REFERENCES SCHOLARSHIP(ScholarshipID)
        )
    ''')

    # Insert sample data
    cursor.executemany('''
        INSERT OR IGNORE INTO PHDSTUDENT (StudentId, FName, LName, StSem, StYear, Supervisor)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        ('AA1234', 'Abimbola', 'Abioye', 'Fall', 2016, 'AO5671'),
        ('AA2345', 'Afia', 'Achebe', 'Fall', 2016, 'AO5671'),
        # Add all other records here
    ])

    cursor.executemany('''
        INSERT OR IGNORE INTO SCHOLARSHIP (ScholarshipID, Type, Source, FundingCountry, FundingOrganization)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        ('SCH1001', 'Merit-Based', 'Government', 'USA', 'National Science Foundation'),
        ('SCH1002', 'Need-Based', 'Private', 'Canada', 'The Gates Scholarship'),
        # Add all other records here
    ])

    cursor.executemany('''
        INSERT OR IGNORE INTO SCHOLARSHIPSUPPORT (StudentId, ScholarshipId, MonthlyStipend, Category)
        VALUES (?, ?, ?, ?)
    ''', [
        ('AJ1836', 'SCH1001', 1000.00, 'local'),
        ('VB1059', 'SCH1001', 1000.00, 'local'),
        # Add all other records here
    ])

    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('doctoral.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM PHDSTUDENT').fetchall()
    scholarships = conn.execute('SELECT * FROM SCHOLARSHIP').fetchall()
    conn.close()
    return render_template('index.html', students=students, scholarships=scholarships)

@app.route('/insert_instructor', methods=['GET', 'POST'])
def insert_instructor():
    if request.method == 'POST':
        student_id = request.form['student_id']
        fname = request.form['fname']
        lname = request.form['lname']
        stsem = request.form['stsem']
        styear = request.form['styear']
        supervisor = request.form['supervisor']
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO PHDSTUDENT (StudentId, FName, LName, StSem, StYear, Supervisor)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, fname, lname, stsem, styear, supervisor))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('insert_instructor.html')

@app.route('/update_instructor', methods=['GET', 'POST'])
def update_instructor():
    if request.method == 'POST':
        student_id = request.form['student_id']
        new_fname = request.form['new_fname']
        new_lname = request.form['new_lname']
        
        conn = get_db_connection()
        conn.execute('''
            UPDATE PHDSTUDENT
            SET FName = ?, LName = ?
            WHERE StudentId = ?
        ''', (new_fname, new_lname, student_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('update_instructor.html')

@app.route('/delete_gra', methods=['GET', 'POST'])
def delete_gra():
    if request.method == 'POST':
        student_id = request.form['student_id']
        
        conn = get_db_connection()
        conn.execute('''
            DELETE FROM PHDSTUDENT
            WHERE StudentId = ?
        ''', (student_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('delete_gra.html')

if __name__ == '__main__':
    app.run(debug=True)
