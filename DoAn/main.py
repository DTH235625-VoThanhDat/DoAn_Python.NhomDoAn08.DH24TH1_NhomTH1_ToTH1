import tkinter as tk
from tkinter import messagebox

# Import các module chức năng
import DoAn.vatlieu as vatlieu
import DoAn.nhanvien as nhanvien
import DoAn.khachhang as khachhang
import DoAn.hoadon as hoadon
import DoAn.chitiethoadon as chitiethoadon

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=800, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("PHẦN MỀM QUẢN LÝ CỬA HÀNG VLXD")
center_window(root, 900, 550)
root.resizable(False, False)

# ====== Tiêu đề ======
title = tk.Label(root, text="PHẦN MỀM QUẢN LÝ CỬA HÀNG VẬT LIỆU XÂY DỰNG",
                 font=("Arial", 22, "bold"), fg="darkblue")
title.pack(pady=30)

# ====== Hướng dẫn ======
guide_text = (
    "Chọn mục trong thanh Menu phía trên để mở các chức năng:\n"
    "- Quản lý vật liệu\n"
    "- Quản lý nhân viên\n"
    "- Quản lý khách hàng\n"
    "- Quản lý hóa đơn\n"
    "- Quản lý chi tiết hóa đơn\n"
)

lbl_guide = tk.Label(root, text=guide_text, font=("Arial", 13), justify="left")
lbl_guide.pack(pady=20)

# ====== Thanh Menu ======
menubar = tk.Menu(root)

menu_quanly = tk.Menu(menubar, tearoff=0)
menu_quanly.add_command(label="Vật liệu", command=vatlieu.open_vatlieu)
menu_quanly.add_command(label="Nhân viên", command=nhanvien.open_nhanvien)
menu_quanly.add_command(label="Khách hàng", command=khachhang.open_khachhang)
menu_quanly.add_command(label="Hóa đơn", command=hoadon.open_hoadon)
menu_quanly.add_command(label="Chi tiết hóa đơn", command=chitiethoadon.open_cthd)
menubar.add_cascade(label="Quản lý", menu=menu_quanly)

menu_help = tk.Menu(menubar, tearoff=0)
menu_help.add_command(label="Giới thiệu", command=lambda: messagebox.showinfo(
    "Giới thiệu", "Phần mềm quản lý cửa hàng VLXD\nTác giả: Bạn\nVersion 1.0"))
menu_help.add_separator()
menu_help.add_command(label="Thoát", command=root.quit)
menubar.add_cascade(label="Trợ giúp", menu=menu_help)

root.config(menu=menubar)

# ====== Chạy ứng dụng ======
root.mainloop()
