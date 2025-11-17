import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import connect_db

# ===================== Mở cửa sổ vật liệu =====================
def open_vatlieu():
    def center_window(win, w=900, h=550):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

    win = tk.Toplevel()
    win.title("Quản lý vật liệu")
    center_window(win)
    win.resizable(False, False)

    tk.Label(win, text="QUẢN LÝ VẬT LIỆU", font=("Arial", 18, "bold")).pack(pady=10)

    # ===================== Frame nhập liệu =====================
    frame = tk.Frame(win)
    frame.pack(pady=5, padx=10, fill="x")

    labels = ["Mã vật liệu", "Tên vật liệu", "Loại vật liệu", "Đơn vị tính", "Giá", "Số lượng"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame, text=label).grid(row=i//2, column=(i%2)*2, padx=5, pady=5, sticky="w")
        entry = tk.Entry(frame, width=25)
        entry.grid(row=i//2, column=(i%2)*2 + 1, padx=5, pady=5)
        entries[label] = entry

    entry_mavl = entries["Mã vật liệu"]
    entry_tenvl = entries["Tên vật liệu"]
    entry_loaivl = entries["Loại vật liệu"]
    entry_dvt = entries["Đơn vị tính"]
    entry_gia = entries["Giá"]
    entry_soluong = entries["Số lượng"]

    # ===================== Bảng dữ liệu =====================
    columns = ("mavl", "tenvl", "loaivl", "dvt", "gia", "soluong")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=12)

    col_names = ["Mã vật liệu", "Tên vật liệu", "Loại vật liệu", "Đơn vị", "Giá", "Số lượng"]
    for col, name in zip(columns, col_names):
        tree.heading(col, text=name)
        tree.column(col, width=130, anchor="center")

    tree.pack(padx=10, pady=10, fill="both")

    # ===================== Hàm làm sạch =====================
    def clear_input():
        for e in entries.values():
            e.delete(0, tk.END)

    # ===================== Load dữ liệu =====================
    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM vatlieu")
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
        finally:
            conn.close()

    # ===================== Thêm =====================
    def add():
        mavl = entry_mavl.get().strip()
        tenvl = entry_tenvl.get().strip()
        loaivl = entry_loaivl.get().strip()
        dvt = entry_dvt.get().strip()
        gia = entry_gia.get().strip()
        soluong = entry_soluong.get().strip()

        if not mavl or not tenvl:
            messagebox.showwarning("Thiếu dữ liệu", "Mã vật liệu và Tên vật liệu là bắt buộc!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO vatlieu VALUES (%s, %s, %s, %s, %s, %s)",
                        (mavl, tenvl, loaivl, dvt, gia, soluong))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm vật liệu!")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    # ===================== Sửa =====================
    def update():
        mavl = entry_mavl.get().strip()
        if not mavl:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn vật liệu để sửa!")
            return

        tenvl = entry_tenvl.get().strip()
        loaivl = entry_loaivl.get().strip()
        dvt = entry_dvt.get().strip()
        gia = entry_gia.get().strip()
        soluong = entry_soluong.get().strip()

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE vatlieu SET tenvl=%s, loaivl=%s, donvitinh=%s, dongia=%s, soluong=%s WHERE mavl=%s",
                (tenvl, loaivl, dvt, gia, soluong, mavl))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật vật liệu!")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    # ===================== Xóa =====================
    def delete():
        selected = tree.selection() 
        if not selected: 
            messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để xóa") 
            return 
        mavl = tree.item(selected)["values"][0] 
        conn = connect_db() 
        cur = conn.cursor() 
        cur.execute("DELETE FROM vatlieu WHERE mavl=%s", (mavl,)) 
        conn.commit() 
        conn.close() 
        load_data() 

    # ===================== Chọn dòng trong bảng =====================
    def select_item(event):
        selected = tree.selection()
        if selected:
            v = tree.item(selected[0], "values")
            entry_mavl.delete(0, tk.END)
            entry_mavl.insert(0, v[0])
            entry_tenvl.delete(0, tk.END)
            entry_tenvl.insert(0, v[1])
            entry_loaivl.delete(0, tk.END)
            entry_loaivl.insert(0, v[2])
            entry_dvt.delete(0, tk.END)
            entry_dvt.insert(0, v[3])
            entry_gia.delete(0, tk.END)
            entry_gia.insert(0, v[4])
            entry_soluong.delete(0, tk.END)
            entry_soluong.insert(0, v[5])

    tree.bind("<ButtonRelease-1>", select_item)

    # ===================== Các nút chức năng =====================
    frame_btn = tk.Frame(win)
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="Thêm", width=10, command=add).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Sửa", width=10, command=update).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Xóa", width=10, command=delete).grid(row=0, column=2, padx=5)
    tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=5)
    tk.Button(frame_btn, text="Thoát", width=10, command=win.destroy).grid(row=0, column=4, padx=5)

    load_data()
