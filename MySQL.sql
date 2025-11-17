CREATE DATABASE IF NOT EXISTS ql_vatlieuxaydung
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ql_vatlieuxaydung;

CREATE TABLE vatlieu (
    mavl VARCHAR(20) NOT NULL,
    tenvl NVARCHAR(150) NOT NULL,
    loaivl NVARCHAR(30),
    donvitinh NVARCHAR(10),
    dongia DECIMAL(15,2) NOT NULL CHECK (dongia >= 0),
    soluong INT DEFAULT 0 CHECK (soluong >= 0),
    PRIMARY KEY (mavl)
);

CREATE TABLE nhanvien (
    manv VARCHAR(20) NOT NULL,
    tennv NVARCHAR(100) NOT NULL,
    gioitinh ENUM('nam','nu') DEFAULT 'nam',
    chucvu NVARCHAR(50),
    sdt VARCHAR(20) CHECK (sdt REGEXP '^0[0-9]{9}$'),
    diachi NVARCHAR(150),
    PRIMARY KEY (manv)
);

CREATE TABLE khachhang (
    makh VARCHAR(20) NOT NULL,
    tenkh NVARCHAR(100) NOT NULL,
    diachi NVARCHAR(150),
    sdt VARCHAR(20) CHECK (sdt REGEXP '^0[0-9]{9}$'),
    PRIMARY KEY (makh)
);

CREATE TABLE hoadon (
    mahd VARCHAR(20) NOT NULL,
    manv VARCHAR(20) NOT NULL,
    makh VARCHAR(20) NOT NULL,
    ngaylap DATETIME DEFAULT CURRENT_TIMESTAMP,
    tongtien DECIMAL(15,2) NOT NULL DEFAULT 0 CHECK (tongtien >= 0),
    PRIMARY KEY (mahd)
);

CREATE TABLE chitiethoadon (
    mahd VARCHAR(20) NOT NULL,
    mavl VARCHAR(20) NOT NULL,
    soluong INT DEFAULT 1 CHECK (soluong > 0),
    dongia DECIMAL(15,2) NOT NULL CHECK (dongia >= 0),
    giamgia DECIMAL(15,2) DEFAULT 0 CHECK (giamgia >= 0),
    thanhtien DECIMAL(15,2) NOT NULL CHECK (thanhtien >= 0),
    PRIMARY KEY (mahd, mavl)
);

ALTER TABLE hoadon ADD CONSTRAINT fk_HOADON_NHANVIEN FOREIGN KEY (manv) REFERENCES nhanvien(manv);
ALTER TABLE hoadon ADD CONSTRAINT fk_HOADON_KHACHHANG FOREIGN KEY (makh) REFERENCES khachhang(makh);
ALTER TABLE chitiethoadon ADD CONSTRAINT fk_CTHD_HOADON FOREIGN KEY (mahd) REFERENCES hoadon(mahd) ON DELETE CASCADE;
ALTER TABLE chitiethoadon ADD CONSTRAINT fk_CTHD_VATLIEU FOREIGN KEY (mavl) REFERENCES vatlieu(mavl);


