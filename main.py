import customtkinter as ctk
from tkinter import messagebox
import subprocess, os, sys, json, re, ctypes, threading
import ipaddress

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    script = sys.executable
    params = " ".join([f'"{a}"' for a in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)
    sys.exit()

base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
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

TRANSLATIONS = {
    "fa": {
        "app_title": "🎮 DNS بهینه‌ساز",
        "app_subtitle": "پینگ بهتری داشته باش",
        "btn_add_dns": "➕ DNS جدید",
        "btn_ping_all": "📡 پینگ همه",
        "btn_ping_full": "📊 تست کامل",
        "btn_current_dns": "👁️ DNS فعلی",
        "tab_dns": "DNS",
        "tab_games": "بازی‌ها",
        "tab_settings": "⚙️ تنظیمات",
        "status_ready": "✅ آماده",
        "net_card_title": "🌐 کارت شبکه فعال",
        "btn_refresh": "🔄 تازه‌سازی",
        "proto_title": "🔌 پروتکل",
        "tools_title": "🛠️ ابزارهای سریع",
        "btn_flush_dns": "🧹 پاک DNS",
        "btn_reset_net": "🔄 ریست شبکه",
        "dns_added_title": "➕ DNS جدید",
        "dns_name": "نام DNS",
        "dns_ip_main": "IP اصلی",
        "dns_ip_secondary": "IP دوم (اختیاری)",
        "btn_save": "💾 ذخیره",
        "warn_required": "نام و IP اصلی الزامی است",
        "err_ip_main": "IP اصلی نامعتبر است (فرمت IPv4/IPv6 صحیح نیست)",
        "err_ip_second": "IP دوم نامعتبر است (فرمت IPv4/IPv6 صحیح نیست)",
        "warn_duplicate_name": "نام تکراری است",
        "status_dns_added": " اضافه شد",
        "edit_dns_title": "✏️ ویرایش DNS",
        "dns_ip_second": "IP دوم",
        "status_dns_edited": " ویرایش شد",
        "delete_only_custom": "فقط DNS های اضافه شده قابل حذف هستند",
        "delete_confirm": "آیا از حذف {name} مطمئنید؟",
        "status_dns_deleted": " حذف شد",
        "warn_select_interface": "لطفاً کارت شبکه مناسب انتخاب کنید",
        "err_invalid_dns_ips": "IP های این DNS نامعتبر هستند؛ لطفاً ویرایش کنید.",
        "status_dns_applied": " روی {iface} ست شد",
        "err_set_dns": "تنظیم DNS ناموفق",
        "status_ping_single": "در حال پینگ {name}...",
        "status_ping_single_done": "پینگ {name}: {lat} ✅",
        "info_no_dns": "هیچ DNS ای موجود نیست",
        "status_ping_all": "پینگ {i}/{total}: {name}",
        "ping_results_title": "نتایج پینگ",
        "ping_results_header": "📊 نتایج پینگ DNS ها",
        "ping_results_sub": "{count} سرور تست شد",
        "status_ping_all_done": "✅ پینگ کامل شد",
        "ping_line": "{name}: {ip} → {val}",
        "fulltest_title_info": "تست کامل",
        "fulltest_no_dns": "هیچ DNS ای موجود نیست",
        "status_fulltest": "تست کامل {i}/{total}: {name}",
        "status_fulltest_done": "✅ تست کامل DNSها تمام شد",
        "fulltest_win_title": "تست کامل DNS",
        "fulltest_header": "📊 رده‌بندی DNS ها",
        "fulltest_sub": "{count} سرور تست شد (پینگ، جیتر، پکت‌لاس و نمره ترکیبی)",
        "fulltest_line": "{idx}. {name} ({ip})\n   پینگ: {ap} | جیتر: {jl} | پکت‌لاس: {pl} | نمره: {sc}",
        "games_best_dns": "🚀 بهترین DNS",
        "games_best_title": "🎯",
        "games_best_body": "بهترین DNS برای {game}:\n{name}\n{ip} → {lat}ms",
        "games_best_not_found": "DNS مناسب یافت نشد",
        "text_win_close": "بستن",
        "current_dns_title": "DNS فعلی",
        "current_dns_header": "📡 DNS های فعلی",
        "current_dns_none": "هیچ DNS فعالی تنظیم نشده",
        "flush_ok": "✅ کش DNS پاک شد",
        "flush_err": "پاک‌سازی DNS ناموفق",
        "reset_confirm": "آیا از ریستارت اتصالات شبکه مطمئنید؟",
        "reset_ok": "شبکه ریستارت شد. لطفاً سیستم را ریستارت کنید.",
        "reset_err": "ریستارت شبکه ناموفق",
        "msg_error": "خطا",
        "msg_warning": "⚠️",
        "msg_delete": "حذف",
        "lang_title": "🈯 زبان",
        "lang_fa": "فارسی",
        "lang_en": "English",
        "no_interface": "(هیچ اینترفیسی یافت نشد)",
        "loading_interface": "(در حال بارگذاری...)",
        "btn_set": "ست",
        "btn_ping": "پینگ",
        "cat_local": "ایرانی",
        "cat_global": "جهانی",
        "cat_custom": "موارد اضافه شده",
        "game_Fortnite": "Fortnite",
        "game_Valorant": "Valorant",
        "game_Counter-Strike 2": "Counter-Strike 2",
        "game_League of Legends": "League of Legends",
        "game_Apex Legends": "Apex Legends",
        "game_Warzone": "Warzone",
        "game_PUBG": "PUBG",
        "game_Rocket League": "Rocket League",
        "game_Overwatch 2": "Overwatch 2",
        "game_GTA Online": "GTA Online",
    },
    "en": {
        "app_title": "🎮 DNS Optimizer",
        "app_subtitle": "Get a better ping",
        "btn_add_dns": "➕ Add DNS",
        "btn_ping_all": "📡 Ping all",
        "btn_ping_full": "📊 Full test",
        "btn_current_dns": "👁️ Current DNS",
        "tab_dns": "DNS",
        "tab_games": "Games",
        "tab_settings": "⚙️ Settings",
        "status_ready": "✅ Ready",
        "net_card_title": "🌐 Active network adapter",
        "btn_refresh": "🔄 Refresh",
        "proto_title": "🔌 Protocol",
        "tools_title": "🛠️ Quick tools",
        "btn_flush_dns": "🧹 Flush DNS",
        "btn_reset_net": "🔄 Reset network",
        "dns_added_title": "➕ New DNS",
        "dns_name": "DNS name",
        "dns_ip_main": "Primary IP",
        "dns_ip_secondary": "Secondary IP (optional)",
        "btn_save": "💾 Save",
        "warn_required": "Name and primary IP are required",
        "err_ip_main": "Primary IP is invalid (IPv4/IPv6 format error)",
        "err_ip_second": "Secondary IP is invalid (IPv4/IPv6 format error)",
        "warn_duplicate_name": "Name already exists",
        "status_dns_added": " added",
        "edit_dns_title": "✏️ Edit DNS",
        "dns_ip_second": "Secondary IP",
        "status_dns_edited": " edited",
        "delete_only_custom": "Only user-added DNS entries can be deleted",
        "delete_confirm": "Are you sure you want to delete {name}?",
        "status_dns_deleted": " deleted",
        "warn_select_interface": "Please select a network adapter",
        "err_invalid_dns_ips": "This DNS has invalid IPs; please edit it.",
        "status_dns_applied": " applied on {iface}",
        "err_set_dns": "Failed to set DNS",
        "status_ping_single": "Pinging {name}...",
        "status_ping_single_done": "Ping {name}: {lat} ✅",
        "info_no_dns": "No DNS servers available",
        "status_ping_all": "Ping {i}/{total}: {name}",
        "ping_results_title": "Ping results",
        "ping_results_header": "📊 DNS ping results",
        "ping_results_sub": "{count} servers tested",
        "status_ping_all_done": "✅ Ping test finished",
        "ping_line": "{name}: {ip} → {val}",
        "fulltest_title_info": "Full test",
        "fulltest_no_dns": "No DNS servers available",
        "status_fulltest": "Full test {i}/{total}: {name}",
        "status_fulltest_done": "✅ Full DNS test finished",
        "fulltest_win_title": "DNS full test",
        "fulltest_header": "📊 DNS ranking",
        "fulltest_sub": "{count} servers tested (ping, jitter, packet loss, score)",
        "fulltest_line": "{idx}. {name} ({ip})\n   Ping: {ap} | Jitter: {jl} | Loss: {pl} | Score: {sc}",
        "games_best_dns": "🚀 Best DNS",
        "games_best_title": "🎯",
        "games_best_body": "Best DNS for {game}:\n{name}\n{ip} → {lat}ms",
        "games_best_not_found": "No suitable DNS found",
        "text_win_close": "Close",
        "current_dns_title": "Current DNS",
        "current_dns_header": "📡 Current DNS servers",
        "current_dns_none": "No DNS configured",
        "flush_ok": "✅ DNS cache flushed",
        "flush_err": "DNS flush failed",
        "reset_confirm": "Are you sure you want to reset network settings?",
        "reset_ok": "Network reset done. Please restart the system.",
        "reset_err": "Network reset failed",
        "msg_error": "Error",
        "msg_warning": "⚠️",
        "msg_delete": "Delete",
        "lang_title": "🈯 Language",
        "lang_fa": "Farsi",
        "lang_en": "English",
        "no_interface": "(No interface found)",
        "loading_interface": "(Loading...)",
        "btn_set": "Set",
        "btn_ping": "Ping",
        "cat_local": "Local",
        "cat_global": "Global",
        "cat_custom": "Custom added",
        "game_Fortnite": "Fortnite",
        "game_Valorant": "Valorant",
        "game_Counter-Strike 2": "Counter-Strike 2",
        "game_League of Legends": "League of Legends",
        "game_Apex Legends": "Apex Legends",
        "game_Warzone": "Warzone",
        "game_PUBG": "PUBG",
        "game_Rocket League": "Rocket League",
        "game_Overwatch 2": "Overwatch 2",
        "game_GTA Online": "GTA Online",
    }
}

def get_text(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS["fa"]).get(key, key)

DEFAULT_DNS = {
    "local": {
        "Shecan": ["178.22.122.100", "185.51.200.2"],
        "Radar": ["10.202.10.10", "10.202.10.11"],
        "Begzar": ["185.55.226.26", "185.55.225.25"],
        "Electro": ["78.157.42.100", "78.157.42.101"],
        "403Online": ["10.202.10.202", "10.202.10.102"],
        "Respina": ["185.12.112.1", "185.12.112.2"]
    },
    "global": {
        "Google": ["8.8.8.8", "8.8.4.4"],
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Quad9": ["9.9.9.9", "149.112.112.112"],
        "OpenDNS": ["208.67.222.222", "208.67.220.220"],
        "AdGuard": ["94.140.14.14", "94.140.15.15"],
        "ControlD": ["76.76.2.0", "76.76.10.0"]
    },
    "custom": {}
}

DEFAULT_GAMES = {
    "Fortnite": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Google": ["8.8.8.8", "8.8.4.4"],
        "Quad9": ["9.9.9.9", "149.112.112.112"]
    },
    "Valorant": {
        "Google": ["8.8.8.8", "8.8.4.4"],
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "OpenDNS": ["208.67.222.222", "208.67.220.220"]
    },
    "Counter-Strike 2": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Google": ["8.8.8.8", "8.8.4.4"],
        "AdGuard": ["94.140.14.14", "94.140.15.15"]
    },
    "League of Legends": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Google": ["8.8.8.8", "8.8.4.4"],
        "OpenDNS": ["208.67.222.222", "208.67.220.220"]
    },
    "Apex Legends": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Quad9": ["9.9.9.9", "149.112.112.112"],
        "Google": ["8.8.8.8", "8.8.4.4"]
    },
    "Warzone": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "OpenDNS": ["208.67.222.222", "208.67.220.220"],
        "Google": ["8.8.8.8", "8.8.4.4"]
    },
    "PUBG": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Quad9": ["9.9.9.9", "149.112.112.112"],
        "Google": ["8.8.8.8", "8.8.4.4"]
    },
    "Rocket League": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "AdGuard": ["94.140.14.14", "94.140.15.15"],
        "Google": ["8.8.8.8", "8.8.4.4"]
    },
    "Overwatch 2": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Google": ["8.8.8.8", "8.8.4.4"],
        "Quad9": ["9.9.9.9", "149.112.112.112"]
    },
    "GTA Online": {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Google": ["8.8.8.8", "8.8.4.4"],
        "OpenDNS": ["208.67.222.222", "208.67.220.220"]
    }
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

