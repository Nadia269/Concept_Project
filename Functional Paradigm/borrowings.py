
from basics import BasicFunction, DatabaseConnection
from book import BookManagement
from member import Member

class Borrowings(BasicFunction):
    books = BookManagement()
    members = Member()
    borrowDate = []
    returnDate = []
    titleBookBorrowing = []
    memberBorrowing = []
    ids = []

    def __init__(self):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM borrowings")
                borrowings = cursor.fetchall()
                self.ids, self.memberBorrowing, self.titleBookBorrowing, self.borrowDate, self.returnDate = self.__loadBorrowingFromDB(borrowings)
            except Exception:
                return "An error occurred while loading members:"
            finally:
                connection.close()

    def getIds(self):
        return self.ids
    
    def getBooks(self):
        return self.books

    def getMembers(self):
        return self.members
    
    def getTitleBookBorrowing(self):
        return self.titleBookBorrowing
    
    def getBorrowDate(self):
        return self.borrowDate
    
    def getReturnDate(self):
        return self.returnDate

    def __loadBorrowingFromDB(self, borrowings):
        ids = self.custom_map(lambda x: x[0], borrowings)
        memberBorrowing = self.custom_map(lambda x: x[1], borrowings)
        titleBookBorrowing = self.custom_map(lambda x: x[2], borrowings)
        borrowDate =  self.custom_map(lambda x: x[3], borrowings)
        returnDate =  self.custom_map(lambda x: x[4], borrowings)
        return ids, memberBorrowing, titleBookBorrowing, borrowDate, returnDate

    def __addBorrowToDB(self, memberId, bookId, borrowDate, returnDate):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO borrowings (member_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)",
                    (memberId, bookId, borrowDate, returnDate)
                )
                connection.commit()
                return "Borrowing has been successfully added to the database!"
            except Exception:
                return f"Failed to add borrowing"
            finally:
                cursor.close()
                connection.close()
        
    def __lamAsDict(self, index):
        return {
            "member": self.memberBorrowing[index],
            "borrowDate": self.borrowDate[index],
            "returnDate": self.returnDate[index],
        }
    
    def borrowBook(self, id_member, id_book, borrowDate, returnDate, booksList, membersList,):
        isValidBook = self.getIndexFromList(booksList.ids, id_book)
        isValidMember = self.getIndexFromList(membersList.ids, id_member)
        if isValidBook > -1 and isValidMember > -1:
            self.__addBorrowToDB(id_member, id_book, borrowDate, returnDate)
            return f"'{booksList.titleList[isValidBook]}' borrowed by {membersList.name[isValidMember]} on {borrowDate} and returned on {returnDate}"

    def historyBook(self, id_book):
        indices = self.getAllIndicesFromList(self.titleBookBorrowing, id_book)
        if self.lenArr(indices) == 0:
            return []
        return self.custom_map(self.__lamAsDict, indices)

    # def historyMember(self, titleBookBorrowingList, memberBorrowingList, borrowDateList, returnDateList):
    #     length = self.lenArr(titleBookBorrowingList)
    #     if length == 0:
    #         return []
    #     return self.custom_map(lambda index: self.__lamAsDict(index, titleBookBorrowingList, memberBorrowingList, borrowDateList, returnDateList), list(range(length)))

    def historyMember(self, id_member, indices = None):
        if indices == None:
            indices = self.getAllIndicesFromList(self.memberBorrowing, id_member)
        if self.lenArr(indices) == 0:
            return
        
        # print(indices)
        currentIndex = indices[0] 
        titleId = self.titleBookBorrowing[currentIndex]
        titleIndex = self.getIndexFromList(self.books.ids, titleId)
        memberIndex = self.getIndexFromList(self.members.ids, id_member)

        # print(titleIndex)
        print(f"'{self.members.name[memberIndex]}' borrowed {self.books.titleList[titleIndex]} on {self.borrowDate[currentIndex]} and returned on {self.returnDate[currentIndex]}")
        self.historyMember(id_member, indices[1:]) 





