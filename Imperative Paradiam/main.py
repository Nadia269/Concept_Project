import sys
import json
from db import init_db
from operations import fetch_books, search_books, add_book, remove_book, update_book
from members import register_member, view_members, update_member
from transactions import record_borrowing, record_returning
from Reports import report_available_books, report_member_history

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Missing command. Usage: python library_db.py <command> [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init_db()
        print("Database initialized.")
    elif command == "fetch":
        print(json.dumps(fetch_books(), indent=2))
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Missing keyword for search. Usage: python library_db.py search <keyword>")
            sys.exit(1)
        keyword = sys.argv[2]
        print(json.dumps(search_books(keyword), indent=2))
    elif command == "add":
        if len(sys.argv) < 6:
            print("Error: Missing arguments for add. Usage: python library_db.py add <title> <author> <genre> <available>")
            sys.exit(1)
        title = sys.argv[2]
        author = sys.argv[3]
        genre = sys.argv[4]
        available = sys.argv[5].lower() == "true"
        add_book(title, author, genre, available)
        print(f"Book '{title}' added.")
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Error: Missing book_id for removal. Usage: python library_db.py remove <book_id>")
            sys.exit(1)
        book_id = int(sys.argv[2])
        remove_book(book_id)
    elif command == "update":
        if len(sys.argv) < 5:
            print("Error: Missing arguments for update. Usage: python library_db.py update <book_id> <field> <value>")
            sys.exit(1)
        book_id = int(sys.argv[2])
        field = sys.argv[3]
        value = sys.argv[4]
        if field == "title":
            update_book(book_id, title=value)
        elif field == "author":
            update_book(book_id, author=value)
        elif field == "genre":
            update_book(book_id, genre=value)
        elif field == "available":
            update_book(book_id, available=value.lower() == "true")
        else:
            print("Error: Unknown field for update.")
            sys.exit(1)
    elif command == "register_member":
        if len(sys.argv) < 4:
            print("Error: Missing arguments. Usage: python library_db.py register_member <name> <email> [phone]")
            sys.exit(1)
        name = sys.argv[2]
        email = sys.argv[3]
        phone = sys.argv[4] if len(sys.argv) > 4 else None
        register_member(name, email, phone)
    elif command == "view_members":
        print(json.dumps(view_members(), indent=2))
    elif command == "update_member":
        if len(sys.argv) < 5:
            print("Error: Missing arguments. Usage: python library_db.py update_member <member_id> <field> <value>")
            sys.exit(1)
        member_id = int(sys.argv[2])
        field = sys.argv[3]
        value = sys.argv[4]
        if field == "name":
            update_member(member_id, name=value)
        elif field == "email":
            update_member(member_id, email=value)
        elif field == "phone":
            update_member(member_id, phone=value)
        elif field == "active":
            update_member(member_id, active=value.lower() == "true")
        else:
            print("Error: Unknown field for update.")
            sys.exit(1)
    elif command == "borrow":
        if len(sys.argv) < 4:
            print("Error: Missing arguments. Usage: python library_db.py borrow <member_id> <bookid>")
            sys.exit(1)
        member_id = int(sys.argv[2])
        bookid = int(sys.argv[3])
        record_borrowing(member_id, bookid)
    elif command == "return":
        if len(sys.argv) < 4:
            print("Error: Missing arguments. Usage: python library_db.py return <member_id> <bookid>")
            sys.exit(1)
        member_id = int(sys.argv[2])
        bookid = int(sys.argv[3])
        record_returning(member_id, bookid)
    elif command == "report_available_books":
        report = report_available_books()
        print("\nAvailable Books Report:")
        for book in report:
            print(book)
    elif command == "report_member_history":
        if len(sys.argv) < 3:
            print("Error: Missing member_id. Usage: python library_db.py report_member_history <member_id>")
            sys.exit(1)
        member_id = int(sys.argv[2])
        report = report_member_history(member_id)
        print(f"\nBorrowing History for Member {member_id}:")
        for record in report:
            print(record)
    else:
        print(f"Error: Unknown command '{command}'.")
        print("Available commands: init, fetch, search, add, remove, update, register_member, view_members, update_member, borrow, return, report_available_books, report_member_history.")
        sys.exit(1)




















