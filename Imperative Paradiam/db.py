import psycopg2

DATABASE_URL = "postgresql://postgres:1234@localhost/library"

def connect_db():  
    return psycopg2.connect(DATABASE_URL)

def init_db():
    with connect_db() as conn:  
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    bookid SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    author VARCHAR NOT NULL,
                    genre VARCHAR NOT NULL,
                    available BOOLEAN DEFAULT TRUE
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    member_id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    email VARCHAR UNIQUE NOT NULL,
                    phone VARCHAR(15),
                    active BOOLEAN DEFAULT TRUE
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id SERIAL PRIMARY KEY,
                    member_id INT NOT NULL REFERENCES members(member_id),
                    bookid INT NOT NULL REFERENCES books(bookid),
                    transaction_type VARCHAR(10) NOT NULL,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
