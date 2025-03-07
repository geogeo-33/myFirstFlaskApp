import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            final_time REAL
        )
    ''')
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    init_db()
    print('データベースを初期化しました!')