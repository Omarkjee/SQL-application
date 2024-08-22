import sqlite3  # or mysql.connector for MySQL

def create_view():
    conn = sqlite3.connect('DOCTORAL.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE VIEW SCHOLARSHIP_DETAILS AS
    SELECT PHDSTUDENT.StudentId AS StuId, 
           PHDSTUDENT.FName AS StuFName, 
           PHDSTUDENT.LName AS StuLName, 
           SCHOLARSHIPSUPPORT.ScholarshipID AS ScholId, 
           SCHOLARSHIP.Type AS ScholType
    FROM PHDSTUDENT
    JOIN SCHOLARSHIPSUPPORT ON PHDSTUDENT.StudentId = SCHOLARSHIPSUPPORT.StudentId
    JOIN SCHOLARSHIP ON SCHOLARSHIPSUPPORT.ScholarshipID = SCHOLARSHIP.ScholarshipID;
    ''')
    conn.commit()
    conn.close()

def query_view_A():
    conn = sqlite3.connect('DOCTORAL.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT StuId, StuFName, StuLName, ScholType 
    FROM SCHOLARSHIP_DETAILS;
    ''')
    results = cursor.fetchall()
    conn.close()
    return results

# Similarly, create functions for query B and C.

# Run the view creation and query functions
create_view()
print(query_view_A())
