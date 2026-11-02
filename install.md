# NEXUS — OSINT Terminal
## Panduan Instalasi, Persiapan, Penggunaan, dan Troubleshooting

> **Versi dokumentasi:** 1.0  
> **Nama aplikasi:** NEXUS — OSINT Terminal  
> **Bahasa:** Python  
> **Platform:** Windows, Linux (termasuk Ubuntu/WSL), dan Termux  
> **Versi Python minimum menurut kode:** Python 3.7+

Dokumen ini menjelaskan persiapan, instalasi, cara menjalankan, penggunaan dasar, penanganan kendala, serta batasan dan etika penggunaan NEXUS.

---

## 1. Tentang NEXUS

NEXUS adalah aplikasi terminal untuk pembelajaran dan eksplorasi **Open-Source Intelligence (OSINT)**. Aplikasi ini menyediakan menu untuk:

1. **OSINT Framework** — menjelajahi kategori dan tautan tools dari OSINT Framework.
2. **Cari Tools** — mencari tools berdasarkan kata kunci.
3. **Kode Pos** — mencari wilayah berdasarkan kode pos lima digit atau nama kelurahan, kecamatan, maupun kota.
4. **Plat Nomor** — melihat perkiraan wilayah berdasarkan kode awal plat kendaraan.
5. **Operator HP** — melihat operator asal berdasarkan awalan nomor seluler.
6. **Perbarui Data** — mengunduh ulang data OSINT Framework.

NEXUS bukan alat untuk membobol akun, menyadap komunikasi, mengambil alih perangkat, atau mengakses database privat. Sebagian menu hanya menampilkan informasi umum dan tautan ke layanan pihak ketiga.

## 2. Peringatan edukasi, hukum, dan etika

**NEXUS dibuat untuk tujuan edukasi, pembelajaran OSINT, riset yang sah, dan penggunaan pada data atau aset yang memang boleh Anda periksa.**

- Gunakan hanya untuk kebutuhan yang sah dan bertanggung jawab.
- Jangan gunakan NEXUS untuk stalking, doxxing, mengintimidasi, mengancam, memeras, atau melecehkan orang lain.
- Jangan mencoba mengakses akun, perangkat, jaringan, atau data pribadi tanpa izin yang jelas.
- Jangan mengumpulkan, menyimpan, atau menyebarkan data pribadi orang lain tanpa dasar hukum dan tujuan yang sah.
- Patuhi hukum yang berlaku, kebijakan privasi, ketentuan layanan situs, dan aturan organisasi atau institusi Anda.
- Pastikan Anda memiliki izin sebelum melakukan pengujian terhadap domain, sistem, atau aset milik pihak lain.
- Hasil pencarian dapat keliru, tidak lengkap, atau sudah kedaluwarsa. Jangan menjadikan hasil NEXUS sebagai satu-satunya dasar untuk mengambil keputusan penting.

**Batasan khusus fitur:**

- **Plat nomor:** NEXUS hanya memperkirakan wilayah dari kode registrasi. Fitur ini tidak mencari identitas atau data pemilik kendaraan.
- **Nomor HP:** NEXUS memperkirakan operator asal dari empat digit awalan. Jika nomor pernah berpindah operator, hasil dapat berbeda dari operator yang sedang digunakan. Fitur ini tidak melacak lokasi atau identitas pemilik nomor.
- **Kode pos:** hasil bergantung pada file lokal atau API yang digunakan. Periksa kembali informasi melalui sumber resmi jika diperlukan.
- **OSINT Framework:** NEXUS hanya menampilkan katalog dan tautan tools. Setiap layanan eksternal memiliki aturan, batasan, dan kebijakan privasinya sendiri.

Dengan menggunakan aplikasi ini, pengguna bertanggung jawab atas aktivitas dan konsekuensi dari penggunaannya.

## 3. Persiapan sebelum instalasi

Siapkan hal-hal berikut:

