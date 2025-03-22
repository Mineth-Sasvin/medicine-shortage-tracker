import sqlite3
from send_notification import send_email
from send_notification import format_email_body

def update_stock(conn, id, new_stock):
    cursor = conn.cursor()
    cursor.execute("UPDATE medicines SET stock = ? WHERE id = ?", (new_stock, id))
    conn.commit()
    
    cursor.execute("SELECT * FROM medicines WHERE id = ?", (id,))
    result = cursor.fetchone()

    if result:
        #Send an email for a successful stock update
        subject = f"Stock Update for {result['name']}"
        body = format_email_body(result['name'], new_stock, result['pharmacy'], is_low_stock=False)
        send_email(result['name'], subject, body)

        #Send a low stock alert if stock < 5
        if new_stock < 5:
            subject = f"⚠️ Low Stock Alert for {result['name']}"
            body = format_email_body(result['name'], new_stock, result['pharmacy'], is_low_stock=True)
            send_email(result['name'], subject, body)

        return result
    else:
        return None
