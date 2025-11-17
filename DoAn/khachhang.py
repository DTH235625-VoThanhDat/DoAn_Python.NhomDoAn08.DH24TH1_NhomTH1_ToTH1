import tkinter as tk
from tkinter import ttk, messagebox
from DoAn.db_connect import connect_db

def open_khachhang():
    def center_window(win, w=700, h=500):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    win = tk.Toplevel()
    win.title("Quản lý khách hàng")
    center_window(win)
    win.resizable(False, False)

    tk.Label(win, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 18, "bold")).pack(pady=10)

    frame_input = tk.Frame(win)
    frame_input.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_input, text="Mã KH").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_makh = tk.Entry(frame_input, width=20)
    entry_makh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Tên KH").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_tenkh = tk.Entry(frame_input, width=25)
    entry_tenkh.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="Địa chỉ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_diachi = tk.Entry(frame_input, width=40)
    entry_diachi.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_input, text="SĐT").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_sdt = tk.Entry(frame_input, width=20)
    entry_sdt.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    columns = ("makh", "tenkh", "diachi", "sdt")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=120, anchor="center")
    tree.pack(padx=10, pady=10, fill="both")

    entries = [entry_makh, entry_tenkh, entry_diachi, entry_sdt]

    def clear_input():
        for e in entries:
            e.delete(0, tk.END)

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM khachhang")
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
        finally:
            conn.close()

    def add():
        makh = entry_makh.get().strip()
        tenkh = entry_tenkh.get().strip()
        diachi = entry_diachi.get().strip()
        sdt = entry_sdt.get().strip()

        if not makh or not tenkh:
            messagebox.showwarning("Thiếu dữ liệu", "Mã KH và Tên KH là bắt buộc!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO khachhang VALUES (%s,%s,%s,%s)", (makh, tenkh, diachi, sdt))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm khách hàng!")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def update():
        makh = entry_makh.get().strip()
        tenkh = entry_tenkh.get().strip()
        diachi = entry_diachi.get().strip()
        sdt = entry_sdt.get().strip()

        if not makh:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn khách hàng để sửa!")
            return

        conn = connect_db()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE khachhang SET tenkh=%s, diachi=%s, sdt=%s WHERE makh=%s",
                        (tenkh, diachi, sdt, makh))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật khách hàng!")
            load_data()
            clear_input()
        finally:
            conn.close()

    def delete():
        makh = entry_makh.get().strip()
        if not makh:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn khách hàng để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa khách hàng này không?"):
            conn = connect_db()
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM khachhang WHERE makh=%s", (makh,))
                conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa khách hàng!")
                load_data()
                clear_input()
            finally:
                conn.close()

    def select_item(event):
        selected = tree.selection()
        if selected:
            v = tree.item(selected[0], "values")
            entry_makh.delete(0, tk.END)
            entry_makh.insert(0, v[0])
            entry_tenkh.delete(0, tk.END)
            entry_tenkh.insert(0, v[1])
            entry_diachi.delete(0, tk.END)
            entry_diachi.insert(0, v[2])
            entry_sdt.delete(0, tk.END)
            entry_sdt.insert(0, v[3])

    tree.bind("<ButtonRelease-1>", select_item)

    frame_btn = tk.Frame(win)
    frame_btn.pack(pady=10)
    tk.Button(frame_btn, text="Thêm", width=10, command=add).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Sửa", width=10, command=update).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Xóa", width=10, command=delete).grid(row=0, column=2, padx=5)
    tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=5)
    tk.Button(frame_btn, text="Thoát", width=10, command=win.destroy).grid(row=0, column=4, padx=5)

    load_data()