- Perangkat Windows, Linux/Ubuntu/WSL, atau Android dengan Termux.
- Python **3.7 atau lebih baru**.
- Koneksi internet untuk mengunduh data OSINT Framework dan melakukan pencarian kode pos online. Koneksi internet tidak wajib untuk semua menu.
- Git, jika ingin mengambil repository langsung dari GitHub.
- Terminal yang mendukung UTF-8 agar banner dan karakter tampilan terbaca dengan baik.
- Ruang penyimpanan yang cukup untuk file aplikasi dan cache data.

### 3.1 Periksa Python

Jalankan:

```bash
python --version
```

Jika perintah tersebut tidak tersedia, coba:

```bash
python3 --version
```

Pastikan versi yang muncul adalah Python 3.7 atau lebih baru. Pada Windows, perintah berikut juga dapat digunakan:

```powershell
py --version
```

### 3.2 Periksa Git (opsional)

```bash
git --version
```

Jika Git belum tersedia, Anda dapat memasangnya sesuai sistem operasi pada bagian instalasi di bawah. Alternatifnya, unduh repository sebagai ZIP dari GitHub lalu ekstrak.

## 4. Instalasi

Pilih petunjuk yang sesuai dengan perangkat Anda. Jalankan perintah satu per satu.

### A. Android — Termux

Disarankan menggunakan Termux dari sumber distribusi resminya dan memperbaruinya secara berkala.

1. Buka Termux.
2. Perbarui daftar paket dan paket yang terpasang:

```bash
pkg update && pkg upgrade -y
```

3. Pasang Python dan Git:

```bash
pkg install python git -y
```

4. Periksa instalasi:

```bash
python --version
git --version
```

5. Masuk ke folder tempat Anda ingin menyimpan project:

```bash
cd ~
```

6. Clone repository (ganti alamat contoh di bawah dengan URL repository GitHub yang benar):

```bash
git clone https://github.com/USERNAME/NAMA-REPOSITORY.git
```

7. Masuk ke folder repository:

```bash
cd NAMA-REPOSITORY
```

8. Lihat nama file yang tersedia:

```bash
ls -la
```

9. Jalankan aplikasi sesuai nama file Python yang ada. Jika file bernama `nexus_osint.py`:

```bash
python nexus_osint.py
```

Jika file di repository Anda bernama `main.py`, gunakan:

```bash
python main.py
```

**Catatan Termux:** kode utama NEXUS menggunakan standard library Python sehingga tidak membutuhkan `pip install` untuk dependency aplikasi. Jangan memasang paket Python secara acak jika tidak ada pesan error yang memang memerlukannya.

### B. Ubuntu / Debian / WSL

1. Perbarui daftar paket:

```bash
sudo apt update
```

2. Pasang Python, Git, dan komponen dasar:

```bash
sudo apt install -y python3 git
```

3. Periksa versi Python dan Git:

```bash
python3 --version
git --version
```

4. Clone repository:

```bash
git clone https://github.com/USERNAME/NAMA-REPOSITORY.git
```

5. Masuk ke folder project:

```bash
cd NAMA-REPOSITORY
```

6. Periksa file:

```bash
ls -la
```

7. Jalankan aplikasi. Untuk file `nexus_osint.py`:

```bash
python3 nexus_osint.py
```

Jika nama file-nya `main.py`:

```bash
python3 main.py
```

Tidak perlu menjalankan `sudo pip install` untuk aplikasi inti NEXUS. Kode menggunakan modul bawaan Python.

### C. Windows

1. Instal Python 3.7 atau lebih baru dari situs resmi Python:  
   https://www.python.org/downloads/
2. Saat instalasi, aktifkan pilihan **Add Python to PATH** jika tersedia.
3. Buka PowerShell atau Command Prompt baru.
4. Periksa Python:

```powershell
py --version
```

5. Periksa Git (jika ingin clone repository):

```powershell
git --version
```

6. Clone repository:

```powershell
git clone https://github.com/USERNAME/NAMA-REPOSITORY.git
```

7. Masuk ke folder project:

```powershell
cd NAMA-REPOSITORY
```

8. Lihat isi folder:

