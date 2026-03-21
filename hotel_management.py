import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
 
DB_NAME = "hotel.db"
 
# ================= PAGE COLOR THEMES =================
THEME_WELCOME = {"bg":"#fdebd0", "btn":"#d68910", "title":"#7d6608"}
THEME_LOGIN   = {"bg":"#ebdef0", "btn":"#884ea0", "title":"#512e5f"}
THEME_DASH    = {"bg":"#e8f8f5", "btn":"#148f77", "title":"#0b5345"}
THEME_CUST    = {"bg":"#ebf5fb", "btn":"#2e86c1", "title":"#1b4f72"}
THEME_ROOM    = {"bg":"#fef9e7", "btn":"#b7950b", "title":"#7d6608"}
THEME_BILL    = {"bg":"#eafaf1", "btn":"#1e8449", "title":"#0b5345"}
THEME_THANKS  = {"bg":"#f4ecf7", "btn":"#6c3483", "title":"#512e5f"}
THEME_TABLE   = {"bg":"#f2f3f4", "btn":"#566573", "title":"#2c3e50"}
 
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_LBL   = ("Segoe UI", 10)
FONT_BTN   = ("Segoe UI", 10, "bold")
 
customer = {}
 
# ================= DATABASE =================
def init_db():
   conn = sqlite3.connect(DB_NAME)
   cur = conn.cursor()
 
   cur.execute("""
   CREATE TABLE IF NOT EXISTS rooms(
       room_type TEXT PRIMARY KEY,
       price INTEGER,
       available INTEGER
   )
   """)
 
   cur.execute("SELECT COUNT(*) FROM rooms")
   if cur.fetchone()[0] == 0:
       rooms = [
           ("🆒 AC Room", 2500, 20),
           ("🌬️ Non-AC Room", 2000, 50),
           ("👑 Deluxe Room", 1500, 10)
       ]
       cur.executemany("INSERT INTO rooms VALUES (?,?,?)", rooms)
 
   cur.execute("""
   CREATE TABLE IF NOT EXISTS customers(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT,
       phone TEXT,
       address TEXT,
       room TEXT,
       days INTEGER,
       bill INTEGER,
       status TEXT,
       time TEXT
   )
   """)
   conn.commit()
   conn.close()
 
# ================= COMMON BUTTON =================
def btn(parent, text, cmd, color):
   return tk.Button(parent, text=text, command=cmd,
                    bg=color, fg="white",
                    font=FONT_BTN, width=18, height=1)
 
# ================= WELCOME =================
# ================= WELCOME =================
def welcome_page():
   t = THEME_WELCOME
   root = tk.Tk()
   root.title("🏨 Welcome")
   root.geometry("520x450")
   root.configure(bg=t["bg"])
 
   # Hotel Name
   tk.Label(
       root,
       text="🏨 GOLDEN VILLA 🏨",
       font=("Segoe UI", 24, "bold"),
       fg=t["title"],
       bg=t["bg"]
   ).pack(pady=12)
 
   # Tagline
   tk.Label(
       root,
       text="✨ Luxury • Comfort • Trust • Care ✨",
       font=("Segoe UI", 11, "italic"),
       bg=t["bg"]
   ).pack(pady=4)
 
   # Address
   tk.Label(
       root,
       text=(
           "📍 Mahabaleshwar – Wai,\n"
           "Satara, Maharashtra – 412803"
       ),
       font=FONT_LBL,
       bg=t["bg"],
       justify="center"
   ).pack(pady=8)
 
   # Contact
   tk.Label(
       root,
       text="📞 +91 9876543210 | +91 9123456789",
       font=FONT_LBL,
       bg=t["bg"]
   ).pack(pady=2)
 
   # Email
   tk.Label(
       root,
       text="📧 goldenvilla@gmail.com",
       font=FONT_LBL,
       bg=t["bg"]
   ).pack(pady=2)
 
   # Welcome Message
   tk.Label(
       root,
       text=(
           "🙏 Welcome to Golden Villa 🙏\n"
           "Your comfort is our priority.\n"
           "Enjoy a peaceful stay with us 🌿"
       ),
       font=("Segoe UI", 10),
       bg=t["bg"],
       justify="center"
   ).pack(pady=15)
 
   # Login Button
   btn(
       root,
       "🔐 Admin Login",
       lambda: [root.destroy(), admin_login()],
       t["btn"]
   ).pack(pady=25)
 
   root.mainloop()
 
# ================= ADMIN LOGIN =================
def admin_login():
   t = THEME_LOGIN
   root = tk.Tk()
   root.title("🔐 Login")
   root.geometry("360x260")
   root.configure(bg=t["bg"])
 
   tk.Label(root, text="🔐 Admin Login",
            font=FONT_TITLE, fg=t["title"], bg=t["bg"]).pack(pady=15)
 
   user = tk.Entry(root, width=22)
   pwd = tk.Entry(root, show="*", width=22)
   user.pack(pady=5)
   pwd.pack(pady=5)
 
   def check():
       if user.get() == "admin" and pwd.get() == "1234":
           root.destroy()
           dashboard()
       else:
           messagebox.showerror("Error", "Invalid Login")
 
   btn(root, "Login ✔️", check, t["btn"]).pack(pady=15)
   root.mainloop()
 
