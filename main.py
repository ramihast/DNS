import customtkinter as ctk
from tkinter import messagebox
import subprocess, os, sys, json, re, ctypes, threading
import ipaddress

# ---------- اجرای خودکار به‌صورت ادمین ----------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit(0)

# حتماً بیرون از تابع و بدون تورفتگی
run_as_admin()  # اگر ادمین نباشد، برنامه را با Run as administrator دوباره اجرا می‌کند

# ---------- مسیر پایه مناسب برای exe تک‌فایله ----------

if getattr(sys, "frozen", False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

font_path = os.path.join(base_path, "assets", "Dana-Regular.ttf")
icon_path = os.path.join(base_path, "assets", "icon.ico")
DNS_FILE = os.path.join(base_path, "dns_list.json")
GAMES_FILE = os.path.join(base_path, "games_list.json")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

try:
    ctk.FontManager.load_font(font_path)
except:
    pass

RLM = "\u200f"

TXT = {
    "app_title": "DNS گیم اپتیمایزر",
    "app_subtitle": "بهترین DNS برای پینگ بهتر بازی‌ها",
    "btn_add_dns": "افزودن DNS",
    "btn_ping_all": "پینگ همه",
    "btn_ping_full": "تست کامل",
    "btn_current_dns": "DNS فعلی",
    "tab_dns": "DNS ها",
    "tab_games": "بازی‌ها",
    "status_ready": "آماده",
    "netcard_title": "کارت شبکه فعال",
    "btn_refresh": "به‌روزرسانی",
    "proto_title": "پروتکل",
    "tools_title": "ابزارهای سریع",
    "btn_flush_dns": "ریست DNS",   # تغییر داده شد
    "btn_reset_net": "ریست شبکه",
    "dns_added_title": "DNS جدید",
    "dns_name": "نام DNS",
    "dns_ip_main": "IP اصلی",
    "dns_ip_secondary": "IP دوم (اختیاری)",
    "btn_save": "ذخیره",
    "warn_required": "نام و IP اصلی الزامی هستند",
    "err_ip_main": "IP اصلی در فرمت IPv4/IPv6 معتبر نیست",
    "err_ip_second": "IP دوم در فرمت IPv4/IPv6 معتبر نیست",
    "warn_duplicate_name": "این نام قبلاً ثبت شده است",
    "status_dns_added": "افزوده شد",
    "edit_dns_title": "ویرایش DNS",
    "dns_ip_second": "IP دوم",
    "status_dns_edited": "ویرایش شد",
    "delete_only_custom": "فقط DNSهای ثبت‌شده توسط کاربر قابل حذف هستند",
    "delete_confirm": "آیا از حذف \"{name}\" مطمئن هستید؟",
    "status_dns_deleted": "حذف شد",
    "warn_select_interface": "لطفاً کارت شبکه را انتخاب کنید",
    "err_invalid_dns_ips": "این DNS شامل IP نامعتبر است، لطفاً اصلاح کنید",
    "status_dns_applied": "روی «{iface}» اعمال شد",
    "err_set_dns": "اعمال DNS با خطا مواجه شد",
    "status_ping_single": "در حال پینگ «{name}»...",
    "status_ping_single_done": "پینگ «{name}»: {lat}",
    "info_no_dns": "هیچ DNSای برای تست یافت نشد",
    "status_ping_all": "پینگ {i}/{total} - «{name}»",
    "ping_results_title": "نتایج پینگ",
    "ping_results_header": "نتیجه پینگ DNSها",
    "ping_results_sub": "{count} سرور تست شد",
    "ping_line": "{name} - {ip}: {val}",
    "full_test_title_info": "تست کامل",
    "full_test_no_dns": "هیچ DNSای برای تست کامل وجود ندارد",
    "status_full_test": "تست کامل {i}/{total} - «{name}»",
    "status_full_test_done": "تست کامل DNSها تمام شد",
    "full_test_win_title": "تست کامل DNS",
    "full_test_header": "رتبه‌بندی DNSها",
    "full_test_sub": "{count} سرور تست شد (پینگ، جیتر، پکت‌لاس، امتیاز)",
    "full_test_line": "{idx}. {name} - {ip} | پینگ: {ap} | جیتر: {jl} | پکت‌لاس: {pl} | امتیاز: {sc}",
    "games_best_dns": "بهترین DNS",
    "games_best_title": "بهترین DNS برای بازی",
    "games_best_body": "بهترین DNS برای «{game}»: {name} ({ip}) با پینگ حدود {lat}ms",
    "games_best_not_found": "DNS مناسبی برای این بازی یافت نشد",
    "text_win_close": "بستن",
    "current_dns_title": "DNS فعلی",
    "current_dns_header": "📡 DNSهای فعلی رابط‌های متصل",
    "current_dns_none": "DNS تنظیم نشده است",
    "flush_ok": "✅ DNS اینترفیس انتخاب‌شده ریست شد",
    "flush_err": "ریست DNS با خطا مواجه شد",
    "reset_confirm": "آیا از ریست تنظیمات شبکه مطمئن هستید؟",
    "reset_ok": "ریست شبکه انجام شد. لطفاً سیستم را ریستارت کنید.",
    "reset_err": "ریست شبکه با خطا مواجه شد",
    "msg_error": "خطا",
    "msg_warning": "⚠️",
    "msg_delete": "حذف",
    "no_interface": "(هیچ کارت شبکه‌ای یافت نشد)",
    "loading_interface": "(در حال بارگذاری...)",
    "btn_set": "اعمال",
    "btn_ping": "پینگ",
    "cat_local": "ایرانی",
    "cat_global": "جهانی",
    "cat_custom": "کاستوم",
}

DEFAULT_DNS = {
    "local": {
        "Shecan": ["178.22.122.100", "185.51.200.2"],
        "Radar": ["10.202.10.10", "10.202.10.11"],
        "Begzar": ["185.55.226.26", "185.55.225.25"],
        "Electro": ["78.157.42.100", "78.157.42.101"],
        "HostIran": ["173.244.49.6", "173.244.49.7"],
        "403Online": ["10.202.10.202", "10.202.10.102"],
        "DNSPro": ["185.55.225.25", "185.55.226.26"],
        "Shatel": ["85.15.1.14", "85.15.1.15"],
        "ParsOnline": ["91.99.96.1", "91.99.96.2"],
        "Mobinnet": ["192.168.100.100", "192.168.100.200"],
    },
    "global": {
        "Google": ["8.8.8.8", "8.8.4.4"],
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Quad9": ["9.9.9.9", "149.112.112.112"],
        "OpenDNS": ["208.67.222.222", "208.67.220.220"],
        "AdGuard": ["94.140.14.14", "94.140.15.15"],
        "CleanBrowsing": ["185.228.168.9", "185.228.169.9"],
        "DNSWatch": ["84.200.69.80", "84.200.70.40"],
        "Yandex": ["77.88.8.8", "77.88.8.1"],
        "Comodo": ["8.26.56.26", "8.20.247.20"],
        "Neustar": ["156.154.70.5", "156.154.71.5"],
    },
    "custom": {}
}

DEFAULT_GAMES = {
    "Fortnite": {"Cloudflare": ["1.1.1.1", "1.0.0.1"], "Google": ["8.8.8.8", "8.8.4.4"]},
    "Valorant": {"Google": ["8.8.8.8", "8.8.4.4"], "Cloudflare": ["1.1.1.1", "1.0.0.1"]},
    "CS2": {"Cloudflare": ["1.1.1.1", "1.0.0.1"], "Quad9": ["9.9.9.9", "149.112.112.112"]},
    "LeagueOfLegends": {"Google": ["8.8.8.8", "8.8.4.4"], "OpenDNS": ["208.67.222.222", "208.67.220.220"]},
    "Dota2": {"Cloudflare": ["1.1.1.1", "1.0.0.1"], "AdGuard": ["94.140.14.14", "94.140.15.15"]},
    "PUBG": {"Google": ["8.8.8.8", "8.8.4.4"], "Quad9": ["9.9.9.9", "149.112.112.112"]},
    "ApexLegends": {"Cloudflare": ["1.1.1.1", "1.0.0.1"], "Google": ["8.8.8.8", "8.8.4.4"]},
    "Warzone": {"Quad9": ["9.9.9.9", "149.112.112.112"], "Cloudflare": ["1.1.1.1", "1.0.0.1"]},
    "Overwatch2": {"Google": ["8.8.8.8", "8.8.4.4"], "Cloudflare": ["1.1.1.1", "1.0.0.1"]},
    "RocketLeague": {"Cloudflare": ["1.1.1.1", "1.0.0.1"], "Google": ["8.8.8.8", "8.8.4.4"]},
}

def is_valid_ip(ip: str) -> bool:
    ip = ip.strip()
    if not ip:
        return False
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def clean_dns_dict(d: dict) -> dict:
    cleaned = {}
    for name, ips in d.items():
        valid_ips = [ip for ip in ips if is_valid_ip(ip)]
        if valid_ips:
            cleaned[name] = valid_ips
    return cleaned

def load_json_safe(path, default):
    try:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2, ensure_ascii=False)
            return default
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            for cat, servers in list(data.items()):
                if isinstance(servers, dict):
                    data[cat] = clean_dns_dict(servers)
        return data
    except:
        return default

