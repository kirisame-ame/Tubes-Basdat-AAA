DROP DATABASE IF EXISTS Papchat;
CREATE DATABASE IF NOT EXISTS Papchat;
USE Papchat;

-- Tabel Level
CREATE TABLE Level (
    id_level INT PRIMARY KEY,
    nama_level VARCHAR(100) NOT NULL,
    upah INT NOT NULL,
    minimum_lensa INT NOT NULL
);

-- Tabel Pengguna
CREATE TABLE Pengguna (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    id_level INT,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    no_telp VARCHAR(100) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    tanggal_pembuatan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_level) REFERENCES Level(id_level)
);

-- Tabel RoomChat
CREATE TABLE RoomChat (
    id_room_chat INT AUTO_INCREMENT PRIMARY KEY,
    nama_room_chat VARCHAR(100),
    tanggal_pembuatan DATE NOT NULL
);

-- Tabel TergabungDalam
CREATE TABLE TergabungDalam (
    id_user INT NOT NULL,
    id_room_chat INT NOT NULL,
    tanggal_bergabung DATE NOT NULL,
    PRIMARY KEY (id_user, id_room_chat),
    FOREIGN KEY (id_user) REFERENCES Pengguna(id_user),
    FOREIGN KEY (id_room_chat) REFERENCES RoomChat(id_room_chat)
);

-- Tabel Lens
CREATE TABLE Lens (
    id_lens INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    nama_lens VARCHAR(100),
    tanggal_rilis DATE NOT NULL,
    FOREIGN KEY (id_user) REFERENCES Pengguna(id_user)
);

-- Tabel TipeLensa
CREATE TABLE TipeLensa (
    id_lens INT NOT NULL,
    tipe_lensa VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_lens, tipe_lensa),
    FOREIGN KEY (id_lens) REFERENCES Lens(id_lens)
);

-- Tabel Premium
CREATE TABLE Premium (
    subscription_number INT NOT NULL,
    id_user INT NOT NULL,
    tanggal_subscribe DATE NOT NULL,
    tanggal_expired DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    PRIMARY KEY (subscription_number, id_user),
    FOREIGN KEY (id_user) REFERENCES Pengguna(id_user)
);

-- Tabel Berteman
CREATE TABLE Berteman (
    id_user1 INT NOT NULL,
    id_user2 INT NOT NULL,
    streak INT,
    tanggal_mulai DATE NOT NULL,
    PRIMARY KEY (id_user1, id_user2),
    FOREIGN KEY (id_user1) REFERENCES Pengguna(id_user),
    FOREIGN KEY (id_user2) REFERENCES Pengguna(id_user)
);

-- Tabel PapMap
CREATE TABLE PapMap (
    waktu_mulai TIMESTAMP NOT NULL,
    waktu_akhir TIMESTAMP NOT NULL,
    id_user INT NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    status VARCHAR(50) NOT NULL,
    PRIMARY KEY (waktu_mulai, waktu_akhir, id_user),
    FOREIGN KEY (id_user) REFERENCES Pengguna(id_user)
);

-- Tabel Konten
CREATE TABLE Konten (
    urutan_pengiriman INT NOT NULL,
    id_room_chat INT NOT NULL,
    id_user INT NOT NULL,
    waktu_pengiriman TIMESTAMP NOT NULL,
    tipe_konten VARCHAR(100),
    disimpan TINYINT(1) CHECK (disimpan IN (0, 1)),
    PRIMARY KEY (urutan_pengiriman, id_room_chat, id_user),
    FOREIGN KEY (id_room_chat) REFERENCES RoomChat(id_room_chat),
    FOREIGN KEY (id_user) REFERENCES Pengguna(id_user)
);

-- Tabel Chat
CREATE TABLE Chat (
    urutan_pengiriman INT NOT NULL,
    id_room_chat INT NOT NULL,
    id_user INT NOT NULL,
    isi_pesan TEXT,
    PRIMARY KEY (urutan_pengiriman, id_room_chat, id_user),
    FOREIGN KEY (urutan_pengiriman, id_room_chat, id_user) REFERENCES Konten(urutan_pengiriman, id_room_chat, id_user)
);

-- Tabel Pap
CREATE TABLE Pap (
    urutan_pengiriman INT NOT NULL,
    id_room_chat INT NOT NULL,
    id_user INT NOT NULL,
    id_lens INT,
    tipe_pap VARCHAR(50) NOT NULL,
    durasi INT,
    PRIMARY KEY (urutan_pengiriman, id_room_chat, id_user),
    FOREIGN KEY (urutan_pengiriman, id_room_chat, id_user) REFERENCES Konten(urutan_pengiriman, id_room_chat, id_user),
    FOREIGN KEY (id_lens) REFERENCES Lens(id_lens)
);

-- Tabel AddOn
CREATE TABLE AddOn (
    id_add_on INT NOT NULL,
    urutan_pengiriman INT NOT NULL,
    id_room_chat INT NOT NULL,
    id_user INT NOT NULL,
    x_awal INT,
    x_akhir INT,
    y_awal INT,
    y_akhir INT,
    tipe_add_on VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_add_on, urutan_pengiriman, id_room_chat, id_user),
    FOREIGN KEY (urutan_pengiriman, id_room_chat, id_user) REFERENCES Konten(urutan_pengiriman, id_room_chat, id_user)
);

-- Tabel Image
CREATE TABLE Image (
    id_add_on INT NOT NULL,
    urutan_pengiriman INT NOT NULL,
    id_room_chat INT NOT NULL,
    id_user INT NOT NULL,
    nama_image VARCHAR(100),
    PRIMARY KEY (id_add_on, urutan_pengiriman, id_room_chat, id_user),
    FOREIGN KEY (id_add_on) REFERENCES AddOn(id_add_on),
    FOREIGN KEY (urutan_pengiriman, id_room_chat, id_user) REFERENCES Konten(urutan_pengiriman, id_room_chat, id_user)
);

-- Tabel Caption
CREATE TABLE Caption (
    id_add_on INT NOT NULL,
    urutan_pengiriman INT NOT NULL,
    id_room_chat INT NOT NULL,
    id_user INT NOT NULL,
    font_style VARCHAR(100),
    teks TEXT,
    PRIMARY KEY (id_add_on, urutan_pengiriman, id_room_chat, id_user),
    FOREIGN KEY (id_add_on) REFERENCES AddOn(id_add_on),
    FOREIGN KEY (urutan_pengiriman, id_room_chat, id_user) REFERENCES Konten(urutan_pengiriman, id_room_chat, id_user)
);
