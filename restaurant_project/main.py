import customtkinter as ctk
import sqlite3
import pandas as pd
from model import predict_review
import matplotlib.pyplot as plt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

OWNER_CODE = "REST123"

# Database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS food_data(
food TEXT PRIMARY KEY,
total_customers INTEGER,
positive_reviews INTEGER,
negative_reviews INTEGER,
positive_rate REAL,
negative_rate REAL
)
""")
conn.commit()

# -------------------------
# Submit Review
# -------------------------
def submit_review():

    food = food_var.get()
    review = review_entry.get()

    if food == "" or review == "":
        result_label.configure(text="Enter all fields ❌")
        return

    sentiment = predict_review(review)

    cursor.execute("SELECT * FROM food_data WHERE food=?", (food,))
    data = cursor.fetchone()

    if data is None:
        if sentiment == "positive":
            cursor.execute("INSERT INTO food_data VALUES(?,?,?,?,?,?)",
            (food,1,1,0,100,0))
        else:
            cursor.execute("INSERT INTO food_data VALUES(?,?,?,?,?,?)",
            (food,1,0,1,0,100))
    else:
        total = data[1] + 1
        pos = data[2]
        neg = data[3]

        if sentiment == "positive":
            pos += 1
        else:
            neg += 1

        pos_rate = (pos/total)*100
        neg_rate = (neg/total)*100

        cursor.execute("""
        UPDATE food_data SET total_customers=?,positive_reviews=?,
        negative_reviews=?,positive_rate=?,negative_rate=? WHERE food=?
        """,(total,pos,neg,pos_rate,neg_rate,food))

    conn.commit()
    result_label.configure(text=f"Saved: {sentiment} ✅")

# -------------------------
# Dashboard
# -------------------------
def owner_dashboard():

    if code_entry.get() != OWNER_CODE:
        result_label.configure(text="Wrong Code ❌")
        return

    dash = ctk.CTkToplevel(root)
    dash.title("Dashboard")

    df = pd.read_sql_query("SELECT * FROM food_data", conn)

    df["status"] = df["positive_rate"].apply(
        lambda x: "Good" if x > 70 else "Improve"
    )

    text = ctk.CTkTextbox(dash, width=500, height=300)
    text.pack(pady=20)

    text.insert("0.0", str(df))

# -------------------------
# Graph
# -------------------------
def show_graph():

    df = pd.read_sql_query("SELECT * FROM food_data", conn)

    if df.empty:
        result_label.configure(text="No Data ❌")
        return

    plt.bar(df['food'], df['positive_reviews'])
    plt.title("Food Popularity")
    plt.xticks(rotation=30)
    plt.show()

# -------------------------
# Excel Export
# -------------------------
def export_excel():

    df = pd.read_sql_query("SELECT * FROM food_data", conn)

    if df.empty:
        result_label.configure(text="No Data ❌")
        return

    df["status"] = df["positive_rate"].apply(
        lambda x: "Good" if x > 70 else "Improve"
    )

    df.to_excel("food_report.xlsx", index=False)

    result_label.configure(text="Excel Saved ✅")

# -------------------------
# GUI Layout
# -------------------------
root = ctk.CTk()
root.geometry("420x550")
root.title("🍽 Restaurant AI Dashboard")

title = ctk.CTkLabel(root, text="Restaurant Analytics", font=("Poppins", 20, "bold"))
title.pack(pady=15)

# Food Dropdown
food_var = ctk.StringVar()

food_menu = ctk.CTkComboBox(root, variable=food_var,
values=["idli","dosa","vada","biryani","ice cream","noodles"])
food_menu.pack(pady=10)

# Review Entry
review_entry = ctk.CTkEntry(root, placeholder_text="Enter Review")
review_entry.pack(pady=10)

# Buttons
ctk.CTkButton(root, text="Submit Review", command=submit_review).pack(pady=10)

code_entry = ctk.CTkEntry(root, placeholder_text="Owner Code")
code_entry.pack(pady=10)

ctk.CTkButton(root, text="Dashboard", command=owner_dashboard).pack(pady=10)
ctk.CTkButton(root, text="Show Graph", command=show_graph).pack(pady=10)
ctk.CTkButton(root, text="Export Excel", command=export_excel).pack(pady=10)

result_label = ctk.CTkLabel(root, text="")
result_label.pack(pady=10)

root.mainloop()