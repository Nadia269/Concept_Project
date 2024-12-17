
from db import connect_db


def view_members():
    conn = None
    cur = None
    members_list = None

    try:
        conn = connect_db()
        
        if conn is None:
            print("Error: Database connection failed.")
            return members_list

        cur = conn.cursor()
        
        query = "SELECT * FROM members"
        
        cur.execute(query)
        
        members_list = []
        
        while True:
            row = cur.fetchone()
            
            if row is None:
                break
            
            member_info = [
                ("member_id", row[0]),
                ("name", row[1]),
                ("email", row[2]),
                ("phone", row[3]),
                ("active", row[4])
            ]
            
            current_member = []
            
            for i in range(len(member_info)):
                current_member.append(member_info[i])
            
            members_list.append(current_member)
        
        if members_list:
            print("Members List:")
            list_index = 0
            while list_index < len(members_list):
                member = members_list[list_index]
                
                member_str = "Member ID: "
                
                detail_index = 0
                while detail_index < len(member):
                    if member[detail_index][0] == "member_id":
                        member_str = member_str + str(member[detail_index][1]) + ", "
                    elif member[detail_index][0] == "name":
                        member_str = member_str + "Name: " + member[detail_index][1] + ", "
                    elif member[detail_index][0] == "email":
                        member_str = member_str + "Email: " + member[detail_index][1] + ", "
                    
                    detail_index = detail_index + 1
                
                print(member_str)
                
                list_index = list_index + 1
    
    except Exception as e:
        print("Error retrieving members: " + str(e))
        members_list = None
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    return members_list





def register_member(name, email, phone):
    registration_successful = 0
    conn = None
    cur = None

    if name == "" or email == "":
        print("Error: Name and email are required.")
        return registration_successful

    try:
        conn = connect_db()
        
        if conn is None:
            print("Error: Database connection failed.")
            return registration_successful

        cur = conn.cursor()
        
        query = "INSERT INTO members (name, email, phone, active) VALUES (%s, %s, %s, %s)"
        
        params = [name, email, phone, True] 

        cur.execute(query, params)
        
        rows_affected = cur.rowcount
        
        if rows_affected > 0:
            conn.commit()
            print("Member '" + name + "' added successfully.")
            registration_successful = 1
        else:
            conn.rollback()
            print("Error: Member registration failed.")
    
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error during registration: " + str(e))
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    return registration_successful





def update_member(member_id, name=None, email=None, phone=None, active=None):
   
    update_successful = False
    query_parts = []
    param_values = []

    with connect_db() as conn:
        with conn.cursor() as cur:
            if name is not None:
                query_parts.append("name = %s")
                param_values.append(name)
            
            if email is not None:
                query_parts.append("email = %s")
                param_values.append(email)
            
            if phone is not None:
                query_parts.append("phone = %s")
                param_values.append(phone)
            
            if active is not None:
                query_parts.append("active = %s")
                param_values.append(1 if active else 0)
            
            if len(query_parts) == 0:
                print("No update parameters provided.")
                return False

            query = "UPDATE members SET " + ", ".join(query_parts) + " WHERE member_id = %s"
            
            param_values.append(member_id)

            try:
                cur.execute(query, param_values)

                if cur.rowcount > 0:
                    conn.commit()
                    update_successful = True
                    print(f"Member with ID {member_id} updated successfully.")
                else:
                    print(f"No member found with ID {member_id}.")

            except Exception as e:
                conn.rollback()
                print(f"Error updating member: {e}")
                update_successful = False

    return update_successful

















