#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEXUS - OSINT Terminal
----------------------
Tanpa dependency eksternal. Jalan di Windows, Linux, dan Termux (Python 3.7+).

Fitur
  1. Jelajah OSINT Framework (data resmi arf.json dari lockfale/OSINT-Framework)
  2. Cari tools OSINT berdasarkan kata kunci
  3. Cek wilayah kode pos (kode pos 5 digit atau nama kelurahan/kecamatan/kota)
  4. Cek daerah asal plat nomor kendaraan
  5. Cek operator nomor HP (format awalan 0, contoh 0812xxxxxxxx)

Opsi
  python nexus_osint.py            jalankan normal
  python nexus_osint.py --update   paksa unduh ulang data OSINT Framework
  python nexus_osint.py --fast     lewati animasi pembuka

Data kode pos detail (opsional)
  - Letakkan file kodepos.csv di folder yang sama dengan script ini, atau di
    ~/.nexus_osint/kodepos.csv, dengan header:
        kodepos,kelurahan,kecamatan,kota,provinsi
  - Tanpa file itu, tool mencoba API online (ubah lewat variabel lingkungan
    NEXUS_KODEPOS_API, gunakan {q} sebagai tempat kata kunci).
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import time
import urllib.parse
import urllib.request
import webbrowser

APP_NAME = "NEXUS"
VERSION = "1.0"

ARF_URLS = [
    "https://raw.githubusercontent.com/lockfale/OSINT-Framework/master/public/arf.json",
    "https://raw.githubusercontent.com/lockfale/OSINT-Framework/main/public/arf.json",
]
KODEPOS_API = os.environ.get("NEXUS_KODEPOS_API", "https://kodepos.vercel.app/search/?q={q}")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".nexus_osint")
CACHE_FILE = os.path.join(CACHE_DIR, "arf.json")
CACHE_TTL = 7 * 24 * 3600  # data framework dianggap segar selama 7 hari

# --------------------------------------------------------------------------
# Warna & gaya
# --------------------------------------------------------------------------
USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
FANCY = USE_COLOR and not os.environ.get("NEXUS_FAST")


def _fg(r, g, b):
    return "\033[38;2;%d;%d;%dm" % (r, g, b) if USE_COLOR else ""


RST = "\033[0m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
CY = (0, 229, 255)      # cyan neon
MG = (255, 56, 176)     # magenta neon
VI = (146, 110, 255)    # violet
LM = (64, 255, 170)     # hijau sukses
AM = (255, 196, 64)     # amber peringatan
RD = (255, 88, 96)      # merah error
WH = (226, 232, 255)    # teks utama
DM = (112, 124, 156)    # teks redup

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def c(color, text, bold=False):
    if not USE_COLOR:
        return text
    return (BOLD if bold else "") + _fg(*color) + text + RST


def vlen(s):
    return len(ANSI_RE.sub("", s))


def pad(s, w):
    return s + " " * max(0, w - vlen(s))


def trunc(s, w):
    if w <= 0:
        return ""
    return s if len(s) <= w else s[: max(0, w - 1)] + "\u2026"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(text, c1, c2):
    if not USE_COLOR:
        return text
    n = max(1, len(text) - 1)
    out = []
    for i, ch in enumerate(text):
        if ch == " ":
            out.append(ch)
            continue
        r, g, b = lerp(c1, c2, i / n)
        out.append("\033[38;2;%d;%d;%dm%s" % (r, g, b, ch))
    return "".join(out) + RST


def enable_ansi():
    if os.name == "nt":
        os.system("")  # mengaktifkan VT100 di Windows 10+
        try:
            import ctypes
            k = ctypes.windll.kernel32
            k.SetConsoleMode(k.GetStdHandle(-11), 7)
        except Exception:
            pass
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def clear():
    if USE_COLOR:
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
    else:
        print("\n" + "=" * 40)


def term_size():
    s = shutil.get_terminal_size((80, 24))
    return s.columns, s.lines


def W():
    cols, _ = term_size()
    return max(38, min(cols - 1, 84))


def compact():
    cols, lines = term_size()
    return lines < 28 or cols < 46


# --------------------------------------------------------------------------
# Komponen tampilan
# --------------------------------------------------------------------------
BANNER = [
    "\u2588\u2588\u2588\u2557   \u2588\u2588\u2557\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2557  \u2588\u2588\u2557\u2588\u2588\u2557   \u2588\u2588\u2557\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557",
    "\u2588\u2588\u2588\u2588\u2557  \u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2550\u2550\u255d\u255a\u2588\u2588\u2557\u2588\u2588\u2554\u255d\u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2550\u2550\u255d",
    "\u2588\u2588\u2554\u2588\u2588\u2557 \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2557   \u255a\u2588\u2588\u2588\u2554\u255d \u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557",
    "\u2588\u2588\u2551\u255a\u2588\u2588\u2557\u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u255d   \u2588\u2588\u2554\u2588\u2588\u2557 \u2588\u2588\u2551   \u2588\u2588\u2551\u255a\u2550\u2550\u2550\u2550\u2588\u2588\u2551",
    "\u2588\u2588\u2551 \u255a\u2588\u2588\u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2554\u255d \u2588\u2588\u2557\u255a\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2551",
    "\u255a\u2550\u255d  \u255a\u2550\u2550\u2550\u255d\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u255d\u255a\u2550\u255d  \u255a\u2550\u255d \u255a\u2550\u2550\u2550\u2550\u2550\u255d \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u255d",
]


