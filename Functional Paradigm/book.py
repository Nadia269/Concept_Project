
from basics import BasicFunction, DatabaseConnection

class BookManagement(BasicFunction):
    ids = []
    authorList = []
    genreList = []
    titleList = []
    lengthBooks = 0

    def __init__(self):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM books")
                books = cursor.fetchall()

                self.ids, self.titleList, self.authorList, self.genreList = self.__loadBooksFromDB(books)
                self.lengthBooks = len(self.ids)

            except Exception as e:
                print("An error occurred while loading books:", str(e))
            finally:
                connection.close()

    def getIds(self):
        return self.ids
    
    def getTitles(self):
        return self.titleList
    
    def getAuthors(self):
        return self.authorList
    
    def getGenres(self):
        return self.genreList


    def __loadBooksFromDB(self, books):
        ids = self.custom_map(lambda x: x[0], books)
        titles = self.custom_map(lambda x: x[1], books)
        authors =  self.custom_map(lambda x: x[2], books)
        genres =  self.custom_map(lambda x: x[3], books)
        return ids, titles, authors, genres


    def __addBookToDB(self, title, author, genre):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)",
                    (title, author, genre)
                )
                connection.commit()
                return True
            except Exception:
                return False
            finally:
                cursor.close()
                connection.close()


    def __removeBookFromDB(self, id):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM books WHERE id = %s", (id,))
                connection.commit()
                if cursor.rowcount > 0:
                    return True
                else:
                    return False
            except Exception:
                return False
            finally:
                cursor.close()
                connection.close()


    def __updateBookFromDB(self, id, title, author, genre):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute(
                    "UPDATE books SET title = %s, author = %s, genre = %s WHERE id = %s",
                    (title, author, genre, id)
                )
                connection.commit()
                return True
            except Exception:
                return False
            finally:
                connection.close()
    
    def __lamAsDict(self, index, titleList, authorList, genreList):
        return {
            "title": titleList[index],
            "author": authorList[index],
            "genre": genreList[index]
        }
    

    ############### Add Book ###################
    def addBook(self, title, author, genre):
        result = self.__addBookToDB(title, author, genre)
        if result:
            return "Book added successfully to database!"
        else:
            return "Failed to add book."


    ############### Remove Book ###################
    def removeBook(self, id):
        result = self.__removeBookFromDB(id)
        if result:
            return f"Book with ID '{id}' removed successfully."
        else:
            return f"No book found with ID '{id}' in database."


    ############### Update #####################
    def updateTitle(self, id, newTitle, ids, authorList, genreList):
        index = self.getIndexFromList(ids, id)
        result = self.__updateBookFromDB(id, newTitle, authorList[index], genreList[index])
        if result:
            return f"This '{newTitle}' book updated successfully!"
        else:
            return f"No book found with '{newTitle}' title in database."
        

    def updateAuthor(self, id, newAuthor, ids, titleList, genreList):
        index = self.getIndexFromList(ids, id)
        result = self.__updateBookFromDB(id, titleList[index], newAuthor, genreList[index])
        if result:
            return f"This '{newAuthor}' name updated successfully!"
        else:
            return f"No book found for '{newAuthor}' in database."
        

    def updateGenre(self, id, newGenre, ids, titleList, authorList):
        index = self.getIndexFromList(ids, id)
        result = self.__updateBookFromDB(id, titleList[index], authorList[index], newGenre)
        if result:
            return f"This '{newGenre}' genre updated successfully!"
        else:
            return f"No book found for this '{newGenre}' in database."


    ##################### Search ############################
    def searchTitleBook(self, title, titleList, authorList, genreList):
        index = self.getIndexFromList(titleList, title)
        if index != -1:
            return f"Title: {titleList[index]}, Author: {authorList[index]}, Genre: {genreList[index]}"
        else:
            return f"No book with the title '{title}' was found!"

        
    def searchAuthorBook(self, author, titleList, authorList, genreList):
        indices = self.getAllIndicesFromList(authorList, author)
        
        if self.lenArr(indices) == 0:
            return f"No book found again with the author name '{author}'"
        
        results = self.custom_map(lambda index: self.__lamAsDict(index, titleList, authorList, genreList), indices)   
        return results
    

    def searchGenreBook(self, genre, titleList, authorList, genreList):
        indices = self.getAllIndicesFromList(genreList, genre)
        if self.lenArr(indices) == 0:
            return f"No book found with this genre '{genre}'"
                
        results = self.custom_map(lambda index: self.__lamAsDict(index, titleList, authorList, genreList), indices)
        return results


    ##################### GetAll ############################
    def getAllBooks(self, titleList, authorList, genreList):
        length = self.lenArr(titleList)
        if length == 0:
            return []
        
        results = self.custom_map(
            lambda index: self.__lamAsDict(index, titleList, authorList, genreList),
            list(range(length))
        )
        return results