```powershell
dir
```

9. Jalankan aplikasi:

```powershell
py nexus_osint.py
```

Jika file bernama `main.py`:

```powershell
py main.py
```

Jika perintah `py` tidak tersedia tetapi `python` tersedia, gunakan:

```powershell
python nexus_osint.py
```

### D. Instalasi tanpa Git (ZIP)

Jika tidak ingin menggunakan Git:

1. Buka halaman repository GitHub.
2. Pilih **Code → Download ZIP**.
3. Ekstrak file ZIP.
4. Buka terminal pada folder hasil ekstraksi.
5. Periksa nama file dengan `ls` (Linux/Termux) atau `dir` (Windows).
6. Jalankan file Python sesuai nama yang tersedia.

Contoh Linux/Termux:

```bash
python3 nexus_osint.py
```

Contoh Windows:

```powershell
py nexus_osint.py
```

> Ganti `USERNAME/NAMA-REPOSITORY` dengan alamat repository yang sebenarnya. Jangan menyalin URL contoh tersebut mentah-mentah.

## 5. Cara menjalankan aplikasi

Dari folder repository, jalankan:

```bash
python nexus_osint.py
```

Untuk Ubuntu yang menggunakan perintah `python3`:

```bash
python3 nexus_osint.py
```

Untuk Windows:

```powershell
py nexus_osint.py
```

Jika nama file berbeda, ganti `nexus_osint.py` dengan nama file yang benar.

### Opsi yang tersedia

**Jalankan normal:**

```bash
python nexus_osint.py
```

**Lewati animasi pembuka:**

```bash
python nexus_osint.py --fast
```

**Paksa unduh ulang data OSINT Framework:**

```bash
python nexus_osint.py --update
```

Di Ubuntu, gunakan `python3` jika `python` tidak mengarah ke Python 3:

```bash
python3 nexus_osint.py --fast
python3 nexus_osint.py --update
```

Di Windows:

```powershell
py nexus_osint.py --fast
py nexus_osint.py --update
```

## 6. Panduan menu dan tombol

| Menu | Fungsi |
|---|---|
| `1` — OSINT Framework | Menjelajahi kategori dan tools |
| `2` — Cari Tools | Mencari tools dengan kata kunci |
| `3` — Kode Pos | Mencari kode pos atau wilayah |
| `4` — Plat Nomor | Memperkirakan wilayah dari kode plat |
| `5` — Operator HP | Memeriksa operator berdasarkan awalan nomor |
| `6` — Perbarui Data | Mengunduh ulang data OSINT Framework |
| `0` — Keluar | Menutup aplikasi |

### Navigasi daftar OSINT Framework

- Masukkan angka untuk membuka kategori atau detail tools.
- `n` atau `>` untuk halaman berikutnya.
- `p` atau `<` untuk halaman sebelumnya.
- `b` untuk kembali.
- `h` untuk kembali ke menu utama.
- `/kata_kunci` untuk mencari dari tampilan daftar jika fitur pencarian tersedia.

### Tampilan detail tools

- `o` — membuka tautan di browser.
- `c` — menyalin URL jika dukungan clipboard tersedia.
- `b` — kembali.
- `h` — kembali ke menu utama.

### Pencarian kode pos

Masukkan kode pos lima digit atau nama wilayah. Contoh format:

```text
12345
```

atau:

```text
nama kecamatan
```

Nama wilayah minimal tiga karakter. Data dapat dibaca dari `kodepos.csv` jika file tersebut tersedia; jika tidak, aplikasi mencoba API online.

### Pemeriksaan plat nomor

Contoh format input:

```text
B 1234 ABC
```

Spasi, titik, dan tanda hubung pada input akan diabaikan. Hasil hanya menunjukkan perkiraan wilayah kode registrasi, bukan data pemilik kendaraan.

### Pemeriksaan operator HP

Contoh format input:

```text
081234567890
```

Format `+62` atau `62` juga dapat dikonversi ke format awalan `0`. Hasil didasarkan pada awalan nomor, bukan pemeriksaan jaringan secara langsung.

