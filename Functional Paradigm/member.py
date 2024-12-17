
from basics import BasicFunction, DatabaseConnection
from book import BookManagement

class Member(BasicFunction):
    books = BookManagement()
    ids = []
    numMembers = 0
    name = []
    phone = []

    def __init__(self):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM members")
                members = cursor.fetchall()
                self.ids, self.name, self.phone = self.__loadMembersFromDB(members)
                self.numMembers += 1
            except Exception as e:
                print("An error occurred while loading members:", str(e))
            finally:
                connection.close()

    def __loadMembersFromDB(self, members):
        ids = self.custom_map(lambda x: x[0], members)
        names = self.custom_map(lambda x: x[1], members)
        phones =  self.custom_map(lambda x: x[2], members)
        return ids, names, phones
    
    def getIds(self):
        return self.ids
    
    def getNames(self):
        return self.name
    
    def getPhones(self):
        return self.phone

    def __addMemberToDB(self, name, phone):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO members (name, phone) VALUES (%s, %s)",
                    (name, phone)
                )
                connection.commit()
                return True
            except Error:
                return False
            finally:
                cursor.close()
                connection.close()

    def __updateMemberFromDB(self, id, name, phone):
        connection = DatabaseConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()

                cursor.execute("UPDATE members SET name = %s, phone = %s WHERE id = %s", (name, phone, id))
                connection.commit()
                return True
            except Exception:
                return "An error occurred while updating the member:"
            finally:
                connection.close()

    ############ Add Membre ###############
    def addMember(self, name, phone):
        result = self.__addMemberToDB(name, phone)
        if result:
            return "Member added successfully to database!"
        else:
            return "Failed to add a member"

    ############ View Membre ###############
    def viewMember(self, id, nameList, phoneList):
        index = self.getIndexFromList(self.ids, id)
        if index != -1:
            return f"Name: {nameList[index]}, Phone: {phoneList[index]}"
        

    def updatePhone(self, id, newPhone, ids, nameList):
        index = self.getIndexFromList(ids, id)
        result = self.__updateMemberFromDB(id, nameList[index], newPhone)
        if result:
            return f"This '{newPhone}' phone updated successfully!"
        else:
            return f"No phone found with '{newPhone}' phone in database."

    def updateName(self, id, newName, ids, phoneList):
        index = self.getIndexFromList(ids, id)
        result = self.__updateMemberFromDB(id, newName, phoneList[index])
        if result:
            return f"This '{newName}' member name updated successfully!"
        else:
            return f"No member found with '{newName}' name in database."