# ================= DASHBOARD =================
def dashboard():
   t = THEME_DASH
   root = tk.Tk()
   root.title("📊 Dashboard")
   root.geometry("380x340")
   root.configure(bg=t["bg"])
 
   tk.Label(root, text="📊 Admin Dashboard",
            font=FONT_TITLE, fg=t["title"], bg=t["bg"]).pack(pady=15)
 
   btn(root, "🆕 New Check-In",
       lambda:[root.destroy(), customer_page()], t["btn"]).pack(pady=5)
 
   btn(root, "🚪 Checkout",
       lambda:[root.destroy(), checkout_page()], t["btn"]).pack(pady=5)
 
   btn(root, "📜 History",
       lambda:[root.destroy(), history_page()], t["btn"]).pack(pady=5)
 
   def exit_app():
       if messagebox.askyesno(
           "Exit Confirmation",
           "Are you sure you want to close the application?"
       ):
           root.destroy()
 
   btn(root, "❌ Exit", exit_app, t["btn"]).pack(pady=15)
   root.mainloop()
 
# ================= CUSTOMER =================
def customer_page():
   t = THEME_CUST
   root = tk.Tk()
   root.title("🧍 Customer")
   root.geometry("380x360")
   root.configure(bg=t["bg"])
 
   tk.Label(root, text="🧍 Customer Details",
            font=FONT_TITLE, fg=t["title"], bg=t["bg"]).pack(pady=10)
 
   def field(text, phone=False):
       tk.Label(root, text=text, bg=t["bg"]).pack()
       e = tk.Entry(root, width=26)
       e.pack(pady=4)
       if phone:
           def validate(p): return (p.isdigit() and len(p) <= 10) or p == ""
           e.config(validate="key",
                    validatecommand=(root.register(validate), "%P"))
       return e
 
   name = field("👤 Name")
   phone = field("📱 Phone (10 digits)", phone=True)
   address = field("🏠 Address")
 
   def next_page():
       if len(phone.get()) != 10:
           messagebox.showerror("Error", "Phone must be exactly 10 digits")
           return
       customer["name"] = name.get()
       customer["phone"] = phone.get()
       customer["address"] = address.get()
       root.destroy()
       room_page()
 
   btn(root, "Next ➡️", next_page, t["btn"]).pack(pady=15)
   root.mainloop()
 
# ================= ROOM =================
def room_page():
   t = THEME_ROOM
   root = tk.Tk()
   root.title("🛏️ Rooms")
   root.geometry("420x360")
   root.configure(bg=t["bg"])
 
   tk.Label(root, text="🛏️ Select Room",
            font=FONT_TITLE, fg=t["title"], bg=t["bg"]).pack(pady=10)
 
   conn = sqlite3.connect(DB_NAME)
   cur = conn.cursor()
   cur.execute("SELECT * FROM rooms")
   rooms = cur.fetchall()
   conn.close()
 
   room_var = tk.StringVar(value=rooms[0][0])
   for r in rooms:
       tk.Radiobutton(
           root, text=f"{r[0]} | ₹{r[1]} | Avl: {r[2]}",
           variable=room_var, value=r[0],
           indicatoron=0, width=34,
           bg="#fff9c4", selectcolor="#f7dc6f"
       ).pack(pady=3)
 
   tk.Label(root, text="📅 Days", bg=t["bg"]).pack()
   days = tk.Spinbox(root, from_=1, to=30, width=5)
   days.pack()
 
   btn(root, "Next ➡️",
       lambda:[customer.update({"room":room_var.get(),
                                "days":int(days.get())}),
               root.destroy(), bill_page()],
       t["btn"]).pack(pady=15)
   root.mainloop()
 
# ================= BILL =================
def bill_page():
   t = THEME_BILL
   root = tk.Tk()
   root.title("🧾 Bill")
   root.geometry("420x340")
   root.configure(bg=t["bg"])
 
   conn = sqlite3.connect(DB_NAME)
   cur = conn.cursor()
   cur.execute("SELECT price FROM rooms WHERE room_type=?",
               (customer["room"],))
   price = cur.fetchone()[0]
   conn.close()
 
   total = price * customer["days"]
   customer["bill"] = total
 
   tk.Label(root, text="🧾 TOTAL BILL",
            font=FONT_TITLE, fg=t["title"], bg=t["bg"]).pack(pady=10)
 
   tk.Label(root,
       text=f"👤 {customer['name']}\n🏨 {customer['room']}\n💰 ₹ {total}",
       bg=t["bg"]).pack(pady=10)
 
   def save():
       conn = sqlite3.connect(DB_NAME)
       cur = conn.cursor()
       cur.execute("""
       INSERT INTO customers
       (name, phone, address, room, days, bill, status, time)
       VALUES (?,?,?,?,?,?,?,?)
       """, (
           customer["name"], customer["phone"], customer["address"],
           customer["room"], customer["days"], customer["bill"],
           "Checked-In", datetime.now().strftime("%d-%m-%Y %H:%M")
       ))
       cur.execute("UPDATE rooms SET available = available - 1 WHERE room_type=?",
                   (customer["room"],))
       conn.commit()
       conn.close()
       root.destroy()
       thankyou_page()
 
   btn(root, "Confirm ✔️", save, t["btn"]).pack(pady=10)
   root.mainloop()
 
