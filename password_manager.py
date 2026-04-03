import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import string
 
# ---------------- DATABASE ----------------
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()
 
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
   username TEXT PRIMARY KEY,
   password TEXT
)
""")
 
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   website TEXT,
   username TEXT,
   password TEXT
)
""")
 
cursor.execute("INSERT OR IGNORE INTO users VALUES ('Abhi','abhi33')")
conn.commit()
 
# ---------------- PASSWORD VALIDATION ----------------
def is_valid_password(password):
   if len(password) < 10: return False
   if not any(c.isupper() for c in password): return False
   if not any(c.islower() for c in password): return False
   if not any(c.isdigit() for c in password): return False
   if not any(c in string.punctuation for c in password): return False
   return True
 
# ---------------- PASSWORD GENERATOR ----------------
def generate_password():
   chars = string.ascii_letters + string.digits + string.punctuation
   pwd = (
       random.choice(string.ascii_uppercase) +
       random.choice(string.ascii_lowercase) +
       random.choice(string.digits) +
       random.choice(string.punctuation) +
       ''.join(random.choice(chars) for _ in range(6))
   )
   pwd = ''.join(random.sample(pwd, len(pwd)))
   password_entry.delete(0, tk.END)
   password_entry.insert(0, pwd)
 
# ---------------- PASSWORD FUNCTIONS ----------------
def save_password():
   if not is_valid_password(password_entry.get()):
       messagebox.showerror("Invalid Password", "Password must be strong!")
       return
   cursor.execute("INSERT INTO passwords VALUES (NULL,?,?,?)",
                  (website_entry.get(), user_entry.get(), password_entry.get()))
   conn.commit()
   load_data()
   clear_fields()
 
def update_password():
   if not is_valid_password(password_entry.get()):
       messagebox.showerror("Invalid Password", "Password must be strong!")
       return
   pid = listbox.get(listbox.curselection())[0]
   cursor.execute("UPDATE passwords SET website=?,username=?,password=? WHERE id=?",
                  (website_entry.get(), user_entry.get(), password_entry.get(), pid))
   conn.commit()
   load_data()
   clear_fields()
 
def delete_password():
   pid = listbox.get(listbox.curselection())[0]
   cursor.execute("DELETE FROM passwords WHERE id=?", (pid,))
   conn.commit()
   load_data()
 
def load_data():
   listbox.delete(0, tk.END)
   for row in cursor.execute("SELECT * FROM passwords"):
       listbox.insert(tk.END, row)
 
def fill_fields(e):
   d = listbox.get(listbox.curselection())
   website_entry.delete(0, tk.END)
   user_entry.delete(0, tk.END)
   password_entry.delete(0, tk.END)
   website_entry.insert(0, d[1])
   user_entry.insert(0, d[2])
   password_entry.insert(0, d[3])
 
def clear_fields():
   website_entry.delete(0, tk.END)
   user_entry.delete(0, tk.END)
   password_entry.delete(0, tk.END)
 
# ---------------- PASSWORD MANAGER UI ----------------
def main_app():
   global root, website_entry, user_entry, password_entry, listbox
 
   root = tk.Tk()
   root.title("🔐 Password Manager")
   root.geometry("900x600")
   root.configure(bg="#0f172a")
 
   tk.Label(root, text="🔐 PASSWORD MANAGER",
            font=("Segoe UI", 26, "bold"),
            bg="#0f172a", fg="#38bdf8").pack(pady=15)
 
   card = tk.Frame(root, bg="#020617", bd=3, relief="ridge")
   card.pack(pady=10)
 
   def lbl(txt,r):
       tk.Label(card, text=txt, bg="#020617", fg="white",
                font=("Segoe UI", 12)).grid(row=r, column=0, pady=8, padx=10)
 
   lbl("🌐 Website",0)
   website_entry = tk.Entry(card, width=40)
   website_entry.grid(row=0, column=1)
 
   lbl("👤 Username / Email",1)
   user_entry = tk.Entry(card, width=40)
   user_entry.grid(row=1, column=1)
 
   lbl("🔑 Password",2)
   password_entry = tk.Entry(card, width=40)
   password_entry.grid(row=2, column=1)
 
   tk.Button(card, text="✨ Generate Password", command=generate_password,
             bg="#22c55e", fg="white", font=("Segoe UI", 11, "bold"),
             width=25).grid(row=3, columnspan=2, pady=10)
 
   btns = tk.Frame(root, bg="#0f172a")
   btns.pack()
 
   tk.Button(btns, text="💾 SAVE", command=save_password,
             bg="#3b82f6", fg="white", width=12).grid(row=0, column=0, padx=8)
 
   tk.Button(btns, text="✏ UPDATE", command=update_password,
             bg="#f59e0b", fg="white", width=12).grid(row=0, column=1, padx=8)
 
   tk.Button(btns, text="🗑 DELETE", command=delete_password,
             bg="#ef4444", fg="white", width=12).grid(row=0, column=2, padx=8)
 
   listbox = tk.Listbox(root, width=110, height=10)
   listbox.pack(pady=20)
   listbox.bind("<<ListboxSelect>>", fill_fields)
 
   load_data()
   root.mainloop()
 
# ---------------- REGISTER ----------------
def open_register():
   r = tk.Toplevel()
   r.title("Register")
   r.geometry("350x300")
   r.configure(bg="#020617")
 
   tk.Label(r, text="📝 Register User",
            font=("Segoe UI", 20, "bold"),
            bg="#020617", fg="#38bdf8").pack(pady=15)
 
   ru = tk.Entry(r, width=30)
   rp = tk.Entry(r, show="*", width=30)
   ru.pack(pady=5); rp.pack(pady=5)
 
   def reg():
       try:
           cursor.execute("INSERT INTO users VALUES (?,?)", (ru.get(), rp.get()))
           conn.commit()
           messagebox.showinfo("Success", "User Registered")
           r.destroy()
       except:
           messagebox.showerror("Error", "Username exists")
 
   tk.Button(r, text="Register", command=reg,
             bg="#22c55e", fg="white", width=20).pack(pady=15)
 
# ---------------- VIEW USERS ----------------
def view_users():
   v = tk.Toplevel()
   v.title("Users")
   v.geometry("300x300")
   lb = tk.Listbox(v, width=30)
   lb.pack(pady=20)
   for u in cursor.execute("SELECT username FROM users"):
       lb.insert(tk.END, u[0])
 
# ---------------- LOGIN ----------------
def login():
   cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (lu.get(), lp.get()))
   if cursor.fetchone():
       login_window.destroy()
       main_app()
   else:
       messagebox.showerror("Error", "Invalid Login")
 
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x420")
login_window.configure(bg="#020617")
 
tk.Label(login_window, text="🔐 Secure Login",
        font=("Segoe UI", 24, "bold"),
        bg="#020617", fg="#38bdf8").pack(pady=30)
 
lu = tk.Entry(login_window, width=30)
lp = tk.Entry(login_window, show="*", width=30)
lu.pack(pady=8); lp.pack(pady=8)
 
tk.Button(login_window, text="🚀 LOGIN", command=login,
         bg="#3b82f6", fg="white", width=22).pack(pady=10)
 
tk.Button(login_window, text="➕ Register User",
         command=open_register,
         bg="#22c55e", fg="white", width=22).pack(pady=5)
 
tk.Button(login_window, text="👥 View Users",
         command=view_users,
         bg="#64748b", fg="white", width=22).pack(pady=5)
 
login_window.mainloop()