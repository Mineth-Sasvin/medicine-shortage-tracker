import sqlite3
from send_notification import send_email

def update_stock(conn, id, new_stock):
    cursor = conn.cursor()
    cursor.execute("UPDATE medicines SET stock = ? WHERE id = ?", (new_stock, id))
    conn.commit()
    
    cursor.execute("SELECT * FROM medicines WHERE id = ?", (id,))
    result = cursor.fetchone()

    if result:
        #Send an email for a regular stock update
        send_email(result['name'], new_stock, result['pharmacy'])

        #Send a low stock alert if stock < 5
        if new_stock < 5:
            send_email(result['name'], new_stock, result['pharmacy'])
        return result
    else:
        return None
