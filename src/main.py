from flask import Flask, render_template
import mysql.connector
app = Flask(__name__)
try:
    con=mysql.connector.connect(host='localhost',
                                user='root',
                                password='your_password',
                                database='QMS')
    print("Database connected successfully!")

except mysql.connector.Error as e:
    print("Database connection failed:", e)
    con = None
@app.route("/")

#Home Page
def home():
    cur=con.cursor()
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
