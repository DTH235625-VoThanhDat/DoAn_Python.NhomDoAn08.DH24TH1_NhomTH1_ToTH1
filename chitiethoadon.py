import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import connect_db

def open_cthd():
    def center_window(win, w=900, h=500):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    win = tk.Toplevel()
    win.title("Quản lý chi tiết hóa đơn")
    center_window(win)
    win.resizable(False, False)

    tk.Label(win, text="QUẢN LÝ CHI TIẾT HÓA ĐƠN", font=("Arial", 18, "bold")).pack(pady=10)

    frame_input = tk.Frame(win)
    frame_input.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_input, text="Mã HĐ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mahd = tk.Entry(frame_input, width=20)
    entry_mahd.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_input, text="Mã VL").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_mavl = tk.Entry(frame_input, width=20)
    entry_mavl.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_input, text="Số lượng").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_soluong = tk.Entry(frame_input, width=20)
    entry_soluong.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_input, text="Đơn giá").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_dongia = tk.Entry(frame_input, width=20)
    entry_dongia.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_input, text="Giảm giá").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_giamgia = tk.Entry(frame_input, width=20)
    entry_giamgia.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_input, text="Thành tiền").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_thanhtien = tk.Entry(frame_input, width=20)
    entry_thanhtien.grid(row=2, column=3, padx=5, pady=5)

    columns = ("mahd", "mavl", "soluong", "dongia", "giamgia", "thanhtien")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=120, anchor="center")
    tree.pack(padx=10, pady=10, fill="both")

    entries = [entry_mahd, entry_mavl, entry_soluong, entry_dongia, entry_giamgia, entry_thanhtien]

    def clear_input():
        for e in entries:
            e.delete(0, tk.END)

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM chitiethoadon")
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
        finally:
            conn.close()

    def calculate_thanhtien():
        try:
            sl = int(entry_soluong.get().strip())
            dg = float(entry_dongia.get().strip())
            gg = float(entry_giamgia.get().strip() or 0)
            thanhtien = sl * dg - gg
            entry_thanhtien.delete(0, tk.END)
            entry_thanhtien.insert(0, str(thanhtien))
        except ValueError:
            entry_thanhtien.delete(0, tk.END)
            entry_thanhtien.insert(0, '0')

    def add():
        mahd = entry_mahd.get().strip()
        mavl = entry_mavl.get().strip()
        soluong = entry_soluong.get().strip() or '0'
        dongia = entry_dongia.get().strip() or '0'
        giamgia = entry_giamgia.get().strip() or '0'
        thanhtien = float(soluong)*float(dongia)-float(giamgia)

        if not mahd or not mavl:
            messagebox.showwarning("Thiếu dữ liệu", "Mã HĐ và Mã VL là bắt buộc!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO chitiethoadon VALUES (%s,%s,%s,%s,%s,%s)",
                        (mahd, mavl, soluong, dongia, giamgia, thanhtien))
            # Update tổng tiền HĐ
            cur.execute("UPDATE hoadon SET tongtien = (SELECT SUM(thanhtien) FROM chitiethoadon WHERE mahd=%s) WHERE mahd=%s",
                        (mahd, mahd))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm chi tiết hóa đơn!")
            load_data()
            clear_input()
        finally:
            conn.close()

    def update():
        mahd = entry_mahd.get().strip()
        mavl = entry_mavl.get().strip()
        soluong = entry_soluong.get().strip() or '0'
        dongia = entry_dongia.get().strip() or '0'
        giamgia = entry_giamgia.get().strip() or '0'
        thanhtien = float(soluong)*float(dongia)-float(giamgia)

        if not mahd or not mavl:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn chi tiết để sửa!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE chitiethoadon SET soluong=%s, dongia=%s, giamgia=%s, thanhtien=%s WHERE mahd=%s AND mavl=%s",
                        (soluong, dongia, giamgia, thanhtien, mahd, mavl))
            cur.execute("UPDATE hoadon SET tongtien = (SELECT SUM(thanhtien) FROM chitiethoadon WHERE mahd=%s) WHERE mahd=%s",
                        (mahd, mahd))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật chi tiết!")
            load_data()
            clear_input()
        finally:
            conn.close()

    def delete():
        mahd = entry_mahd.get().strip()
        mavl = entry_mavl.get().strip()
        if not mahd or not mavl:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn chi tiết để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa chi tiết này?"):
            conn = connect_db()
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM chitiethoadon WHERE mahd=%s AND mavl=%s", (mahd, mavl))
                cur.execute("UPDATE hoadon SET tongtien = (SELECT COALESCE(SUM(thanhtien),0) FROM chitiethoadon WHERE mahd=%s) WHERE mahd=%s", (mahd, mahd))
                conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa chi tiết!")
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