def save_json_safe(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ping_latency(ip, timeout_ms=1000):
    try:
        af_switch = "-6" if ":" in ip else "-4"
        args = ["ping", af_switch, "-n", "1", "-w", str(timeout_ms), ip]
        r = subprocess.run(args, capture_output=True, text=True,
                           encoding="utf-8", errors="ignore")
        if r.returncode != 0 and "TTL=" not in r.stdout.upper():
            return float("inf")
        s = r.stdout
        if re.search(r"<\s*1\s*ms", s, flags=re.IGNORECASE):
            return 1
        m = re.search(r"(\d+)\s*ms", s, flags=re.IGNORECASE)
        return int(m.group(1)) if m else float("inf")
    except Exception:
        return float("inf")

def ping_stats(ip, count=5, timeout_ms=1000):
    rtts, lost = [], 0
    for _ in range(count):
        try:
            af_switch = "-6" if ":" in ip else "-4"
            args = ["ping", af_switch, "-n", "1", "-w", str(timeout_ms), ip]
            r = subprocess.run(args, capture_output=True, text=True,
                               encoding="utf-8", errors="ignore")
            s = r.stdout
            if r.returncode != 0 or "TTL=" not in s.upper():
                lost += 1
            else:
                if re.search(r"<\s*1\s*ms", s, flags=re.IGNORECASE):
                    rtts.append(1.0)
                else:
                    m = re.search(r"(\d+)\s*ms", s, flags=re.IGNORECASE)
                    if m:
                        rtts.append(float(m.group(1)))
                    else:
                        lost += 1
        except Exception:
            lost += 1
    total = count
    if not rtts:
        return float("inf"), float("inf"), float("inf")
    avg_ping = sum(rtts) / len(rtts)
    packet_loss = (lost / total) * 100.0
    if len(rtts) >= 2:
        diffs = [abs(rtts[i] - rtts[i-1]) for i in range(1, len(rtts))]
        jitter = sum(diffs) / len(diffs)
    else:
        jitter = 0.0
    return avg_ping, packet_loss, jitter

class DNSGameOptimizer:
    def __init__(self):
        self.root = ctk.CTk()
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass

        self.root.geometry("900x700")
        self.root.minsize(780, 600)
        self.root.resizable(True, True)
        self.root.title(f"{RLM}{TXT['app_title']}")

        self.green = "#22c55e"
        self.dark = "#1e1e1e"
        self.darker = "#1b1b1b"
        self.card = "#2a2f2a"
        self.blue = "#3b82f6"

        self.font_title = ctk.CTkFont(family="Dana", size=22, weight="bold")
        self.font_header = ctk.CTkFont(family="Dana", size=14, weight="bold")
        self.font_normal = ctk.CTkFont(family="Dana", size=12, weight="bold")

        self.dns_data = load_json_safe(DNS_FILE, DEFAULT_DNS)
        self.games_data = load_json_safe(GAMES_FILE, DEFAULT_GAMES)

        self.interface_names = []
        self.selected_interface = ctk.StringVar(value=f"{RLM}{TXT['loading_interface']}")
        self.protocol_mode = ctk.StringVar(value="IPv4")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        self.setup_ui()
        self.update_interface_list()

    # شبکه
    def get_all_interfaces(self):
        interfaces = []
        try:
            r = subprocess.run(
                "netsh interface show interface",
                shell=True, capture_output=True, text=True,
                encoding="utf-8", errors="ignore"
            )
            lines = r.stdout.splitlines()
            active_interfaces, all_interfaces = [], []
            for line in lines:
                line = line.strip()
                if not line or line.startswith("-"):
                    continue
                if "Admin State" in line and "State" in line:
                    continue
                parts = re.split(r"\s{2,}", line)
                if len(parts) >= 4:
                    name = parts[-1].strip()
                    if not name:
                        continue
                    state = "Connected" if "Connected" in line else "Disconnected"
                    all_interfaces.append((name, state))
                    if "Connected" in line:
                        active_interfaces.append((name, state))
            interfaces = active_interfaces + [i for i in all_interfaces if i not in active_interfaces]
        except Exception:
            pass
        if not interfaces:
            interfaces = [
                ("Wi-Fi", "Connected"),
                ("Ethernet", "Disconnected"),
                ("Local Area Connection", "Disconnected"),
            ]
        return interfaces[:20]

    def update_interface_list(self):
        all_interfaces = self.get_all_interfaces()
        active = [n for n, s in all_interfaces if s == "Connected"]
        inactive = [n for n, s in all_interfaces if s != "Connected"]
        self.interface_names = active + inactive
        if not self.interface_names:
            self.interface_names = [f"{RLM}{TXT['no_interface']}"]

        if self.selected_interface.get() not in self.interface_names:
            self.selected_interface.set(self.interface_names[0])

        if hasattr(self, "interface_menu"):
            self.interface_menu.configure(values=self.interface_names)
        if hasattr(self, "status"):
            self.update_status_display()

    def update_status_display(self):
        net = self.selected_interface.get()
        proto = self.protocol_mode.get()
        self.status.configure(text=f"{RLM}{net} | {proto}", text_color=self.green)

    def on_interface_change(self, selection):
        self.selected_interface.set(selection)
        self.update_status_display()

    def on_protocol_change(self, selection):
        self.protocol_mode.set(selection)
        self.update_status_display()

    def refresh_interfaces(self):
        self.update_interface_list()
        self.status.configure(text=f"{RLM}{TXT['btn_refresh']}", text_color=self.green)

    # UI اصلی
    def setup_ui(self):
        main = ctk.CTkFrame(self.root, fg_color=self.dark)
        main.grid(row=0, column=0, sticky="nsew")
        main.grid_rowconfigure(2, weight=1)
        main.grid_columnconfigure(0, weight=1)

        title = ctk.CTkFrame(main, fg_color=self.dark)
        title.grid(row=0, column=0, sticky="ew", pady=(10, 0))
        ctk.CTkLabel(
            title, text=f"{RLM}{TXT['app_title']}",
            text_color=self.green, font=self.font_title
        ).pack(pady=(4, 2))
        ctk.CTkLabel(
            title, text=f"{RLM}{TXT['app_subtitle']}",
            text_color="#bfbfbf", font=self.font_normal
        ).pack(pady=(0, 6))

        topbar = ctk.CTkFrame(main, fg_color=self.darker)
        topbar.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 0))
        topbar.grid_columnconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        left_frame.pack(expand=True)

        top_btn_width = 120
        top_btn_height = 32

        self.btn_tab_dns = ctk.CTkButton(
            left_frame, text=f"{RLM}{TXT['tab_dns']}",
            width=top_btn_width, height=top_btn_height,
            fg_color=self.green, hover_color="#23985d",
            text_color=self.darker, font=self.font_normal,
            command=lambda: self.on_top_tab_change("dns")
        )
        self.btn_tab_dns.pack(side="left", padx=4, pady=8)

        self.btn_tab_games = ctk.CTkButton(
            left_frame, text=f"{RLM}{TXT['tab_games']}",
            width=top_btn_width, height=top_btn_height,
            fg_color="#111111", hover_color="#374151",
            text_color="white", font=self.font_normal,
            command=lambda: self.on_top_tab_change("games")
        )
        self.btn_tab_games.pack(side="left", padx=4, pady=8)

        self.btn_add_dns = ctk.CTkButton(
            left_frame, text=f"{RLM}{TXT['btn_add_dns']}",
            width=top_btn_width, height=top_btn_height,
            fg_color=self.green, hover_color="#23985d",
            text_color=self.darker, font=self.font_normal,
            command=self.open_add_dns_window
        )
        self.btn_add_dns.pack(side="left", padx=4, pady=8)

        self.btn_current_dns = ctk.CTkButton(
            left_frame, text=f"{RLM}{TXT['btn_current_dns']}",
            width=top_btn_width, height=top_btn_height,
            fg_color=self.green, hover_color="#23985d",
            text_color=self.darker, font=self.font_normal,
            command=self.show_current_dns
        )
        self.btn_current_dns.pack(side="left", padx=4, pady=8)

        self.btn_ping_all = ctk.CTkButton(
            left_frame, text=f"{RLM}{TXT['btn_ping_all']}",
            width=top_btn_width, height=top_btn_height,
            fg_color=self.green, hover_color="#23985d",
            text_color=self.darker, font=self.font_normal,
            command=self.ping_all_dns
        )
        self.btn_ping_all.pack(side="left", padx=4, pady=8)

        self.btn_ping_full = ctk.CTkButton(
            left_frame, text=f"{RLM}{TXT['btn_ping_full']}",
            width=top_btn_width, height=top_btn_height,
            fg_color=self.blue, hover_color="#2563eb",
            text_color="white", font=self.font_normal,
            command=self.ping_all_advanced
        )
        self.btn_ping_full.pack(side="left", padx=4, pady=8)

        content = ctk.CTkFrame(main, fg_color=self.dark)
        content.grid(row=2, column=0, sticky="nsew", padx=10, pady=8)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self.tab_dns_root = ctk.CTkFrame(content, fg_color=self.dark)
        self.tab_games_root = ctk.CTkFrame(content, fg_color=self.dark)
        self.tab_dns_root.grid(row=0, column=0, sticky="nsew")
        self.tab_games_root.grid(row=0, column=0, sticky="nsew")
        self.tab_games_root.grid_remove()

        # تب DNS
        dns_root = ctk.CTkFrame(self.tab_dns_root, fg_color=self.dark)
        dns_root.pack(fill="both", expand=True, padx=6, pady=(6, 0))
        dns_root.grid_rowconfigure(1, weight=1)
        dns_root.grid_columnconfigure(0, weight=1)

        cats_row = ctk.CTkFrame(dns_root, fg_color=self.dark)
        cats_row.grid(row=0, column=0, sticky="ew", pady=(6, 6))
        for c in range(3):
            cats_row.grid_columnconfigure(c, weight=1)

        self.btn_cat_local = ctk.CTkButton(
            cats_row, text=f"{RLM}{TXT['cat_local']}",
            fg_color=self.green, hover_color="#16a34a",
            text_color="black", font=self.font_header,
            height=30, corner_radius=8,
            command=lambda: self.set_dns_category("local")
        )
        self.btn_cat_local.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_cat_global = ctk.CTkButton(
            cats_row, text=f"{RLM}{TXT['cat_global']}",
            fg_color="#1f2933", hover_color="#374151",
            text_color="white", font=self.font_header,
            height=30, corner_radius=8,
            command=lambda: self.set_dns_category("global")
        )
        self.btn_cat_global.grid(row=0, column=1, padx=4, sticky="ew")

        self.btn_cat_custom = ctk.CTkButton(
            cats_row, text=f"{RLM}{TXT['cat_custom']}",
            fg_color="#1f2933", hover_color="#374151",
            text_color="white", font=self.font_header,
            height=30, corner_radius=8,
            command=lambda: self.set_dns_category("custom")
        )
        self.btn_cat_custom.grid(row=0, column=2, padx=4, sticky="ew")

        self.dns_list_frame = ctk.CTkScrollableFrame(dns_root, fg_color=self.dark)
        self.dns_list_frame.grid(row=1, column=0, sticky="nsew", pady=(4, 0))

        # تب بازی‌ها
        self.frame_games = ctk.CTkScrollableFrame(self.tab_games_root, fg_color=self.dark)
        self.frame_games.pack(fill="both", expand=True, padx=10, pady=6)

        # نوار پایینی
        self.bottom_settings = self.build_bottom_settings()
        self.bottom_settings.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 4))

        self.current_dns_category = "local"
        self.build_dns_list()
        self.build_games_tab()

        self.status = ctk.CTkLabel(
            self.root, text=f"{RLM}{TXT['status_ready']}",
            anchor="center", font=self.font_normal,
            text_color=self.green, fg_color=self.darker, height=24
        )
        self.status.grid(row=2, column=0, sticky="ew", pady=(0, 2))

        self.on_top_tab_change("dns")

    def build_bottom_settings(self):
        frame = ctk.CTkFrame(self.root, fg_color=self.dark)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        # کارت شبکه
        netcard = ctk.CTkFrame(frame, fg_color=self.card, corner_radius=12)
        netcard.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        netcard.grid_columnconfigure(0, weight=1)
        netcard.grid_columnconfigure(1, weight=0)

        self.netlabel = ctk.CTkLabel(
            netcard, text=f"{RLM}{TXT['netcard_title']}",
            font=self.font_header, text_color=self.green,
            anchor="e", justify="right"
        )
        self.netlabel.grid(row=0, column=0, columnspan=2, sticky="e",
                           padx=10, pady=(10, 4))

        self.interface_menu = ctk.CTkOptionMenu(
            netcard, variable=self.selected_interface,
            values=self.interface_names,
            fg_color=self.darker, button_color=self.green,
            button_hover_color="#23985d",
            text_color="white", font=self.font_normal,
            width=180, height=32,
            command=self.on_interface_change
        )
        self.interface_menu.grid(row=1, column=0, sticky="ew",
                                 padx=(10, 4), pady=(0, 10))

        self.btn_refresh_if = ctk.CTkButton(
            netcard, text=f"{RLM}{TXT['btn_refresh']}",
            fg_color=self.blue, hover_color="#2563eb",
            text_color="white", font=self.font_normal,
            width=110, height=32, command=self.refresh_interfaces
        )
        self.btn_refresh_if.grid(row=1, column=1, sticky="e",
                                 padx=(0, 10), pady=(0, 10))

        # پروتکل
        protocard = ctk.CTkFrame(frame, fg_color=self.card, corner_radius=12)
        protocard.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)
        protocard.grid_columnconfigure(0, weight=1)

        self.protolabel = ctk.CTkLabel(
            protocard, text=f"{RLM}{TXT['proto_title']}",
            font=self.font_header, text_color=self.green,
            anchor="e", justify="right"
        )
        self.protolabel.grid(row=0, column=0, sticky="e",
                             padx=10, pady=(10, 4))

        self.protocol_menu = ctk.CTkOptionMenu(
            protocard, variable=self.protocol_mode,
            values=["IPv4", "IPv6"],
            fg_color=self.darker, button_color=self.green,
            button_hover_color="#23985d",
            text_color="white", font=self.font_normal,
            width=140, height=32,
            command=self.on_protocol_change
        )
        self.protocol_menu.grid(row=1, column=0, sticky="e",
                                padx=10, pady=(0, 10))

        # ابزارهای سریع
        toolscard = ctk.CTkFrame(frame, fg_color=self.card, corner_radius=12)
        toolscard.grid(row=0, column=2, sticky="nsew", padx=4, pady=4)
        toolscard.grid_columnconfigure(0, weight=1)

        self.toolslabel = ctk.CTkLabel(
            toolscard, text=f"{RLM}{TXT['tools_title']}",
            font=self.font_header, text_color=self.green,
            anchor="e", justify="right"
        )
        self.toolslabel.grid(row=0, column=0, sticky="e",
                             padx=10, pady=(10, 4))

        btnframe = ctk.CTkFrame(toolscard, fg_color="transparent")
        btnframe.grid(row=1, column=0, sticky="e",
                      pady=(6, 10), padx=10)

        self.btn_flush = ctk.CTkButton(
            btnframe, text=f"{RLM}{TXT['btn_flush_dns']}",
            fg_color="#3fb881", hover_color="#2fa668",
            text_color=self.darker, font=self.font_normal,
            width=130, height=32, command=self.flush_dns
        )
        self.btn_flush.pack(side="right", padx=4, pady=4)

        self.btn_reset_net = ctk.CTkButton(
            btnframe, text=f"{RLM}{TXT['btn_reset_net']}",
            fg_color="#f59e0b", hover_color="#d97706",
            text_color="white", font=self.font_normal,
            width=130, height=32, command=self.restart_network
        )
        self.btn_reset_net.pack(side="right", padx=4, pady=4)

        return frame

    def on_top_tab_change(self, which):
        if which == "dns":
            self.tab_games_root.grid_remove()
            self.tab_dns_root.grid()
            self.btn_tab_dns.configure(fg_color=self.green, text_color=self.darker)
            self.btn_tab_games.configure(fg_color="#111111", text_color="white")
        else:
            self.tab_dns_root.grid_remove()
            self.tab_games_root.grid()
            self.btn_tab_games.configure(fg_color=self.green, text_color=self.darker)
            self.btn_tab_dns.configure(fg_color="#111111", text_color="white")

    def set_dns_category(self, cat):
        self.current_dns_category = cat
        if cat == "local":
            self.btn_cat_local.configure(fg_color=self.green, text_color="black")
            self.btn_cat_global.configure(fg_color="#1f2933", text_color="white")
            self.btn_cat_custom.configure(fg_color="#1f2933", text_color="white")
        elif cat == "global":
            self.btn_cat_local.configure(fg_color="#1f2933", text_color="white")
            self.btn_cat_global.configure(fg_color=self.green, text_color="black")
            self.btn_cat_custom.configure(fg_color="#1f2933", text_color="white")
        else:
            self.btn_cat_local.configure(fg_color="#1f2933", text_color="white")
            self.btn_cat_global.configure(fg_color="#1f2933", text_color="white")
            self.btn_cat_custom.configure(fg_color=self.green, text_color="black")
        self.build_dns_list()

    def build_dns_list(self):
        for w in self.dns_list_frame.winfo_children():
            w.destroy()

        servers = self.dns_data.get(self.current_dns_category, {})
        grid = ctk.CTkFrame(self.dns_list_frame, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=2, pady=2)
        for c in range(4):
            grid.grid_columnconfigure(c, weight=1)

        row, col = 0, 0
        for name, ips in servers.items():
            card = ctk.CTkFrame(grid, fg_color=self.card, corner_radius=8)
            card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

            ctk.CTkLabel(
                card, text=f"{RLM}{name}",
                font=self.font_header, text_color=self.green,
                anchor="center"
            ).pack(pady=(4, 2), padx=4)

            ip_text = "\n".join(ips)
            ctk.CTkLabel(
                card, text=ip_text,
                text_color="#cccccc",
                font=ctk.CTkFont(family="Dana", size=11, weight="bold"),
                anchor="center", justify="center"
            ).pack(pady=(0, 4), padx=4)

            btn_frame = ctk.CTkFrame(card, fg_color="transparent")
            btn_frame.pack(pady=(0, 4))

            ctk.CTkButton(
                btn_frame, text=f"{RLM}{TXT['btn_set']}",
                width=60, fg_color=self.green,
                hover_color="#23985d", text_color=self.darker,
                font=self.font_normal,
                command=lambda n=name, i=ips: self.apply_dns(n, i)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                btn_frame, text=f"{RLM}{TXT['btn_ping']}",
                width=60, fg_color="#555555",
                hover_color="#444444", text_color=self.green,
                font=self.font_normal,
                command=lambda n=name, i=ips: self.ping_single(n, i)
            ).pack(side="left", padx=2)

            if self.current_dns_category == "custom":
                edit_frame = ctk.CTkFrame(card, fg_color="transparent")
                edit_frame.pack(pady=(0, 4))

                ctk.CTkButton(
                    edit_frame, text=f"{RLM}ویرایش",
                    fg_color=self.blue, hover_color="#2563eb",
                    text_color="white", font=self.font_normal,
                    width=70, height=26,
                    command=lambda n=name: self.open_edit_dns_window("custom", n)
                ).pack(side="left", padx=4)

                ctk.CTkButton(
                    edit_frame, text=f"{RLM}حذف",
                    fg_color="#ef4444", hover_color="#b91c1c",
                    text_color="white", font=self.font_normal,
                    width=70, height=26,
                    command=lambda n=name: self.delete_dns("custom", n)
                ).pack(side="left", padx=4)

            col += 1
            if col >= 4:
                col = 0
                row += 1

    def build_games_tab(self):
        grid = ctk.CTkFrame(self.frame_games, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=10, pady=10)
        for c in range(4):
            grid.grid_columnconfigure(c, weight=1)

        row, col = 0, 0
        for game in self.games_data.keys():
            card = ctk.CTkFrame(grid, fg_color=self.card, corner_radius=10)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            game_label_text = TXT.get(f"game_{game}", game)
            ctk.CTkLabel(
                card, text=f"{RLM}{game_label_text}",
                font=self.font_header, text_color=self.green,
                anchor="center"
            ).pack(pady=(8, 4), padx=8)

            ctk.CTkButton(
                card, text=f"{RLM}{TXT['games_best_dns']}",
                width=110, fg_color=self.green,
                hover_color="#23985d", text_color=self.darker,
                font=self.font_normal,
                command=lambda g=game: self.optimize_for_game(g)
            ).pack(pady=(0, 10), padx=8)

            col += 1
            if col >= 4:
                col = 0
                row += 1

    # CRUD DNS
    def open_add_dns_window(self):
        w = ctk.CTkToplevel(self.root)
        w.title(TXT["dns_added_title"])
        w.geometry("420x320")
        w.configure(fg_color=self.dark)

        ctk.CTkLabel(
            w, text=f"{RLM}{TXT['dns_name']}",
            text_color=self.green, font=self.font_normal
        ).pack(pady=(16, 6))
        name = ctk.CTkEntry(w, width=350, font=self.font_normal, height=32)
        name.pack(pady=4)

        ctk.CTkLabel(
            w, text=f"{RLM}{TXT['dns_ip_main']}",
            text_color=self.green, font=self.font_normal
        ).pack(pady=(10, 6))
        ip1 = ctk.CTkEntry(w, width=350, font=self.font_normal, height=32)
        ip1.pack(pady=4)

        ctk.CTkLabel(
            w, text=f"{RLM}{TXT['dns_ip_secondary']}",
            text_color=self.green, font=self.font_normal
        ).pack(pady=(10, 6))
        ip2 = ctk.CTkEntry(w, width=350, font=self.font_normal, height=32)
        ip2.pack(pady=(0, 16))

        def save():
            n = name.get().strip()
            i1 = ip1.get().strip()
            i2 = ip2.get().strip()

            if not n or not i1:
                messagebox.showwarning(TXT["msg_warning"], TXT["warn_required"])
                return
            if not is_valid_ip(i1):
                messagebox.showerror(TXT["msg_error"], TXT["err_ip_main"])
                return
            if i2 and not is_valid_ip(i2):
                messagebox.showerror(TXT["msg_error"], TXT["err_ip_second"])
                return

            self.dns_data.setdefault("custom", {})
            if n in self.dns_data["custom"]:
                messagebox.showwarning(TXT["msg_warning"], TXT["warn_duplicate_name"])
                return

            ips_list = [i1]
            if i2:
                ips_list.append(i2)
            self.dns_data["custom"][n] = ips_list
            save_json_safe(DNS_FILE, self.dns_data)
            self.build_dns_list()
            self.status.configure(
                text=f"{RLM}{n} {TXT['status_dns_added']}",
                text_color=self.green
            )
            w.destroy()

        ctk.CTkButton(
            w, text=f"{RLM}{TXT['btn_save']}",
            fg_color=self.green, width=200, height=36,
            font=self.font_normal, command=save
        ).pack(pady=(0, 14))

    def open_edit_dns_window(self, category, dns_name):
        if category != "custom":
            messagebox.showwarning(TXT["msg_warning"], TXT["delete_only_custom"])
            return

        current_ips = self.dns_data.get(category, {}).get(dns_name, [])
        w = ctk.CTkToplevel(self.root)
        w.title(TXT["edit_dns_title"])
        w.geometry("420x320")
        w.configure(fg_color=self.dark)

        ctk.CTkLabel(
            w, text=f"{RLM}{TXT['dns_name']}",
            text_color=self.green, font=self.font_normal
        ).pack(pady=(16, 6))
        name_entry = ctk.CTkEntry(w, width=350, font=self.font_normal, height=32)
        name_entry.pack(pady=4)
        name_entry.insert(0, dns_name)

        ctk.CTkLabel(
            w, text=f"{RLM}{TXT['dns_ip_main']}",
            text_color=self.green, font=self.font_normal
        ).pack(pady=(10, 6))
        ip1_entry = ctk.CTkEntry(w, width=350, font=self.font_normal, height=32)
        ip1_entry.pack(pady=4)
        if len(current_ips) >= 1:
            ip1_entry.insert(0, current_ips[0])

        ctk.CTkLabel(
            w, text=f"{RLM}{TXT['dns_ip_second']}",
            text_color=self.green, font=self.font_normal
        ).pack(pady=(10, 6))
        ip2_entry = ctk.CTkEntry(w, width=350, font=self.font_normal, height=32)
        ip2_entry.pack(pady=(0, 16))
        if len(current_ips) >= 2:
            ip2_entry.insert(0, current_ips[1])

        def save_edit():
            new_name = name_entry.get().strip()
            i1 = ip1_entry.get().strip()
            i2 = ip2_entry.get().strip()

            if not new_name or not i1:
                messagebox.showwarning(TXT["msg_warning"], TXT["warn_required"])
                return
            if not is_valid_ip(i1):
                messagebox.showerror(TXT["msg_error"], TXT["err_ip_main"])
                return
            if i2 and not is_valid_ip(i2):
                messagebox.showerror(TXT["msg_error"], TXT["err_ip_second"])
                return

            cat_dict = self.dns_data.setdefault(category, {})
            if new_name != dns_name and new_name in cat_dict:
                messagebox.showwarning(TXT["msg_warning"], TXT["warn_duplicate_name"])
                return

            if new_name != dns_name:
                cat_dict.pop(dns_name, None)

            ips_list = [i1]
            if i2:
                ips_list.append(i2)
            cat_dict[new_name] = ips_list
            save_json_safe(DNS_FILE, self.dns_data)
            self.build_dns_list()
            self.status.configure(
                text=f"{RLM}{new_name} {TXT['status_dns_edited']}",
                text_color=self.green
            )
            w.destroy()

        ctk.CTkButton(
            w, text=f"{RLM}{TXT['btn_save']}",
            fg_color=self.green, width=200, height=36,
            font=self.font_normal, command=save_edit
        ).pack(pady=(0, 14))

    def delete_dns(self, category, dns_name):
        if category != "custom":
            messagebox.showwarning(TXT["msg_warning"], TXT["delete_only_custom"])
            return
        if not messagebox.askyesno(
            TXT["msg_delete"],
            TXT["delete_confirm"].format(name=dns_name)
        ):
            return
        try:
            cat_dict = self.dns_data.get(category, {})
            if dns_name in cat_dict:
                cat_dict.pop(dns_name)
                save_json_safe(DNS_FILE, self.dns_data)
                self.build_dns_list()
                self.status.configure(
                    text=f"{RLM}{dns_name} {TXT['status_dns_deleted']}",
                    text_color="#ff5555"
                )
        except Exception as e:
            messagebox.showerror(TXT["msg_error"], str(e))

    # اعمال DNS و پینگ
    def apply_dns(self, name, ips):
        interface = self.selected_interface.get()
        if TXT["no_interface"] in interface or TXT["loading_interface"] in interface:
            messagebox.showwarning(TXT["msg_warning"], TXT["warn_select_interface"])
            return

        checked_ips = [ip.strip() for ip in ips if ip.strip()]
        if not checked_ips or not all(is_valid_ip(ip) for ip in checked_ips):
            messagebox.showerror(TXT["msg_error"], TXT["err_invalid_dns_ips"])
            return

        proto = self.protocol_mode.get().lower()
        try:
            subprocess.run(
                f'netsh interface {proto} delete dnsservers name="{interface}" all',
                shell=True, check=True
            )
            subprocess.run(
                f'netsh interface {proto} set dnsservers name="{interface}" static {checked_ips[0]} primary',
                shell=True, check=True
            )
            if len(checked_ips) > 1:
                subprocess.run(
                    f'netsh interface {proto} add dnsservers name="{interface}" {checked_ips[1]} index=2',
                    shell=True, check=True
                )
            self.status.configure(
                text=f"{RLM}{name} {TXT['status_dns_applied'].format(iface=interface)}",
                text_color=self.green
            )
        except subprocess.CalledProcessError:
            messagebox.showerror(TXT["msg_error"], TXT["err_set_dns"])
        except Exception as e:
            messagebox.showerror(TXT["msg_error"], str(e))

    def ping_single(self, name, ips):
        def worker():
            self.status.configure(
                text=f"{RLM}{TXT['status_ping_single'].format(name=name)}",
                text_color=self.green
            )
            lat = ping_latency(ips[0])
            statustext = f"{lat} ms" if lat != float("inf") else "Timeout"
            self.status.configure(
                text=f"{RLM}{TXT['status_ping_single_done'].format(name=name, lat=statustext)}",
                text_color=self.green
            )
        threading.Thread(target=worker, daemon=True).start()

    def ping_all_dns(self):
        all_ips = [(n, i[0]) for c in self.dns_data.values() for n, i in c.items()]
        if not all_ips:
            messagebox.showinfo(TXT["ping_results_title"], TXT["info_no_dns"])
            return
        threading.Thread(
            target=self.ping_all_thread,
            args=(all_ips,),
            daemon=True
        ).start()

    def ping_all_thread(self, dns_list):
        results = []
        total = len(dns_list)
        for idx, (n, ip) in enumerate(dns_list, start=1):
            self.root.after(
                0,
                lambda i=idx, name=n: self.status.configure(
                    text=f"{RLM}{TXT['status_ping_all'].format(i=i, total=total, name=name)}",
                    text_color=self.green
                )
            )
            lat = ping_latency(ip)
            results.append((n, ip, lat))
        self.root.after(0, lambda: self.show_ping_results(results))

    def show_ping_results(self, results):
        lines = []
        for name, ip, lat in results:
            val = f"{lat} ms" if lat != float("inf") else "Timeout"
            lines.append(TXT["ping_line"].format(name=name, ip=ip, val=val))
        text = "\n".join(lines)
        self.status.configure(
            text=f"{RLM}{TXT['status_ready']}",
            text_color=self.green
        )
        self.show_text_window(
            TXT["ping_results_title"],
            TXT["ping_results_header"],
            TXT["ping_results_sub"].format(count=len(results)),
            text,
            640, 430
        )

    def ping_all_advanced(self):
        all_ips = [(n, i[0]) for c in self.dns_data.values() for n, i in c.items()]
        if not all_ips:
            messagebox.showinfo(TXT["full_test_title_info"], TXT["full_test_no_dns"])
            return
        threading.Thread(
            target=self.ping_all_advanced_thread,
            args=(all_ips,),
            daemon=True
        ).start()

    def ping_all_advanced_thread(self, dns_list):
        results = []
        total = len(dns_list)
        for idx, (n, ip) in enumerate(dns_list, start=1):
            self.root.after(
                0,
                lambda i=idx, name=n: self.status.configure(
                    text=f"{RLM}{TXT['status_full_test'].format(i=i, total=total, name=name)}",
                    text_color=self.green
                )
            )
            avg_ping, packet_loss, jitter = ping_stats(ip)
            if avg_ping == float("inf"):
                score = 0
            else:
                score = max(0, 100 - avg_ping - jitter - packet_loss * 0.5)
            results.append((n, ip, avg_ping, jitter, packet_loss, score))

        results.sort(key=lambda x: (-x[5], x[2]))

        lines = []
        for idx, (name, ip, ap, jt, pl, sc) in enumerate(results, start=1):
            lines.append(
                TXT["full_test_line"].format(
                    idx=idx, name=name, ip=ip,
                    ap=f"{ap:.1f}", jl=f"{jt:.1f}",
                    pl=f"{pl:.1f}%", sc=f"{sc:.1f}"
                )
            )
        text = "\n".join(lines)
        self.status.configure(
            text=f"{RLM}{TXT['status_full_test_done']}",
            text_color=self.green
        )
        self.show_text_window(
            TXT["full_test_win_title"],
            TXT["full_test_header"],
            TXT["full_test_sub"].format(count=len(results)),
            text,
            680, 460
        )

    def optimize_for_game(self, gamename):
        mapping = self.games_data.get(gamename, {})
        if not mapping:
            messagebox.showinfo(TXT["games_best_title"], TXT["games_best_not_found"])
            return

        dns_candidates = []
        for dnsname, ips in mapping.items():
            if not ips:
                continue
            ip = ips[0]
            dns_candidates.append((dnsname, ip))

        if not dns_candidates:
            messagebox.showinfo(TXT["games_best_title"], TXT["games_best_not_found"])
            return

        best = None
        for name, ip in dns_candidates:
            lat = ping_latency(ip)
            if lat == float("inf"):
                continue
            if best is None or lat < best[2]:
                best = (name, ip, lat)

        if best is None:
            messagebox.showinfo(TXT["games_best_title"], TXT["games_best_not_found"])
            return

        dnsname, ip, lat = best
        self.apply_dns(dnsname, [ip])
        body = TXT["games_best_body"].format(game=gamename, name=dnsname, ip=ip, lat=int(lat))
        messagebox.showinfo(TXT["games_best_title"], body)

    def show_current_dns(self):
        try:
            proto = self.protocol_mode.get().lower()
            interface = self.selected_interface.get()

            if TXT["no_interface"] in interface or TXT["loading_interface"] in interface:
                messagebox.showwarning(TXT["msg_warning"], TXT["warn_select_interface"])
                return

            cmd = f'netsh interface {proto} show dnsservers name="{interface}"'
            r = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                encoding="utf-8", errors="ignore"
            )
            raw = r.stdout

            primary, secondary = None, None
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                m = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                if m:
                    ip = m.group(1)
                    if primary is None:
                        primary = ip
                    elif secondary is None:
                        secondary = ip

            if not primary and not secondary:
                out = TXT["current_dns_none"]
            else:
                lines = [f"رابط: {interface}"]
                if primary:
                    lines.append(f"DNS اصلی: {primary}")
                if secondary:
                    lines.append(f"DNS ثانویه: {secondary}")
                out = "\n".join(lines)

        except Exception as e:
            out = str(e)

        self.show_text_window(
            TXT["current_dns_title"],
            TXT["current_dns_header"],
            "",
            out,
            400, 260
        )

    def flush_dns(self):
        interface = self.selected_interface.get()
        if TXT["no_interface"] in interface or TXT["loading_interface"] in interface:
            messagebox.showwarning(TXT["msg_warning"], TXT["warn_select_interface"])
            return

        proto = self.protocol_mode.get().lower()
        try:
            cmd_auto = f'netsh interface {proto} set dnsservers name="{interface}" dhcp'
            r1 = subprocess.run(
                cmd_auto, shell=True, capture_output=True, text=True,
                encoding="utf-8", errors="ignore"
            )
            if r1.returncode != 0:
                raise Exception(r1.stdout + "\n" + r1.stderr)

            r2 = subprocess.run(
                "ipconfig /flushdns", shell=True,
                capture_output=True, text=True,
                encoding="utf-8", errors="ignore"
            )
            if r2.returncode != 0:
                raise Exception(r2.stdout + "\n" + r2.stderr)

            messagebox.showinfo(TXT["btn_flush_dns"], TXT["flush_ok"])
            self.status.configure(
                text=f"{RLM}{TXT['flush_ok']}",
                text_color=self.green
            )
        except Exception as e:
            messagebox.showerror(TXT["btn_flush_dns"], f"{TXT['flush_err']}\n\n{e}")

    def restart_network(self):
        if not messagebox.askyesno(TXT["btn_reset_net"], TXT["reset_confirm"]):
            return
        try:
            cmds = ["netsh int ip reset", "netsh winsock reset"]
            for c in cmds:
                subprocess.run(c, shell=True, check=True)
            messagebox.showinfo(TXT["btn_reset_net"], TXT["reset_ok"])
        except Exception:
            messagebox.showerror(TXT["btn_reset_net"], TXT["reset_err"])

    def show_text_window(self, title, header, subtitle, body, w=600, h=400):
        win = ctk.CTkToplevel(self.root)
        win.title(title)
        win.geometry(f"{w}x{h}")
        win.configure(fg_color=self.dark)

        top = ctk.CTkFrame(win, fg_color=self.dark)
        top.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(
            top, text=f"{RLM}{header}",
            font=self.font_header, text_color=self.green
        ).pack(anchor="w", pady=(0, 2))
        if subtitle:
            ctk.CTkLabel(
                top, text=f"{RLM}{subtitle}",
                font=self.font_normal, text_color="#bbbbbb"
            ).pack(anchor="w")

        textframe = ctk.CTkFrame(win, fg_color=self.darker)
        textframe.pack(fill="both", expand=True, padx=10, pady=10)
        textbox = ctk.CTkTextbox(
            textframe, fg_color=self.darker, text_color="white",
            font=self.font_normal, wrap="word"
        )
        textbox.pack(fill="both", expand=True, padx=6, pady=6)
        textbox.insert("1.0", body)
        textbox.configure(state="disabled")

        ctk.CTkButton(
            win, text=f"{RLM}{TXT['text_win_close']}",
            fg_color=self.green, hover_color="#23985d",
            text_color=self.darker, font=self.font_normal,
            width=120, height=32, command=win.destroy
        ).pack(pady=(0, 10))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DNSGameOptimizer()
    app.run()
