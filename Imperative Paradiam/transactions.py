from db import connect_db

def manual_execute_and_fetch(cursor, query, params=None):

    cursor.execute(query, params) if params else cursor.execute(query)
    
    results = []
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        results.append(row)
    
    return results


def record_borrowing(member_id, bookid):
    """Record when a book is borrowed using imperative approach."""
    conn = connect_db()
    try:
        cur = conn.cursor()
        
        # Check if the book exists
        book_rows = manual_execute_and_fetch(cur, "SELECT * FROM books WHERE bookid = %s", (bookid,))
        if not book_rows:
            print(f"Error: Book {bookid} does not exist in the library.")
            return
        
        # Check if the book is currently borrowed
        transaction_rows = manual_execute_and_fetch(
            cur, 
            """
            SELECT transaction_type 
            FROM transactions 
            WHERE bookid = %s 
            ORDER BY transaction_date DESC 
            LIMIT 1
            """, 
            (bookid,)
        )
        
        if transaction_rows and transaction_rows[0][0] == 'borrow':
            print(f"Error: Book {bookid} is currently borrowed by another member.")
            return
        
        # Check if the member is active
        member_rows = manual_execute_and_fetch(
            cur, 
            "SELECT active FROM members WHERE member_id = %s", 
            (member_id,)
        )
        
        if not member_rows:
            print(f"Error: Member {member_id} does not exist.")
            return
        
        if not member_rows[0][0]:
            print(f"Error: Member {member_id} is not active and cannot borrow books.")
            return
        
        # Insert a new transaction
        cur.execute(
            """
            INSERT INTO transactions (member_id, bookid, transaction_type)
            VALUES (%s, %s, 'borrow')
            """, 
            (member_id, bookid)
        )
        
        conn.commit()
        print(f"Book {bookid} borrowed by Member {member_id}.")
    
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    
    finally:
        cur.close()
        conn.close()



def record_returning(member_id, bookid):
    """Record when a book is returned using imperative approach."""
    conn = connect_db()
    try:
        cur = conn.cursor()
        
        # Check if the book exists
        book_rows = manual_execute_and_fetch(cur, "SELECT * FROM books WHERE bookid = %s", (bookid,))
        if not book_rows:
            print(f"Error: Book {bookid} does not exist in the library.")
            return
        
        # Check if the member has borrowed the book and not yet returned it
        transaction_rows = manual_execute_and_fetch(
            cur, 
            """
            SELECT transaction_type 
            FROM transactions 
            WHERE member_id = %s AND bookid = %s 
            ORDER BY transaction_date DESC 
            LIMIT 1
            """, 
            (member_id, bookid)
        )
        
        if not transaction_rows or transaction_rows[0][0] != 'borrow':
            print(f"Error: Member {member_id} has not borrowed Book {bookid} or it has already been returned.")
            return
        
        # If All okay
        cur.execute(
            """
            INSERT INTO transactions (member_id, bookid, transaction_type)
            VALUES (%s, %s, 'return')
            """, 
            (member_id, bookid)
        )
        
        conn.commit()
        print(f"Book {bookid} returned by Member {member_id}.")
    
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    
    finally:
        cur.close()
        conn.close()
































