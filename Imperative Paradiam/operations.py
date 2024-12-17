from db import connect_db

def fetch_books():

    conn = None
    cur = None
    books_list = None

    try:
        conn = connect_db()
        
        if conn is None:
            print("Error: Database connection failed.")
            return books_list

        cur = conn.cursor()
        
        query = "SELECT * FROM books"
        
        cur.execute(query)
        
        books_list = []
        
        while True:
            row = cur.fetchone()
            
            if row is None:
                break
            
            # list of tuple
            book_info = [
                ("bookid", row[0]),
                ("title", row[1]),
                ("author", row[2]),
                ("genre", row[3]),
                ("available", row[4])
            ]
            
            current_book = []
            
            index = 0
            while index < len(book_info):
                current_book.append(book_info[index])
                index = index + 1
            
            books_list.append(current_book)
    
    except Exception as e:
        print("Error retrieving books: " + str(e))
        books_list = None
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    return books_list



def search_books(keyword):
    """Search books by   title, author, or genre."""
    conn = None
    cur = None
    books_list = None

    try:
        conn = connect_db()
        
        if conn is None:
            print("Error: Database connection failed.")
            return books_list

        cur = conn.cursor()
        
        query = """
        SELECT * FROM books 
        WHERE 
            LOWER(' ' || title || ' ') LIKE %s OR 
            LOWER(' ' || author || ' ') LIKE %s OR 
            LOWER(' ' || genre || ' ') LIKE %s
        """
        
        processed_keyword = " "
        
        index = 0
        while index < len(keyword):
            processed_keyword = processed_keyword + keyword[index]
            index = index + 1
        
        processed_keyword = processed_keyword + " "
        processed_keyword = processed_keyword.lower()
        processed_keyword = "% " + processed_keyword.strip() + " %"
        
        params = [processed_keyword, processed_keyword, processed_keyword]
        
        cur.execute(query, params)
        
        books_list = []
        
        while True:
            row = cur.fetchone()
            
            if row is None:
                break
            
            #  list of tuples
            book_info = [
                ("bookid", row[0]),
                ("title", row[1]),
                ("author", row[2]),
                ("genre", row[3]),
                ("available", row[4])
            ]
            
            current_book = []
            
            index = 0
            while index < len(book_info):
                current_book.append(book_info[index])
                index = index + 1
            
            books_list.append(current_book)
    
    except Exception as e:
        print("Error searching books: " + str(e))
        books_list = None
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    return books_list

# def search_books(keyword):
#     """Search books by title, author, or genre."""
#     conn = None
#     cur = None
#     books_list = None

#     try:
#         conn = connect_db()
        
#         if conn is None:
#             print("Error: Database connection failed.")
#             return books_list

#         cur = conn.cursor()
        
#         query = "SELECT * FROM books WHERE title ILIKE %s OR author ILIKE %s OR genre ILIKE %s"
        
#         like_keyword = "%"
        
#         index = 0
#         while index < len(keyword):
#             like_keyword = like_keyword + keyword[index]
#             index = index + 1
#         like_keyword = like_keyword + "%"
        
#         params = [like_keyword, like_keyword, like_keyword]
        
#         cur.execute(query, params)
        
#         books_list = []
        
#         while True:
#             row = cur.fetchone()
            
#             if row is None:
#                 break
            
#             book_info = [
#                 ("bookid", row[0]),
#                 ("title", row[1]),
#                 ("author", row[2]),
#                 ("genre", row[3]),
#                 ("available", row[4])
#             ]
            
#             current_book = []
            
#             index = 0
#             while index < len(book_info):
#                 current_book.append(book_info[index])
#                 index = index + 1
            
#             books_list.append(current_book)
    
#     except Exception as e:
#         # Manual error handling
#         print("Error searching books: " + str(e))
#         books_list = None
    
#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()
    
#     return books_list

def add_book(title, author, genre, available):
    conn = None
    cur = None
    book_added = 0

    if title == "" or author == "" or genre == "":
        print("Error: Title, author, and genre are required.")
        return book_added

    try:
        conn = connect_db()
        
        if conn is None:
            print("Error: Database connection failed.")
            return book_added

        cur = conn.cursor()
        
        query = "INSERT INTO books (title, author, genre, available) VALUES (%s, %s, %s, %s)"
        
        params = [title, author, genre, available]
        
        cur.execute(query, params)
        
        rows_affected = cur.rowcount
        
        if rows_affected > 0:
            conn.commit()
            print("Book added successfully.")
            book_added = 1
        else:
            conn.rollback()
            print("Error: Book addition failed.")
    
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error adding book: " + str(e))
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    return book_added

def remove_book(book_id):
    """Remove a book from the database by its book_id."""
    conn = None
    cur = None
    book_removed = 0

    try:
        conn = connect_db()
        
        if conn is None:
            print("Error: Database connection failed.")
            return book_removed

        cur = conn.cursor()
        
        query = "DELETE FROM books WHERE bookid = %s"
        
        params = [book_id]
        
        cur.execute(query, params)
        
        rows_affected = cur.rowcount
        
        if rows_affected > 0:
            conn.commit()
            print("Book with ID " + str(book_id) + " removed.")
            book_removed = 1
        else:
            conn.rollback()
            print("Book with ID " + str(book_id) + " not found.")
    
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error removing book: " + str(e))
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    return book_removed



def update_book(book_id, title=None, author=None, genre=None, available=None):
    conn = None
    cur = None
    book_updated = 0

    fields = []
    values = []

    if title:
        fields_length = len(fields)
        fields[fields_length:] = ["title = %s"]
        
        values_length = len(values)
        values[values_length:] = [title]
    
    if author:
        fields_length = len(fields)
        fields[fields_length:] = ["author = %s"]
        
        values_length = len(values)
        values[values_length:] = [author]
    
    if genre:
        fields_length = len(fields)
        fields[fields_length:] = ["genre = %s"]
        
        values_length = len(values)
        values[values_length:] = [genre]
    
    if available is not None:
        fields_length = len(fields)
        fields[fields_length:] = ["available = %s"]
        
        values_length = len(values)
        values[values_length:] = [available]

    if len(fields) == 0:
        print("No update fields provided.")
        return book_updated

    try:
        conn = connect_db()
        
        if conn is None:
            print("Error: Database connection failed.")
            return book_updated

        cur = conn.cursor()
        
        query = "UPDATE books SET "
        
        field_string = ""
        field_index = 0
        while field_index < len(fields):
            if field_index > 0:
                field_string = field_string + ", "
            field_string = field_string + fields[field_index]
            field_index = field_index + 1
        
        query = query + field_string + " WHERE bookid = %s"
        
        values_length = len(values)
        values[values_length:] = [book_id]
        
     
        cur.execute(query, values)
        
       
        rows_affected = cur.rowcount
        
      
        if rows_affected > 0:
            conn.commit()
            print("Book with ID " + str(book_id) + " updated.")
            book_updated = 1
        else:
            conn.rollback()
            print("Book with ID " + str(book_id) + " not found.")
    
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error updating book: " + str(e))
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    return book_updated


























