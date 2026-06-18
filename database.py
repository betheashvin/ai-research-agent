import sqlite3

DB_NAME = "research.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
                 CREATE TABLE IF NOT EXISTS reports(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 topic TEXT NOT NULL,
                 report TEXT NOT NULL, 
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                 """)
    conn.commit()
    conn.close()

def save_report(topic, report):
    conn = sqlite3.connect(DB_NAME)

    conn.execute("INSERT INTO reports(topic, report) VALUES(?, ?)", (topic, report))

    conn.commit()
    conn.close()

def get_reports():
    
    conn = sqlite3.connect(DB_NAME)

    reports = conn.execute("""
                           SELECT id, topic, created_at
                           FROM reports
                           ORDER BY id DESC 
                           """).fetchall()
    conn.close()

    return reports

def get_report(report_id):

    conn = sqlite3.connect(DB_NAME)

    report = conn.execute("""
                          SELECT * 
                          FROM REPORTS 
                          WHERE ID = ? 
                          """, (report_id,)).fetchone()
    
    conn.close()

    return report

def delete_report(report_id):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("DELETE FROM reports WHERE id=?", (report_id,))

    conn.commit()
    conn.close()


