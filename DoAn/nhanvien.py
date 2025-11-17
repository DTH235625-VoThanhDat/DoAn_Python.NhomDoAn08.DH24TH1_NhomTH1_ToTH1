import tkinter as tk
from tkinter import ttk, messagebox
from DoAn.db_connect import connect_db

def open_nhanvien():
    def center_window(win, w=700, h=500):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    win = tk.Toplevel()
    win.title("Quản lý nhân viên")
    center_window(win)
    win.resizable(False, False)

    tk.Label(win, text="QUẢN LÝ NHÂN VIÊN", font=("Arial", 18, "bold")).pack(pady=10)

    frame_input = tk.Frame(win)
    frame_input.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_input, text="Mã NV").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_manv = tk.Entry(frame_input, width=20)
    entry_manv.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Tên NV").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_tennv = tk.Entry(frame_input, width=25)
    entry_tennv.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Giới tính").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    gender_var = tk.StringVar(value="nam")
    tk.Radiobutton(frame_input, text="Nam", variable=gender_var, value="nam").grid(row=1, column=1, sticky="w")
    tk.Radiobutton(frame_input, text="Nữ", variable=gender_var, value="nu").grid(row=1, column=1, padx=60, sticky="w")

    tk.Label(frame_input, text="Chức vụ").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_chucvu = tk.Entry(frame_input, width=25)
    entry_chucvu.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="SĐT").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_sdt = tk.Entry(frame_input, width=20)
    entry_sdt.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Địa chỉ").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_diachi = tk.Entry(frame_input, width=25)
    entry_diachi.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    columns = ("manv", "tennv", "gioitinh", "chucvu", "sdt", "diachi")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=100, anchor="center")
    tree.pack(padx=10, pady=10, fill="both")

    entries = [entry_manv, entry_tennv, entry_chucvu, entry_sdt, entry_diachi]

    def clear_input():
        gender_var.set("nam")
        for e in entries:
            e.delete(0, tk.END)

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM nhanvien")
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
        finally:
            conn.close()

    def add():
        manv = entry_manv.get().strip()
        tennv = entry_tennv.get().strip()
        gioitinh = gender_var.get()
        chucvu = entry_chucvu.get().strip()
        sdt = entry_sdt.get().strip()
        diachi = entry_diachi.get().strip()

        if not manv or not tennv:
            messagebox.showwarning("Thiếu dữ liệu", "Mã NV và Tên NV là bắt buộc!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO nhanvien VALUES (%s,%s,%s,%s,%s,%s)",
                        (manv, tennv, gioitinh, chucvu, sdt, diachi))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm nhân viên!")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def update():
        manv = entry_manv.get().strip()
        tennv = entry_tennv.get().strip()
        gioitinh = gender_var.get()
        chucvu = entry_chucvu.get().strip()
        sdt = entry_sdt.get().strip()
        diachi = entry_diachi.get().strip()

        if not manv:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn nhân viên để sửa!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("""UPDATE nhanvien SET tennv=%s, gioitinh=%s, chucvu=%s, sdt=%s, diachi=%s WHERE manv=%s""",
                        (tennv, gioitinh, chucvu, sdt, diachi, manv))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật nhân viên!")
            load_data()
            clear_input()
        finally:
            conn.close()

    def delete():
        manv = entry_manv.get().strip()
        if not manv:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn nhân viên để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này không?"):
            conn = connect_db()
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM nhanvien WHERE manv=%s", (manv,))
                conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa nhân viên!")
                load_data()
                clear_input()
            finally:
                conn.close()

    def select_item(event):
        selected = tree.selection()
        if selected:
            v = tree.item(selected[0], "values")
            entry_manv.delete(0, tk.END)
            entry_manv.insert(0, v[0])
            entry_tennv.delete(0, tk.END)
            entry_tennv.insert(0, v[1])
            gender_var.set(v[2])
            entry_chucvu.delete(0, tk.END)
            entry_chucvu.insert(0, v[3])
            entry_sdt.delete(0, tk.END)
            entry_sdt.insert(0, v[4])
            entry_diachi.delete(0, tk.END)
            entry_diachi.insert(0, v[5])

    tree.bind("<ButtonRelease-1>", select_item)

    frame_btn = tk.Frame(win)
    frame_btn.pack(pady=10)
    tk.Button(frame_btn, text="Thêm", width=10, command=add).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Sửa", width=10, command=update).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Xóa", width=10, command=delete).grid(row=0, column=2, padx=5)
    tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=5)
    tk.Button(frame_btn, text="Thoát", width=10, command=win.destroy).grid(row=0, column=4, padx=5)

    load_data()