## 7. Data kode pos lokal (opsional)

Jika ingin pencarian kode pos menggunakan data lokal, letakkan file bernama:

```text
kodepos.csv
```

di salah satu lokasi berikut:

1. Folder yang sama dengan file script NEXUS; atau
2. Folder cache `~/.nexus_osint/`.

File CSV harus memiliki header berikut:

```csv
kodepos,kelurahan,kecamatan,kota,provinsi
```

Contoh struktur data (data berikut hanya contoh format):

```csv
kodepos,kelurahan,kecamatan,kota,provinsi
12345,Contoh Kelurahan,Contoh Kecamatan,Contoh Kota,Contoh Provinsi
```

Pastikan:
- Nama header ditulis dengan benar.
- File disimpan sebagai CSV dengan encoding UTF-8.
- Urutan kolom mengikuti header.
- Setiap baris memiliki data yang sesuai.

Jika file lokal tidak tersedia atau tidak menghasilkan kecocokan, NEXUS mencoba API online. API tersebut memerlukan koneksi internet dan dapat berubah atau tidak tersedia sewaktu-waktu.

### Mengubah alamat API kode pos

Secara default, kode menggunakan API:

```text
https://kodepos.vercel.app/search/?q={q}
```

Jika ingin menggunakan endpoint lain yang kompatibel, atur environment variable `NEXUS_KODEPOS_API`. Endpoint harus menerima kata kunci pada bagian `{q}` dan mengembalikan JSON dengan struktur data yang dapat dibaca aplikasi.

Contoh Linux/Termux untuk sesi terminal saat ini:

```bash
export NEXUS_KODEPOS_API='https://alamat-api-anda.example/search/?q={q}'
python nexus_osint.py
```

Contoh PowerShell:

```powershell
$env:NEXUS_KODEPOS_API = "https://alamat-api-anda.example/search/?q={q}"
py nexus_osint.py
```

Ganti alamat contoh dengan endpoint yang benar-benar Anda kelola atau percayai.

## 8. Cache dan pembaruan data

Data OSINT Framework disimpan dalam cache di:

```text
~/.nexus_osint/arf.json
```

Cache dianggap masih segar selama tujuh hari. Saat data masih segar, aplikasi dapat menggunakan cache tanpa mengunduh ulang.

Untuk memaksa pembaruan:

```bash
python nexus_osint.py --update
```

Jika pembaruan gagal, aplikasi dapat menggunakan cache lama atau daftar bawaan yang lebih kecil. Karena itu, tidak semua kategori mungkin muncul saat sedang offline.

## 9. Troubleshooting — mengatasi kendala

Ikuti langkah sesuai pesan error yang muncul. Jalankan perintah dari folder project kecuali disebutkan lain.

### A. `python: command not found`

Python belum terpasang atau perintahnya berbeda.

**Termux:**

```bash
pkg update
pkg install python -y
python --version
```

**Ubuntu/Debian/WSL:**

```bash
sudo apt update
sudo apt install -y python3
python3 --version
```

**Windows PowerShell:**

```powershell
py --version
```

Jika `py` tersedia, jalankan aplikasi dengan `py nexus_osint.py`.

### B. `No such file or directory`

Terminal tidak berada di folder project atau nama file salah.

Periksa lokasi saat ini:

```bash
pwd
```

Lihat isi folder:

```bash
ls -la
```

Di Windows:

```powershell
Get-Location
dir
```

Masuk ke folder project menggunakan `cd`, lalu jalankan file dengan nama yang benar. Perhatikan huruf besar-kecil pada Linux dan Termux.

### C. `Permission denied`

Biasanya file atau folder tidak memiliki izin yang sesuai.

Untuk menjalankan melalui Python, gunakan:

```bash
python3 nexus_osint.py
```

Jika memang ingin menjalankan file secara langsung, beri izin eksekusi:

```bash
chmod +x nexus_osint.py
```

Kemudian:

```bash
./nexus_osint.py
```

