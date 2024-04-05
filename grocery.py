import mysql.connector

class Groceries:
    def __init__(self):
        try:
            # Establishing a connection to the MySQL database
            self.conn = mysql.connector.connect(user='root', password='Ranjith@5018', host='localhost', database='app', auth_plugin='mysql_native_password')
            self.my_cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return

        self.pin = '123'
        self.is_authenticated = self.authenticate()

        if not self.is_authenticated:
            print('Invalid PIN. Exiting program.')
            return

        self.groceries = self.load_groceries_from_db()

    def authenticate(self):
        try:
            pin_attempt = input('Enter PIN: ')
            if pin_attempt == self.pin:
                return True
            else:
                print('Invalid PIN. Exiting program.')
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def load_groceries_from_db(self):
        try:
            self.my_cursor.execute("select * from groceries")
            return self.my_cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []


    def find_grocery(self):
        try:
            choice = input("Please type 'name' to find by name, 'type' to find by type, 'quantity' to find by quantity, or 'price' to find by price: ")

            if choice in ('name', 'type', 'quantity', 'price'):
                search_term = input(f"What are you looking for? (by {choice}): ")
                matching_groceries = [grocery for grocery in self.groceries if grocery[self.get_index(choice)] == search_term]
                if matching_groceries:
                    for gro in matching_groceries:
                        print(f"Name: {gro[1]}, Type: {gro[2]}, Quantity: {gro[3]}, Price: {gro[4]}")
                else:
                    print(f"No groceries found matching {choice}: {search_term}")
            else:
                print("Invalid option. Please try again with a valid input.")

        except Exception as e:
            print(f"Error: {e}")


    def get_index(self, choice):
        # Returns the index corresponding to the choice made by the user
        # This method assumes that the order of elements in the tuples is: id, name, type, quantity, price
        if choice == 'name':
            return 1
        elif choice == 'type':
            return 2
        elif choice == 'quantity':
            return 3
        elif choice == 'price':
            return 4
        else:
            raise ValueError("Invalid choice")


    def add_grocery(self):
        try:
            g_name = input("Please input name: ")
            g_type = input("Please input type: ")
            quantity = input("Please input quantity: ")
            price = input("Please input price: ")

            # Validate price as numeric
            if not price.isdigit():
                print("Invalid price. Please enter a valid number.")
                return

            # Insert new grocery data into the database
            insert_query = "INSERT INTO groceries (id, g_name, g_type, quantity, price) VALUES (NULL, %s, %s, %s, %s)"
            data = (g_name, g_type, quantity, price)
            self.my_cursor.execute(insert_query, data)
            self.conn.commit()  # Commit the transaction
            print(f"The grocery has been added to your collection:\n")
            self.groceries = self.load_groceries_from_db()  # Refresh the local grocery list from the database
            self.view_grocery()
        except mysql.connector.Error as err:
            self.conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error: {err}")


    def view_grocery(self):
        if not self.groceries:
            print("No groceries in your collection.")
        else:
            for grocery in self.groceries:
                print(f"ID: {grocery[0]}, Name: {grocery[1]}, Type: {grocery[2]}, Quantity: {grocery[3]}, Price: {grocery[4]}")


    def update_grocery(self):
        try:
            g_id = input("Enter the ID of the grocery you want to update: ")
            new_quantity = input("Enter the new quantity: ")
            new_price = input("Enter the new price: ")

            # Validate price as numeric
            if not new_price.isdigit():
                print("Invalid price. Please enter a valid number.")
                return

            # Update grocery data in the database
            update_query = "UPDATE groceries SET quantity = %s, price = %s WHERE id = %s"
            data = (new_quantity, new_price, g_id)
            self.my_cursor.execute(update_query, data)
            self.conn.commit()  # Commit the transaction
            print(f"The grocery with ID {g_id} has been updated.")
            self.groceries = self.load_groceries_from_db()  # Refresh the local grocery list from the database
        except mysql.connector.Error as err:
            self.conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error: {err}")


    def delete_grocery(self):
        try:
            g_id = input("Enter the ID of the grocery you want to delete: ")

            # Delete grocery data from the database
            delete_query = "DELETE FROM groceries WHERE id = %s"
            data = (g_id,)
            self.my_cursor.execute(delete_query, data)
            self.conn.commit()  # Commit the transaction
            print(f"The grocery with ID {g_id} has been deleted.")
            self.groceries = self.load_groceries_from_db()  # Refresh the local grocery list from the database
        except mysql.connector.Error as err:
            self.conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error: {err}")



def main():
    new_grocery = Groceries()

    if not new_grocery.is_authenticated:
        print('Invalid PIN. Exiting program.')
        return

    while True:
        try:
            inp = input("Options: 'find', 'add', 'update', 'delete', 'view', 'end'\nWhat would you like to do: ").strip().lower()
            if inp == "find":
                new_grocery.find_grocery()
            elif inp == "add":
                new_grocery.add_grocery()
            elif inp == "update":
                new_grocery.update_grocery()
            elif inp == "delete":
                new_grocery.delete_grocery()
            elif inp == "view":
                new_grocery.view_grocery()
            elif inp == "end":
                print("\nThank you! \n Visit again")
                break
            else:
                print("\nInvalid option. Please try again.\n")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()








