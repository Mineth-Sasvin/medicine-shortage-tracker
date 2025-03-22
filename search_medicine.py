import sqlite3

def search_medicine():
    conn = sqlite3.connect('medicine.db')
    cursor = conn.cursor()

    # Take user input for search type
    search_type = input("Search by (1) Medicine Name or (2) Category: ")

    if search_type == '1':
        name = input("Enter medicine name: ")
        cursor.execute("SELECT * FROM medicines WHERE name LIKE ?", ('%' + name + '%',))
    elif search_type == '2':
        category = input("Enter medicine category: ")
        cursor.execute("SELECT * FROM medicines WHERE category LIKE ?", ('%' + category + '%',))
    else:
        print("Invalid option. Try again.")
        conn.close()
        return
    
    # Fetch results
    results = cursor.fetchall()

    if results:
        print("\n=== Search Results ===")
        for row in results:
            print(f"ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Category: {row[2]}")
            print(f"Available Stock: {row[3]}")
            print(f"Pharmacy: {row[4]}")
            print(f"Location: {row[5]}")
            print(f"Last Updated: {row[6]}")
            print("-" * 30)
    else:
        print("No matching records found.")
    
    conn.close()

# Call the search function
if __name__ == "__main__":
    search_medicine()