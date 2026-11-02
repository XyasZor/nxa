# NXA — Panduan Instalasi

Panduan ini berisi dua cara instalasi: **Termux (Android)** dan **Ubuntu (Linux)**.

## Informasi penting

- NXA dibuat menggunakan Python.
- **Tidak membutuhkan library/paket Python tambahan** berdasarkan source `nxa.py`.
- Virtual environment (`venv`) **opsional**, tetapi disarankan agar lingkungan Python tetap rapi dan tidak mengganggu paket sistem.
- Pastikan file `nxa.py` sudah berada di folder tempat kamu akan menjalankan perintah.
- Perintah di setiap bagian sudah dikelompokkan agar bisa disalin sekaligus. Jalankan satu kelompok sesuai urutannya.

---

# 1. Instalasi di Termux

## A. Pasang kebutuhan dasar

Buka Termux, lalu salin seluruh kelompok perintah ini:

```bash
pkg update -y && pkg upgrade -y
pkg install python -y
```

Periksa instalasi Python:

```bash
python --version
```

## B. Siapkan folder aplikasi

Buat folder khusus, lalu masuk ke folder tersebut:

```bash
mkdir -p ~/nxa
cd ~/nxa
```

Letakkan atau salin file `nxa.py` ke folder `~/nxa`.

Jika file berada di folder Download Android, aktifkan akses penyimpanan terlebih dahulu:

```bash
termux-setup-storage
```

Setelah izin diberikan, salin file dari folder Download:

```bash
cp ~/storage/downloads/nxa.py ~/nxa/nxa.py
cd ~/nxa
```

> Jika file kamu berada di lokasi lain, sesuaikan alamat sumber pada perintah `cp`.

## C. (Opsional) Buat dan aktifkan virtual environment

Termux umumnya sudah menyediakan modul `venv` bersama paket Python. Buat lingkungan virtual dengan:

```bash
cd ~/nxa
python -m venv .venv
source .venv/bin/activate
```

Jika berhasil, biasanya prompt terminal akan menampilkan awalan `(.venv)`.

Karena NXA tidak membutuhkan dependency eksternal, kamu tidak perlu menjalankan `pip install` untuk aplikasi ini.

Jika pembuatan venv gagal karena modul venv tidak tersedia, perbarui atau pasang ulang Python:

```bash
pkg update -y && pkg install python -y
```

## D. Jalankan NXA

Saat berada di folder aplikasi dan (jika memakai venv) lingkungan virtual sudah aktif:

```bash
cd ~/nxa
python nxa.py
```

Mode cepat tanpa animasi pembuka:

```bash
python nxa.py --fast
```

Memperbarui data OSINT Framework secara paksa:

```bash
python nxa.py --update
```

## E. Matikan atau aktifkan kembali virtual environment

Keluar dari venv tanpa menutup Termux:

```bash
deactivate
```

Untuk mengaktifkannya lagi di sesi Termux berikutnya:

```bash
cd ~/nxa
source .venv/bin/activate
```

Untuk menjalankan aplikasi setelah venv aktif:

```bash
python nxa.py
```

Jika tidak memakai venv, cukup masuk ke folder aplikasi dan jalankan `python nxa.py`.

---

# 2. Instalasi di Ubuntu

## A. Perbarui sistem dan pasang Python

Salin seluruh kelompok perintah berikut:

```bash
sudo apt update
sudo apt install -y python3 python3-venv
```

Periksa versi Python:

```bash
python3 --version
```

## B. Siapkan folder aplikasi

Buat folder khusus dan masuk ke dalamnya:

```bash
mkdir -p ~/nxa
cd ~/nxa
```

Letakkan file `nxa.py` di folder `~/nxa`.

Jika file berada di folder Downloads, salin dengan:

```bash
cp ~/Downloads/nxa.py ~/nxa/nxa.py
cd ~/nxa
```

> Jika file berada di lokasi lain, sesuaikan alamat sumber pada perintah `cp`.

## C. (Opsional) Buat dan aktifkan virtual environment

Buat venv:

```bash
cd ~/nxa
python3 -m venv .venv
source .venv/bin/activate
```

Jika berhasil, prompt terminal biasanya menampilkan awalan `(.venv)`.

NXA tidak membutuhkan dependency eksternal, jadi tidak ada perintah `pip install` tambahan yang perlu dijalankan.

Jika muncul pesan bahwa `venv` tidak tersedia, pasang paketnya:

```bash
sudo apt update
sudo apt install -y python3-venv
```

Kemudian buat ulang venv:

```bash
cd ~/nxa
python3 -m venv .venv
source .venv/bin/activate
```

## D. Jalankan NXA

Saat berada di folder aplikasi dan (jika memakai venv) venv sudah aktif:

```bash
cd ~/nxa
python nxa.py
```

Mode cepat tanpa animasi pembuka:

```bash
python nxa.py --fast
```

Memperbarui data OSINT Framework secara paksa:

```bash
python nxa.py --update
```

## E. Matikan atau aktifkan kembali virtual environment

Keluar dari venv:

```bash
deactivate
```

Untuk mengaktifkannya kembali di terminal atau sesi berikutnya:

```bash
cd ~/nxa
source .venv/bin/activate
```

Setelah aktif, jalankan aplikasi:

```bash
python nxa.py
```

---

# 3. Perintah ringkas

| Kebutuhan | Termux | Ubuntu |
|---|---|---|
| Menjalankan aplikasi | `python nxa.py` | `python nxa.py` |
| Mode cepat | `python nxa.py --fast` | `python nxa.py --fast` |
| Update data framework | `python nxa.py --update` | `python nxa.py --update` |
| Aktifkan venv | `source .venv/bin/activate` | `source .venv/bin/activate` |
| Matikan venv | `deactivate` | `deactivate` |

## Catatan

1. Jalankan perintah dari folder yang berisi `nxa.py`, kecuali perintah sudah menggunakan `cd ~/nxa`.
2. Venv hanya perlu dibuat **satu kali**. Pada penggunaan berikutnya, cukup aktifkan kembali dengan `source .venv/bin/activate`.
3. Menjalankan `deactivate` hanya menonaktifkan venv; folder `.venv` tidak terhapus.
4. Untuk menghapus venv dan membuatnya ulang, nonaktifkan dahulu, lalu jalankan:

```bash
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
```

Pada Termux, gunakan `python` sebagai pengganti `python3` jika perintah `python3` tidak tersedia.