def banner_lines():
    cols, _ = term_size()
    if compact():
        return [gradient("\u25c6 NEXUS // OSINT TERMINAL v" + VERSION, MG, CY)]
    out = []
    for i, ln in enumerate(BANNER):
        out.append(gradient(ln, lerp(CY, MG, i / 5), lerp(MG, VI, i / 5)))
    out.append(c(DM, "OSINT TERMINAL  //  Indonesia toolkit  //  v" + VERSION))
    return out


def status_line():
    n = len(STATE["flat"])
    return (c(DM, "data ") + c(WH, STATE["src"]) + c(DM, "   tools ") + c(WH, str(n))
            + c(DM, "   kategori ") + c(WH, str(STATE["folders"])))


def header():
    clear()
    for ln in banner_lines():
        print(ln)
    print(status_line())
    print()


def panel(title, lines, color=None):
    color = color or CY
    w = W()
    inner = w - 4
    t = "[ %s ]" % title
    if len(t) > w - 4:
        t = t[: w - 4]
    fill = max(0, w - 3 - len(t))
    print(c(color, "\u256d\u2500") + c(MG, t) + c(color, "\u2500" * fill + "\u256e"))
    for ln in lines:
        print(c(color, "\u2502 ") + pad(ln, inner) + c(color, " \u2502"))
    print(c(color, "\u2570" + "\u2500" * (w - 2) + "\u256f"))


def kv(label, value, lc=DM, vc=WH, lw=9):
    inner = W() - 4
    avail = max(10, inner - lw - 1)
    parts = textwrap.wrap(str(value), avail, break_long_words=True) or [""]
    out = []
    for i, p in enumerate(parts):
        out.append(c(lc, (label if i == 0 else "").ljust(lw)) + " " + c(vc, p))
    return out


def wrap_plain(text, color=DM):
    inner = W() - 4
    return [c(color, p) for p in textwrap.wrap(text, inner)] or [""]


PROMPT = c(CY, "\u2570\u2500") + c(MG, ">", True) + " "


def read_line(prompt=PROMPT):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def note(kind, text):
    color = {"ok": LM, "warn": AM, "err": RD, "info": CY}[kind]
    sym = {"ok": "\u25cf", "warn": "\u25b2", "err": "\u2716", "info": "\u25c6"}[kind]
    print(c(color, sym) + " " + c(WH, text))


def progress(label, steps=24, delay=0.012):
    if not FANCY:
        return
    for i in range(steps + 1):
        filled = "\u2588" * i
        empty = "\u2591" * (steps - i)
        bar = gradient(filled, CY, MG) + c(DM, empty)
        sys.stdout.write("\r" + c(DM, label.ljust(22)) + bar + " " + c(WH, "%3d%%" % int(i * 100 / steps)))
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")


# --------------------------------------------------------------------------
# Utilitas sistem (buka URL, salin)
# --------------------------------------------------------------------------
def open_url(url):
    try:
        if shutil.which("termux-open-url"):
            subprocess.run(["termux-open-url", url], check=False)
            return True
        return bool(webbrowser.open(url))
    except Exception:
        return False


def copy_text(text):
    cmds = [["termux-clipboard-set"], ["clip"], ["pbcopy"], ["wl-copy"],
            ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]
    for cmd in cmds:
        if shutil.which(cmd[0]):
            try:
                subprocess.run(cmd, input=text.encode("utf-8"), check=True)
                return True
            except Exception:
                continue
    return False