def ping_latency(ip, timeout_ms=2000):
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

def ping_stats(ip, count=10, timeout_ms=2000):
    rtts = []
    lost = 0
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

        self.lang = ctk.StringVar(value="fa")
        self.root.title(f"{RLM}{self.t('app_title')}")
        self.root.geometry("880x740")
        self.root.resizable(False, False)

        self.green = "#2fc973"
        self.dark = "#1e1e1e"
        self.darker = "#1b1b1b"
        self.card = "#2a2f2a"
        self.blue = "#3b82f6"

        self.font_title = ctk.CTkFont(family="Dana", size=22, weight="bold")
        self.font_header = ctk.CTkFont(family="Dana", size=15, weight="bold")
        self.font_normal = ctk.CTkFont(family="Dana", size=13, weight="bold")

        self.dns_data = load_json_safe(DNS_FILE, DEFAULT_DNS)
        self.games_data = load_json_safe(GAMES_FILE, DEFAULT_GAMES)

        self.interface_names = []
        self.selected_interface = ctk.StringVar(value=f"{RLM}{self.t('loading_interface')}")
        self.protocol_mode = ctk.StringVar(value="IPv4")

        self.setup_ui()
        self.update_interface_list()

    def t(self, key):
        return get_text(self.lang.get(), key)

    def get_all_interfaces(self):
        interfaces = []
        try:
            r = subprocess.run("netsh interface show interface", shell=True,
                               capture_output=True, text=True, encoding="utf-8")
            lines = r.stdout.splitlines()
            active_interfaces, all_interfaces = [], []
            for line in lines:
                line = line.strip()
                if not line or line.startswith(('=', '-')):
                    continue
                if 'Admin State' in line and 'State' in line:
                    continue
                parts = re.split(r'\s{2,}', line)
                if len(parts) >= 4:
                    name = parts[-1].strip('"\'')
                    if name and len(name) > 1:
                        state = "Connected" if "Connected" in line else "Disconnected"
                        all_interfaces.append((name, state))
                        if "Connected" in line:
                            active_interfaces.append((name, state))
            interfaces = active_interfaces + [i for i in all_interfaces if i not in active_interfaces]
        except Exception:
            pass
        if not interfaces:
            interfaces = [("Wi-Fi", "Connected"),
                          ("Ethernet", "Disconnected"),
                          ("Local Area Connection", "Disconnected")]
        return interfaces[:20]

    def update_interface_list(self):
        all_interfaces = self.get_all_interfaces()
        active = [n for n, s in all_interfaces if s == "Connected"]
        inactive = [n for n, s in all_interfaces if s != "Connected"]
        self.interface_names = active + inactive
        if not self.interface_names:
            self.interface_names = [f"{RLM}{self.t('no_interface')}"]
        if self.selected_interface.get() not in self.interface_names:
            self.selected_interface.set(self.interface_names[0])
        if hasattr(self, 'interface_menu'):
            self.interface_menu.configure(values=self.interface_names)
        if hasattr(self, 'status'):
            self.update_status_display()

    def update_status_display(self):
        net = self.selected_interface.get()
        proto = self.protocol_mode.get()
        self.status.configure(text=f"{RLM}🌐 {net} | {proto}", text_color=self.green)

    def on_interface_change(self, selection):
        self.selected_interface.set(selection)
        self.update_status_display()

    def on_protocol_change(self, selection):
        self.protocol_mode.set(selection)
        self.update_status_display()

    def refresh_interfaces(self):
        self.update_interface_list()
        self.status.configure(text=f"{RLM}✅ {self.t('btn_refresh')}", text_color=self.green)

    def setup_ui(self):
        title = ctk.CTkFrame(self.root, fg_color=self.dark)
        title.pack(fill="x", pady=10)
        self.title_label = ctk.CTkLabel(title, text=f"{RLM}{self.t('app_title')}",
                                        text_color=self.green, font=self.font_title)
        self.title_label.pack(pady=(4, 2))
        self.subtitle_label = ctk.CTkLabel(title, text=f"{RLM}{self.t('app_subtitle')}",
                                           text_color="#bfbfbf", font=self.font_normal)
        self.subtitle_label.pack(pady=(0, 6))

        topbar = ctk.CTkFrame(self.root, fg_color=self.darker)
        topbar.pack(fill="x", padx=15, pady=(5, 0))

        self.btn_add_dns = ctk.CTkButton(
            topbar, text=f"{RLM}{self.t('btn_add_dns')}", width=140,
            fg_color=self.green, hover_color="#23985d",
            text_color=self.darker, font=self.font_normal,
            command=self.open_add_dns_window
        )
        self.btn_add_dns.pack(side="left", padx=6, pady=8)

        self.btn_ping_all = ctk.CTkButton(
            topbar, text=f"{RLM}{self.t('btn_ping_all')}", width=140,
            fg_color=self.green, hover_color="#23985d",
            text_color=self.darker, font=self.font_normal,
            command=self.ping_all_dns
        )
        self.btn_ping_all.pack(side="left", padx=6, pady=8)

        self.btn_ping_full = ctk.CTkButton(
            topbar, text=f"{RLM}{self.t('btn_ping_full')}", width=140,
            fg_color=self.blue, hover_color="#2563eb",
            text_color="white", font=self.font_normal,
            command=self.ping_all_advanced
        )
        self.btn_ping_full.pack(side="left", padx=6, pady=8)

        self.btn_current_dns = ctk.CTkButton(
            topbar, text=f"{RLM}{self.t('btn_current_dns')}", width=150,
            fg_color=self.green, hover_color="#23985d",
            text_color=self.darker, font=self.font_normal,
            command=self.show_current_dns
        )
        self.btn_current_dns.pack(side="right", padx=6, pady=8)

        self.lang_menu = ctk.CTkOptionMenu(
            topbar,
            variable=self.lang,
            values=["fa", "en"],
            fg_color=self.darker,
            button_color=self.green,
            button_hover_color="#23985d",
            text_color="#ffffff",
            font=self.font_normal,
            width=90,
            height=30,
            command=self.on_language_change
        )
        self.lang_menu.pack(side="right", padx=6, pady=8)

        self.tabs = ctk.CTkTabview(self.root, width=820, height=540)
        self.tabs.pack(padx=15, pady=12)
        try:
            self.tabs._segmented_button.configure(
                font=self.font_header,
                fg_color="#1f1f1f",
                selected_color="#2b2b2b",
                text_color=self.green
            )
        except:
            pass

        self.tab_dns = self.tabs.add(f"{RLM}{self.t('tab_dns')}")
        self.tab_games = self.tabs.add(f"{RLM}{self.t('tab_games')}")
        self.tab_settings = self.tabs.add(f"{RLM}{self.t('tab_settings')}")

        self.frame_dns = ctk.CTkFrame(self.tab_dns, fg_color=self.dark)
        self.frame_games = ctk.CTkFrame(self.tab_games, fg_color=self.dark)
        self.frame_settings = ctk.CTkFrame(self.tab_settings, fg_color=self.dark)
        for frame in [self.frame_dns, self.frame_games, self.frame_settings]:
            frame.pack(fill="both", expand=True, pady=8)

        self.build_dns_tab()
        self.build_games_tab()
        self.build_settings_tab()

        self.status = ctk.CTkLabel(
            self.root, text=f"{RLM}{self.t('status_ready')}",
            anchor="center", font=self.font_normal,
            text_color=self.green,
            fg_color=self.darker, height=40
        )
        self.status.pack(side="bottom", fill="x", pady=6)

    def build_settings_tab(self):
        main_frame = ctk.CTkFrame(self.frame_settings, fg_color=self.dark)
        main_frame.pack(fill="both", expand=True, padx=20, pady=16)

        net_card = ctk.CTkFrame(main_frame, fg_color=self.card, corner_radius=15)
        net_card.pack(fill="x", pady=(0, 14))

        self.net_label = ctk.CTkLabel(
            net_card, text=f"{RLM}{self.t('net_card_title')}",
            font=self.font_header, text_color=self.green
        )
        self.net_label.pack(pady=(14, 10))

        self.interface_menu = ctk.CTkOptionMenu(
            net_card,
            variable=self.selected_interface,
            values=self.interface_names,
            fg_color=self.darker,
            button_color=self.green,
            button_hover_color="#23985d",
            text_color="#ffffff",
            font=self.font_normal,
            width=500,
            height=40,
            command=self.on_interface_change
        )
        self.interface_menu.pack(pady=(0, 12), padx=20)

        self.btn_refresh_if = ctk.CTkButton(
            net_card, text=f"{RLM}{self.t('btn_refresh')}",
            fg_color=self.blue, hover_color="#2563eb",
            text_color="white", font=self.font_normal,
            width=120, command=self.refresh_interfaces
        )
        self.btn_refresh_if.pack(pady=(0, 12))

        proto_card = ctk.CTkFrame(main_frame, fg_color=self.card, corner_radius=15)
        proto_card.pack(fill="x", pady=(0, 14))

        self.proto_label = ctk.CTkLabel(
            proto_card, text=f"{RLM}{self.t('proto_title')}",
            font=self.font_header, text_color=self.green
        )
        self.proto_label.pack(pady=(14, 10))

        self.protocol_menu = ctk.CTkOptionMenu(
            proto_card,
            variable=self.protocol_mode,
            values=["IPv4", "IPv6"],
            fg_color=self.darker,
            button_color=self.green,
            button_hover_color="#23985d",
            text_color="#ffffff",
            font=self.font_normal,
            width=200,
            height=40,
            command=self.on_protocol_change
        )
        self.protocol_menu.pack(pady=(0, 14), padx=20)

        tools_card = ctk.CTkFrame(main_frame, fg_color=self.card, corner_radius=15)
        tools_card.pack(fill="x", pady=(0, 0))

        self.tools_label = ctk.CTkLabel(
            tools_card, text=f"{RLM}{self.t('tools_title')}",
            font=self.font_header, text_color=self.green
        )
        self.tools_label.pack(pady=(14, 10))

        btn_frame = ctk.CTkFrame(tools_card, fg_color="transparent")
        btn_frame.pack(pady=(4, 14), padx=20)

        self.btn_flush = ctk.CTkButton(
            btn_frame, text=f"{RLM}{self.t('btn_flush_dns')}",
            fg_color="#3fb881", hover_color="#2fa668",
            text_color=self.darker, font=self.font_normal,
            width=140, command=self.flush_dns
        )
        self.btn_flush.pack(side="left", padx=8)

        self.btn_reset_net = ctk.CTkButton(
            btn_frame, text=f"{RLM}{self.t('btn_reset_net')}",
            fg_color="#f59e0b", hover_color="#d97706",
            text_color="white", font=self.font_normal,
            width=140, command=self.restart_network
        )
        self.btn_reset_net.pack(side="left", padx=8)

    def build_dns_tab(self):
        self.dns_frame = ctk.CTkScrollableFrame(self.frame_dns, fg_color=self.dark)
        self.dns_frame.pack(fill="both", expand=True, padx=15, pady=12)
        self.refresh_dns_ui()

    def refresh_dns_ui(self):
        for w in self.dns_frame.winfo_children():
            w.destroy()

        order = [("local", "cat_local"), ("global", "cat_global"), ("custom", "cat_custom")]

        for key, tkey in order:
            servers = self.dns_data.get(key, {})
            if not servers:
                continue
            ctk.CTkLabel(
                self.dns_frame, text=f"{RLM}📁 {self.t(tkey)}",
                text_color=self.green, font=self.font_header,
                anchor="e"
            ).pack(fill="x", pady=(8, 4))

            grid = ctk.CTkFrame(self.dns_frame, fg_color="transparent")
            grid.pack(pady=4, padx=2, fill="x")

            row, col = 0, 0
            for name, ips in servers.items():
                card = ctk.CTkFrame(grid, fg_color=self.card, corner_radius=10)
                card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

                ctk.CTkLabel(
                    card, text=f"{RLM}{name}",
                    font=self.font_header, text_color=self.green,
                    anchor="center"
                ).pack(pady=(6, 2), padx=6)

                ctk.CTkLabel(
                    card, text="\n".join(ips),
                    text_color="#ccc",
                    font=ctk.CTkFont(family="Dana", size=11, weight="bold"),
                    anchor="center"
                ).pack(pady=(0, 4), padx=6)

                btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                btn_frame.pack(pady=(0, 6))

                ctk.CTkButton(
                    btn_frame, text=f"{RLM}{self.t('btn_set')}", width=55,
                    fg_color=self.green, hover_color="#23985d",
                    text_color=self.darker, font=self.font_normal,
                    command=lambda n=name, i=ips: self.apply_dns(n, i)
                ).pack(side="left", padx=4)

                ctk.CTkButton(
                    btn_frame, text=f"{RLM}{self.t('btn_ping')}", width=55,
                    fg_color="#555", hover_color="#444",
                    text_color=self.green, font=self.font_normal,
                    command=lambda n=name, i=ips: self.ping_single(n, i)
                ).pack(side="left", padx=4)

                if key == "custom":
                    edit_frame = ctk.CTkFrame(card, fg_color="transparent")
                    edit_frame.pack(pady=(0, 6))
                    ctk.CTkButton(
                        edit_frame, text=f"{RLM}✏️", width=30,
                        fg_color=self.blue, hover_color="#2563eb",
                        text_color="white", font=self.font_normal,
                        command=lambda c=key, n=name: self.open_edit_dns_window(c, n)
                    ).pack(side="left", padx=4)
                    ctk.CTkButton(
                        edit_frame, text=f"{RLM}🗑", width=30,
                        fg_color="#ef4444", hover_color="#b91c1c",
                        text_color="white", font=self.font_normal,
                        command=lambda c=key, n=name: self.delete_dns(c, n)
                    ).pack(side="left", padx=4)

                col += 1
                if col == 4:
                    row += 1
                    col = 0

            grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def open_add_dns_window(self):
        w = ctk.CTkToplevel(self.root)
        w.title(self.t("dns_added_title"))
        w.geometry("420x320")
        w.configure(fg_color=self.dark)

        ctk.CTkLabel(
            w, text=f"{RLM}{self.t('dns_name')}", text_color=self.green,
            font=self.font_normal
        ).pack(pady=(16, 6))
        name = ctk.CTkEntry(w, width=350, font=self.font_normal, height=35)
        name.pack(pady=4)

        ctk.CTkLabel(
            w, text=f"{RLM}{self.t('dns_ip_main')}", text_color=self.green,
            font=self.font_normal
        ).pack(pady=(10, 6))
        ip1 = ctk.CTkEntry(w, width=350, font=self.font_normal, height=35)
        ip1.pack(pady=4)

        ctk.CTkLabel(
            w, text=f"{RLM}{self.t('dns_ip_secondary')}", text_color=self.green,
            font=self.font_normal
        ).pack(pady=(10, 6))
        ip2 = ctk.CTkEntry(w, width=350, font=self.font_normal, height=35)
        ip2.pack(pady=(0, 16))

        def save():
            n, i1, i2 = name.get().strip(), ip1.get().strip(), ip2.get().strip()
            if not n or not i1:
                return messagebox.showwarning(self.t("msg_warning"), self.t("warn_required"))
            if not is_valid_ip(i1):
                return messagebox.showerror(self.t("msg_error"), self.t("err_ip_main"))
            if i2 and not is_valid_ip(i2):
                return messagebox.showerror(self.t("msg_error"), self.t("err_ip_second"))
            self.dns_data.setdefault("custom", {})
            if n in self.dns_data["custom"]:
                return messagebox.showwarning(self.t("msg_warning"), self.t("warn_duplicate_name"))
            ips_list = [i1]
            if i2:
                ips_list.append(i2)
            self.dns_data["custom"][n] = ips_list
            save_json_safe(DNS_FILE, self.dns_data)
            self.refresh_dns_ui()
            self.status.configure(
                text=f"{RLM}✅ {n}{self.t('status_dns_added')}",
                text_color=self.green
            )
            w.destroy()

        ctk.CTkButton(
            w, text=f"{RLM}{self.t('btn_save')}", fg_color=self.green,
            width=200, height=40, font=self.font_normal,
            command=save
        ).pack(pady=(0, 14))

    def open_edit_dns_window(self, category, dns_name):
        if category != "custom":
            return messagebox.showwarning(self.t("msg_warning"), self.t("delete_only_custom"))
        current_ips = self.dns_data.get(category, {}).get(dns_name, [])

        w = ctk.CTkToplevel(self.root)
        w.title(self.t("edit_dns_title"))
        w.geometry("420x320")
        w.configure(fg_color=self.dark)

        ctk.CTkLabel(
            w, text=f"{RLM}{self.t('dns_name')}", text_color=self.green,
            font=self.font_normal
        ).pack(pady=(16, 6))
        name_entry = ctk.CTkEntry(w, width=350, font=self.font_normal, height=35)
        name_entry.pack(pady=4)
        name_entry.insert(0, dns_name)

        ctk.CTkLabel(
            w, text=f"{RLM}{self.t('dns_ip_main')}", text_color=self.green,
            font=self.font_normal
        ).pack(pady=(10, 6))
        ip1_entry = ctk.CTkEntry(w, width=350, font=self.font_normal, height=35)
        ip1_entry.pack(pady=4)
        if len(current_ips) >= 1:
            ip1_entry.insert(0, current_ips[0])

        ctk.CTkLabel(
            w, text=f"{RLM}{self.t('dns_ip_second')}", text_color=self.green,
            font=self.font_normal
        ).pack(pady=(10, 6))
        ip2_entry = ctk.CTkEntry(w, width=350, font=self.font_normal, height=35)
        ip2_entry.pack(pady=(0, 16))
        if len(current_ips) >= 2:
            ip2_entry.insert(0, current_ips[1])

        def save_edit():
            new_name = name_entry.get().strip()
            i1, i2 = ip1_entry.get().strip(), ip2_entry.get().strip()
            if not new_name or not i1:
                return messagebox.showwarning(self.t("msg_warning"), self.t("warn_required"))
            if not is_valid_ip(i1):
                return messagebox.showerror(self.t("msg_error"), self.t("err_ip_main"))
            if i2 and not is_valid_ip(i2):
                return messagebox.showerror(self.t("msg_error"), self.t("err_ip_second"))
            cat_dict = self.dns_data.setdefault(category, {})
            if new_name != dns_name and new_name in cat_dict:
                return messagebox.showwarning(self.t("msg_warning"), self.t("warn_duplicate_name"))
            if new_name != dns_name:
                cat_dict.pop(dns_name, None)
            ips_list = [i1]
            if i2:
                ips_list.append(i2)
            cat_dict[new_name] = ips_list
            save_json_safe(DNS_FILE, self.dns_data)
            self.refresh_dns_ui()
            self.status.configure(
                text=f"{RLM}✅ {new_name}{self.t('status_dns_edited')}",
                text_color=self.green
            )
            w.destroy()

        ctk.CTkButton(
            w, text=f"{RLM}{self.t('btn_save')}", fg_color=self.green,
            width=200, height=40, font=self.font_normal,
            command=save_edit
        ).pack(pady=(0, 14))

    def delete_dns(self, category, dns_name):
        if category != "custom":
            return messagebox.showwarning(self.t("msg_warning"), self.t("delete_only_custom"))
        if not messagebox.askyesno(self.t("msg_delete"),
                                   self.t("delete_confirm").format(name=dns_name)):
            return
        try:
            cat_dict = self.dns_data.get(category, {})
            if dns_name in cat_dict:
                cat_dict.pop(dns_name)
                save_json_safe(DNS_FILE, self.dns_data)
                self.refresh_dns_ui()
                self.status.configure(
                    text=f"{RLM}🗑 {dns_name}{self.t('status_dns_deleted')}",
                    text_color="#ff5555"
                )
        except Exception as e:
            messagebox.showerror(self.t("msg_error"), str(e))

    def apply_dns(self, name, ips):
        interface = self.selected_interface.get()
        if self.t("no_interface") in interface or self.t("loading_interface") in interface:
            return messagebox.showwarning(self.t("msg_warning"), self.t("warn_select_interface"))
        checked_ips = [ip.strip() for ip in ips if ip.strip()]
        if not checked_ips or not all(is_valid_ip(ip) for ip in checked_ips):
            return messagebox.showerror(self.t("msg_error"), self.t("err_invalid_dns_ips"))
        proto = self.protocol_mode.get().lower()
        try:
            subprocess.run(f'netsh interface {proto} delete dnsservers "{interface}" all',
                           shell=True, check=True)
            subprocess.run(f'netsh interface {proto} set dnsservers "{interface}" static {checked_ips[0]} primary',
                           shell=True, check=True)
            if len(checked_ips) > 1:
                subprocess.run(f'netsh interface {proto} add dnsservers "{interface}" {checked_ips[1]} index=2',
                               shell=True, check=True)
            self.status.configure(
                text=f"{RLM}✅ {name}{self.t('status_dns_applied').format(iface=interface)}",
                text_color=self.green
            )
        except subprocess.CalledProcessError:
            messagebox.showerror(self.t("msg_error"), self.t("err_set_dns"))
        except Exception as e:
            messagebox.showerror(self.t("msg_error"), str(e))

    def ping_single(self, name, ips):
        self.status.configure(
            text=f"{RLM}{self.t('status_ping_single').format(name=name)}",
            text_color=self.green
        )
        lat = ping_latency(ips[0])
        status_text = f"{lat} ms" if lat != float("inf") else "Timeout"
        self.status.configure(
            text=f"{RLM}{self.t('status_ping_single_done').format(name=name, lat=status_text)}",
            text_color=self.green
        )

    def ping_all_dns(self):
        all_ips = [(n, i[0]) for c in self.dns_data.values() for n, i in c.items()]
        if not all_ips:
            return messagebox.showinfo(self.t("ping_results_title"), self.t("info_no_dns"))
        threading.Thread(target=self._ping_all_thread,
                         args=(all_ips,), daemon=True).start()

    def _ping_all_thread(self, dns_list):
        results = []
        total = len(dns_list)
        for idx, (n, ip) in enumerate(dns_list, start=1):
            self.root.after(
                0,
                lambda i=idx, name=n: self.status.configure(
                    text=f"{RLM}{self.t('status_ping_all').format(i=i, total=total, name=name)}",
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
            lines.append(self.t("ping_line").format(name=name, ip=ip, val=val))
        text = "\n".join(lines)
        self.status.configure(text=f"{RLM}{self.t('status_ping_all_done')}",
                              text_color=self.green)
        self.show_text_window(
            self.t("ping_results_title"),
            self.t("ping_results_header"),
            self.t("ping_results_sub").format(count=len(results)),
            text, 640, 430
        )

    def ping_all_advanced(self):
        all_ips = [(n, i[0]) for c in self.dns_data.values() for n, i in c.items()]
        if not all_ips:
            return messagebox.showinfo(self.t("fulltest_title_info"), self.t("fulltest_no_dns"))
        threading.Thread(target=self._ping_all_advanced_thread,
                         args=(all_ips,), daemon=True).start()

    def _ping_all_advanced_thread(self, dns_list):
        results = []
        total = len(dns_list)
        for idx, (name, ip) in enumerate(dns_list, start=1):
            self.root.after(
                0,
                lambda i=idx, n=name: self.status.configure(
                    text=f"{RLM}{self.t('status_fulltest').format(i=i, total=total, name=n)}",
                    text_color=self.green
                )
            )
            avg_ping, packet_loss, jitter = ping_stats(ip, count=10)
            score = avg_ping * 0.6 + jitter * 0.3 + packet_loss * 1.0
            results.append({
                "name": name,
                "ip": ip,
                "avg_ping": avg_ping,
                "packet_loss": packet_loss,
                "jitter": jitter,
                "score": score
            })
        results.sort(key=lambda x: x["score"])
        self.root.after(0, lambda: self.show_advanced_results(results))

    def show_advanced_results(self, results):
        lines = []
        for idx, r in enumerate(results, start=1):
            ap = "∞" if r["avg_ping"] == float("inf") else f"{r['avg_ping']:.1f} ms"
            jl = "∞" if r["jitter"] == float("inf") else f"{r['jitter']:.1f} ms"
            pl = "∞" if r["packet_loss"] == float("inf") else f"{r['packet_loss']:.1f} %"
            sc = "∞" if r["score"] == float("inf") else f"{r['score']:.1f}"
            lines.append(
                self.t("fulltest_line").format(
                    idx=idx,
                    name=r["name"],
                    ip=r["ip"],
                    ap=ap,
                    jl=jl,
                    pl=pl,
                    sc=sc
                )
            )
        text = "\n\n".join(lines)
        self.status.configure(text=f"{RLM}{self.t('status_fulltest_done')}",
                              text_color=self.green)
        self.show_text_window(
            self.t("fulltest_win_title"),
            self.t("fulltest_header"),
            self.t("fulltest_sub").format(count=len(results)),
            text,
            760,
            520
        )

    def build_games_tab(self):
        self.games_frame = ctk.CTkScrollableFrame(self.frame_games, fg_color=self.dark)
        self.games_frame.pack(fill="both", expand=True, padx=15, pady=12)
        grid = ctk.CTkFrame(self.games_frame, fg_color="transparent")
        grid.pack(pady=4, padx=2, fill="x")
        row, col = 0, 0
        for game in self.games_data.keys():
            card = ctk.CTkFrame(grid, fg_color=self.card, corner_radius=10)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            game_label_text = self.t(f"game_{game}")
            ctk.CTkLabel(
                card, text=f"{RLM}🎮 {game_label_text}",
                font=self.font_header, text_color=self.green,
                anchor="center"
            ).pack(pady=(8, 4), padx=8)

            ctk.CTkButton(
                card, text=f"{RLM}{self.t('games_best_dns')}",
                width=100, fg_color=self.green, hover_color="#23985d",
                text_color=self.darker, font=self.font_normal,
                command=lambda g=game: self.optimize_for_game(g)
            ).pack(pady=(0, 10), padx=8)

            col += 1
            if col == 4:
                row += 1
                col = 0
        grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def optimize_for_game(self, game):
        dns_list = self.games_data.get(game, {})
        best, best_lat = None, float("inf")
        for name, ips in dns_list.items():
            if not ips or not is_valid_ip(ips[0]):
                continue
            lat = ping_latency(ips[0])
            if lat < best_lat:
                best_lat, best = lat, (name, ips)
        game_label_text = self.t(f"game_{game}")
        if best:
            self.apply_dns(best[0], best[1])
            messagebox.showinfo(
                self.t("games_best_title"),
                self.t("games_best_body").format(
                    game=game_label_text, name=best[0], ip=best[1][0], lat=best_lat
                )
            )
        else:
            messagebox.showwarning(self.t("msg_warning"), self.t("games_best_not_found"))

    def show_text_window(self, win_title, header_text, subtitle,
                         body_text, width=560, height=420):
        w = ctk.CTkToplevel(self.root)
        w.title(win_title)
        w.geometry(f"{width}x{height}")
        w.configure(fg_color=self.dark)
        ctk.CTkLabel(
            w, text=f"{RLM}{header_text}",
            text_color=self.green, font=self.font_title
        ).pack(pady=(16, 6))
        if subtitle:
            ctk.CTkLabel(
                w, text=f"{RLM}{subtitle}",
                text_color="#bfbfbf", font=self.font_normal
            ).pack(pady=(0, 10))
        box = ctk.CTkTextbox(
            w, width=width-40, height=height-150,
            fg_color=self.card, text_color="#f3f3f3",
            font=self.font_normal
        )
        box.pack(padx=20, pady=(0, 14), fill="both", expand=True)
        box.insert("1.0", body_text)
        box.configure(state="disabled")
        ctk.CTkButton(
            w, text=f"{RLM}{self.t('text_win_close')}",
            fg_color=self.green, width=120, height=35,
            font=self.font_normal, command=w.destroy
        ).pack(pady=(0, 10))

    def show_current_dns(self):
        interface = self.selected_interface.get()
        if self.t("no_interface") in interface or self.t("loading_interface") in interface:
            return messagebox.showwarning(self.t("msg_warning"), self.t("warn_select_interface"))
        proto = self.protocol_mode.get().lower()
        r = subprocess.run(
            f'netsh interface {proto} show dnsservers "{interface}"',
            shell=True, capture_output=True, text=True
        )
        out = r.stdout.strip() or self.t("current_dns_none")
        self.show_text_window(
            self.t("current_dns_title"),
            self.t("current_dns_header"),
            f"{interface} | {proto.upper()}",
            out, 620, 420
        )

    def flush_dns(self):
        try:
            subprocess.run("ipconfig /flushdns", shell=True, check=True)
            self.status.configure(text=f"{RLM}{self.t('flush_ok')}",
                                  text_color=self.green)
        except:
            messagebox.showerror(self.t("msg_error"), self.t("flush_err"))

    def restart_network(self):
        if messagebox.askyesno(self.t("msg_warning"), self.t("reset_confirm")):
            try:
                subprocess.run("netsh winsock reset", shell=True)
                subprocess.run("netsh int ip reset", shell=True)
                messagebox.showinfo("✅", self.t("reset_ok"))
            except:
                messagebox.showerror(self.t("msg_error"), self.t("reset_err"))

    def on_language_change(self, selection):
        self.lang.set(selection)
        self.refresh_texts()
        self.refresh_dns_ui()
        # تب بازی‌ها دکمه‌اش از self.t می‌خواند، نیازی به rebuild نیست

    def refresh_texts(self):
        self.root.title(f"{RLM}{self.t('app_title')}")
        self.title_label.configure(text=f"{RLM}{self.t('app_title')}")
        self.subtitle_label.configure(text=f"{RLM}{self.t('app_subtitle')}")
        self.btn_add_dns.configure(text=f"{RLM}{self.t('btn_add_dns')}")
        self.btn_ping_all.configure(text=f"{RLM}{self.t('btn_ping_all')}")
        self.btn_ping_full.configure(text=f"{RLM}{self.t('btn_ping_full')}")
        self.btn_current_dns.configure(text=f"{RLM}{self.t('btn_current_dns')}")
        self.net_label.configure(text=f"{RLM}{self.t('net_card_title')}")
        self.btn_refresh_if.configure(text=f"{RLM}{self.t('btn_refresh')}")
        self.proto_label.configure(text=f"{RLM}{self.t('proto_title')}")
        self.tools_label.configure(text=f"{RLM}{self.t('tools_title')}")
        self.btn_flush.configure(text=f"{RLM}{self.t('btn_flush_dns')}")
        self.btn_reset_net.configure(text=f"{RLM}{self.t('btn_reset_net')}")
        self.status.configure(text=f"{RLM}{self.t('status_ready')}")

        # به‌روزرسانی لیبل تب‌ها
        # (کتابخانه Tabview اجازه تغییر متن تب را مستقیم نمی‌دهد؛ ساده‌ترین راه:
        # تب را دوباره بسازی. اینجا فقط عنوان‌های داخلی را دوزبانه نگه می‌داریم.)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DNSGameOptimizer()
    app.run()
