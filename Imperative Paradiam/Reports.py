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

def report_available_books():

    query = "SELECT bookid, title, author, genre FROM Books WHERE available = TRUE"
    
    conn = connect_db()
    try:
        cursor = conn.cursor()
        
        rows = manual_execute_and_fetch(cursor, query)
        
        result = []
        index = 0
        while index < len(rows):
            row = rows[index]
            result.append({
                "Book ID": row[0],
                "Title": row[1],
                "Author": row[2],
                "Genre": row[3],
            })
            index += 1
        
        return result
    
    except Exception as e:
        print(f"An error occurred while generating available books report: {e}")
        return []
    
    finally:
        cursor.close()
        conn.close()

def report_member_history(member_id):

    query = """
        SELECT t.transaction_id, t.bookid, b.title, t.transaction_type, t.transaction_date
        FROM Transactions t
        JOIN Books b ON t.bookid = b.bookid
        WHERE t.member_id = %s
        ORDER BY t.transaction_date
    """
    
    conn = connect_db()
    try:
        cursor = conn.cursor()
        
        rows = manual_execute_and_fetch(cursor, query, (member_id,))
        
        result = []
        index = 0
        while index < len(rows):
            row = rows[index]
            # list of dictory 
            result.append({
                "Transaction ID": row[0],
                "Book ID": row[1],
                "Book Title": row[2],
                "Action": row[3],
                "Date": row[4],
            })
            index += 1
        
        return result
    
    except Exception as e:
        print(f"An error occurred while generating member history report: {e}")
        return []
    
    finally:
        cursor.close()
        conn.close()

