def http_get(url, timeout=10):
    req = urllib.request.Request(url, headers={
        "User-Agent": "%s/%s (terminal)" % (APP_NAME, VERSION),
        "Accept": "application/json,*/*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


# --------------------------------------------------------------------------
# OSINT Framework (arf.json)
# --------------------------------------------------------------------------
FALLBACK_TREE = {"name": "OSINT Framework", "type": "folder", "children": [
    {"name": "Username", "type": "folder", "children": [
        {"name": "Sherlock (T)", "type": "url", "url": "https://github.com/sherlock-project/sherlock",
         "description": "Mencari satu username di banyak situs sosial.", "input": "Username"},
        {"name": "WhatsMyName", "type": "url", "url": "https://whatsmyname.app",
         "description": "Pencarian username lintas situs lewat browser.", "input": "Username"}]},
    {"name": "Email Address", "type": "folder", "children": [
        {"name": "Have I Been Pwned", "type": "url", "url": "https://haveibeenpwned.com",
         "description": "Memeriksa apakah email muncul dalam kebocoran data publik.", "input": "Email"}]},
    {"name": "Domain Name", "type": "folder", "children": [
        {"name": "crt.sh", "type": "url", "url": "https://crt.sh",
         "description": "Pencarian sertifikat TLS untuk menemukan subdomain.", "input": "Domain"},
        {"name": "urlscan.io", "type": "url", "url": "https://urlscan.io",
         "description": "Memindai dan mengarsipkan halaman web.", "input": "URL"},
        {"name": "VirusTotal", "type": "url", "url": "https://www.virustotal.com",
         "description": "Reputasi domain, URL, dan file.", "input": "Domain, URL, hash"}]},
    {"name": "IP and Infrastructure", "type": "folder", "children": [
        {"name": "Shodan (R)", "type": "url", "url": "https://www.shodan.io",
         "description": "Mesin pencari perangkat yang terhubung ke internet.", "input": "IP, domain, query"},
        {"name": "Censys (R)", "type": "url", "url": "https://search.censys.io",
         "description": "Pemetaan host dan sertifikat di internet.", "input": "IP, domain"}]},
    {"name": "Geolocation and Maps", "type": "folder", "children": [
        {"name": "OpenStreetMap", "type": "url", "url": "https://www.openstreetmap.org",
         "description": "Peta terbuka dengan data jalan dan bangunan.", "input": "Lokasi"},
        {"name": "Google Maps", "type": "url", "url": "https://maps.google.com",
         "description": "Peta dan citra jalan.", "input": "Lokasi"}]},
    {"name": "Archives", "type": "folder", "children": [
        {"name": "Wayback Machine", "type": "url", "url": "https://web.archive.org",
         "description": "Arsip riwayat halaman web.", "input": "URL"}]},
    {"name": "Metadata", "type": "folder", "children": [
        {"name": "ExifTool (T)", "type": "url", "url": "https://exiftool.org",
         "description": "Membaca metadata file gambar dan dokumen.", "input": "File"}]},
]}

STATE = {"tree": FALLBACK_TREE, "src": "-", "flat": [], "folders": 0}


def is_folder(n):
    return n.get("type") == "folder" or "children" in n


def flatten(node, path=()):
    for ch in node.get("children", []):
        if is_folder(ch):
            for item in flatten(ch, path + (ch.get("name", ""),)):
                yield item
        else:
            yield ch, path


def count_tools(node):
    return sum(1 for _ in flatten(node))


def count_folders(node):
    total = 0
    for ch in node.get("children", []):
        if is_folder(ch):
            total += 1 + count_folders(ch)
    return total


def clean_name(t):
    return re.sub(r"\s*\((?:T|D|R|M)\)", "", t.get("name", "")).strip() or "(tanpa nama)"


def tags_of(t):
    nm = t.get("name", "")
    tags = []
    if t.get("localInstall") or "(T)" in nm:
        tags.append("T")
    if t.get("googleDork") or "(D)" in nm:
        tags.append("D")
    if t.get("registration") or "(R)" in nm:
        tags.append("R")
    if t.get("editUrl") or "(M)" in nm:
        tags.append("M")
    if t.get("api"):
        tags.append("API")
    return tags


TAG_DESC = {"T": "dipasang lokal", "D": "Google dork", "R": "butuh registrasi",
            "M": "URL diedit manual", "API": "punya API"}


def read_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) and data.get("children") else None
    except Exception:
        return None


def load_framework(force=False):
    if not force and os.path.exists(CACHE_FILE):
        age = time.time() - os.path.getmtime(CACHE_FILE)
        if age < CACHE_TTL:
            t = read_json_file(CACHE_FILE)
            if t:
                return t, "cache %dj" % int(age // 3600)
    for url in ARF_URLS:
        try:
            raw = http_get(url, 8)
            t = json.loads(raw)
            if isinstance(t, dict) and t.get("children"):
                os.makedirs(CACHE_DIR, exist_ok=True)
                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    f.write(raw)
                return t, "online"
        except Exception:
            continue
    t = read_json_file(CACHE_FILE)
    if t:
        return t, "cache lama"
    return FALLBACK_TREE, "bawaan (offline)"


def index_tree(tree, src):
    STATE["tree"] = tree
    STATE["src"] = src
    STATE["flat"] = list(flatten(tree))
    STATE["folders"] = count_folders(tree)


# --------------------------------------------------------------------------
# Layar daftar generik (dipakai browse & hasil cari)
# --------------------------------------------------------------------------
def list_screen(title, crumb, rows, hint, allow_search=True):
    """rows: list dict(name, icon, ic, nc, right, rc). Return (aksi, indeks)."""
    page = 0
    msg = ""
    while True:
        _, lines = term_size()
        head_h = 4 if compact() else 10
        per = max(5, min(18, lines - head_h - 8))
        pages = max(1, (len(rows) + per - 1) // per)
        page = max(0, min(page, pages - 1))
        header()
        if crumb:
            ctext = crumb if len(crumb) <= W() - 8 else "\u2026" + crumb[-(W() - 9):]
            print(c(DM, "jalur ") + c(CY, ctext))
        inner = W() - 4
        body = []
        start = page * per
        for i, r in enumerate(rows[start:start + per], start + 1):
            right = r.get("right", "")
            name_max = inner - 3 - 1 - 1 - 1 - (len(right) + 1 if right else 0)
            name = trunc(r["name"], name_max)
            gap = inner - (3 + 1 + 1 + 1 + len(name) + len(right))
            body.append(c(DM, "%3d" % i) + " " + c(r.get("ic", CY), r.get("icon", "\u25c6")) + " "
                        + c(r.get("nc", WH), name) + " " * max(1, gap) + c(r.get("rc", DM), right))
        if not rows:
            body.append(c(DM, "(kosong)"))
        ttl = title if pages == 1 else "%s  %d/%d" % (title, page + 1, pages)
        panel(ttl, body)
        print(c(DM, hint))
        if msg:
            note("warn", msg)
            msg = ""
        s = read_line()
        if s is None:
            return ("home", None)
        sl = s.lower()
        if sl == "":
            continue
        if sl == "b":
            return ("back", None)
        if sl == "h":
            return ("home", None)
        if sl in ("n", ">"):
            page = (page + 1) % pages
            continue
        if sl in ("p", "<"):
            page = (page - 1) % pages
            continue
        if allow_search and sl.startswith("/"):
            return ("search", s[1:].strip())
        if sl.isdigit():
            idx = int(sl)
            if 1 <= idx <= len(rows):
                return ("open", idx - 1)
            msg = "Nomor di luar daftar (1-%d)." % len(rows)
            continue
        msg = "Perintah tidak dikenal."


def tool_rows(items, show_path=False):
    rows = []
    for t, path in items:
        tags = " ".join(tags_of(t))
        right = (path[-1] if show_path and path else tags)
        rows.append(dict(name=clean_name(t), icon="\u25c6", ic=CY, nc=WH, right=right, rc=AM if not show_path else DM))
    return rows


def tool_detail(tool, path):
    while True:
        header()
        inner = W() - 4
        lines = []
        lines += kv("Nama", clean_name(tool), vc=CY)
        lines += kv("URL", tool.get("url", "-"), vc=VI)
        if path:
            lines += kv("Jalur", " > ".join(path))
        if tool.get("description"):
            lines += kv("Deskripsi", tool["description"])
        if tool.get("bestFor"):
            lines += kv("Cocok", tool["bestFor"])
        if tool.get("input"):
            lines += kv("Input", tool["input"])
        if tool.get("output"):
            lines += kv("Output", tool["output"])
        meta = []
        if tool.get("pricing"):
            meta.append("harga: " + tool["pricing"])
        if tool.get("status"):
            meta.append("status: " + tool["status"])
        if tool.get("opsec"):
            meta.append("opsec: " + tool["opsec"])
        if meta:
            lines += kv("Info", ", ".join(meta))
        if tool.get("opsecNote"):
            lines += kv("Catatan", tool["opsecNote"])
        tg = tags_of(tool)
        if tg:
            lines += kv("Tag", ", ".join("%s = %s" % (x, TAG_DESC[x]) for x in tg), vc=AM)
        panel("DETAIL TOOL", lines)
        print(c(DM, "o = buka di browser   c = salin URL   b = kembali   h = menu"))
        s = read_line()
        if s is None:
            return "home"
        sl = s.lower()
        if sl in ("b", ""):
            return None
        if sl == "h":
            return "home"
        if sl == "o":
            note("ok" if open_url(tool.get("url", "")) else "err",
                 "Membuka browser..." if tool.get("url") else "URL tidak tersedia.")
            time.sleep(0.8)
        elif sl == "c":
            ok = copy_text(tool.get("url", ""))
            note("ok" if ok else "warn", "URL disalin." if ok else "Clipboard tidak tersedia, salin manual dari layar.")
            time.sleep(1.0 if ok else 2.0)


def screen_browse():
    stack = [STATE["tree"]]
    names = []
    while True:
        node = stack[-1]
        children = node.get("children", [])
        rows = []
        for ch in children:
            if is_folder(ch):
                rows.append(dict(name=ch.get("name", "?"), icon="\u25b8", ic=MG, nc=WH,
                                 right=str(count_tools(ch)), rc=DM))
            else:
                rows.append(dict(name=clean_name(ch), icon="\u25c6", ic=CY, nc=WH,
                                 right=" ".join(tags_of(ch)), rc=AM))
        title = names[-1].upper() if names else "OSINT FRAMEWORK"
        act, idx = list_screen(title, " / ".join(["root"] + names), rows,
                               "angka = buka   n/p = halaman   b = kembali   h = menu   /kata = cari")
        if act == "home":
            return
        if act == "back":
            if len(stack) == 1:
                return
            stack.pop()
            names.pop()
        elif act == "search":
            if screen_search(idx or None) == "home":
                return
        elif act == "open":
            ch = children[idx]
            if is_folder(ch):
                stack.append(ch)
                names.append(ch.get("name", "?"))
            else:
                if tool_detail(ch, tuple(names)) == "home":
                    return


def screen_search(query=None):
    while True:
        if not query:
            header()
            panel("CARI TOOLS", wrap_plain("Ketik kata kunci. Contoh: username, domain, email, maps, dork. "
                                           "Beberapa kata dicocokkan sekaligus. Kosongkan untuk kembali."))
            query = read_line()
            if not query:
                return None
        terms = query.lower().split()
        hits = []
        for t, p in STATE["flat"]:
            hay = " ".join([t.get("name", ""), t.get("description", ""), t.get("bestFor", ""),
                            t.get("input", ""), t.get("output", ""), " ".join(p)]).lower()
            if all(x in hay for x in terms):
                nm = clean_name(t).lower()
                score = 0 if all(x in nm for x in terms) else 1
                hits.append((score, nm, t, p))
        hits.sort(key=lambda h: (h[0], h[1]))
        items = [(h[2], h[3]) for h in hits]
        if not items:
            header()
            note("warn", "Tidak ada hasil untuk \"%s\"." % query)
            time.sleep(1.4)
            query = None
            continue
        while True:
            act, idx = list_screen("HASIL: " + trunc(query, 22), "%d tools cocok" % len(items),
                                   tool_rows(items, show_path=True),
                                   "angka = detail   n/p = halaman   b = cari lagi   h = menu",
                                   allow_search=False)
            if act == "home":
                return "home"
            if act == "back":
                query = None
                break
            if act == "open":
                t, p = items[idx]
                if tool_detail(t, p) == "home":
                    return "home"


def related_tools(keyword):
    return screen_search(keyword)


# --------------------------------------------------------------------------
# Kode pos
# --------------------------------------------------------------------------
ZONA_POS = {
    "1": "Jakarta dan sekitarnya (DKI Jakarta, Tangerang, Bogor, Depok, Bekasi)",
    "2": "Sumatera bagian utara dan barat (Aceh, Sumut, Sumbar, Riau, Kepri)",
    "3": "Sumatera bagian selatan (Sumsel, Babel, Jambi, Bengkulu, Lampung)",
    "4": "Jawa Barat dan Banten",
    "5": "Jawa Tengah dan DI Yogyakarta",
    "6": "Jawa Timur",
    "7": "Kalimantan",
    "8": "Bali dan Nusa Tenggara",
    "9": "Sulawesi, Maluku, dan Papua",
}


def pick(d, *keys):
    for k in keys:
        v = d.get(k)
        if v not in (None, ""):
            return str(v)
    return "-"


def norm_postal(d):
    return dict(
        kode=pick(d, "kodepos", "code", "postal_code", "zip", "kode_pos"),
        kel=pick(d, "kelurahan", "village", "desa", "urban"),
        kec=pick(d, "kecamatan", "district", "sub_district"),
        kota=pick(d, "kota", "regency", "city", "kabupaten", "kota_kab"),
        prov=pick(d, "provinsi", "province", "propinsi"),
    )


_LOCAL_POSTAL = {"loaded": False, "rows": None}


def local_postal():
    if not _LOCAL_POSTAL["loaded"]:
        _LOCAL_POSTAL["loaded"] = True
        for p in (os.path.join(SCRIPT_DIR, "kodepos.csv"), os.path.join(CACHE_DIR, "kodepos.csv")):
            if os.path.exists(p):
                try:
                    rows = []
                    with open(p, encoding="utf-8-sig", newline="") as f:
                        for d in csv.DictReader(f):
                            rows.append(norm_postal({(k or "").strip().lower(): (v or "").strip() for k, v in d.items()}))
                    _LOCAL_POSTAL["rows"] = rows
                    break
                except Exception:
                    continue
    return _LOCAL_POSTAL["rows"]


def search_local_postal(q):
    rows = local_postal()
    if rows is None:
        return None
    if re.fullmatch(r"\d{5}", q):
        return [r for r in rows if r["kode"] == q]
    terms = q.lower().split()
    return [r for r in rows if all(t in " ".join(r.values()).lower() for t in terms)]


def search_online_postal(q):
    url = KODEPOS_API.replace("{q}", urllib.parse.quote(q))
    data = json.loads(http_get(url, 10))
    items = data.get("data") if isinstance(data, dict) else data
    if not isinstance(items, list):
        return []
    return [norm_postal(d) for d in items if isinstance(d, dict)]


def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        key = tuple(r.values())
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def postal_result(q):
    lines = []
    is_code = bool(re.fullmatch(r"\d{5}", q))
    if is_code:
        zona = ZONA_POS.get(q[0], "-")
        lines += kv("Kode pos", q, vc=CY)
        lines += kv("Zona", zona + " (perkiraan dari digit pertama)")
    rows = search_local_postal(q)
    source = "file kodepos.csv"
    err = None
    if rows is None or (not rows):
        try:
            rows = search_online_postal(q)
            source = "API online"
        except Exception as e:
            err = e
            rows = rows or []
    rows = dedupe(rows)
    if rows:
        if lines:
            lines.append("")
        lines.append(c(DM, "sumber: %s, %d hasil" % (source, len(rows))))
        for r in rows[:8]:
            lines.append(c(CY, r["kode"], True) + "  " + c(WH, trunc(r["kel"], W() - 14)))
            lines += [c(DM, "      " + x) for x in textwrap.wrap(
                "Kec. %s, %s, %s" % (r["kec"], r["kota"], r["prov"]), W() - 10)]
        if len(rows) > 8:
            lines.append(c(AM, "...dan %d hasil lain. Persempit pencarian." % (len(rows) - 8)))
    else:
        if lines:
            lines.append("")
        if err is not None:
            lines += wrap_plain("Data detail tidak bisa diambil (offline atau API tidak merespons). "
                                "Tambahkan kodepos.csv di folder script, atau set NEXUS_KODEPOS_API.", AM)
        else:
            lines += wrap_plain("Tidak ditemukan. Coba kata kunci lain atau periksa kode pos.", AM)
    return lines


def screen_postal():
    while True:
        header()
        panel("KODE POS", wrap_plain(
            "Masukkan kode pos 5 digit, atau nama kelurahan/kecamatan/kota. Kosongkan untuk kembali."))
        q = read_line()
        if not q or q.lower() == "b":
            return
        if q.isdigit() and len(q) != 5:
            note("warn", "Kode pos harus 5 digit.")
            time.sleep(1.2)
            continue
        if not q.isdigit() and len(q) < 3:
            note("warn", "Nama minimal 3 huruf.")
            time.sleep(1.2)
            continue
        print()
        note("info", "Mencari...")
        panel("HASIL KODE POS", postal_result(q))
        if after_result("maps") == "home":
            return


# --------------------------------------------------------------------------
# Plat nomor
# --------------------------------------------------------------------------
PLAT = {
    # Sumatera
    "BL": ("Aceh", "Seluruh Aceh"),
    "BB": ("Sumatera Utara", "Tapanuli, Nias, Sibolga, Padang Sidempuan"),
    "BK": ("Sumatera Utara", "Medan, Deli Serdang, Langkat, Karo, Simalungun, Asahan"),
    "BA": ("Sumatera Barat", "Padang, Bukittinggi, Pariaman, Payakumbuh"),
    "BM": ("Riau", "Pekanbaru, Dumai, Kampar, Siak"),
    "BP": ("Kepulauan Riau", "Batam, Tanjungpinang, Bintan, Karimun"),
    "BH": ("Jambi", "Seluruh Jambi"),
    "BG": ("Sumatera Selatan", "Palembang, Ogan, Muara Enim, Lubuklinggau"),
    "BN": ("Kepulauan Bangka Belitung", "Pangkalpinang, Bangka, Belitung"),
    "BD": ("Bengkulu", "Seluruh Bengkulu"),
    "BE": ("Lampung", "Bandar Lampung, Metro, Lampung Selatan, Lampung Tengah"),
    # Jawa bagian barat
    "A": ("Banten", "Serang, Cilegon, Pandeglang, Lebak"),
    "B": ("DKI Jakarta dan sekitarnya", "Jakarta, Depok, Bekasi, Tangerang, Tangerang Selatan"),
    "D": ("Jawa Barat", "Bandung, Cimahi, Bandung Barat"),
    "E": ("Jawa Barat", "Cirebon, Indramayu, Majalengka, Kuningan"),
    "F": ("Jawa Barat", "Bogor, Sukabumi, Cianjur"),
    "T": ("Jawa Barat", "Karawang, Purwakarta, Subang"),
    "Z": ("Jawa Barat", "Garut, Tasikmalaya, Ciamis, Sumedang, Banjar, Pangandaran"),
    # Jawa Tengah dan DIY
    "G": ("Jawa Tengah", "Pekalongan, Tegal, Brebes, Batang, Pemalang"),
    "H": ("Jawa Tengah", "Semarang, Kendal, Salatiga, Demak"),
    "K": ("Jawa Tengah", "Pati, Kudus, Jepara, Rembang, Blora, Grobogan"),
    "R": ("Jawa Tengah", "Banyumas, Cilacap, Purbalingga, Banjarnegara"),
    "AA": ("Jawa Tengah", "Kedu: Magelang, Purworejo, Temanggung, Wonosobo, Kebumen"),
    "AD": ("Jawa Tengah", "Surakarta, Sukoharjo, Boyolali, Klaten, Sragen, Karanganyar, Wonogiri"),
    "AB": ("DI Yogyakarta", "Yogyakarta, Sleman, Bantul, Kulon Progo, Gunungkidul"),
    # Jawa Timur
    "L": ("Jawa Timur", "Surabaya"),
    "M": ("Jawa Timur", "Madura: Bangkalan, Sampang, Pamekasan, Sumenep"),
    "N": ("Jawa Timur", "Malang, Batu, Probolinggo, Pasuruan, Lumajang"),
    "P": ("Jawa Timur", "Besuki: Jember, Banyuwangi, Bondowoso, Situbondo"),
    "S": ("Jawa Timur", "Bojonegoro, Lamongan, Tuban, Mojokerto, Jombang"),
    "W": ("Jawa Timur", "Sidoarjo, Gresik"),
    "AE": ("Jawa Timur", "Madiun, Ngawi, Magetan, Ponorogo, Pacitan"),
    "AG": ("Jawa Timur", "Kediri, Blitar, Tulungagung, Nganjuk, Trenggalek"),
    # Bali dan Nusa Tenggara
    "DK": ("Bali", "Seluruh Bali"),
    "DR": ("Nusa Tenggara Barat", "Pulau Lombok: Mataram, Lombok Barat, Lombok Tengah, Lombok Timur"),
    "EA": ("Nusa Tenggara Barat", "Pulau Sumbawa: Sumbawa, Bima, Dompu"),
    "DH": ("Nusa Tenggara Timur", "Pulau Timor: Kupang, Timor Tengah, Belu"),
    "EB": ("Nusa Tenggara Timur", "Pulau Flores dan sekitarnya"),
    "ED": ("Nusa Tenggara Timur", "Pulau Sumba"),
    # Kalimantan
    "KB": ("Kalimantan Barat", "Pontianak, Singkawang, Sambas, Ketapang"),
    "KH": ("Kalimantan Tengah", "Palangka Raya, Kotawaringin, Kapuas"),
    "DA": ("Kalimantan Selatan", "Banjarmasin, Banjarbaru, Martapura"),
    "KT": ("Kalimantan Timur", "Samarinda, Balikpapan, Bontang, Kutai"),
    "KU": ("Kalimantan Utara", "Tarakan, Bulungan, Nunukan"),
    # Sulawesi, Maluku, Papua
    "DB": ("Sulawesi Utara", "Manado, Minahasa, Bolaang Mongondow"),
    "DL": ("Sulawesi Utara", "Kepulauan Sangihe dan Talaud"),
    "DM": ("Gorontalo", "Seluruh Gorontalo"),
    "DN": ("Sulawesi Tengah", "Palu, Donggala, Poso"),
    "DT": ("Sulawesi Tenggara", "Kendari, Kolaka, Bau-Bau"),
    "DD": ("Sulawesi Selatan", "Makassar, Gowa, Maros, Bone, Pare-Pare"),
    "DC": ("Sulawesi Barat", "Mamuju, Majene, Polewali Mandar"),
    "DE": ("Maluku", "Ambon, Maluku Tengah, Seram"),
    "DG": ("Maluku Utara", "Ternate, Tidore, Halmahera"),
    "PA": ("Papua", "Jayapura, Merauke, Biak"),
    "DS": ("Papua", "Kode lama wilayah Papua"),
    "PB": ("Papua Barat", "Manokwari, Sorong, Fakfak"),
    # Khusus
    "CD": ("Korps Diplomatik", "Kendaraan perwakilan negara asing"),
    "CC": ("Korps Konsuler", "Kendaraan perwakilan konsuler"),
    "RI": ("Pejabat negara", "Kode khusus kendaraan pejabat tinggi negara"),
}

PLAT_RE = re.compile(r"^([A-Z]{1,2})(\d{1,4})([A-Z]{0,3})$")


def parse_plate(raw):
    s = re.sub(r"[\s\-.]", "", raw.upper())
    m = PLAT_RE.match(s)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


def plate_lines(raw):
    p = parse_plate(raw)
    if not p:
        return wrap_plain("Format tidak dikenali. Contoh: B 1234 ABC, AB1234CD, DK 55 X.", AM)
    prefix, num, suffix = p
    info = PLAT.get(prefix)
    lines = kv("Plat", " ".join(x for x in (prefix, num, suffix) if x), vc=CY)
    lines += kv("Kode", prefix)
    if info:
        lines += kv("Wilayah", info[0], vc=LM)
        lines += kv("Cakupan", info[1])
    else:
        lines += kv("Wilayah", "Kode tidak ada di daftar tool ini", vc=AM)
    lines += kv("Nomor", num)
    if suffix:
        lines += kv("Seri", suffix)
    lines.append("")
    lines += wrap_plain("Hanya menunjukkan kode wilayah registrasi, bukan data pemilik. "
                        "Untuk data resmi gunakan layanan Samsat.", DM)
    return lines


def screen_plate():
    while True:
        header()
        panel("PLAT NOMOR", wrap_plain(
            "Masukkan plat nomor, contoh: B 1234 ABC atau AB1234CD. Kosongkan untuk kembali."))
        q = read_line()
        if not q or q.lower() == "b":
            return
        print()
        panel("HASIL PLAT NOMOR", plate_lines(q))
        if after_result("vehicle") == "home":
            return


# --------------------------------------------------------------------------
# Operator seluler
# --------------------------------------------------------------------------
OPERATOR = {}


def _reg(prefixes, operator, brand, group=""):
    for p in prefixes:
        OPERATOR[p] = (operator, brand, group)


_reg(["0811"], "Telkomsel", "kartuHalo")
_reg(["0812", "0813", "0821", "0822"], "Telkomsel", "simPATI")
_reg(["0823", "0852", "0853"], "Telkomsel", "Kartu AS")
_reg(["0851"], "Telkomsel", "by.U")
_reg(["0814", "0815", "0816", "0855", "0856", "0857", "0858"], "Indosat Ooredoo Hutchison", "IM3 / Mentari")
_reg(["0895", "0896", "0897", "0898", "0899"], "Tri (3)", "Tri", "Indosat Ooredoo Hutchison")
_reg(["0817", "0818", "0819", "0859", "0877", "0878"], "XL Axiata", "XL", "XLSmart")
_reg(["0831", "0832", "0833", "0838"], "AXIS", "AXIS", "XLSmart")
_reg(["0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"], "Smartfren", "Smartfren", "XLSmart")


def parse_phone(raw):
    """Kembalikan (nomor_dengan_0, dikonversi_dari_62) atau (None, alasan)."""
    s = re.sub(r"[\s\-.()]", "", raw)
    converted = False
    if s.startswith("+62"):
        s, converted = "0" + s[3:], True
    elif s.startswith("62") and len(s) >= 11:
        s, converted = "0" + s[2:], True
    if not s.isdigit():
        return None, "Nomor hanya boleh berisi angka."
    if not s.startswith("0"):
        return None, "Nomor harus diawali 0, contoh 0812xxxxxxxx."
    if not 10 <= len(s) <= 13:
        return None, "Panjang nomor tidak wajar (10-13 digit termasuk angka 0)."
    return s, converted


def fmt_phone(n):
    return "-".join(x for x in (n[:4], n[4:8], n[8:]) if x)


def phone_lines(raw):
    n, info = parse_phone(raw)
    if n is None:
        return wrap_plain(info, AM)
    lines = kv("Nomor", fmt_phone(n), vc=CY)
    if info:
        lines += wrap_plain("Format +62 dikonversi ke awalan 0.", DM)
    if n[1] != "8":
        lines += kv("Jenis", "Bukan nomor seluler (kemungkinan telepon tetap, kode area %s)" % n[:3], vc=AM)
        return lines
    pre = n[:4]
    op = OPERATOR.get(pre)
    lines += kv("Awalan", pre)
    if op:
        lines += kv("Operator", op[0], vc=LM)
        lines += kv("Merek", op[1])
        if op[2]:
            lines += kv("Grup", op[2])
    else:
        lines += kv("Operator", "Awalan tidak ada di daftar tool ini", vc=AM)
    lines.append("")
    lines += wrap_plain("Berdasarkan awalan asli. Nomor yang pindah operator (portabilitas) "
                        "tetap tampil sebagai operator awalnya.", DM)
    return lines


def screen_phone():
    while True:
        header()
        panel("OPERATOR SELULER", wrap_plain(
            "Masukkan nomor HP dengan awalan 0, contoh: 0812 3456 7890. Kosongkan untuk kembali."))
        q = read_line()
        if not q or q.lower() == "b":
            return
        print()
        panel("HASIL OPERATOR", phone_lines(q))
        if after_result("phone") == "home":
            return


def after_result(keyword):
    """Menu kecil setelah hasil. Return 'home' bila harus ke menu utama."""
    print(c(DM, "Enter = cek lagi   s = tools OSINT terkait   b = kembali"))
    s = read_line()
    if s is None:
        return "home"
    sl = s.lower()
    if sl == "b":
        return "home"
    if sl == "s":
        return related_tools(keyword)
    return None


# --------------------------------------------------------------------------
# Menu utama
# --------------------------------------------------------------------------
def startup(force=False):
    if FANCY:
        clear()
        for ln in banner_lines():
            print(ln)
            time.sleep(0.04)
        print()
        progress("modul lokal", 20)
    note("info", "Menyinkronkan OSINT Framework...")
    tree, src = load_framework(force)
    index_tree(tree, src)
    if src.startswith("bawaan"):
        note("warn", "Tidak bisa mengunduh arf.json, memakai daftar bawaan yang kecil.")
        time.sleep(1.2)
    else:
        note("ok", "%d tools dimuat (%s)." % (len(STATE["flat"]), src))
        if FANCY:
            time.sleep(0.5)


def screen_update():
    header()
    note("info", "Mengunduh ulang arf.json...")
    tree, src = load_framework(force=True)
    index_tree(tree, src)
    if src == "online":
        note("ok", "Selesai: %d tools." % len(STATE["flat"]))
    else:
        note("warn", "Gagal mengunduh, sumber aktif: %s." % src)
    time.sleep(1.5)


MENU = [
    ("1", "OSINT Framework", "jelajahi kategori dan tools"),
    ("2", "Cari Tools", "cari dengan kata kunci"),
    ("3", "Kode Pos", "wilayah dari kode pos atau nama"),
    ("4", "Plat Nomor", "daerah asal kendaraan"),
    ("5", "Operator HP", "dari awalan 08xx"),
    ("6", "Perbarui Data", "unduh ulang arf.json"),
    ("0", "Keluar", ""),
]


def main_menu():
    while True:
        header()
        inner = W() - 4
        lines = []
        for key, name, desc in MENU:
            left = c(MG, "[%s]" % key, True) + " " + c(WH, name.ljust(16))
            room = inner - 4 - 1 - 16 - 1
            lines.append(left + " " + c(DM, trunc(desc, room)))
        panel("MENU UTAMA", lines)
        s = read_line()
        if s is None or s == "0":
            break
        if s == "1":
            screen_browse()
        elif s == "2":
            screen_search()
        elif s == "3":
            screen_postal()
        elif s == "4":
            screen_plate()
        elif s == "5":
            screen_phone()
        elif s == "6":
            screen_update()
    clear()
    print(gradient("NEXUS offline. Sampai jumpa.", CY, MG))


def main():
    enable_ansi()
    global USE_COLOR, FANCY
    if "--fast" in sys.argv:
        FANCY = False
    try:
        startup(force="--update" in sys.argv)
        main_menu()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