Cara menjalankan melalui `python3` biasanya lebih sederhana dan tidak memerlukan izin eksekusi.

### D. `SyntaxError` atau `IndentationError`

Kemungkinan file tidak tersalin dengan benar, ada indentasi yang berubah, atau versi Python terlalu lama.

Periksa versi:

```bash
python3 --version
```

Pastikan:
- File diunduh utuh dari repository.
- Spasi indentasi tidak diubah secara acak.
- Tidak ada karakter tambahan akibat proses copy-paste.
- Anda menjalankan file Python yang benar.

Jika file rusak, unduh ulang repository atau pulihkan file dari Git:

```bash
git status
git restore nexus_osint.py
```

**Perhatian:** `git restore nexus_osint.py` membuang perubahan lokal pada file tersebut. Cadangkan perubahan Anda terlebih dahulu jika masih diperlukan.

### E. Data OSINT Framework gagal diunduh

Penyebab umum:
- Tidak ada koneksi internet.
- DNS atau jaringan sedang bermasalah.
- GitHub atau endpoint sumber sedang tidak dapat diakses.
- Koneksi dibatasi firewall, proxy, atau jaringan publik.

Coba periksa koneksi:

```bash
ping -c 4 github.com
```

Kemudian coba pembaruan ulang:

```bash
python3 nexus_osint.py --update
```

Jika masih gagal, jalankan aplikasi secara normal. NEXUS dapat menggunakan cache lama atau daftar bawaan offline. Data offline mungkin lebih sedikit dan tidak selalu terbaru.

### F. Pencarian kode pos tidak menghasilkan data

Periksa hal berikut:
- Koneksi internet aktif jika memakai API online.
- Kata kunci minimal tiga karakter untuk nama wilayah.
- Kode pos terdiri dari tepat lima digit.
- Jika memakai CSV lokal, nama file harus `kodepos.csv`.
- Header CSV harus sesuai format pada bagian 7.

Anda juga dapat memeriksa apakah file tersedia:

```bash
ls -l kodepos.csv
```

Jika file berada di folder cache:

```bash
ls -l ~/.nexus_osint/kodepos.csv
```

### G. Clipboard tidak tersedia saat memilih `c`

Fitur salin URL bergantung pada dukungan clipboard di sistem operasi.

**Termux:** pasang aplikasi pendamping Termux:API yang sesuai, lalu pasang paketnya:

```bash
pkg install termux-api
```

Fitur clipboard juga memerlukan aplikasi Termux:API pada Android dan izin yang sesuai.

**Ubuntu dengan lingkungan desktop:**

```bash
sudo apt install -y xclip
```

Jika menggunakan Wayland:

```bash
sudo apt install -y wl-clipboard
```

Pada server Ubuntu tanpa desktop, clipboard mungkin memang tidak tersedia. Salin URL secara manual dari layar.

### H. Browser tidak terbuka

Pastikan perangkat memiliki browser default dan lingkungan terminal mendukung pembukaan URL.

Di Termux, beberapa fungsi pembukaan tautan memerlukan dukungan aplikasi Termux:API atau mekanisme pembuka URL yang tersedia. Jika gagal, salin URL dari detail tools dan buka secara manual.

### I. Tampilan warna atau karakter berantakan

Coba jalankan tanpa animasi:

```bash
python3 nexus_osint.py --fast
```

Jika warna mengganggu atau terminal tidak mendukung warna ANSI:

```bash
NO_COLOR=1 python3 nexus_osint.py
```

Perbesar jendela terminal dan gunakan terminal yang mendukung UTF-8.

### J. `externally-managed-environment` saat menggunakan pip

Aplikasi inti NEXUS tidak memerlukan instalasi dependency melalui pip. Jika muncul pesan tersebut karena Anda mencoba memasang paket yang tidak diperlukan, hentikan proses instalasi dan jalankan aplikasi menggunakan Python sistem:

```bash
python3 nexus_osint.py
```

Jangan menggunakan `sudo pip install` atau memaksa instalasi ke Python sistem hanya untuk menjalankan NEXUS.

