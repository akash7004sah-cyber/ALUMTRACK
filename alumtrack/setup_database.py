import sqlite3

# Create database
connection = sqlite3.connect("alumtrack.db")

cursor = connection.cursor()

# Create alumni table
cursor.execute("""
CREATE TABLE IF NOT EXISTS alumni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    course TEXT,
    graduation_year INTEGER,
    company TEXT,
    position TEXT,
    industry TEXT,
    location TEXT,
    status TEXT,
    verified TEXT
)
""")

# Delete old demo data
cursor.execute("DELETE FROM alumni")

# 20 demo alumni
alumni = [
    ("Rahul Sharma", "rahul@gmail.com", "BBA AI & DS", 2026, "Google", "Software Engineer", "Technology", "Bengaluru", "Working", "Verified"),
    ("Aman Kumar", "aman@gmail.com", "BCA Data Science", 2025, "TCS", "Data Analyst", "IT", "Mumbai", "Working", "Verified"),
    ("Priya Singh", "priya@gmail.com", "BBA", 2024, "Deloitte", "Business Analyst", "Finance", "Bengaluru", "Working", "Verified"),
    ("Rohit Verma", "rohit@gmail.com", "BCA", 2023, "Infosys", "Developer", "IT", "Pune", "Working", "Verified"),
    ("Neha Gupta", "neha@gmail.com", "BBA AI & DS", 2026, "Microsoft", "Data Scientist", "Technology", "Hyderabad", "Working", "Verified"),
    ("Arjun Das", "arjun@gmail.com", "BCA Data Science", 2025, "Accenture", "Software Developer", "IT", "Bengaluru", "Working", "Pending"),
    ("Sneha Patel", "sneha@gmail.com", "BBA", 2024, "EY", "Consultant", "Finance", "Mumbai", "Working", "Verified"),
    ("Karan Mehta", "karan@gmail.com", "BCA", 2023, "Amazon", "Cloud Engineer", "Technology", "Chennai", "Working", "Verified"),
    ("Ananya Roy", "ananya@gmail.com", "BBA AI & DS", 2025, "IBM", "Data Analyst", "Technology", "Kolkata", "Working", "Verified"),
    ("Vivek Singh", "vivek@gmail.com", "BCA Data Science", 2024, "Wipro", "Developer", "IT", "Bengaluru", "Working", "Pending"),
    ("Riya Sharma", "riya@gmail.com", "BBA", 2023, "KPMG", "Financial Analyst", "Finance", "Delhi", "Working", "Verified"),
    ("Aditya Kumar", "aditya@gmail.com", "BCA", 2025, "Flipkart", "Software Engineer", "E-commerce", "Bengaluru", "Working", "Verified"),
    ("Simran Kaur", "simran@gmail.com", "BBA AI & DS", 2026, "Infosys", "AI Analyst", "Technology", "Pune", "Working", "Verified"),
    ("Nikhil Jain", "nikhil@gmail.com", "BCA Data Science", 2024, "Capgemini", "Data Engineer", "IT", "Bengaluru", "Working", "Pending"),
    ("Pooja Das", "pooja@gmail.com", "BBA", 2023, "HDFC Bank", "Business Analyst", "Banking", "Mumbai", "Working", "Verified"),
    ("Aryan Gupta", "aryan@gmail.com", "BCA", 2025, "Swiggy", "Product Analyst", "E-commerce", "Bengaluru", "Working", "Verified"),
    ("Ishita Roy", "ishita@gmail.com", "BBA AI & DS", 2024, "Deloitte", "Data Consultant", "Technology", "Hyderabad", "Working", "Verified"),
    ("Manish Kumar", "manish@gmail.com", "BCA Data Science", 2023, "Tech Mahindra", "Developer", "IT", "Pune", "Working", "Pending"),
    ("Tanya Singh", "tanya@gmail.com", "BBA", 2025, "Accenture", "HR Analyst", "Consulting", "Bengaluru", "Working", "Verified"),
    ("Dev Raj", "dev@gmail.com", "BCA", 2024, "Startup", "Founder", "Entrepreneurship", "Bengaluru", "Entrepreneur", "Verified")
]

cursor.executemany("""
INSERT INTO alumni
(name, email, course, graduation_year, company, position,
industry, location, status, verified)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", alumni)

connection.commit()
connection.close()

print("Database created successfully!")
print("20 alumni added!")