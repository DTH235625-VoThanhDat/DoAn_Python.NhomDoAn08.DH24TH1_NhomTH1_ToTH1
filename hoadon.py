import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import connect_db
import datetime

def open_hoadon():
    def center_window(win, w=800, h=500):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    win = tk.Toplevel()
    win.title("Quản lý hóa đơn")
    center_window(win)
    win.resizable(False, False)

    tk.Label(win, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 18, "bold")).pack(pady=10)

    frame_input = tk.Frame(win)
    frame_input.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_input, text="Mã HĐ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mahd = tk.Entry(frame_input, width=20)
    entry_mahd.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Mã NV").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_manv = tk.Entry(frame_input, width=20)
    entry_manv.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Mã KH").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_makh = tk.Entry(frame_input, width=20)
    entry_makh.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Ngày lập").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_ngaylap = tk.Entry(frame_input, width=20)
    entry_ngaylap.insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    entry_ngaylap.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Tổng tiền").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_tongtien = tk.Entry(frame_input, width=20)
    entry_tongtien.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    columns = ("mahd", "manv", "makh", "ngaylap", "tongtien")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=120, anchor="center")
    tree.pack(padx=10, pady=10, fill="both")

    entries = [entry_mahd, entry_manv, entry_makh, entry_ngaylap, entry_tongtien]

    def clear_input():
        for e in entries:
            e.delete(0, tk.END)
        entry_ngaylap.insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM hoadon")
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
        finally:
            conn.close()

    def add():
        mahd = entry_mahd.get().strip()
        manv = entry_manv.get().strip()
        makh = entry_makh.get().strip()
        ngaylap = entry_ngaylap.get().strip()
        tongtien = entry_tongtien.get().strip() or '0'

        if not mahd or not manv or not makh:
            messagebox.showwarning("Thiếu dữ liệu", "Mã HĐ, Mã NV, Mã KH là bắt buộc!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO hoadon VALUES (%s,%s,%s,%s,%s)", (mahd, manv, makh, ngaylap, tongtien))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm hóa đơn!")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def update():
        mahd = entry_mahd.get().strip()
        manv = entry_manv.get().strip()
        makh = entry_makh.get().strip()
        ngaylap = entry_ngaylap.get().strip()
        tongtien = entry_tongtien.get().strip() or '0'

        if not mahd:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn hóa đơn để sửa!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE hoadon SET manv=%s, makh=%s, ngaylap=%s, tongtien=%s WHERE mahd=%s",
                        (manv, makh, ngaylap, tongtien, mahd))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật hóa đơn!")
            load_data()
            clear_input()
        finally:
            conn.close()

    def delete():
        mahd = entry_mahd.get().strip()
        if not mahd:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn hóa đơn để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa hóa đơn này không?"):
            conn = connect_db()
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM hoadon WHERE mahd=%s", (mahd,))
                conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa hóa đơn!")
                load_data()
                clear_input()
            finally:
                conn.close()

    def select_item(event):
        selected = tree.selection()
        if selected:
            v = tree.item(selected[0], "values")
            for i, e in enumerate(entries):
                e.delete(0, tk.END)
                e.insert(0, v[i])

    tree.bind("<ButtonRelease-1>", select_item)

    frame_btn = tk.Frame(win)
    frame_btn.pack(pady=10)
    tk.Button(frame_btn, text="Thêm", width=10, command=add).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Sửa", width=10, command=update).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Xóa", width=10, command=delete).grid(row=0, column=2, padx=5)
    tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=5)
    tk.Button(frame_btn, text="Thoát", width=10, command=win.destroy).grid(row=0, column=4, padx=5)

    load_data()
