import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Sample data to insert into the table
sample_data = [
    ('Paracetamol', 'Painkiller', 20, 'ABC Pharmacy', 'Colombo'),
    ('Amoxicillin', 'Antibiotic', 0, 'XYZ Pharmacy', 'Kandy'),
    ('Insulin', 'Hormone', 5, 'MedCare', 'Galle'),
    ('Cetirizine', 'Antihistamine', 30, 'MediMart', 'Jaffna'),
    ('Ibuprofen', 'Painkiller', 10, 'HealthFirst', 'Colombo')
]

# Insert the sample data
for data in sample_data:
    cursor.execute('''
        INSERT INTO medicines (name, category, stock, pharmacy, location)
        VALUES (?, ?, ?, ?, ?)
    ''', data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Sample data inserted successfully!")