# ================= THANK YOU =================
def thankyou_page():
   t = THEME_THANKS
   root = tk.Tk()
   root.title("🙏 Thank You")
   root.geometry("420x300")
   root.configure(bg=t["bg"])
 
   tk.Label(root, text="🙏 THANK YOU 🙏",
            font=FONT_TITLE, fg=t["title"], bg=t["bg"]).pack(pady=10)
 
   tk.Label(root,
       text="We truly appreciate your visit.\n"
            "Please visit again, stay safe,\n"
            "and thank you for trusting us.\n"
            "Your comfort and safety mean a lot to us 💖",
       bg=t["bg"], justify="center", font=FONT_LBL).pack(pady=10)
 
   def exit_page():
       if messagebox.askyesno(
           "Confirmation",
           "Are you sure you want to go to Admin Dashboard?"
       ):
           root.destroy()
           dashboard()
 
   btn(root, "Exit ⬅️", exit_page, t["btn"]).pack(pady=15)
   root.mainloop()
 
# ================= CHECKOUT =================
def checkout_page():
   t = THEME_TABLE
   root = tk.Tk()
   root.title("🚪 Checkout")
   root.geometry("750x420")
   root.configure(bg=t["bg"])
 
   tk.Label(root, text="🚪 Checkout Page",
            font=FONT_TITLE, fg=t["title"], bg=t["bg"]).pack(pady=10)
 
   tree = ttk.Treeview(
       root, columns=("id","name","room","status"), show="headings"
   )
   tree.pack(fill="both", expand=True, padx=10, pady=5)
 
   for c in ("id","name","room","status"):
       tree.heading(c, text=c.upper())
 
   tree.tag_configure("checked_in", background="#f8c6d8")   # 🌸 Pink
   tree.tag_configure("checked_out", background="#b7e1cd")  # 🟢 Green
 
   def load_data():
       for i in tree.get_children():
           tree.delete(i)
       conn = sqlite3.connect(DB_NAME)
       cur = conn.cursor()
       cur.execute("SELECT id,name,room,status FROM customers")
       for r in cur.fetchall():
           tag = "checked_in" if r[3] == "Checked-In" else "checked_out"
           tree.insert("", "end", values=r, tags=(tag,))
       conn.close()
 
   load_data()
 
   def checkout():
       if not tree.selection():
           return
       cid, _, room, status = tree.item(tree.selection())["values"]
       if status != "Checked-In":
           return
       conn = sqlite3.connect(DB_NAME)
       cur = conn.cursor()
       cur.execute("UPDATE customers SET status='Checked-Out' WHERE id=?", (cid,))
       cur.execute("UPDATE rooms SET available = available + 1 WHERE room_type=?", (room,))
       conn.commit()
       conn.close()
       messagebox.showinfo("Success", "Checkout Successful")
       load_data()
 
   def exit_page():
       if messagebox.askyesno(
           "Exit Confirmation",
           "Are you sure you want to go to Admin Dashboard?"
       ):
           root.destroy()
           dashboard()
 
   btn(root, "Checkout ✔️", checkout, t["btn"]).pack(pady=6)
   btn(root, "Exit ❌", exit_page, t["btn"]).pack(pady=4)
   root.mainloop()
 
# ================= HISTORY =================
def history_page():
   t = THEME_TABLE
   root = tk.Tk()
   root.title("📜 History")
   root.geometry("700x400")
   root.configure(bg=t["bg"])
 
   tk.Label(root, text="📜 Customer History",
            font=FONT_TITLE, fg=t["title"], bg=t["bg"]).pack(pady=10)
 
   tree = ttk.Treeview(
       root, columns=("id","name","room","status"), show="headings"
   )
   tree.pack(fill="both", expand=True)
 
   for c in ("id","name","room","status"):
       tree.heading(c, text=c.upper())
 
   conn = sqlite3.connect(DB_NAME)
   cur = conn.cursor()
   cur.execute("SELECT id,name,room,status FROM customers")
   for r in cur.fetchall():
       tree.insert("", "end", values=r)
   conn.close()
 
   def exit_page():
       if messagebox.askyesno(
           "Exit Confirmation",
           "Are you sure you want to go to Admin Dashboard?"
       ):
           root.destroy()
           dashboard()
 
   btn(root, "Exit ❌", exit_page, t["btn"]).pack(pady=10)
   root.mainloop()
 
# ================= START =================
init_db()
welcome_page()