### K. Aplikasi langsung kembali ke terminal atau berhenti

Jalankan ulang dan perhatikan pesan error lengkap:

```bash
python3 nexus_osint.py
```

Jika menggunakan Windows:

```powershell
py nexus_osint.py
```

Pastikan file tidak kosong atau terpotong:

```bash
wc -l nexus_osint.py
```

Jika masalah berlanjut, catat:
1. Sistem operasi dan versinya.
2. Versi Python.
3. Perintah yang dijalankan.
4. Pesan error lengkap.
5. Langkah yang menyebabkan error.

Jangan sertakan nomor HP pribadi, alamat, token, password, atau data sensitif ketika membagikan log.

## 10. Memperbarui NEXUS dari GitHub

Jika repository sudah di-clone menggunakan Git, masuk ke folder project lalu jalankan:

```bash
git pull
```

Periksa perubahan lokal sebelum memperbarui:

```bash
git status
```

Jika Anda mengubah file sendiri, simpan atau cadangkan perubahan tersebut terlebih dahulu agar tidak tertimpa.

Setelah pembaruan selesai, jalankan kembali:

```bash
python3 nexus_osint.py
```

Di Windows:

```powershell
py nexus_osint.py
```

## 11. Privasi dan keamanan penggunaan

- Hindari memasukkan data pribadi yang tidak diperlukan.
- Jangan membagikan hasil pencarian yang berisi informasi sensitif.
- Periksa kebijakan privasi layanan pihak ketiga sebelum mengirim data ke situs eksternal.
- Ingat bahwa ketika Anda membuka layanan eksternal, data yang dimasukkan dapat diproses oleh penyedia layanan tersebut sesuai kebijakan mereka.
- Jangan menganggap hasil OSINT sebagai bukti identitas seseorang.
- Hapus file hasil atau data lokal yang tidak lagi diperlukan, terutama jika berisi informasi sensitif.
- Unduh repository dan pembaruan hanya dari sumber yang Anda percaya.

## 12. Batasan teknis

- Kode aplikasi menyatakan kompatibilitas Python 3.7+.
- Aplikasi inti tidak membutuhkan dependency eksternal Python.
- Fitur OSINT Framework membutuhkan akses internet untuk data terbaru.
- Pencarian kode pos online membutuhkan akses ke API yang dikonfigurasi.
- Daftar operator dan kode plat merupakan data statis di dalam kode dan dapat menjadi usang.
- Informasi wilayah plat dan operator HP hanya berupa perkiraan berdasarkan awalan.
- Ketersediaan, akurasi, dan ketentuan tools pihak ketiga berada di luar kendali NEXUS.

## 13. Ringkasan perintah cepat

### Termux

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/USERNAME/NAMA-REPOSITORY.git
cd NAMA-REPOSITORY
ls -la
python nexus_osint.py
```

### Ubuntu / WSL

```bash
sudo apt update
sudo apt install -y python3 git
git clone https://github.com/USERNAME/NAMA-REPOSITORY.git
cd NAMA-REPOSITORY
ls -la
python3 nexus_osint.py
```

### Windows PowerShell

```powershell
git clone https://github.com/USERNAME/NAMA-REPOSITORY.git
cd NAMA-REPOSITORY
dir
py nexus_osint.py
```

### Opsi aplikasi

```bash
python nexus_osint.py --fast
python nexus_osint.py --update
```

> Jika nama file di repository bukan `nexus_osint.py`, ganti nama tersebut sesuai file yang tersedia. Kode sumber NEXUS yang didokumentasikan menggunakan nama `nexus_osint.py`.

---

## 14. Penutup

Terima kasih telah menggunakan NEXUS. Gunakan teknologi OSINT untuk meningkatkan pengetahuan, keamanan, dan kemampuan riset secara bertanggung jawab.

**Educational Use Only — Do Not Misuse.**  
**Jangan gunakan tools ini untuk aktivitas ilegal, pelanggaran privasi, atau tindakan yang merugikan orang lain.**
