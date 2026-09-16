# سورس اشرف | يوزربوت تيليثون
# كل شيء في ملف واحد | تخزين JSON | بدون بوت خارجي | بدون قواعد بيانات
# @OOOO6O6

import asyncio
import gzip
import html
import http.client
import io
import json
import os
import random
import re
import string
import sys
import time
import zlib
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pytz
import uuid

try:
    import brotli
except ImportError:
    brotli = None

try:
    from getids import get_date_as_string
except ImportError:
    import subprocess
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "git+https://github.com/AmanoTeam/python-getids.git",
             "--break-system-packages", "--quiet"],
            timeout=60,
        )
        from getids import get_date_as_string
    except Exception:
        get_date_as_string = None

from telethon import TelegramClient, events, functions, types, Button
from telethon.errors import (
    ChatAdminRequiredError,
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    UserAdminInvalidError,
    UsernameNotOccupiedError,
    ChannelPrivateError,
    ChannelBannedError,
    UserIdInvalidError,
    InviteHashExpiredError,
    InviteHashInvalidError,
    UserBannedInChannelError,
    UsersTooMuchError,
    AccessTokenExpiredError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, LeaveChannelRequest, DeleteChannelRequest, GetFullChannelRequest, JoinChannelRequest, InviteToChannelRequest, CreateChannelRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest, ImportContactsRequest
from telethon.tl.functions.messages import CheckChatInviteRequest, ImportChatInviteRequest, ReportRequest
from telethon.tl.functions.account import ReportPeerRequest, UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    ChatInvite,
    ChatInviteAlready,
    User,
    Channel,
    Chat,
    InputReportReasonSpam,
    InputReportReasonPornography,
    InputReportReasonViolence,
    InputReportReasonChildAbuse,
    InputReportReasonCopyright,
    InputReportReasonFake,
    InputReportReasonIllegalDrugs,
    InputReportReasonOther,
    DocumentAttributeAudio,
    DocumentAttributeFilename,
    InputMediaDice,
    InputPhoneContact,
    ChannelParticipantsAdmins,
)

# ============================================================
# إعدادات البوت الأساسية (معدلة)
# ============================================================
API_ID = 37010703
API_HASH = "eae9dc5c2ba7acda9c7b677f2586daa8"
BOT_TOKEN = "8271206565:AAFFSUXaEyCeLQU2X6mFP8kd_rO0HRtz5vI"
OWNER_ID = 8245228909
OWNER_NAME = "اشرف"
PREFIX = "."

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# دوال التخزين (مستلة من main.py)
# ============================================================
def _path(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def db_read(name, default=None):
    p = _path(name)
    if not os.path.exists(p):
        return {} if default is None else default
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {} if default is None else default

def db_write(name, data):
    with open(_path(name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def db_get(name, key, default=None):
    return db_read(name).get(str(key), default)

def db_set(name, key, value):
    data = db_read(name)
    data[str(key)] = value
    db_write(name, data)

def db_del(name, key):
    data = db_read(name)
    if str(key) in data:
        del data[str(key)]
        db_write(name, data)
        return True
    return False

# ============================================================
# دوال الزخرفة (من السكربت القديم)
# ============================================================
def fancy_text(text, style="script"):
    fancy_styles = {
        "script": {
            'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡', 'i': '𝐢', 'j': '𝐣',
            'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭',
            'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
            'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 'H': '𝐇', 'I': '𝐈', 'J': '𝐉',
            'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍', 'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓',
            'U': '𝐔', 'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
            '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
        }
    }
    fancy_map = fancy_styles.get(style, fancy_styles["script"])
    result = []
    for char in text:
        if char in fancy_map:
            result.append(fancy_map[char])
        else:
            result.append(char)
    return ''.join(result)

def fancy_button_text(text):
    return fancy_text(text, "script")

def convert_to_bold_thick(text):
    bold_map = {
        'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷',
        'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁',
        'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜', 'J': '𝗝',
        'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧',
        'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵',
    }
    result = []
    for char in text:
        if char in bold_map:
            result.append(bold_map[char])
        else:
            result.append(char)
    return ''.join(result)

# دوال الوقت (من app القديم)
time_styles = {
    "1": "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    "2": "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    "3": "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫",
    "4": "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
    "5": "0123456789",
    "6": "۰۱۲۳۴۵۶۷۸۹",
    "7": "٠١٢٣٤٥٦٧٨٩",
    "8": "₀₁₂₃₄₅₆₇₈₉",
    "9": "⓪①②③④⑤⑥⑦⑧⑨",
    "10": "⁰¹²³⁴⁵⁶⁷⁸⁹",
    "11": "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    "12": "⓿❶❷❸❹❺❻❼❽❾"
}

country_timezones = {
    "مصر": "Africa/Cairo",
    "السعودية": "Asia/Riyadh",
    "الامارات": "Asia/Dubai",
    "الكويت": "Asia/Kuwait",
    "قطر": "Asia/Qatar",
    "البحرين": "Asia/Bahrain",
    "عمان": "Asia/Muscat",
    "الاردن": "Asia/Amman",
    "فلسطين": "Asia/Gaza",
    "لبنان": "Asia/Beirut",
    "سوريا": "Asia/Damascus",
    "العراق": "Asia/Baghdad",
}

user_time_style = {}

def apply_fancy_time_style(time_str, style_num):
    style = time_styles.get(str(style_num), time_styles["1"])
    result = []
    for char in time_str:
        if char.isdigit():
            idx = int(char)
            if idx < len(style):
                result.append(style[idx])
            else:
                result.append(char)
        else:
            result.append(char)
    return ''.join(result)

def get_timezone_for_country(country_name):
    country_lower = country_name.lower().strip()
    for country, tz in country_timezones.items():
        if country_lower == country.lower():
            return tz
    return None

def get_real_time_formatted(timezone_str, style_num):
    try:
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        hour = now.strftime("%I").lstrip("0")
        minute = now.strftime("%M")
        normal_time = f"{hour}:{minute}"
        fancy_time = apply_fancy_time_style(normal_time, style_num)
        return fancy_time
    except:
        return None

# ============================================================
# دوال مساعدة (من main.py)
# ============================================================
def get_display_name(user):
    if user is None:
        return "مجهول"
    name = user.first_name or ""
    if getattr(user, "last_name", None):
        name += f" {user.last_name}"
    return name.strip() or "مجهول"

def mention(user):
    if user is None:
        return "مجهول"
    return f"[{get_display_name(user)}](tg://user?id={user.id})"

def readable_time(seconds):
    seconds = int(seconds)
    result = ""
    for unit, count in (("ي", 86400), ("س", 3600), ("د", 60), ("ث", 1)):
        if seconds >= count:
            val = seconds // count
            seconds %= count
            result += f"{val}{unit} "
    return result.strip() or "0ث"

def get_real_speed(speed_value):
    if speed_value < 0:
        speed_value = 0
    if speed_value > 60:
        speed_value = 60
    return float(speed_value)

# ============================================================
# نظام الفلود والسرعة من main.py (معدل)
# ============================================================
class TextFloodGuard:
    def __init__(self, is_premium=False):
        self.is_premium = is_premium
        self.capacity = 100
        self.refill_rate = 100.0
        self.tokens = self.capacity
        self.last_update = time.time()
        self.total_sent = 0
        self.daily_limit = 100000 if is_premium else 50000
        self.last_send_times = []

    async def wait_if_needed(self):
        self.total_sent += 1
        now = time.time()
        self.tokens = min(
            self.capacity, self.tokens + (now - self.last_update) * self.refill_rate
        )
        self.last_update = now
        if self.tokens < 1:
            wait = (1 - self.tokens) / self.refill_rate
            if wait > 0:
                await asyncio.sleep(wait)
                self.tokens = 1
        self.tokens -= 1

    def get_stats(self):
        now = time.time()
        recent = len([t for t in self.last_send_times if now - t < 8])
        rate = (
            recent / max(now - self.last_send_times[0], 1)
            if self.last_send_times
            else 0
        )
        return {
            "type": " بريميوم" if self.is_premium else " عادي",
            "tokens": f"{self.tokens:.1f}/{self.capacity}",
            "refill": f"{self.refill_rate}/s",
            "rate": f"{rate:.2f} msg/s",
            "total": self.total_sent,
            "daily_max": self.daily_limit,
        }

# ============================================================
# مولد السبام (من main.py)
# ============================================================
_DEFAULT_INSULTS = {
    "qrayb": [
        "امك", "ابوك", "اختك", "اخوك", "خالتك", "عمتك", "جدتك", "مرتك",
        "خواتك", "اهلك", "عيلتك", "بنت امك", "ولد عمك", "عمك", "خالك",
    ],
    "feal": [
        "تتناك", "تتوسك", "ترضع الزباب", "تفتح رجليها", "تبيع نفسها",
        "تشتغل قحبه", "تلحق الرجال", "تتمرمغ", "تركع للكل", "تشحت نيك",
    ],
    "jomla": [
        "بالشارع", "بكل رخص", "قدام الكل", "بالمجان", "من غير ما تستحي",
        "بطابور طويل", "بكل الكروبات", "وانت تتفرج", "بارخص سعر",
        "لكل من هب ودب",
    ],
    "sifat": [
        "كسش جعلني فداه", "توكسك", "منيوك", "خرا عليك", "يا معفن",
        "يا وسخ", "قحبه", "ديوث", "معرص", "يا حقير", "يا زفت", "يا قليل الاصل",
    ],
    "laheq": [
        "وش فيه", "جان شنو", "شكو", "ليش هيك", "عاد", "بعد", "ولك",
        "يا كلب", "يا خنزير", "ولا شلون", "", "", "",
    ],
    "sakhira": [
        "انت ماشي على موال اللي يرفع لك سيقان اختك تقعد تمجد له ولا شلون",
        "من كثر ما انت ذليل صرت تعتبر رفع سيقان محارمك انجاز تفتخر فيه",
        "كل ما ضاقت عليك الدنيا تروح تنيك اهلك وترجع مبسوط",
        "لو الذل شخص جان انت ابوه يا ابن الشرموطه الغبيه",
    ],
    "templates": [
        "{qrayb} {feal} {jomla} {sifat}",
        "{qrayb} {feal} {jomla} {laheq}",
        "{qrayb} {feal} {jomla}",
        "{qrayb} {sifat} {laheq}",
        "{qrayb} {feal} {jomla}، {sifat} {laheq}",
        "والله {qrayb} {feal} {jomla} {sifat}",
        "{sifat} {laheq}، {qrayb} {feal} {jomla}",
        "{qrayb} {feal} {jomla} وانت ساكت يا {sifat}",
        "{sakhira}",
        "{sakhira} {sifat}",
        "على فكرة؟ {sakhira} {laheq}",
        "{sifat}، {sakhira}",
        "تعرف انت ايش؟ {sakhira}",
    ],
    "حشوات": [
        "منفوخ", "ممزق", "متسع", "ضيق", "أسود", "متورم", "منكمش", "مبلل",
        "مقرف", "منتن", "لزج", "ساخن", "ملتهب", "محروق", "منهار",
    ],
    "قوالب_فتحات": [
        "تعرف امك كانت فتحتها كذا ( )، بعد ما شافت زبي صار كذا ( )",
        "امك يوم شافت زبي قالت ( )، اختك قالت ( )، انا قلت ( )",
        "كس امك قبل كان ( )، بعد ما سويتها صار ( )",
        "اختك تقول فتحتها ( )، وانا اقولها لا ( )",
    ],
}

INSULTS = {}

def _load_insults():
    global INSULTS
    path = os.path.join(DATA_DIR, "insults.json")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(_DEFAULT_INSULTS, f, ensure_ascii=False, indent=2)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in _DEFAULT_INSULTS.items():
            data.setdefault(k, v)
        INSULTS = data
    except:
        INSULTS = _DEFAULT_INSULTS

def generate_insult():
    if not INSULTS:
        _load_insults()
    ftpl = INSULTS.get("قوالب_فتحات") or []
    use_fillable = ftpl and random.random() < 0.4
    if use_fillable:
        text = random.choice(ftpl)
        fillers = INSULTS.get("حشوات") or [""]
        while "(" in text and ")" in text:
            text = re.sub(r"\(\s*\)", random.choice(fillers), text, count=1)
    else:
        tpl = random.choice(INSULTS["templates"])
        text = tpl.format(
            qrayb=random.choice(INSULTS.get("qrayb") or [""]),
            feal=random.choice(INSULTS.get("feal") or [""]),
            jomla=random.choice(INSULTS.get("jomla") or [""]),
            sifat=random.choice(INSULTS.get("sifat") or [""]),
            laheq=random.choice(INSULTS.get("laheq") or [""]),
            sakhira=random.choice(INSULTS.get("sakhira") or [""]),
        )
    return re.sub(r"\s+", " ", text).strip("، ").strip()

def insult_combos():
    n = len(INSULTS.get("templates", [1]))
    for k in ("qrayb", "feal", "jomla", "sifat", "laheq", "sakhira"):
        n *= max(len(INSULTS.get(k, [""])), 1)
    fillers = len(INSULTS.get("حشوات") or [1])
    for ftpl in INSULTS.get("قوالب_فتحات") or []:
        slots = ftpl.count("(")
        n += fillers ** max(slots, 1)
    return n

# ============================================================
# دوال فحص الروابط (من main.py)
# ============================================================
def _bc_extract(text):
    text = (text or "").strip().replace("https://", "").replace("http://", "")
    if "+" in text or "/joinchat/" in text:
        return ("invite", text.split("+")[-1].split("/")[-1])
    m = re.match(r"t\.me/(.+?)(?:/|$)", text)
    if m:
        return ("username", m.group(1))
    if text.startswith("@"):
        return ("username", text[1:])
    if re.match(r"^-?\d+$", text):
        return ("chat_id", int(text))
    if text:
        return ("username", text)
    return None

def _bc_name(entity):
    if isinstance(entity, User):
        n = (getattr(entity, "first_name", "") + " " + getattr(entity, "last_name", "")).strip()
        return n or str(getattr(entity, "id", "؟"))
    return str(getattr(entity, "title", "") or getattr(entity, "id", "؟"))

def _bc_type(entity):
    if isinstance(entity, User):
        return "user"
    if getattr(entity, "broadcast", False):
        return "channel"
    if getattr(entity, "megagroup", False):
        return "group"
    return "chat"

async def _bc_check_entity(client, identifier):
    try:
        entity = await client.get_entity(identifier)
    except UsernameNotOccupiedError:
        return "BANNED_OR_NOT_FOUND"
    except ChannelPrivateError:
        return "BANNED_OR_PRIVATE"
    except ChannelBannedError:
        return "BANNED"
    except UserIdInvalidError:
        return "INVALID_USER_ID"
    except ValueError:
        return "NOT_FOUND"
    except Exception:
        return "NOT_FOUND"
    return f"OK|{_bc_type(entity)}|{_bc_name(entity)}"

async def _bc_check_invite(client, hashv):
    try:
        result = await client(CheckChatInviteRequest(hash=hashv))
    except InviteHashExpiredError:
        return "BANNED_OR_EXPIRED"
    except InviteHashInvalidError:
        return "BANNED_OR_INVALID"
    except ChannelPrivateError:
        return "BANNED_OR_PRIVATE"
    except ChannelBannedError:
        return "BANNED"
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"
    if isinstance(result, ChatInviteAlready):
        entity = getattr(result, "chat", None)
        if entity:
            return f"OK|{_bc_type(entity)}|{_bc_name(entity)}"
        return "OK|chat|MEMBER"
    if isinstance(result, ChatInvite):
        title = str(getattr(result, "title", "?") or "?")
        if getattr(result, "scam", False) or getattr(result, "fake", False):
            return f"SCAM_FAKE|{title}"
        try:
            await client(ImportChatInviteRequest(hash=hashv))
            return f"OK|{('channel' if getattr(result, 'channel', False) else 'group')}|{title}"
        except ChannelPrivateError:
            return f"TOOLTIP: This group can't be displayed because it violated Telegram's Terms of Service.\n  -> {title}"
        except ChannelBannedError:
            return f"BANNED|{title}"
        except UserBannedInChannelError:
            return f"BANNED_YOU|{title}"
        except UsersTooMuchError:
            return f"FULL|{title}"
        except InviteHashExpiredError:
            return f"EXPIRED|{title}"
        except Exception as e:
            return f"ERROR: {e}"
    return "ERROR: Unknown response"

def _bc_translate(res):
    if res is None:
        return " سليم | لا يوجد حظر"
    if res.startswith("OK|"):
        _, t, name = (res.split("|", 2) + ["", ""])[:3]
        return f" سليم | النوع: {t} | الاسم: {name}"
    if res == "BANNED_OR_NOT_FOUND":
        return " محظور أو غير موجود"
    if res == "BANNED_OR_PRIVATE":
        return " محظور أو خاص"
    if res == "BANNED":
        return " محظور (BANNED)"
    if res == "BANNED_YOU":
        return " محظور أنت فيه"
    if res == "BANNED_OR_EXPIRED":
        return "⏰ الرابط منتهٍ أو محظور"
    if res == "BANNED_OR_INVALID":
        return " الرابط غير صالح أو محظور"
    if res == "INVALID_USER_ID":
        return " معرف مستخدم غير صالح"
    if res == "NOT_FOUND":
        return "🔍 غير موجود"
    if res == "FULL":
        return " المجموعة ممتلئة"
    if res == "EXPIRED":
        return "⏰ الرابط منتهي الصلاحية"
    if res.startswith("SCAM_FAKE|"):
        parts = res.split("|", 1)
        return f" رابط وهمي/نصب (SCAM): {parts[1] if len(parts) > 1 else '؟'}"
    if res.startswith("TOOLTIP:"):
        return " " + res.replace("TOOLTIP:", "").strip().replace("None", "؟")
    if res.startswith("ERROR"):
        return "⚠️ " + res
    if res.startswith("FLOOD_WAIT"):
        return "⏳ " + res
    return res.replace("None", "؟")

# ============================================================
# قوائم الأوامر (مستلة من main.py مع تعديل م5)
# ============================================================
MENU_MAIN = f"""**[ سورس اشرف ]**
=========================

مرحبا بك عزيزي
هذه قائمة أقسام الأوامر — أرسل رقم القسم:

`{PREFIX}م1` | أوامر الإدارة
`{PREFIX}م2` | أوامر المجموعة
`{PREFIX}م3` | أوامر الكشف والايدي
`{PREFIX}م4` | أوامر الردود
`{PREFIX}م5` | أوامر الترحيب (خاص)
`{PREFIX}م6` | أوامر حماية الخاص
`{PREFIX}م7` | أوامر الإذاعة
`{PREFIX}م8` | أوامر البوت
`{PREFIX}م9` | أوامر المنع والترجمة
`{PREFIX}م10` | أوامر السبام والصملات
`{PREFIX}م11` | أوامر البروفايل
`{PREFIX}م12` | أوامر الصيغ
`{PREFIX}م13` | أوامر التسلية
`{PREFIX}م14` | أوامر التحكم
`{PREFIX}م15` | أوامر الذكاء الاصطناعي
`{PREFIX}م16` | أوامر التحديثات
`{PREFIX}م17` | فحص و بلاغات (باند و شد)
`{PREFIX}م18` | الاسم الوقتي (وقت حي بجانب اسمك)
`{PREFIX}م19` | محول الصوت (تغيير الصوت بمؤثرات)
`{PREFIX}م20` | الكتم (حذف رسائل المكتومين)
`{PREFIX}م21` | أوامر الحذف (حذف رسائلك)
`{PREFIX}م22` | أوامر المؤقته (حفظ الصور المؤقتة)
`{PREFIX}م23` | أوامر الانتحال (نسخ واستعادة الحساب)
`{PREFIX}م24` | أوامر المراقبة (تتبع المستخدمين)
`{PREFIX}م25` | أوامر النشر (5 رسائل و 10 كروبات)"""

MENU = {
    "م1": """**| أوامر الإدارة :**

`{p}حظر` | بالرد أو المعرف لحظر شخص
`{p}الغاء حظر` | لفك حظر شخص
`{p}طرد` | لطرد شخص من المجموعة
`{p}رفع مشرف` <لقب> | لرفع شخص مشرف
`{p}تنزيل مشرف` | لتنزيل مشرف
`{p}تثبيت` | لتثبيت رسالة بالرد
`{p}الغاء تثبيت` | لإلغاء التثبيت
`{p}مسح` <عدد> | لحذف رسائل
`{p}تحذير` | لتحذير عضو
`{p}التحذيرات` | لعرض تحذيرات عضو
`{p}حذف التحذيرات` | لمسح تحذيرات عضو""",
    "م2": """**| أوامر المجموعة :**

`{p}المشرفين` | لعرض مشرفي المجموعة
`{p}الاعضاء` | لعرض عدد الأعضاء
`{p}معلومات` | لعرض معلومات المجموعة
`{p}البوتات` | لعرض البوتات في المجموعة""",
    "م3": """**| أوامر الكشف والايدي :**

`{p}الايدي` | بالرد أو المعرف لعرض الايدي
`{p}كشف` | لعرض معلومات مستخدم
`{p}صورة` | لجلب صورة مستخدم
`{p}انشاء` | بالرد/المعرف لعرض تاريخ الإنشاء ودولة الحساب""",
    "م4": """**| أوامر الردود :**

`{p}اضف رد` <كلمة> | بالرد لإضافة رد على كلمة
`{p}حذف رد` <كلمة> | لحذف رد
`{p}الردود` | لعرض جميع الردود
`{p}مسح الردود` | لحذف كل الردود""",
    "م5": """**| أوامر الترحيب (خاص) :**

`{p}اضف ترحيب` <النص> | لإضافة ترحيب نصي (يرد في الخاص)
`{p}اضف ملصق ترحيب` | بالرد على ملصق أو متحركة لحفظها كترحيب
`{p}حذف الترحيبات` | لحذف النص والملصق معاً
`{p}تشغيل الترحيب` | لتفعيل الرد التلقائي على الخاص
`{p}ايقاف الترحيب` | لإيقاف الرد التلقائي""",
    "م6": """**| أوامر حماية الخاص :**

`{p}الحماية تشغيل` | لتشغيل حماية الخاص
`{p}الحماية تعطيل` | لتعطيل حماية الخاص
`{p}سماح` | للسماح لشخص بالخاص
`{p}رفض` | لرفض شخص من الخاص
`{p}المسموحين` | لعرض المسموح لهم""",
    "م7": """**| أوامر الإذاعة :**

`{p}للكروبات` <النص> | لنشر رسالة بكل مجموعاتك
`{p}للخاص` <النص> | لإرسال رسالة لكل محادثاتك الخاصة""",
    "م8": """**| أوامر البوت :**

`{p}فحص` | لعرض معلومات السورس
`{p}بنك` | لعرض سرعة الاستجابة
`{p}اعادة تشغيل` | لإعادة تشغيل السورس
`{p}الوقت` | لعرض مدة التشغيل
`{p}حالة` | لعرض معلومات الحساب والحالة""",
    "م9": """**| أوامر المنع والترجمة :**

`{p}منع` <كلمة> | لمنع كلمة في المجموعة
`{p}الغاء منع` <كلمة> | لإلغاء منع كلمة
`{p}قائمة المنع` | لعرض الكلمات الممنوعة
`{p}ترجمة` <كود> | بالرد لترجمة النص""",
    "م10": """**| أوامر السبام والصملات :**

`{p}نيكه` | سبام سب مولّد تلقائياً (بالرد يستهدف)
`{p}خلاص` | لإيقاف السبام
`{p}سرعه` <ثواني> | لضبط سرعة الإرسال (0 = فوري)
`{p}تتبع` | رد تلقائي بالسب على أي رسالة خاصة
`{p}كافي` | لإيقاف الرد التلقائي
`{p}معاينة سب` | لعرض عينات من المولّد
`{p}عدد السب` | لعرض عدد التراكيب الممكنة
`{p}اضف سب` <النوع> <النص> | لإثراء المكتبة
  (الأنواع: قريب | فعل | جمله | صفه | لاحقه | ساخره | قالبه)
`{p}حماية الفلود` | لتشغيل/إيقاف الحماية
`{p}الفلود` | لعرض إحصائيات الحماية
`{p}تحديد` | بالرد لتحديد رسالة من المحفوظات
`{p}تشغيل التحويل` | لبدء التحويل من المحفوظات
`{p}ايقاف التحويل` | لإيقاف التحويل
`{p}ديلاي` <ثواني> | لضبط زمن التحويل""",
    "م11": """**| أوامر البروفايل :**

`{p}تغيير اسم` <الاسم> | لتغيير اسمك
`{p}تغيير بايو` <النص> | لتغيير نبذتك
`{p}تغيير صورة` | بالرد لتغيير صورتك
`{p}حسابي` | لعرض معلومات حسابك""",
    "م12": """**| أوامر الصيغ :**

`{p}ملصق` | بالرد على صورة لتحويلها ملصق
`{p}صورة` | بالرد على ملصق لتحويله صورة
`{p}صوت` | بالرد على مقطع/أغنية/صوت/فيديو لتحويله بصمة صوت""",
    "م13": """**| أوامر التسلية :**

`{p}نسبة الحب` | لعرض نسبة الحب
`{p}نسبة الغباء` | لعرض نسبة الغباء
`{p}قلوب` | لعرض قلوب متحركة
`{p}عد` <رقم> | للعد التنازلي
`{p}نرد` | لرمي النرد""",
    "م14": """**| أوامر التحكم :**

`{p}التحكم تشغيل` | لتفعيل تحكم مستخدمين آخرين
`{p}التحكم تعطيل` | لتعطيل التحكم
`{p}اضف متحكم` | بالرد لإضافة متحكم
`{p}ازالة متحكم` | بالرد لإزالة متحكم
`{p}المتحكمين` | لعرض المتحكمين""",
    "م15": """**| أوامر الذكاء الاصطناعي (للمالك فقط):**

`{p}ذكاء` <نص> | محادثة تفاعلية + تنفيذ أدوات Telethon (JSON) ورد النتيجة
`{p}ذكاء مفعل` | تفعيل الوضع الشامل للأمر فقط (يحقق تعريف الأدوات بـ JSON parameters وينفّذ أي أداة بلا حدود). لا رد تلقائي بالخاص
`{p}ذكاء تشغيل` | رد تلقائي بالخاص (بدون أدوات)
`{p}ذكاء تعطيل` | إيقاف الرد التلقائي
`{p}ذكاء سياق` <رقم> | عدد رسائل السياق (الافتراضي 50)
`{p}ذكاء ذاكرة` | عرض الذاكرة | `{p}ذكاء ذاكرة مسح` لمسحها
`{p}ذكاء جلسة` | عرض/مسح جلسة المحادثة التفاعلية
`{p}دليل الذكاء` | توليد دليل السورس | `{p}ادوات الذكاء` لعرض الأدوات
`{p}تعليمات الذكاء` | عرض التعليمات | `<نص>` تعديل | `افتراضي` إرجاع

ملاحظة: في الوضع الشامل يكتب الذكاء استدعاء أداة JSON (بما فيها raw_tl بلا قيود) فينفّذها الكود ويعرض النتيجة ويتابع المحادثة.""",
    "م16": """**| أوامر التحديثات :**

`{p}تحديث` | لتنزيل آخر تحديث من GitHub وإعادة التشغيل
`{p}تحديثات` | لعرض آخر التحديثات والإضافات من GitHub
`{p}اخر_تحديث` | لعرض آخر إصدار منشور""",
    "م17": """**| فحص و بلاغات (باند و شد):**

**الفحص:**
`{p}فحص` <رابط> | فحص قناة/حساب
`{p}فحص_دعوه` <رابط> | فحص رابط دعوة
`{p}فحص_مجموعه` | فحص المجموعة الحالية

**البلاغات (بدون عدد):**
`{p}شد_هدف` <رابط> | ضبط الهدف
`{p}شد_نوع` <نوع> | نوع البلاغ
`{p}شد_رساله` <نص> | نص البلاغ
`{p}شد_سرعه` <ثواني> | التأخير بين البلاغات
`{p}شد` <رابط> | بدأ بلاغ مستمر
`{p}شد_ايقاف` | إيقاف البلاغ
`{p}شد_اعداد` | عرض الإعدادات""",
    "م18": """**| الاسم الوقتي (وقت حي بجانب اسمك):**

`{p}وقتي` | عرض الحالة والمعاينة والتوقيت
`{p}وقتي تشغيل` | يفعّل التحديث التلقائي كل دقيقة
`{p}وقتي ايقاف` | يوقفه
`{p}وقتي شكل <رقم>` | يختار شكل زخرفة الأرقام (مع أمثلة حية)
`{p}وقتي توقيت <بلد/مدينة>` | يختار التوقيت (بغداد/السعودية/مصر/لندن/...)""",
    "م19": """**| محول الصوت (تغيير الصوت بمؤثرات):**

`{p}صوتي` | عرض قائمة التأثيرات المتاحة (25 تأثيراً)
`{p}صوتي <رقم>` | بالرد على مقطع صوتي/فيديو لتطبيق التأثير (عبر API خارجي)
`{p}صوتي سجل` | التسجيل في خدمة الصوت لأول مرة

**التأثيرات:** سنجاب، عميق، روبوت، صدى، عكسي، همس، مكبر، هاتف، كهف، فضائي، هيليوم، شيطان، راديو، تحت الماء، وحش، 8-بت، فنطاز، بطيء، سريع، تأتأة، مكتوم، جوقة، سكران، تريمولو""",
    "م20": """**| الكتم (حذف رسائل المكتومين في كل الأماكن):**

`{p}كتم` | بالرد أو المعرف لكتم شخص (تُحذف رسائله في الخاص والمجموعات والقنوات)
`{p}الغاء كتم` | بالرد أو المعرف لفك كتم شخص
`{p}المكتومين` | لعرض قائمة المكتومين
`{p}مسح كل المكتومين` | لفك كتم جميع المكتومين""",
    "م21": """**| أوامر الحذف (حذف رسائلك):**

`{p}حذف` | يحذف جميع رسائلك في المحادثة الحالية (خاص أو مجموعة)""",
    "م22": """**| أوامر المؤقته (حفظ الصور المؤقتة):**

`{p}حفظ المؤقته` | بالرد على صورة لحفظها في المحفوظات (ترسل لك في الخاص)""",
    "م23": """**| أوامر الانتحال (نسخ واستعادة الحساب):**

`{p}انتحال` | بالرد على رسالة شخص لنسخ صورته واسمه وبايوه
`{p}استعاده` | استعادة صورتك واسمك وبايوك الأصليين
`{p}معلوماتي` | عرض معلومات حسابك وحالة الأوامر (بديل عن فحص)""",
    "م24": """**| أوامر المراقبة (تتبع المستخدمين):**

`{p}مراقبه` | بالرد على رسالة الهدف لبدء مراقبته (يحذف من القائمة بعد 3 دقائق من عدم النشاط)
`{p}الغاء المراقبه` | بالرد أو بدون لإنهاء مراقبة مستخدم أو كل المستخدمين في المحادثة""",
    "م25": """**| أوامر النشر (5 رسائل و 10 كروبات):**

`{p}تحديد رساله النشر <النص>` | حفظ الرسالة الأولى
`{p}تحديد رساله النشر 2 <النص>` | حفظ الرسالة الثانية
`{p}تحديد رساله النشر 3 <النص>` | حفظ الرسالة الثالثة
`{p}تحديد رساله النشر 4 <النص>` | حفظ الرسالة الرابعة
`{p}تحديد رساله النشر 5 <النص>` | حفظ الرسالة الخامسة

`{p}تحديد كروب النشر <رابط/يوزر>` | حفظ الكروب الأول
`{p}تحديد كروب النشر 2 <رابط/يوزر>` | حفظ الكروب الثاني
`{p}تحديد كروب النشر 3 <رابط/يوزر>` | حفظ الكروب الثالث
`{p}تحديد كروب النشر 4 <رابط/يوزر>` | حفظ الكروب الرابع
`{p}تحديد كروب النشر 5 <رابط/يوزر>` | حفظ الكروب الخامس
`{p}تحديد كروب النشر 6 <رابط/يوزر>` | حفظ الكروب السادس
`{p}تحديد كروب النشر 7 <رابط/يوزر>` | حفظ الكروب السابع
`{p}تحديد كروب النشر 8 <رابط/يوزر>` | حفظ الكروب الثامن
`{p}تحديد كروب النشر 9 <رابط/يوزر>` | حفظ الكروب التاسع
`{p}تحديد كروب النشر 10 <رابط/يوزر>` | حفظ الكروب العاشر

`{p}تحديد سرعة النشر <ثواني>` | ضبط السرعة (من 5 إلى 120 ثانية)
`{p}بدء النشر` | بدء عملية النشر
`{p}ايقاف النشر` | إيقاف النشر"""
}

# ============================================================
# كلاس جلسة المستخدم (UserbotSession) المعدّل بالكامل
# ============================================================
class UserbotSession:
    def __init__(self, client, user_id, session_key):
        self.client = client
        self.user_id = user_id
        self.session_key = session_key
        self.running = True
        self.current_user = None
        self.my_id = None
        self.flood_guard = None

        # متغيرات السبام والتحويل
        self.spam_delay = 0.0
        self.spam_running = False
        self.spam_task = None
        self.forward_delay = 0.5
        self.forward_running = False
        self.forward_task = None
        self.selected_saved_msg = None
        self.follow_running = False

        # متغيرات أخرى
        self.auto_reply_text = None
        self.replied_users = set()
        self.muted_users = set()
        self.clock = False
        self.clock_timezone = "Africa/Cairo"
        self.clock_task = None
        self.source_enabled = False
        self.radar_target = None
        self.radar_target_name = None
        self.original_name = None
        self.original_lastname = None
        self.original_bio = None
        self.original_photo_path = None
        self.is_copying = False
        self.active_decoration = None
        self.processing_message_ids = set()

        # متغيرات جديدة للمراقبة والانتحال والنشر والمؤقته
        self.monitoring_users = {}
        self.monitoring_tasks = {}
        self.publish_messages = []
        self.publish_groups = []
        self.publish_speed = 5.0
        self.publish_active = False
        self.publish_task = None
        self.radar_speed = 0.0

        # ===== متغيرات الترحيب الجديدة (خاص) =====
        self.welcome_text = None          # نص الترحيب
        self.welcome_media_path = None    # مسار ملف الملصق/المتحركة
        self.welcome_enabled = False      # تشغيل/إيقاف
        self.welcomed_users = set()       # لمنع التكرار في نفس الجلسة

        # بيانات التخزين
        self.db_data = {}

        asyncio.create_task(self.init_user())
        self.setup_handlers()
        print(f"[{self.session_key[:8]}] تم إنشاء جلسة للمستخدم {self.user_id}")

    async def init_user(self):
        try:
            self.current_user = await self.client.get_me()
            self.my_id = self.current_user.id
            is_premium = getattr(self.current_user, 'premium', False)
            self.flood_guard = TextFloodGuard(is_premium=is_premium)
            # تحميل إعدادات الترحيب من ملف JSON
            welcome_data = self._db_read("welcome_settings")
            self.welcome_text = welcome_data.get("text")
            self.welcome_media_path = welcome_data.get("media_path")
            self.welcome_enabled = welcome_data.get("enabled", False)
            print(f"[{self.session_key[:8]}] تم تسجيل دخول الحساب: {self.current_user.first_name}")
        except Exception as e:
            print(f"[{self.session_key[:8]}] خطأ في تسجيل الدخول: {e}")

    async def get_me_safe(self):
        if not self.current_user:
            await self.init_user()
        return self.current_user

    def is_my_message(self, event):
        if not self.my_id:
            return False
        return event.sender_id == self.my_id

    # ============================================================
    # دوال مساعدة للتخزين (محاكاة main.py)
    # ============================================================
    def _path(self, name):
        return os.path.join(DATA_DIR, f"{self.user_id}_{name}.json")

    def _db_read(self, name, default=None):
        p = self._path(name)
        if not os.path.exists(p):
            return {} if default is None else default
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {} if default is None else default

    def _db_write(self, name, data):
        with open(self._path(name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _db_get(self, name, key, default=None):
        return self._db_read(name).get(str(key), default)

    def _db_set(self, name, key, value):
        data = self._db_read(name)
        data[str(key)] = value
        self._db_write(name, data)

    def _db_del(self, name, key):
        data = self._db_read(name)
        if str(key) in data:
            del data[str(key)]
            self._db_write(name, data)
            return True
        return False

    # ============================================================
    # دوال الأوامر (مستلة من main.py)
    # ============================================================
    async def edit_or_reply(self, event, text, link_preview=False, **kwargs):
        text = str(text)
        try:
            if len(text) < 4096:
                try:
                    return await event.edit(text, link_preview=link_preview, **kwargs)
                except Exception:
                    return await event.reply(text, link_preview=link_preview, **kwargs)
            file = io.BytesIO(text.encode("utf-8"))
            file.name = "result.txt"
            reply = await event.get_reply_message()
            target = reply or event
            sent = await target.reply("الناتج طويل/كبير — تم إرساله كملف ", file=file)
            try:
                await event.delete()
            except:
                pass
            return sent
        except Exception as e:
            return await event.reply(f"خطأ: {e}")

    async def edit_delete(self, event, text, seconds=8, link_preview=False):
        try:
            msg = await event.edit(text, link_preview=link_preview)
        except Exception:
            try:
                msg = await event.reply(text, link_preview=link_preview)
            except Exception:
                return
        await asyncio.sleep(seconds)
        try:
            await msg.delete()
        except:
            pass

    async def get_target_user(self, event):
        reply = await event.get_reply_message()
        if reply:
            try:
                user = await self.client.get_entity(reply.sender_id)
                return user, reply.sender_id
            except Exception:
                return None, reply.sender_id
        return None, None

    # ============================================================
    # دوال السبام (من main.py)
    # ============================================================
    async def _keep_typing(self, chat_id):
        while self.spam_running:
            try:
                async with self.client.action(chat_id, "typing"):
                    await asyncio.sleep(4)
            except:
                pass

    async def _spam_loop(self, chat_id, reply_to=None):
        while self.spam_running:
            word = generate_insult()
            try:
                if self.flood_guard:
                    await self.flood_guard.wait_if_needed()
                await self.client.send_message(chat_id, word, reply_to=reply_to)
            except Exception as e:
                print(f"spam error: {e}")
            if self.spam_delay > 0:
                await asyncio.sleep(self.spam_delay)

    async def _forward_loop(self, chat_id):
        while self.forward_running:
            if not self.selected_saved_msg:
                self.forward_running = False
                break
            try:
                await self.client.forward_messages(chat_id, self.selected_saved_msg)
            except Exception as e:
                print(f"forward error: {e}")
            await asyncio.sleep(self.forward_delay)

    # ============================================================
    # دوال الساعة (_clock_loop)
    # ============================================================
    async def _clock_loop(self):
        while self.clock:
            try:
                style_num = user_time_style.get(self.user_id, "1")
                time_now = get_real_time_formatted(self.clock_timezone, style_num)
                if time_now:
                    me = await self.get_me_safe()
                    if me:
                        name_parts = me.first_name.split("|")
                        base_name = name_parts[0].strip()
                        bold_time = convert_to_bold_thick(time_now)
                        await self.client(UpdateProfileRequest(first_name=f"{base_name} | {bold_time}"))
                await asyncio.sleep(60)
            except Exception as e:
                print(f"خطأ في الساعة: {e}")
                await asyncio.sleep(60)

    # ============================================================
    # دوال المراقبة (من app (11) (3).py)
    # ============================================================
    async def start_monitoring(self, chat_id, target_user_id, target_username=""):
        try:
            if chat_id not in self.monitoring_users:
                self.monitoring_users[chat_id] = {}
            if target_user_id in self.monitoring_users[chat_id]:
                return False
            self.monitoring_users[chat_id][target_user_id] = {
                "last_activity": time.time(),
                "username": target_username
            }
            if chat_id not in self.monitoring_tasks or self.monitoring_tasks[chat_id].done():
                self.monitoring_tasks[chat_id] = asyncio.create_task(
                    self._monitoring_loop(chat_id)
                )
            return True
        except Exception as e:
            print(f"خطأ في بدء المراقبة: {e}")
            return False

    async def stop_monitoring(self, chat_id, target_user_id):
        try:
            if chat_id in self.monitoring_users:
                if target_user_id in self.monitoring_users[chat_id]:
                    del self.monitoring_users[chat_id][target_user_id]
                    if not self.monitoring_users[chat_id]:
                        del self.monitoring_users[chat_id]
                        if chat_id in self.monitoring_tasks:
                            self.monitoring_tasks[chat_id].cancel()
                            del self.monitoring_tasks[chat_id]
                    return True
            return False
        except Exception as e:
            print(f"خطأ في إيقاف المراقبة: {e}")
            return False

    async def stop_all_monitoring(self, chat_id=None):
        try:
            if chat_id:
                if chat_id in self.monitoring_users:
                    del self.monitoring_users[chat_id]
                if chat_id in self.monitoring_tasks:
                    self.monitoring_tasks[chat_id].cancel()
                    del self.monitoring_tasks[chat_id]
            else:
                for task in self.monitoring_tasks.values():
                    task.cancel()
                self.monitoring_tasks.clear()
                self.monitoring_users.clear()
            return True
        except Exception as e:
            print(f"خطأ في إيقاف جميع مهام المراقبة: {e}")
            return False

    async def update_user_activity(self, chat_id, user_id):
        try:
            if chat_id in self.monitoring_users:
                if user_id in self.monitoring_users[chat_id]:
                    self.monitoring_users[chat_id][user_id]["last_activity"] = time.time()
        except:
            pass

    async def _monitoring_loop(self, chat_id):
        try:
            while chat_id in self.monitoring_users and self.running:
                try:
                    current_time = time.time()
                    users_to_notify = []
                    for user_id, data in self.monitoring_users[chat_id].items():
                        if current_time - data["last_activity"] >= 180:
                            users_to_notify.append((user_id, data["username"]))
                    for user_id, username in users_to_notify:
                        try:
                            if chat_id in self.monitoring_users and user_id in self.monitoring_users[chat_id]:
                                del self.monitoring_users[chat_id][user_id]
                        except Exception as e:
                            print(f"خطأ في إزالة المستخدم: {e}")
                    if chat_id in self.monitoring_users and not self.monitoring_users[chat_id]:
                        del self.monitoring_users[chat_id]
                        break
                    await asyncio.sleep(10)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"خطأ في حلقة المراقبة: {e}")
                    await asyncio.sleep(10)
        except asyncio.CancelledError:
            pass
        finally:
            if chat_id in self.monitoring_tasks:
                del self.monitoring_tasks[chat_id]

    # ============================================================
    # دوال الانتحال (من app (11) (3).py)
    # ============================================================
    async def copy_user_profile(self, target_id):
        try:
            if not self.original_name:
                me = await self.get_me_safe()
                self.original_name = me.first_name or ""
                self.original_lastname = me.last_name or ""
                try:
                    photos = await self.client(GetUserPhotosRequest(user_id='me', offset=0, max_id=0, limit=1))
                    if photos.photos:
                        path = await self.client.download_media(photos.photos[0], file="./temp_original_photo.jpg")
                        self.original_photo_path = path
                except:
                    pass
            full = await self.client(GetFullUserRequest(target_id))
            target_user = full.users[0]
            bio = full.full_user.about
            try:
                photos = await self.client(GetUserPhotosRequest(user_id=target_id, offset=0, max_id=0, limit=1))
                if photos.photos:
                    file_path = await self.client.download_media(photos.photos[0], file="./temp_copy_photo.jpg")
                    await self.client(UploadProfilePhotoRequest(file=await self.client.upload_file(file_path)))
                    if os.path.exists(file_path):
                        os.remove(file_path)
            except:
                pass
            await self.client(UpdateProfileRequest(first_name=target_user.first_name or ""))
            await self.client(UpdateProfileRequest(last_name=target_user.last_name if target_user.last_name else ""))
            await self.client(UpdateProfileRequest(about=bio if bio else ""))
            self.is_copying = True
            return True
        except Exception as e:
            print(f"خطأ في النسخ: {e}")
            return False

    async def restore_my_profile(self):
        if not self.original_name:
            return False
        try:
            try:
                photos = await self.client(GetUserPhotosRequest(user_id='me', offset=0, max_id=0, limit=1))
                if photos.photos:
                    await self.client(DeletePhotosRequest(id=[photos.photos[0]]))
            except:
                pass
            if self.original_photo_path and os.path.exists(self.original_photo_path):
                file = await self.client.upload_file(self.original_photo_path)
                await self.client(UploadProfilePhotoRequest(file=file))
            await self.client(UpdateProfileRequest(first_name=self.original_name))
            await self.client(UpdateProfileRequest(last_name=self.original_lastname or ""))
            await self.client(UpdateProfileRequest(about=self.original_bio or ""))
            self.original_name = None
            self.original_photo_path = None
            self.is_copying = False
            return True
        except Exception as e:
            print(f"خطأ في الاستعادة: {e}")
            return False

    # ============================================================
    # دوال النشر (من app (11) (3).py مع تعديل العدد)
    # ============================================================
    async def start_publish(self, e):
        try:
            if not self.publish_messages:
                return
            if not self.publish_groups:
                return
            if self.publish_task and not self.publish_task.done():
                self.publish_active = False
                self.publish_task.cancel()
                await asyncio.sleep(0.5)
            self.publish_active = True
            self.publish_task = asyncio.create_task(self.publish_loop(e))
        except Exception as ex:
            print(f"خطأ في بدء النشر: {ex}")

    async def publish_loop(self, e):
        count = 0
        try:
            while self.publish_active and self.running:
                for message in self.publish_messages:
                    if not self.publish_active or not self.running:
                        break
                    for group in self.publish_groups:
                        if not self.publish_active or not self.running:
                            break
                        try:
                            if self.flood_guard:
                                await self.flood_guard.wait_if_needed()
                            await self.client.send_message(group, message)
                            count += 1
                            real_speed = get_real_speed(self.publish_speed)
                            if real_speed > 0:
                                await asyncio.sleep(real_speed)
                        except FloodWaitError as fw:
                            await asyncio.sleep(fw.seconds + random.uniform(1, 3))
                        except Exception as ex:
                            print(f"خطأ في النشر: {ex}")
                            await asyncio.sleep(random.uniform(1, 3))
        except asyncio.CancelledError:
            pass
        finally:
            self.publish_active = False

    # ============================================================
    # دوال المؤقته (حفظ الصور)
    # ============================================================
    async def save_temp_photo(self, event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            return await self.edit_delete(event, "- رد على صورة", 6)
        try:
            path = await reply.download_media(file=f"temp_photo_{int(time.time())}.jpg")
            if path:
                await self.client.send_file("me", path)
                if os.path.exists(path):
                    os.remove(path)
                await self.edit_or_reply(event, "تم حفظ الصورة في المحفوظات ✅")
            else:
                await self.edit_delete(event, "- فشل في تحميل الصورة", 6)
        except Exception as ex:
            await self.edit_delete(event, f"خطأ: {ex}", 6)

    # ============================================================
    # دوال الترحيب الجديدة (خاص)
    # ============================================================
    def _save_welcome_settings(self):
        data = {
            "text": self.welcome_text,
            "media_path": self.welcome_media_path,
            "enabled": self.welcome_enabled
        }
        self._db_write("welcome_settings", data)

    async def add_welcome_text(self, event, text):
        self.welcome_text = text.strip()
        # حذف الميديا إذا موجودة
        if self.welcome_media_path and os.path.exists(self.welcome_media_path):
            try:
                os.remove(self.welcome_media_path)
            except:
                pass
            self.welcome_media_path = None
        self._save_welcome_settings()
        await self.edit_or_reply(event, f"تم إضافة الترحيب النصي ✅\nالنص: {text.strip()}")

    async def add_welcome_sticker(self, event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            return await self.edit_delete(event, "- رد على ملصق أو متحركة", 6)
        # حذف النص السابق
        self.welcome_text = None
        # تحميل الملف
        try:
            ext = "webp" if reply.sticker else "gif" if getattr(reply.media, 'mime_type', '').startswith('video/') else "media"
            path = await reply.download_media(file=f"welcome_{self.user_id}.{ext}")
            if path:
                # حذف الملف القديم
                if self.welcome_media_path and os.path.exists(self.welcome_media_path) and self.welcome_media_path != path:
                    try:
                        os.remove(self.welcome_media_path)
                    except:
                        pass
                self.welcome_media_path = path
                self._save_welcome_settings()
                await self.edit_or_reply(event, "تم حفظ الملصق/المتحركة كترحيب ✅")
            else:
                await self.edit_delete(event, "- فشل في تحميل الملف", 6)
        except Exception as ex:
            await self.edit_delete(event, f"خطأ: {ex}", 6)

    async def clear_welcome(self, event):
        self.welcome_text = None
        if self.welcome_media_path and os.path.exists(self.welcome_media_path):
            try:
                os.remove(self.welcome_media_path)
            except:
                pass
            self.welcome_media_path = None
        self.welcome_enabled = False
        self.welcomed_users.clear()
        self._save_welcome_settings()
        await self.edit_or_reply(event, "تم حذف جميع الترحيبات ✅")

    async def enable_welcome(self, event):
        if not self.welcome_text and not self.welcome_media_path:
            return await self.edit_delete(event, "- لا يوجد ترحيب مضاف! أضف نصاً أو ملصقاً أولاً", 8)
        self.welcome_enabled = True
        self.welcomed_users.clear()
        self._save_welcome_settings()
        await self.edit_or_reply(event, "تم تشغيل الترحيب ✅")

    async def disable_welcome(self, event):
        self.welcome_enabled = False
        self.welcomed_users.clear()
        self._save_welcome_settings()
        await self.edit_or_reply(event, "تم إيقاف الترحيب ✅")

    # ============================================================
    # معالج الأوامر الرئيسي (setup_handlers)
    # ============================================================
    def setup_handlers(self):
        # ============================================================
        # أمر القائمة الرئيسية
        # ============================================================
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الاوامر") + r"$"))
        async def cmds(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, MENU_MAIN)

        # ============================================================
        # أوامر الأقسام (م1 إلى م25)
        # ============================================================
        for sec, txt in MENU.items():
            def _make(txt):
                async def handler(e):
                    if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                        return
                    await self.edit_or_reply(e, txt.format(p=PREFIX))
                return handler
            self.client.add_event_handler(
                _make(txt),
                events.NewMessage(pattern=re.compile("^\\" + PREFIX + sec + "$"), outgoing=True)
            )
            self.client.add_event_handler(
                _make(txt),
                events.MessageEdited(pattern=re.compile("^\\" + PREFIX + sec + "$"), outgoing=True)
            )

        # ============================================================
        # الأوامر الفردية (مستلة من main.py مع إضافة أوامر الترحيب الجديدة وحذف القديمة)
        # ============================================================
        # --- أوامر الإدارة (م1) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حظر") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def ban_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            try:
                await self.client(EditBannedRequest(e.chat_id, uid, ChatBannedRights(until_date=None, view_messages=True)))
            except Exception as ex:
                return await self.edit_delete(e, f"- تعذر الحظر: `{ex}`", 8)
            await self.edit_or_reply(e, f"تم حظر {mention(user)} ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الغاء حظر") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def unban_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            try:
                await self.client(EditBannedRequest(e.chat_id, uid, ChatBannedRights(until_date=None, view_messages=False, send_messages=False, send_media=False, send_stickers=False, send_gifs=False, send_games=False, send_inline=False, embed_links=False)))
            except Exception as ex:
                return await self.edit_delete(e, f"- تعذر فك الحظر: `{ex}`", 8)
            await self.edit_or_reply(e, f"تم فك حظر {mention(user)} ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("طرد") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def kick_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            try:
                await self.client.kick_participant(e.chat_id, uid)
            except Exception as ex:
                return await self.edit_delete(e, f"- تعذر الطرد: `{ex}`", 8)
            await self.edit_or_reply(e, f"تم طرد {mention(user)} ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("رفع مشرف") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def promote_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            title = "مشرف"
            args = e.pattern_match.group(1)
            uid = None
            if reply:
                uid = reply.sender_id
                if args and args.strip():
                    title = args.strip()
            elif args and args.strip():
                parts = args.strip().split(maxsplit=1)
                try:
                    uid = (await self.client.get_entity(parts[0])).id
                except Exception:
                    return await self.edit_delete(e, "- لم أجد المستخدم", 8)
                if len(parts) > 1:
                    title = parts[1]
            if not uid:
                return await self.edit_delete(e, "- رد على شخص لرفعه", 8)
            rights = ChatAdminRights(
                change_info=True, post_messages=True, edit_messages=True,
                delete_messages=True, ban_users=True, invite_users=True,
                pin_messages=True, add_admins=False, manage_call=True,
            )
            try:
                await self.client(EditAdminRequest(e.chat_id, uid, rights, title[:16]))
            except Exception as ex:
                return await self.edit_delete(e, f"- تعذر الرفع: `{ex}`", 8)
            user, _ = await self.get_target_user(e)
            await self.edit_or_reply(e, f"تم رفع {mention(user)} مشرفاً ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تنزيل مشرف") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def demote_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            rights = ChatAdminRights(
                change_info=False, post_messages=False, edit_messages=False,
                delete_messages=False, ban_users=False, invite_users=False,
                pin_messages=False, add_admins=False,
            )
            try:
                await self.client(EditAdminRequest(e.chat_id, uid, rights, ""))
            except Exception as ex:
                return await self.edit_delete(e, f"- تعذر التنزيل: `{ex}`", 8)
            await self.edit_or_reply(e, f"تم تنزيل {mention(user)} من الإشراف ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تثبيت") + r"$", outgoing=True))
        async def pin_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            if not reply:
                return await self.edit_delete(e, "- رد على رسالة لتثبيتها", 8)
            try:
                await self.client.pin_message(e.chat_id, reply.id, notify=True)
            except Exception as ex:
                return await self.edit_delete(e, f"- تعذر التثبيت: `{ex}`", 8)
            await self.edit_delete(e, "تم التثبيت ✅", 5)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الغاء تثبيت") + r"$", outgoing=True))
        async def unpin_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            try:
                if reply:
                    await self.client.unpin_message(e.chat_id, reply.id)
                else:
                    await self.client.unpin_message(e.chat_id)
            except Exception as ex:
                return await self.edit_delete(e, f"- تعذر الإلغاء: `{ex}`", 8)
            await self.edit_delete(e, "تم إلغاء التثبيت ✅", 5)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("مسح") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def delete_msgs_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            args = e.pattern_match.group(1)
            count = 0
            if reply:
                msgs = []
                async for msg in self.client.iter_messages(e.chat_id, min_id=reply.id - 1, reverse=True):
                    msgs.append(msg.id)
                    if len(msgs) >= 500:
                        break
                if msgs:
                    await self.client.delete_messages(e.chat_id, msgs)
                    count = len(msgs)
            elif args and args.strip().isdigit():
                n = int(args.strip())
                msgs = []
                async for msg in self.client.iter_messages(e.chat_id, limit=n + 1):
                    msgs.append(msg.id)
                if msgs:
                    await self.client.delete_messages(e.chat_id, msgs)
                    count = len(msgs)
            else:
                return await self.edit_delete(e, "- رد على رسالة أو ضع عدداً", 8)
            m = await self.client.send_message(e.chat_id, f"تم حذف {count} رسالة ✅")
            await asyncio.sleep(4)
            await m.delete()

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحذير") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def warn_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص لتحذيره", 8)
            key = f"{e.chat_id}"
            warns = self._db_read("warns")
            chat = warns.get(key, {})
            chat[str(uid)] = chat.get(str(uid), 0) + 1
            warns[key] = chat
            self._db_write("warns", warns)
            n = chat[str(uid)]
            text = f"تم تحذير {mention(user)}\nعدد التحذيرات: {n}/3"
            if n >= 3:
                try:
                    await self.client(EditBannedRequest(e.chat_id, uid, ChatBannedRights(until_date=None, send_messages=True)))
                    text += "\nتم كتمه لتجاوزه الحد ✅"
                except Exception:
                    pass
                chat[str(uid)] = 0
                warns[key] = chat
                self._db_write("warns", warns)
            await self.edit_or_reply(e, text)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("التحذيرات") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def warns_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص", 8)
            n = self._db_read("warns").get(f"{e.chat_id}", {}).get(str(uid), 0)
            await self.edit_or_reply(e, f"تحذيرات {mention(user)}: {n}/3")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حذف التحذيرات") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def clear_warns_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص", 8)
            warns = self._db_read("warns")
            key = f"{e.chat_id}"
            if key in warns and str(uid) in warns[key]:
                warns[key][str(uid)] = 0
                self._db_write("warns", warns)
            await self.edit_or_reply(e, f"تم حذف تحذيرات {mention(user)} ✅")

        # --- أوامر المجموعة (م2) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("المشرفين") + r"$", outgoing=True))
        async def admins_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            admins = []
            async for u in self.client.iter_participants(e.chat_id, filter=ChannelParticipantsAdmins):
                admins.append(f"• {mention(u)} — `{u.id}`")
            txt = "**| مشرفو المجموعة :**\n\n" + "\n".join(admins)
            await self.edit_or_reply(e, txt)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الاعضاء") + r"$", outgoing=True))
        async def members_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            full = await self.client.get_participants(e.chat_id, limit=0)
            await self.edit_or_reply(e, f"**عدد أعضاء** {e.chat.title}: `{full.total}`")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("معلومات") + r"$", outgoing=True))
        async def info_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = await e.get_chat()
            full = await self.client.get_participants(e.chat_id, limit=0)
            txt = f"""**| معلومات المجموعة :**
**الاسم:** {chat.title}
**الايدي:** `{e.chat_id}`
**عدد الأعضاء:** `{full.total}`
**المعرف:** @{chat.username if getattr(chat, 'username', None) else 'خاصة'}"""
            await self.edit_or_reply(e, txt)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("البوتات") + r"$", outgoing=True))
        async def bots_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            bots = []
            async for u in self.client.iter_participants(e.chat_id):
                if u.bot:
                    bots.append(f"• {mention(u)} — `{u.id}`")
            if not bots:
                return await self.edit_or_reply(e, "- لا يوجد بوتات في هذه المجموعة")
            await self.edit_or_reply(e, "**| البوتات :**\n\n" + "\n".join(bots))

        # --- أوامر الكشف والايدي (م3) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الايدي") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def id_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            args = e.pattern_match.group(1)
            reply = await e.get_reply_message()
            if args and args.strip():
                try:
                    p = await self.client.get_entity(args.strip())
                except Exception as ex:
                    return await self.edit_delete(e, f"`{ex}`", 6)
                name = getattr(p, "title", None) or get_display_name(p)
                return await self.edit_or_reply(e, f"ايدي `{name}` هو `{p.id}`")
            if reply:
                txt = f"**ايدي الدردشة:** `{e.chat_id}`\n**ايدي المرسل:** `{reply.sender_id}`"
                if reply.media:
                    txt += "\n**نوع:** ميديا"
                return await self.edit_or_reply(e, txt)
            await self.edit_or_reply(e, f"**ايدي الدردشة:** `{e.chat_id}`")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("كشف") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def whois_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not user:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            txt = f"""**| كشف المستخدم :**
**الاسم:** {get_display_name(user)}
**الايدي:** `{user.id}`
**المعرف:** @{user.username if user.username else 'لا يوجد'}
**بوت:** {'نعم' if user.bot else 'لا'}
**مقيد:** {'نعم' if getattr(user, 'restricted', False) else 'لا'}
**الرابط:** [هنا](tg://user?id={user.id})"""
            await self.edit_or_reply(e, txt)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("صورة") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def photo_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not user:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            m = await self.edit_or_reply(e, "- جاري الجلب...")
            try:
                photo = await self.client.download_profile_photo(user.id)
                if not photo:
                    return await self.edit_delete(e, "- لا يوجد صورة", 6)
                await self.client.send_file(e.chat_id, photo, caption=f"صورة {mention(user)}")
                os.remove(photo)
                await m.delete()
            except Exception as ex:
                await self.edit_delete(e, f"`{ex}`", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("انشاء") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def created_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not user:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            def estimate_date(uid):
                if uid < 1000000:
                    return "2013-2014"
                elif uid < 10000000:
                    return "2014-2015"
                elif uid < 100000000:
                    return "2015-2017"
                elif uid < 1000000000:
                    return "2017-2019"
                else:
                    return "2019-الآن"
            est = estimate_date(uid)
            await self.edit_or_reply(e, f"**تقدير تاريخ الإنشاء:** {est}")

        # --- أوامر الردود (م4) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("اضف رد") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def add_reply_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            word = e.pattern_match.group(1)
            if not reply or not word or not word.strip():
                return await self.edit_delete(e, "- رد على النص واكتب: اضف رد <الكلمة>", 8)
            if not reply.text:
                return await self.edit_delete(e, "- الرد يجب أن يكون نصاً", 8)
            self._db_set("replies", word.strip(), reply.text)
            await self.edit_or_reply(e, f"تم إضافة رد على: `{word.strip()}` ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حذف رد") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def del_reply_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            word = e.pattern_match.group(1)
            if not word or not word.strip():
                return await self.edit_delete(e, "- اكتب: حذف رد <الكلمة>", 8)
            if self._db_del("replies", word.strip()):
                await self.edit_or_reply(e, f"تم حذف الرد: `{word.strip()}` ✅")
            else:
                await self.edit_delete(e, "- لا يوجد رد بهذا الاسم", 8)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الردود") + r"$", outgoing=True))
        async def replies_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            data = self._db_read("replies")
            if not data:
                return await self.edit_or_reply(e, "- لا يوجد ردود مضافة")
            txt = "**| الردود المضافة :**\n\n" + "\n".join(f"• `{k}`" for k in data)
            await self.edit_or_reply(e, txt)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("مسح الردود") + r"$", outgoing=True))
        async def clear_replies_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self._db_write("replies", {})
            await self.edit_or_reply(e, "تم حذف جميع الردود ✅")

        # --- أوامر الترحيب الجديدة (م5) --- تم حذف الأوامر القديمة واستبدالها بالجديدة
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("اضف ترحيب") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def add_welcome_text_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            text = e.pattern_match.group(1)
            if not text or not text.strip():
                return await self.edit_delete(e, "- اكتب النص بعد الأمر", 8)
            await self.add_welcome_text(e, text.strip())

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("اضف ملصق ترحيب") + r"$", outgoing=True))
        async def add_welcome_sticker_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.add_welcome_sticker(e)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حذف الترحيبات") + r"$", outgoing=True))
        async def clear_welcome_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.clear_welcome(e)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تشغيل الترحيب") + r"$", outgoing=True))
        async def enable_welcome_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.enable_welcome(e)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ايقاف الترحيب") + r"$", outgoing=True))
        async def disable_welcome_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.disable_welcome(e)

        # --- أوامر حماية الخاص (م6) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الحماية تشغيل") + r"$", outgoing=True))
        async def pm_on_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self._db_set("settings", "pmpermit", True)
            await self.edit_or_reply(e, "تم تشغيل حماية الخاص ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الحماية تعطيل") + r"$", outgoing=True))
        async def pm_off_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self._db_set("settings", "pmpermit", False)
            await self.edit_or_reply(e, "تم تعطيل حماية الخاص ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("سماح") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def allow_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            uid = e.chat_id if e.is_private else None
            if not uid:
                return await self.edit_delete(e, "- هذا الأمر للخاص فقط", 8)
            allowed = self._db_read("pm_allowed")
            allowed[str(uid)] = True
            self._db_write("pm_allowed", allowed)
            counts = self._db_read("pm_counts")
            counts.pop(str(uid), None)
            self._db_write("pm_counts", counts)
            await self.edit_or_reply(e, "تم السماح لهذا الشخص بالخاص ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("رفض") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def deny_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            uid = e.chat_id if e.is_private else None
            if not uid:
                return await self.edit_delete(e, "- هذا الأمر للخاص فقط", 8)
            allowed = self._db_read("pm_allowed")
            allowed.pop(str(uid), None)
            self._db_write("pm_allowed", allowed)
            await self.edit_or_reply(e, "تم رفض هذا الشخص من الخاص ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("المسموحين") + r"$", outgoing=True))
        async def allowed_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            allowed = self._db_read("pm_allowed")
            if not allowed:
                return await self.edit_or_reply(e, "- لا يوجد مسموح لهم")
            txt = "**| المسموح لهم بالخاص :**\n\n" + "\n".join(f"• `{k}`" for k in allowed)
            await self.edit_or_reply(e, txt)

        # --- أوامر الإذاعة (م7) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("للكروبات") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def broadcast_groups_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            text = e.pattern_match.group(1)
            if not reply and not (text and text.strip()):
                return await self.edit_delete(e, "- اكتب نصاً أو رد على رسالة", 8)
            m = await self.edit_or_reply(e, "- جاري النشر بالمجموعات...")
            done, failed = 0, 0
            async for dialog in self.client.iter_dialogs():
                if dialog.is_group:
                    try:
                        if reply:
                            await self.client.send_message(dialog.id, reply)
                        else:
                            await self.client.send_message(dialog.id, text.strip())
                        done += 1
                        await asyncio.sleep(0.5)
                    except Exception:
                        failed += 1
            await m.edit(f"تم النشر ✅\nنجح: {done} | فشل: {failed}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("للخاص") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def broadcast_private_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            text = e.pattern_match.group(1)
            if not reply and not (text and text.strip()):
                return await self.edit_delete(e, "- اكتب نصاً أو رد على رسالة", 8)
            m = await self.edit_or_reply(e, "- جاري النشر بالخاص...")
            done, failed = 0, 0
            async for dialog in self.client.iter_dialogs():
                if dialog.is_user and not dialog.entity.bot:
                    try:
                        if reply:
                            await self.client.send_message(dialog.id, reply)
                        else:
                            await self.client.send_message(dialog.id, text.strip())
                        done += 1
                        await asyncio.sleep(0.5)
                    except Exception:
                        failed += 1
            await m.edit(f"تم النشر ✅\nنجح: {done} | فشل: {failed}")

        # --- أوامر البوت (م8) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("فحص") + r"$", outgoing=True))
        async def check_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            up = readable_time(time.time() - START_TIME.timestamp())
            me = await self.client.get_me()
            txt = f"""**[ سورس اشرف ]**
=========================

**الحالة:** يعمل ✅
**المالك:** {OWNER_NAME}
**الحساب:** {get_display_name(me)}
**البادئة:** `{PREFIX}`
**مدة التشغيل:** {up}
**المكتبة:** Telethon
**التخزين:** JSON

لعرض الأوامر أرسل `{PREFIX}الاوامر`
للتحديثات والتحسينات اشترك: https://t.me/acjava"""
            await self.edit_or_reply(e, txt)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حالة") + r"$", outgoing=True))
        async def status_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            up = readable_time(time.time() - START_TIME.timestamp())
            me = await self.client.get_me()
            txt = f"""**[ سورس اشرف ]**
=========================

**الحالة:** يعمل ✅
**المالك:** {OWNER_NAME}
**الحساب:** {get_display_name(me)}
**البادئة:** `{PREFIX}`
**مدة التشغيل:** {up}
**المكتبة:** Telethon
**التخزين:** JSON

لعرض الأوامر أرسل `{PREFIX}الاوامر`"""
            await self.edit_or_reply(e, txt)

        # --- أمر فحص الروابط (مستل من main.py) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("فحص") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def check_link_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = (e.pattern_match.group(1) or "").strip()
            if not arg:
                return await self.edit_delete(e, f"- اكتب: {PREFIX}فحص <رابط/معرف>", 8)
            m = await self.edit_or_reply(e, "🔍 جاري الفحص...")
            try:
                parsed = _bc_extract(arg)
                if not parsed:
                    return await m.edit(" مدخل غير صالح")
                kind, value = parsed
                if kind == "invite":
                    res = await _bc_check_invite(self.client, value)
                    await m.edit(_bc_translate(res))
                else:
                    res = await _bc_check_entity(self.client, value)
                    await m.edit(_bc_translate(res))
            except Exception as ex:
                await m.edit(f"خطأ: {ex}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("فحص_دعوه") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def check_invite_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = (e.pattern_match.group(1) or "").strip()
            if not arg:
                return await self.edit_delete(e, f"- اكتب: {PREFIX}فحص_دعوه <رابط الدعوة>", 8)
            m = await self.edit_or_reply(e, "🔍 جاري فحص الدعوة...")
            try:
                parsed = _bc_extract(arg)
                if not parsed or parsed[0] != "invite":
                    return await m.edit(" هذا ليس رابط دعوة صالحاً")
                res = await _bc_check_invite(self.client, parsed[1])
                await m.edit(_bc_translate(res))
            except Exception as ex:
                await m.edit(f"خطأ: {ex}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("فحص_مجموعه") + r"$", outgoing=True))
        async def check_group_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            m = await self.edit_or_reply(e, "🔍 جاري فحص المجموعة الحالية...")
            try:
                chat = await e.get_chat()
                await m.edit(f"**فحص المجموعة:**\nالاسم: {chat.title}\nالايدي: `{e.chat_id}`\nالنوع: {'قناة' if getattr(chat, 'broadcast', False) else 'مجموعة'}")
            except Exception as ex:
                await m.edit(f"خطأ: {ex}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("بنك") + r"$", outgoing=True))
        async def ping_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            start = time.time()
            m = await self.edit_or_reply(e, "...")
            ms = (time.time() - start) * 1000
            await m.edit(f"**السرعة:** `{ms:.2f}` ms")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الوقت") + r"$", outgoing=True))
        async def uptime_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            up = readable_time(time.time() - START_TIME.timestamp())
            await self.edit_or_reply(e, f"**مدة التشغيل:** {up}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("اعادة تشغيل") + r"$", outgoing=True))
        async def restart_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, "- جاري إعادة التشغيل...")
            self._db_set("settings", "restart_chat", e.chat_id)
            self._db_set("settings", "restart_msg", e.id)
            await self.client.disconnect()
            os.execl(sys.executable, sys.executable, os.path.abspath(__file__))

        # --- أوامر المنع والترجمة (م9) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("منع") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def banword_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            word = e.pattern_match.group(1)
            if not word or not word.strip():
                return await self.edit_delete(e, "- اكتب: منع <الكلمة>", 8)
            data = self._db_read("locked")
            key = f"{e.chat_id}"
            words = data.get(key, [])
            if word.strip() not in words:
                words.append(word.strip())
            data[key] = words
            self._db_write("locked", data)
            await self.edit_or_reply(e, f"تم منع الكلمة: `{word.strip()}` ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الغاء منع") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def unbanword_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            word = e.pattern_match.group(1)
            if not word or not word.strip():
                return await self.edit_delete(e, "- اكتب: الغاء منع <الكلمة>", 8)
            data = self._db_read("locked")
            key = f"{e.chat_id}"
            words = data.get(key, [])
            if word.strip() in words:
                words.remove(word.strip())
                data[key] = words
                self._db_write("locked", data)
                await self.edit_or_reply(e, f"تم إلغاء منع: `{word.strip()}` ✅")
            else:
                await self.edit_delete(e, "- الكلمة غير ممنوعة", 8)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("قائمة المنع") + r"$", outgoing=True))
        async def list_banwords_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            words = self._db_read("locked").get(f"{e.chat_id}", [])
            if not words:
                return await self.edit_or_reply(e, "- لا يوجد كلمات ممنوعة")
            txt = "**| الكلمات الممنوعة :**\n\n" + "\n".join(f"• `{w}`" for w in words)
            await self.edit_or_reply(e, txt)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ترجمة") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def translate_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            arg = e.pattern_match.group(1)
            lang = "ar"
            text = None
            if reply and reply.text:
                text = reply.text
                if arg and arg.strip():
                    lang = arg.strip()
            elif arg and len(arg.strip().split(maxsplit=1)) > 1:
                parts = arg.strip().split(maxsplit=1)
                lang = parts[0]
                text = parts[1]
            if not text:
                return await self.edit_delete(e, "- رد على نص | مثال: ترجمة en", 8)
            try:
                from googletrans import Translator
                tr = Translator()
                res = tr.translate(text, dest=lang)
                await self.edit_or_reply(e, f"**الترجمة ({res.src} | {lang}):**\n\n{res.text}")
            except Exception as ex:
                await self.edit_delete(e, f"- تعذر الترجمة (ثبّت googletrans): `{ex}`", 10)

        # --- أوامر السبام والصملات (م10) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("نيكه") + r"$", outgoing=True))
        async def spam_start_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if self.spam_running:
                return await self.edit_delete(e, "- الإرسال يعمل بالفعل", 6)
            reply = await e.get_reply_message()
            reply_to = reply.id if reply else None
            self.spam_running = True
            self._db_set("settings", "spam_active", True)
            self._db_set("settings", "spam_chat", e.chat_id)
            self._db_set("settings", "spam_reply", reply_to)
            self._db_set("settings", "spam_delay", self.spam_delay)
            self.spam_task = asyncio.ensure_future(self._spam_loop(e.chat_id, reply_to))
            asyncio.ensure_future(self._keep_typing(e.chat_id))
            msg = f" بدأ الإرسال... ⏱ {self.spam_delay}ث"
            if reply_to:
                msg += "\n مستهدف: على الرسالة المُشار إليها"
            await self.edit_or_reply(e, msg)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("خلاص") + r"$", outgoing=True))
        async def spam_stop_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if not self.spam_running:
                return await self.edit_delete(e, "- الإرسال متوقف بالفعل", 6)
            self.spam_running = False
            self._db_set("settings", "spam_active", False)
            if self.spam_task and not self.spam_task.done():
                self.spam_task.cancel()
            await self.edit_or_reply(e, " تم إيقاف الإرسال")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("سرعه") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def speed_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = e.pattern_match.group(1)
            try:
                delay = float(arg.strip())
                if delay < 0:
                    return await self.edit_delete(e, "- الوقت يجب أن يكون 0 أو أكثر", 6)
                self.spam_delay = delay
                await self.edit_or_reply(e, f"تم ضبط وقت الإرسال إلى {delay}ث ✅")
            except:
                await self.edit_delete(e, "- قيمة غير صالحة | مثال: سرعه 0.5", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تتبع") + r"$", outgoing=True))
        async def follow_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self.follow_running = True
            await self.edit_or_reply(e, "تم تفعيل التتبع ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("كافي") + r"$", outgoing=True))
        async def stop_follow_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self.follow_running = False
            await self.edit_or_reply(e, "تم إيقاف التتبع ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("معاينة سب") + r"$", outgoing=True))
        async def preview_insult_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            samples = "\n".join(f"• {generate_insult()}" for _ in range(5))
            await self.edit_or_reply(e, f"**| عينات من المولّد :**\n\n{samples}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("عدد السب") + r"$", outgoing=True))
        async def count_insult_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, f"عدد التراكيب الممكنة: `{insult_combos():,}`")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("اضف سب") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def add_insult_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = (e.pattern_match.group(1) or "").strip()
            parts = arg.split(maxsplit=1)
            if len(parts) < 2:
                return await self.edit_delete(e, "- اكتب: اضف سب <النوع> <النص>", 8)
            types_map = {
                "قريب": "qrayb", "فعل": "feal", "جمله": "jomla",
                "صفه": "sifat", "لاحقه": "laheq", "ساخره": "sakhira", "قالبه": "templates"
            }
            if parts[0] not in types_map:
                return await self.edit_delete(e, f"- الأنواع: {', '.join(types_map.keys())}", 8)
            key = types_map[parts[0]]
            INSULTS.setdefault(key, [])
            INSULTS[key].append(parts[1])
            path = os.path.join(DATA_DIR, f"{self.user_id}_insults.json")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(INSULTS, f, ensure_ascii=False, indent=2)
            except:
                pass
            await self.edit_or_reply(e, f"تم إضافة إلى `{parts[0]}` ✅\nالتراكيب الآن: `{insult_combos():,}`")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حماية الفلود") + r"$", outgoing=True))
        async def toggle_flood_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if self.flood_guard:
                self.flood_guard = None
                await self.edit_or_reply(e, "حماية الفلود: معطلة")
            else:
                me = await self.get_me_safe()
                is_premium = getattr(me, 'premium', False)
                self.flood_guard = TextFloodGuard(is_premium=is_premium)
                await self.edit_or_reply(e, "حماية الفلود: مفعلة")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الفلود") + r"$", outgoing=True))
        async def flood_stats_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if not self.flood_guard:
                return await self.edit_delete(e, "- الحماية غير مهيأة", 6)
            s = self.flood_guard.get_stats()
            txt = f"""**🛡️ حماية الفلود**

الحساب: {s['type']}
Tokens: {s['tokens']}
Refill: {s['refill']}
المعدل: {s['rate']}
المرسل: {s['total']}/{s['daily_max']}"""
            await self.edit_or_reply(e, txt)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد") + r"$", outgoing=True))
        async def select_msg_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            if not reply:
                return await self.edit_delete(e, "- رد على الرسالة في المحفوظات", 8)
            me = await self.client.get_me()
            if e.chat_id != me.id:
                return await self.edit_delete(e, "- استخدم هذا الأمر في المحفوظات فقط", 8)
            self.selected_saved_msg = reply
            preview = (reply.text or "[وسائط]")[:50]
            await self.edit_or_reply(e, f"تم تحديد الرسالة ✅\n📝 {preview}...")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تشغيل التحويل") + r"$", outgoing=True))
        async def forward_start_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if not self.selected_saved_msg:
                return await self.edit_delete(e, "- لم يتم تحديد رسالة! استخدم .تحديد أولاً", 8)
            if self.forward_running:
                return await self.edit_delete(e, "- التحويل يعمل بالفعل", 6)
            self.forward_running = True
            self.forward_task = asyncio.ensure_future(self._forward_loop(e.chat_id))
            await self.edit_or_reply(e, f" تشغيل التحويل من المحفوظات... delay: {self.forward_delay}ث")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ايقاف التحويل") + r"$", outgoing=True))
        async def forward_stop_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if not self.forward_running:
                return await self.edit_delete(e, "- التحويل متوقف بالفعل", 6)
            self.forward_running = False
            await self.edit_or_reply(e, " تم إيقاف التحويل")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ديلاي") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def delay_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = e.pattern_match.group(1)
            try:
                delay = float(arg.strip())
                if delay <= 0:
                    return await self.edit_delete(e, "- الوقت يجب أن يكون أكبر من 0", 6)
                self.forward_delay = delay
                await self.edit_or_reply(e, f"تم ضبط ديلاي التحويل إلى {delay}ث ✅")
            except:
                await self.edit_delete(e, "- قيمة غير صالحة | مثال: ديلاي 0.5", 6)

        # --- أوامر البروفايل (م11) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تغيير اسم") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_name_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            name = e.pattern_match.group(1)
            if not name or not name.strip():
                return await self.edit_delete(e, "- اكتب الاسم بعد الأمر", 8)
            parts = name.strip().split(maxsplit=1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ""
            try:
                await self.client(UpdateProfileRequest(first_name=first, last_name=last))
            except Exception as ex:
                return await self.edit_delete(e, f"`{ex}`", 8)
            await self.edit_or_reply(e, "تم تغيير الاسم ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تغيير بايو") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_bio_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            bio = e.pattern_match.group(1)
            if not bio or not bio.strip():
                return await self.edit_delete(e, "- اكتب البايو بعد الأمر", 8)
            try:
                await self.client(UpdateProfileRequest(about=bio.strip()))
            except Exception as ex:
                return await self.edit_delete(e, f"`{ex}`", 8)
            await self.edit_or_reply(e, "تم تغيير البايو ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تغيير صورة") + r"$", outgoing=True))
        async def set_photo_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            if not reply or not reply.media:
                return await self.edit_delete(e, "- رد على صورة", 8)
            m = await self.edit_or_reply(e, "- جاري التغيير...")
            try:
                photo = await self.client.download_media(reply.media)
                up = await self.client.upload_file(photo)
                await self.client(UploadProfilePhotoRequest(file=up))
                os.remove(photo)
                await m.edit("تم تغيير الصورة ✅")
            except Exception as ex:
                await m.edit(f"`{ex}`")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حسابي") + r"$", outgoing=True))
        async def myaccount_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            me = await self.client.get_me()
            txt = f"""**| معلومات حسابك :**
**الاسم:** {get_display_name(me)}
**الايدي:** `{me.id}`
**المعرف:** @{me.username if me.username else 'لا يوجد'}
**الرقم:** `+{me.phone if me.phone else 'مخفي'}`
**بريميوم:** {'نعم' if getattr(me, 'premium', False) else 'لا'}"""
            await self.edit_or_reply(e, txt)

        # --- أوامر الصيغ (م12) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ملصق") + r"$", outgoing=True))
        async def to_sticker_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            if not reply or not reply.photo:
                return await self.edit_delete(e, "- رد على صورة", 8)
            m = await self.edit_or_reply(e, "- جاري التحويل...")
            try:
                img = await self.client.download_media(reply.media)
                await self.client.send_file(e.chat_id, img, force_document=False, attributes=[DocumentAttributeFilename("sticker.webp")])
                os.remove(img)
                await m.delete()
            except Exception as ex:
                await m.edit(f"`{ex}`")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("صورة") + r"$", outgoing=True))
        async def to_image_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            if not reply or not reply.sticker:
                return await self.edit_delete(e, "- رد على ملصق", 8)
            m = await self.edit_or_reply(e, "- جاري التحويل...")
            try:
                st = await self.client.download_media(reply.media)
                await self.client.send_file(e.chat_id, st, force_document=False)
                os.remove(st)
                await m.delete()
            except Exception as ex:
                await m.edit(f"`{ex}`")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("صوت") + r"$", outgoing=True))
        async def to_voice_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            reply = await e.get_reply_message()
            if not reply or not (reply.audio or reply.voice or reply.video or reply.document or reply.video_note):
                return await self.edit_delete(e, "- رد على مقطع/أغنية/صوت/فيديو لتحويله إلى بصمة صوت", 8)
            m = await self.edit_or_reply(e, "- جاري التحويل إلى بصمة صوت...")
            tmp_in = None
            tmp_out = None
            try:
                tmp_in = await self.client.download_media(reply.media)
                tmp_out = tmp_in + "_voice.ogg"
                proc = await asyncio.create_subprocess_exec(
                    "ffmpeg", "-i", tmp_in,
                    "-vn", "-c:a", "libopus",
                    "-b:a", "32k", "-ar", "48000", "-ac", "1",
                    "-y", tmp_out,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await asyncio.wait_for(proc.wait(), timeout=120)
                if proc.returncode != 0:
                    return await m.edit(" فشل التحويل — تأكد من أن الملف صالح")
                await self.client.send_file(
                    e.chat_id, tmp_out,
                    voice_note=True,
                    attributes=[DocumentAttributeAudio(voice=True, duration=0)],
                    reply_to=reply.id,
                )
                await m.delete()
            except Exception as ex:
                await m.edit(f" خطأ: {ex}")
            finally:
                for f in (tmp_in, tmp_out):
                    if f and os.path.exists(f):
                        try: os.remove(f)
                        except: pass

        # --- أوامر التسلية (م13) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("نسبة الحب") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def love_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, f"نسبة الحب: {random.randint(0, 100)}% ♥")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("نسبة الغباء") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def stupid_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, f"نسبة الغباء: {random.randint(0, 100)}% 🤡")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("نرد") + r"$", outgoing=True))
        async def dice_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await e.delete()
            await self.client.send_message(e.chat_id, file=InputMediaDice(emoticon="\U0001F3B2"))

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("قلوب") + r"$", outgoing=True))
        async def hearts_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            hearts = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "❤️‍🔥"]
            for h in hearts:
                try:
                    await e.edit(h * 5)
                    await asyncio.sleep(0.4)
                except:
                    break

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("عد") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def countdown_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = e.pattern_match.group(1)
            if not arg or not arg.strip().isdigit():
                return await self.edit_delete(e, "- اكتب: عد <رقم>", 8)
            n = min(int(arg.strip()), 100)
            for i in range(n, -1, -1):
                try:
                    await e.edit(f"⏳ {i}")
                    await asyncio.sleep(1)
                except:
                    break
            await e.edit("انتهى ✅")

        # --- أوامر التحكم (م14) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("التحكم تشغيل") + r"$", outgoing=True))
        async def sudo_on_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self._db_set("settings", "sudo", True)
            await self.edit_or_reply(e, "تم تفعيل التحكم ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("التحكم تعطيل") + r"$", outgoing=True))
        async def sudo_off_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self._db_set("settings", "sudo", False)
            await self.edit_or_reply(e, "تم تعطيل التحكم ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("اضف متحكم") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def add_sudo_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص", 8)
            sudos = self._db_read("sudo_users")
            sudos[str(uid)] = get_display_name(user)
            self._db_write("sudo_users", sudos)
            await self.edit_or_reply(e, f"تم إضافة {mention(user)} متحكماً ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ازالة متحكم") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def remove_sudo_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص", 8)
            if self._db_del("sudo_users", uid):
                await self.edit_or_reply(e, f"تم إزالة {mention(user)} من المتحكمين ✅")
            else:
                await self.edit_delete(e, "- ليس متحكماً", 8)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("المتحكمين") + r"$", outgoing=True))
        async def sudo_list_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            sudos = self._db_read("sudo_users")
            if not sudos:
                return await self.edit_or_reply(e, "- لا يوجد متحكمين")
            txt = "**| المتحكمين :**\n\n" + "\n".join(f"• {v} — `{k}`" for k, v in sudos.items())
            await self.edit_or_reply(e, txt)

        # --- أوامر الذكاء الاصطناعي (م15) مبسطة ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ذكاء") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def ai_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, "⚠️ هذه الميزة تحتاج إلى تكوين API خارجي (QuillBot). تم تعطيلها مؤقتاً.")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ذكاء تشغيل") + r"$", outgoing=True))
        async def ai_on_cmd(e):
            await self.edit_or_reply(e, "⚠️ الميزة معطلة حالياً.")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ذكاء تعطيل") + r"$", outgoing=True))
        async def ai_off_cmd(e):
            await self.edit_or_reply(e, "⚠️ الميزة معطلة حالياً.")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ذكاء مفعل") + r"$", outgoing=True))
        async def ai_full_cmd(e):
            await self.edit_or_reply(e, "⚠️ الميزة معطلة حالياً.")

        # --- أوامر التحديثات (م16) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديث") + r"$", outgoing=True))
        async def update_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, "⚠️ ميزة التحديث معطلة في هذه النسخة.")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديثات") + r"$", outgoing=True))
        async def updates_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, "⚠️ ميزة التحديثات معطلة.")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("اخر_تحديث") + r"$", outgoing=True))
        async def last_update_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, "⚠️ ميزة آخر تحديث معطلة.")

        # --- أوامر الفحص والبلاغات (م17) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("فحص") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def check_entity_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = (e.pattern_match.group(1) or "").strip()
            if not arg:
                return await self.edit_delete(e, f"- اكتب: {PREFIX}فحص <رابط/معرف>", 8)
            m = await self.edit_or_reply(e, "🔍 جاري الفحص...")
            try:
                entity = await self.client.get_entity(arg)
                name = get_display_name(entity)
                typ = "قناة" if getattr(entity, 'broadcast', False) else "مجموعة" if getattr(entity, 'megagroup', False) else "مستخدم"
                await m.edit(f"**الفحص:**\nالنوع: {typ}\nالاسم: {name}\nالايدي: `{entity.id}`\nالمعرف: @{entity.username if entity.username else 'لا يوجد'}")
            except Exception as ex:
                await m.edit(f"خطأ: {ex}")

        # أوامر البلاغ (شد) - مبسطة
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("شد_هدف") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def report_target_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = (e.pattern_match.group(1) or "").strip()
            if not arg:
                return await self.edit_delete(e, "- اكتب: شد_هدف <رابط/معرف>", 8)
            self._db_set("report_cfg", "target", arg)
            await self.edit_or_reply(e, f"تم ضبط الهدف: {arg}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("شد_نوع") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def report_type_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = (e.pattern_match.group(1) or "").strip()
            types = ["spam","porn","violence","child_abuse","copyright","fake","illegal","other"]
            if not arg or arg not in types:
                return await self.edit_delete(e, f"- الأنواع: {', '.join(types)}", 8)
            self._db_set("report_cfg", "reason", arg)
            await self.edit_or_reply(e, f"تم ضبط نوع البلاغ: {arg}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("شد_رساله") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def report_msg_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = (e.pattern_match.group(1) or "").strip()
            if not arg:
                return await self.edit_delete(e, "- اكتب نص البلاغ", 8)
            self._db_set("report_cfg", "message", arg)
            await self.edit_or_reply(e, f"تم ضبط رسالة البلاغ:\n{arg}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("شد_سرعه") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def report_speed_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = (e.pattern_match.group(1) or "").strip()
            if not arg.isdigit():
                return await self.edit_delete(e, "- اكتب عدداً (ثواني)", 8)
            speed = max(1, min(int(arg), 60))
            self._db_set("report_cfg", "speed", speed)
            await self.edit_or_reply(e, f"سرعة البلاغ (تأخير): {speed} ثانية")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("شد") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def report_start_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            target = (e.pattern_match.group(1) or "").strip()
            if not target:
                target = self._db_get("report_cfg", "target")
            if not target:
                return await self.edit_delete(e, "- حدد هدفاً باستخدام .شد_هدف أو اكتبه مع الأمر", 8)
            self._db_set("report_cfg", "target", target)
            self._db_set("report_cfg", "running", True)
            msg = f" بدأ البلاغ المستمر على:\n{target}"
            await self.edit_or_reply(e, msg)
            asyncio.create_task(self._report_loop(e, target))

        async def _report_loop(self, e, target):
            cfg = self._db_read("report_cfg")
            reason = cfg.get("reason", "spam")
            message = cfg.get("message", "محتوى مخالف لشروط تلغرام")
            speed = cfg.get("speed", 3)
            sent = 0
            while self._db_get("report_cfg", "running", False):
                try:
                    entity = await self.client.get_entity(target)
                    reason_obj = InputReportReasonSpam()
                    await self.client(ReportPeerRequest(peer=entity, reason=reason_obj, message=message))
                    sent += 1
                except Exception as ex:
                    print(f"بلاغ فشل: {ex}")
                    break
                await asyncio.sleep(speed)
            self._db_set("report_cfg", "running", False)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("شد_ايقاف") + r"$", outgoing=True))
        async def report_stop_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self._db_set("report_cfg", "running", False)
            await self.edit_or_reply(e, "تم إيقاف البلاغ المستمر")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("شد_اعداد") + r"$", outgoing=True))
        async def report_settings_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            cfg = self._db_read("report_cfg")
            txt = f"""**| إعدادات الشد الداخلي:**
الهدف: {cfg.get('target', 'لايوجد')}
النوع: {cfg.get('reason', 'spam')}
الرسالة: {cfg.get('message', '')}
السرعة: {cfg.get('speed', 3)} ثانية
يعمل الآن: {'نعم' if cfg.get('running', False) else 'لا'}

الأوامر:
`{PREFIX}شد_هدف` <رابط/يوزر>
`{PREFIX}شد_نوع` <نوع>
`{PREFIX}شد_رساله` <نص>
`{PREFIX}شد_سرعه` <ثواني>
`{PREFIX}شد` | يبدأ البلاغ المستمر
`{PREFIX}شد_ايقاف` | يوقفه"""
            await self.edit_or_reply(e, txt)

        # --- أوامر الاسم الوقتي (م18) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("وقتي") + r"$", outgoing=True))
        async def time_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            active = self.clock
            tz = self.clock_timezone
            now = datetime.now(pytz.timezone(tz)) if tz else datetime.now()
            time_str = now.strftime("%I:%M %p")
            await self.edit_or_reply(e, f"**الاسم الوقتي:**\nالحالة: {'مفعل' if active else 'معطل'}\nالتوقيت: {tz}\nالوقت الحالي: {time_str}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("وقتي تشغيل") + r"$", outgoing=True))
        async def time_on_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self.clock = True
            if self.clock_task and not self.clock_task.done():
                self.clock_task.cancel()
            self.clock_task = asyncio.create_task(self._clock_loop())
            await self.edit_or_reply(e, "تم تفعيل الاسم الوقتي ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("وقتي ايقاف") + r"$", outgoing=True))
        async def time_off_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self.clock = False
            if self.clock_task and not self.clock_task.done():
                self.clock_task.cancel()
            await self.edit_or_reply(e, "تم إيقاف الاسم الوقتي ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("وقتي شكل") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def time_style_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = e.pattern_match.group(1)
            if not arg or not arg.strip().isdigit():
                styles = "\n".join(f"{k}: {v}" for k, v in time_styles.items())
                await self.edit_or_reply(e, f"**أنماط الأرقام:**\n{styles}\n\nاختر رقماً: .وقتي شكل <رقم>")
                return
            num = arg.strip()
            if num in time_styles:
                user_time_style[self.user_id] = num
                await self.edit_or_reply(e, f"تم ضبط نمط الأرقام إلى {num} ✅")
            else:
                await self.edit_delete(e, "- رقم غير صحيح", 8)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("وقتي توقيت") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def time_zone_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            country = e.pattern_match.group(1)
            if not country or not country.strip():
                return await self.edit_delete(e, "- اكتب اسم البلد أو المدينة", 8)
            tz = get_timezone_for_country(country.strip())
            if tz:
                self.clock_timezone = tz
                await self.edit_or_reply(e, f"تم ضبط التوقيت إلى {country.strip()} ({tz}) ✅")
            else:
                await self.edit_delete(e, "- لم أجد هذا البلد", 8)

        # --- أوامر محول الصوت (م19) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("صوتي") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def voice_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = e.pattern_match.group(1)
            if not arg:
                effects = [
                    "1- سنجاب", "2- عميق", "3- روبوت", "4- صدى", "5- عكسي",
                    "6- همس", "7- مكبر", "8- هاتف", "9- كهف", "10- فضائي",
                    "11- هيليوم", "12- شيطان", "13- راديو", "14- تحت الماء",
                    "15- وحش", "16- 8-بت", "17- فنطاز", "18- بطيء", "19- سريع",
                    "20- تأتأة", "21- مكتوم", "22- جوقة", "23- سكران", "24- تريمولو"
                ]
                await self.edit_or_reply(e, f"**مؤثرات الصوت:**\n{', '.join(effects)}\n\nاستخدم: .صوتي <رقم> بالرد على مقطع صوتي/فيديو")
                return
            try:
                num = int(arg.strip())
            except:
                return await self.edit_delete(e, "- رقم غير صحيح", 8)
            if num < 1 or num > 24:
                return await self.edit_delete(e, "- رقم خارج النطاق (1-24)", 8)
            reply = await e.get_reply_message()
            if not reply or not (reply.audio or reply.voice or reply.video or reply.document):
                return await self.edit_delete(e, "- رد على مقطع صوتي/فيديو/أغنية", 8)
            m = await self.edit_or_reply(e, "- جاري تطبيق المؤثر...")
            tmp_in = None
            tmp_out = None
            try:
                tmp_in = await self.client.download_media(reply.media)
                tmp_out = tmp_in + "_effect.ogg"
                effect_map = {
                    1: "asetrate=44100*1.3,aresample=44100",
                    2: "asetrate=44100*0.8,aresample=44100",
                    3: "aecho=0.8:0.9:1000:0.3",
                    4: "aecho=0.8:0.9:500:0.3",
                    5: "areverse",
                    6: "aecho=0.2:0.3:50:0.2",
                    7: "volume=3",
                    8: "aecho=0.5:0.5:100:0.1,aecho=0.5:0.5:200:0.1",
                    9: "aecho=0.8:0.9:1000:0.4",
                    10: "aecho=0.5:0.5:200:0.2,aecho=0.5:0.5:400:0.2",
                    11: "asetrate=44100*1.6,aresample=44100",
                    12: "aecho=0.5:0.5:100:0.1,aecho=0.5:0.5:200:0.1,aecho=0.5:0.5:300:0.1",
                    13: "aecho=0.5:0.5:150:0.1",
                    14: "aecho=0.5:0.5:300:0.2",
                    15: "aecho=0.5:0.5:200:0.2,aecho=0.5:0.5:400:0.2",
                    16: "asetrate=44100*0.5,aresample=44100",
                    17: "aecho=0.5:0.5:100:0.1,aecho=0.5:0.5:200:0.1",
                    18: "atempo=0.7",
                    19: "atempo=1.5",
                    20: "aecho=0.5:0.5:50:0.1",
                    21: "volume=0.3",
                    22: "chorus=0.5:0.9:50|0.4:0.9:60|0.3:0.9:70",
                    23: "aecho=0.5:0.5:100:0.1,aecho=0.5:0.5:200:0.1,atempo=0.8",
                    24: "tremolo=0.1:0.5",
                }
                filter_str = effect_map.get(num, "")
                if not filter_str:
                    return await m.edit("مؤثر غير مدعوم")
                proc = await asyncio.create_subprocess_exec(
                    "ffmpeg", "-i", tmp_in,
                    "-af", filter_str,
                    "-c:a", "libopus",
                    "-b:a", "32k", "-ar", "48000", "-ac", "1",
                    "-y", tmp_out,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await asyncio.wait_for(proc.wait(), timeout=120)
                if proc.returncode != 0:
                    return await m.edit(" فشل تطبيق المؤثر")
                await self.client.send_file(e.chat_id, tmp_out, voice_note=True, attributes=[DocumentAttributeAudio(voice=True, duration=0)], reply_to=reply.id)
                await m.delete()
            except Exception as ex:
                await m.edit(f" خطأ: {ex}")
            finally:
                for f in (tmp_in, tmp_out):
                    if f and os.path.exists(f):
                        try: os.remove(f)
                        except: pass

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("صوتي سجل") + r"$", outgoing=True))
        async def voice_register_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.edit_or_reply(e, "⚠️ ميزة التسجيل معطلة حالياً (تحتاج إلى API خارجي).")

        # --- أوامر الكتم (م20) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("كتم") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def mute_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            self.muted_users.add(uid)
            await self.edit_or_reply(e, f"تم كتم {mention(user)} ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الغاء كتم") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def unmute_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            user, uid = await self.get_target_user(e)
            if not uid:
                return await self.edit_delete(e, "- رد على شخص أو ضع معرفه", 8)
            if uid in self.muted_users:
                self.muted_users.remove(uid)
                await self.edit_or_reply(e, f"تم فك كتم {mention(user)} ✅")
            else:
                await self.edit_delete(e, "- هذا الشخص ليس مكتوماً", 8)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("المكتومين") + r"$", outgoing=True))
        async def muted_list_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if not self.muted_users:
                return await self.edit_or_reply(e, "- لا يوجد مكتومين")
            txt = "**| المكتومين :**\n\n" + "\n".join(f"• `{uid}`" for uid in self.muted_users)
            await self.edit_or_reply(e, txt)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("مسح كل المكتومين") + r"$", outgoing=True))
        async def clear_muted_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self.muted_users.clear()
            await self.edit_or_reply(e, "تم فك كتم جميع المكتومين ✅")

        # --- أوامر الحذف (م21) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حذف") + r"$", outgoing=True))
        async def delete_my_msgs_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            me = await self.get_me_safe()
            if not me:
                return
            m = await self.edit_or_reply(e, "- جاري حذف رسائلك...")
            deleted = 0
            batch = []
            async for msg in self.client.iter_messages(e.chat_id, from_user=me.id):
                batch.append(msg.id)
                if len(batch) >= 100:
                    try:
                        await self.client.delete_messages(e.chat_id, batch)
                        deleted += len(batch)
                    except Exception:
                        pass
                    batch = []
                    await asyncio.sleep(0.5)
            if batch:
                try:
                    await self.client.delete_messages(e.chat_id, batch)
                    deleted += len(batch)
                except Exception:
                    pass
            await m.edit(f"تم حذف {deleted} من رسائلك في هذه المحادثة ✅")

        # --- أوامر المؤقته (م22) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حفظ المؤقته") + r"$", outgoing=True))
        async def temp_photo_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            await self.save_temp_photo(e)

        # --- أوامر الانتحال (م23) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("انتحال") + r"$", outgoing=True))
        async def impersonate_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if e.is_reply:
                reply = await e.get_reply_message()
                if reply and reply.sender_id:
                    await self.copy_user_profile(reply.sender_id)
                    await self.edit_or_reply(e, "تم نسخ الحساب بنجاح ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("استعاده") + r"$", outgoing=True))
        async def restore_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if await self.restore_my_profile():
                await self.edit_or_reply(e, "تم استعادة الحساب الأصلي ✅")
            else:
                await self.edit_delete(e, "- لا توجد معلومات محفوظة للاستعادة", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("معلوماتي") + r"$", outgoing=True))
        async def my_info_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            me = await self.get_me_safe()
            if not me:
                return
            txt = f"""**| معلومات حسابي :**
الاسم: {get_display_name(me)}
الايدي: `{me.id}`
المعرف: @{me.username if me.username else 'لا يوجد'}
الرقم: +{me.phone if me.phone else 'مخفي'}
بريميوم: {'نعم' if getattr(me, 'premium', False) else 'لا'}
حالة الانتحال: {'مفعل' if self.is_copying else 'معطل'}"""
            await self.edit_or_reply(e, txt)

        # --- أوامر المراقبة (م24) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("مراقبه") + r"$", outgoing=True))
        async def start_monitoring_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if not e.is_reply:
                return await self.edit_delete(e, "- رد على رسالة الهدف", 8)
            reply = await e.get_reply_message()
            if not reply or not reply.sender_id:
                return await self.edit_delete(e, "- لم أستطع تحديد الهدف", 8)
            target_id = reply.sender_id
            try:
                user = await self.client.get_entity(target_id)
                username = getattr(user, 'username', '')
            except:
                username = ''
            if await self.start_monitoring(e.chat_id, target_id, username):
                await self.edit_or_reply(e, f"تم بدء مراقبة المستخدم `{target_id}` ✅")
            else:
                await self.edit_delete(e, "- المستخدم قيد المراقبة بالفعل", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الغاء المراقبه") + r"$", outgoing=True))
        async def stop_monitoring_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if e.is_reply:
                reply = await e.get_reply_message()
                if reply and reply.sender_id:
                    if await self.stop_monitoring(e.chat_id, reply.sender_id):
                        await self.edit_or_reply(e, f"تم إيقاف مراقبة المستخدم `{reply.sender_id}` ✅")
                    else:
                        await self.edit_delete(e, "- هذا المستخدم ليس قيد المراقبة", 6)
                    return
            # إيقاف كل المراقبة في هذه المحادثة
            await self.stop_all_monitoring(e.chat_id)
            await self.edit_or_reply(e, "تم إيقاف مراقبة جميع المستخدمين في هذه المحادثة ✅")

        # --- أوامر النشر (م25) ---
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد رساله النشر") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_msg1(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            text = e.pattern_match.group(1).strip()
            if not text:
                return await self.edit_delete(e, "- اكتب النص بعد الأمر", 8)
            if len(self.publish_messages) < 1:
                self.publish_messages.append(text)
            else:
                self.publish_messages[0] = text
            await self.edit_or_reply(e, f"تم حفظ الرسالة الأولى ✅\n{text}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد رساله النشر 2") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_msg2(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            text = e.pattern_match.group(1).strip()
            if not text:
                return await self.edit_delete(e, "- اكتب النص بعد الأمر", 8)
            if len(self.publish_messages) < 2:
                self.publish_messages.append(text)
            else:
                self.publish_messages[1] = text
            await self.edit_or_reply(e, f"تم حفظ الرسالة الثانية ✅\n{text}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد رساله النشر 3") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_msg3(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            text = e.pattern_match.group(1).strip()
            if not text:
                return await self.edit_delete(e, "- اكتب النص بعد الأمر", 8)
            if len(self.publish_messages) < 3:
                self.publish_messages.append(text)
            else:
                self.publish_messages[2] = text
            await self.edit_or_reply(e, f"تم حفظ الرسالة الثالثة ✅\n{text}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد رساله النشر 4") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_msg4(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            text = e.pattern_match.group(1).strip()
            if not text:
                return await self.edit_delete(e, "- اكتب النص بعد الأمر", 8)
            if len(self.publish_messages) < 4:
                self.publish_messages.append(text)
            else:
                self.publish_messages[3] = text
            await self.edit_or_reply(e, f"تم حفظ الرسالة الرابعة ✅\n{text}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد رساله النشر 5") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_msg5(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            text = e.pattern_match.group(1).strip()
            if not text:
                return await self.edit_delete(e, "- اكتب النص بعد الأمر", 8)
            if len(self.publish_messages) < 5:
                self.publish_messages.append(text)
            else:
                self.publish_messages[4] = text
            await self.edit_or_reply(e, f"تم حفظ الرسالة الخامسة ✅\n{text}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group1(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 1:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[0] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب الأول ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 2") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group2(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 2:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[1] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب الثاني ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 3") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group3(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 3:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[2] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب الثالث ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 4") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group4(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 4:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[3] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب الرابع ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 5") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group5(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 5:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[4] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب الخامس ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 6") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group6(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 6:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[5] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب السادس ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 7") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group7(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 7:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[6] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب السابع ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 8") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group8(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 8:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[7] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب الثامن ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 9") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group9(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 9:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[8] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب التاسع ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد كروب النشر 10") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_group10(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            chat = e.pattern_match.group(1).strip()
            if not chat:
                return await self.edit_delete(e, "- اكتب رابط أو يوزر الكروب", 8)
            try:
                entity = await self.client.get_entity(chat)
                if len(self.publish_groups) < 10:
                    self.publish_groups.append(entity.id)
                else:
                    self.publish_groups[9] = entity.id
                await self.edit_or_reply(e, f"تم حفظ الكروب العاشر ✅\n{chat}")
            except Exception as ex:
                await self.edit_delete(e, f"- لم أجد الكروب: {ex}", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("تحديد سرعة النشر") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_publish_speed_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = e.pattern_match.group(1).strip()
            if not arg:
                return await self.edit_delete(e, "- اكتب سرعة بالثواني (5-120)", 8)
            try:
                speed = float(arg)
                if speed < 5:
                    speed = 5
                if speed > 120:
                    speed = 120
                self.publish_speed = speed
                await self.edit_or_reply(e, f"تم ضبط سرعة النشر إلى {speed} ثانية ✅")
            except:
                await self.edit_delete(e, "- قيمة غير صالحة", 6)

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("بدء النشر") + r"$", outgoing=True))
        async def start_publish_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if not self.publish_messages:
                return await self.edit_delete(e, "- لا توجد رسائل نشر محفوظة", 6)
            if not self.publish_groups:
                return await self.edit_delete(e, "- لا توجد كروبات نشر محفوظة", 6)
            if self.publish_active:
                return await self.edit_delete(e, "- النشر يعمل بالفعل", 6)
            await self.start_publish(e)
            await self.edit_or_reply(e, f"بدأ النشر ✅\nرسائل: {len(self.publish_messages)}\nكروبات: {len(self.publish_groups)}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("ايقاف النشر") + r"$", outgoing=True))
        async def stop_publish_cmd(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            if not self.publish_active:
                return await self.edit_delete(e, "- النشر غير مفعل", 6)
            self.publish_active = False
            if self.publish_task and not self.publish_task.done():
                self.publish_task.cancel()
            await self.edit_or_reply(e, "تم إيقاف النشر ✅")

        # ============================================================
        # معالجات تلقائية (من main.py) - تم حذف معالج الترحيب القديم
        # ============================================================
        @self.client.on(events.NewMessage(incoming=True))
        async def auto_reply_watcher(e):
            if not self.running or self.user_id in banned_users:
                return
            if e.sender_id == self.my_id:
                return
            if self.auto_reply_text and e.is_private:
                if e.sender_id not in self.replied_users:
                    await e.reply(self.auto_reply_text)
                    self.replied_users.add(e.sender_id)

        @self.client.on(events.NewMessage(incoming=True))
        async def mute_watcher(e):
            if not self.running or self.user_id in banned_users:
                return
            if e.sender_id in self.muted_users:
                try:
                    await e.delete()
                except:
                    pass

        @self.client.on(events.NewMessage(incoming=True))
        async def pmpermit_watcher(e):
            if not self.running or self.user_id in banned_users:
                return
            if not e.is_private or e.sender_id == self.my_id:
                return
            if not self._db_get("settings", "pmpermit", False):
                return
            sender = await e.get_sender()
            if sender is None or sender.bot or getattr(sender, "verified", False):
                return
            uid = str(e.sender_id)
            if self._db_read("pm_allowed").get(uid):
                return
            counts = self._db_read("pm_counts")
            n = counts.get(uid, 0) + 1
            counts[uid] = n
            self._db_write("pm_counts", counts)
            if n >= 5:
                try:
                    await self.client(BlockRequest(e.sender_id))
                    await e.respond("تم حظرك لتكرار الرسائل.")
                except Exception:
                    pass
                counts.pop(uid, None)
                self._db_write("pm_counts", counts)
                return
            try:
                await e.respond(f"**| حماية الخاص — سورس اشرف**\n\nهذا حساب محمي، انتظر موافقة صاحب الحساب.\nتكرار الرسائل سيؤدي لحظرك.\n\nتحذير {n}/5")
            except:
                pass

        @self.client.on(events.NewMessage(incoming=True))
        async def replies_watcher(e):
            if not self.running or self.user_id in banned_users:
                return
            if e.sender_id == self.my_id:
                return
            if not e.text:
                return
            data = self._db_read("replies")
            if not data:
                return
            reply = data.get(e.raw_text.strip())
            if reply:
                try:
                    await e.reply(reply)
                except:
                    pass

        @self.client.on(events.NewMessage(incoming=True))
        async def lock_watcher(e):
            if not self.running or self.user_id in banned_users:
                return
            if e.sender_id == self.my_id:
                return
            if not e.text or not e.is_group:
                return
            words = self._db_read("locked").get(f"{e.chat_id}", [])
            if not words:
                return
            low = e.raw_text.lower()
            if any(w.lower() in low for w in words):
                try:
                    await e.delete()
                except:
                    pass

        @self.client.on(events.NewMessage(incoming=True))
        async def radar_watcher(e):
            if not self.running or self.user_id in banned_users:
                return
            if e.sender_id == self.my_id:
                return
            if self.radar_target and e.sender_id == self.radar_target:
                if self.spam_running:
                    word = generate_insult()
                    try:
                        if self.flood_guard:
                            await self.flood_guard.wait_if_needed()
                        await e.reply(word)
                    except:
                        pass

        # ============================================================
        # معالج الترحيب الجديد (خاص)
        # ============================================================
        @self.client.on(events.NewMessage(incoming=True))
        async def welcome_private_handler(e):
            if not self.running or self.user_id in banned_users:
                return
            # فقط في الخاص
            if not e.is_private:
                return
            # لا نرد على رسائلي أنا
            if e.sender_id == self.my_id:
                return
            # لا نرد على البوتات
            if e.sender and e.sender.bot:
                return
            # التحقق من التفعيل
            if not self.welcome_enabled:
                return
            # التأكد من وجود ترحيب (نص أو ملصق)
            if not self.welcome_text and not self.welcome_media_path:
                return
            # منع التكرار لنفس المستخدم في الجلسة
            if e.sender_id in self.welcomed_users:
                return
            # إضافة المستخدم إلى القائمة المردود عليها
            self.welcomed_users.add(e.sender_id)
            try:
                if self.welcome_text:
                    await e.reply(self.welcome_text)
                elif self.welcome_media_path and os.path.exists(self.welcome_media_path):
                    await self.client.send_file(e.sender_id, self.welcome_media_path)
            except Exception as ex:
                print(f"خطأ في الترحيب الخاص: {ex}")

        # ============================================================
        # أمر الرد التلقائي (من app القديم)
        # ============================================================
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("رد تلقائي") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_auto_reply(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            text = e.pattern_match.group(1)
            if not text or not text.strip():
                return await self.edit_delete(e, "- اكتب الرد بعد الأمر", 8)
            self.auto_reply_text = text.strip()
            self.replied_users.clear()
            await self.edit_or_reply(e, "تم إضافة الرد التلقائي ✅")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("حذف الرد") + r"$", outgoing=True))
        async def del_auto_reply(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self.auto_reply_text = None
            self.replied_users.clear()
            await self.edit_or_reply(e, "تم حذف الرد التلقائي ✅")

        # ============================================================
        # أوامر إضافية من app القديم (الانتحال، البلش، إلخ) - تم دمجها سابقاً
        # ============================================================
        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("بلش") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_radar(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            target_user = None
            if e.is_reply:
                reply = await e.get_reply_message()
                if reply and reply.sender_id:
                    target_user = reply.sender_id
            else:
                arg = e.pattern_match.group(1)
                if arg and arg.strip():
                    try:
                        entity = await self.client.get_entity(arg.strip())
                        target_user = entity.id
                    except:
                        return
            if target_user:
                self.radar_target = target_user
                await self.edit_or_reply(e, f"تم تعيين الهدف: {target_user}")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("الغاء البلش") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def stop_radar(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            self.radar_target = None
            await self.edit_or_reply(e, "تم إلغاء التتبع")

        @self.client.on(events.NewMessage(pattern=r"^\." + re.escape("سرعه البلش") + r"(?:\s|$)([\s\S]*)", outgoing=True))
        async def set_radar_speed(e):
            if not self.running or self.user_id in banned_users or not self.is_my_message(e):
                return
            arg = e.pattern_match.group(1).strip()
            try:
                speed = float(arg)
                if speed < 0:
                    speed = 0
                if speed > 60:
                    speed = 60
                self.radar_speed = speed
                await self.edit_or_reply(e, f"تم ضبط سرعة البلش إلى {speed} ثانية ✅")
            except:
                await self.edit_delete(e, "- قيمة غير صالحة", 6)

    # ============================================================
    # دالة إيقاف الجلسة
    # ============================================================
    async def stop(self):
        self.running = False
        self.spam_running = False
        if self.spam_task and not self.spam_task.done():
            self.spam_task.cancel()
        if self.clock_task and not self.clock_task.done():
            self.clock_task.cancel()
        self.forward_running = False
        if self.forward_task and not self.forward_task.done():
            self.forward_task.cancel()
        self.publish_active = False
        if self.publish_task and not self.publish_task.done():
            self.publish_task.cancel()
        await self.stop_all_monitoring()
        try:
            await self.client.disconnect()
        except:
            pass
        print(f"[{self.session_key[:8]}] تم إيقاف جلسة المستخدم {self.user_id}")

# ============================================================
# دوال البوت الرئيسية (من app القديم)
# ============================================================
# متغيرات البوت العامة
allowed_users = set()
banned_users = set()
waiting_sessions = {}
all_clients = []
user_clients = {}
waiting_user_add = set()
waiting_user_ban = set()
waiting_user_unban = set()
pending_requests = {}
request_notified = {}
source_enabled = {}
waiting_phone = {}
waiting_code = {}
waiting_2fa = {}
phone_clients = {}
START_TIME = datetime.now(pytz.UTC)

bot = TelegramClient("manager", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern="/start"))
async def start(e):
    user_id = e.sender_id
    if user_id in banned_users:
        await e.reply(fancy_text("""
╔══════════════════════════╗
║            𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅          
╚══════════════════════════╝

✧ المطور حظرك من البوت
✧ لمراسله المطور @C_GGV
""", "script"))
        return
    if user_id not in allowed_users and user_id != OWNER_ID:
        await e.reply(fancy_text("""
╔══════════════════════════╗
║            𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅          
╚══════════════════════════╝

✧ هلا منور
✧ انت غير مصرح لك باستخدام البوت
✧ ابعت /request عشان تبعث طلب تفعيل 
""", "script"))
        return
    user_sessions_count = len(user_clients.get(user_id, []))
    panel_text = fancy_text(f"""
╔══════════════════════════╗
║          𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅   
╚══════════════════════════╝

✧ عدد جلساتك ↤ {user_sessions_count}

⋆⋅☆⋅⋆ ──── ⋆⋅☆⋅⋆
""", "script")
    if user_id == OWNER_ID:
        total_users = len(allowed_users)
        add_session_text = fancy_button_text(" اضافـه جلسه")
        add_user_text = fancy_button_text(" اضافـه مستخدم")
        ban_user_text = fancy_button_text(" حظر مستخدم")
        unban_user_text = fancy_button_text(" فك حظر مستخدم")
        enable_src_text = fancy_button_text(" تفعيل السورس")
        disable_src_text = fancy_button_text(" تعطيل السورس")
        login_phone_text = fancy_button_text(" تفعيل بالرقم")
        panel_text = fancy_text(f"""
╔══════════════════════════╗
║          𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅   
╚══════════════════════════╝

✧ عدد المستخدمين ↤ {total_users}
✧ عدد جلساتك ↤ {user_sessions_count}

⋆⋅☆⋅⋆ ──── ⋆⋅☆⋅⋆
""", "script")
        buttons = [
            [Button.inline(add_session_text, "addsession")],
            [Button.inline(ban_user_text, "banuser"), Button.inline(add_user_text, "adduser")],
            [Button.inline(unban_user_text, "unbanuser")],
            [Button.inline(enable_src_text, "enable_source"), Button.inline(disable_src_text, "disable_source")],
            [Button.inline(login_phone_text, "login_phone")]
        ]
    else:
        add_session_text = fancy_button_text(" اضافـه جلسه")
        enable_src_text = fancy_button_text(" تفعيل السورس")
        disable_src_text = fancy_button_text(" تعطيل السورس")
        login_phone_text = fancy_button_text(" تفعيل بالرقم")
        buttons = [
            [Button.inline(add_session_text, "addsession")],
            [Button.inline(enable_src_text, "enable_source"), Button.inline(disable_src_text, "disable_source")],
            [Button.inline(login_phone_text, "login_phone")]
        ]
    await e.reply(panel_text, buttons=buttons)

@bot.on(events.NewMessage(pattern="/request"))
async def request(e):
    user_id = e.sender_id
    if user_id in pending_requests:
        await e.reply(fancy_text("""
╔══════════════════════════╗
║            𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅          
╚══════════════════════════╝

✧ اصبر المالك يقبلك كن هادئاً
""", "script"))
        return
    if user_id in banned_users:
        await e.reply(fancy_text(" ✧ تم حظرك من البوت", "script"))
        return
    if user_id in request_notified:
        await e.reply(fancy_text("""
╔══════════════════════════╗
║            𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅          
╚══════════════════════════╝

 ✧ اصبر المالك يقبلك كن هادئ
""", "script"))
        return
    pending_requests[user_id] = True
    request_notified[user_id] = True
    accept_text = fancy_button_text(" قبول")
    reject_text = fancy_button_text(" رفض")
    await bot.send_message(OWNER_ID, fancy_text(f"""
╔══════════════════════════╗
║          𝐍𝐄𝐖 𝐑𝐄𝐐𝐔𝐄𝐒𝐓     
╚══════════════════════════╝

✧ المستخدم ↤ {user_id}
✧ يطلب تشغيل البوت
""", "script"), buttons=[
        [Button.inline(accept_text, f"acc_{user_id}")],
        [Button.inline(reject_text, f"rej_{user_id}")]
    ])
    await e.reply(fancy_text("""
╔══════════════════════════╗
║            𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅          
╚══════════════════════════╝

✧ تم ارسال طلبك انتظر ان يقبلك المالك
""", "script"))

@bot.on(events.NewMessage(pattern="/source"))
async def source(e):
    user_id = e.sender_id
    if user_id in banned_users:
        await e.reply(fancy_text("تم حظرك من البوت", "script"))
        return
    if user_id not in allowed_users and user_id != OWNER_ID:
        return
    source_text = fancy_text("""
╔══════════════════════════╗
║          𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅   
╚══════════════════════════╝


━━━━━━━━━━━━━━━━━━━━━━━━
✧ قنـاه السـورس ↤ @esraf4
✧ المـطـور ↤ @C_GGV
✧ الـبـوت ↤ @TelethonByKevobot
━━━━━━━━━━━━━━━━━━━━━━━━

✧ اضـغـط لـلـنـسـخ
""", "script")
    buttons = [
        [Button.inline(fancy_button_text(" نسـخ اسـم السـورس"), "copy_source")],
        [Button.inline(fancy_button_text(" نسخ رابط القناه"), "copy_channel")],
        [Button.inline(fancy_button_text(" نسـخ يوزر البوت"), "copy_bot")],
        [Button.inline(fancy_button_text(" نسـخ يوزر المطور"), "copy_dev")]
    ]
    await e.reply(source_text, buttons=buttons)

@bot.on(events.NewMessage(pattern="/sessions"))
async def list_sessions(e):
    user_id = e.sender_id
    if user_id in banned_users:
        await e.reply(fancy_text("تم حظرك من البوت", "script"))
        return
    if user_id not in allowed_users and user_id != OWNER_ID:
        return
    sessions = user_clients.get(user_id, [])
    if not sessions:
        await e.reply(fancy_text("✧ مافي جلسات", "script"))
        return
    session_list = []
    for i, session in enumerate(sessions):
        try:
            me = await session.get_me_safe()
            name = me.first_name if me else "الحساب"
        except:
            name = "الحساب"
        session_list.append(f"✧ الجلسة {i+1} ↤ {name} (ارسل /stop_session {i+1} لايقافها)")
    text = fancy_text(f"""
╔══════════════════════════╗
║        𝐌𝐘 𝐒𝐄𝐒𝐒𝐈𝐎𝐍𝐒     
╚══════════════════════════╝

{chr(10).join(session_list)}

✧ عدد الجلسات ↤ {len(sessions)}
""", "script")
    await e.reply(text)

@bot.on(events.NewMessage(pattern="/stop_session (\\d+)"))
async def stop_session(e):
    user_id = e.sender_id
    if user_id in banned_users:
        await e.reply(fancy_text("تم حظرك من البوت", "script"))
        return
    if user_id not in allowed_users and user_id != OWNER_ID:
        return
    try:
        session_index = int(e.pattern_match.group(1)) - 1
        sessions = user_clients.get(user_id, [])
        if 0 <= session_index < len(sessions):
            session = sessions[session_index]
            await session.stop()
            sessions.pop(session_index)
            await e.reply(fancy_text("✧ تم إيقاف الجلسة", "script"))
        else:
            await e.reply(fancy_text("✧ رقم الجلسة غلط", "script"))
    except:
        await e.reply(fancy_text(" حصلت مشكلة", "script"))

@bot.on(events.NewMessage(pattern="/delsession"))
async def delsession_command(e):
    user_id = e.sender_id
    if user_id in banned_users:
        await e.reply(fancy_text("تم حظرك من البوت", "script"))
        return
    if user_id not in allowed_users and user_id != OWNER_ID:
        return
    sessions = user_clients.get(user_id, [])
    if not sessions:
        await e.reply(fancy_text("✧ مافي جلسات لحذفها", "script"))
        return
    buttons = []
    for i, session in enumerate(sessions):
        try:
            me = await session.get_me_safe()
            name = me.first_name if me else f"جلسة {i+1}"
        except:
            name = f"جلسة {i+1}"
        buttons.append([Button.inline(fancy_button_text(f"🗑 حذف {name}"), f"del_session_{i}")])
    buttons.append([Button.inline(fancy_button_text("❌ الغاء"), "cancel_del")])
    await e.reply(fancy_text("""
╔══════════════════════════╗
║      𝐃𝐄𝐋𝐄𝐓𝐄 𝐒𝐄𝐒𝐒𝐈𝐎𝐍    
╚══════════════════════════╝

✧ اختر الجلسة التي تبي تحذفها من الجذور
✧ سيتم إيقاف الوهمي اونلاين والساعة وكل المهام وقطع الاتصال
""", "script"), buttons=buttons)

@bot.on(events.NewMessage)
async def handle_session_messages(e):
    user_id = e.sender_id
    if user_id in waiting_sessions:
        session_string = e.raw_text.strip()
        waiting_sessions.pop(user_id)
        try:
            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            await client.connect()
            me = await client.get_me()
            session_key = str(uuid.uuid4())
            user_session = UserbotSession(client, user_id, session_key)
            all_clients.append(user_session)
            if user_id not in user_clients:
                user_clients[user_id] = []
            user_clients[user_id].append(user_session)
            await e.reply(fancy_text(f"""
╔══════════════════════════╗
║        𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐀𝐃𝐃𝐄𝐃     
╚══════════════════════════╝

✧ تم تشغيل الجلسه بنجاح
✧ الحساب ↤ {me.first_name}

✧ عشان تشوف الجلسات اكتب /sessions
""", "script"))
        except Exception as ex:
            await e.reply(fancy_text(f"✧ حصلت مشكلة : {str(ex)}", "script"))

@bot.on(events.NewMessage)
async def handle_phone_login(e):
    user_id = e.sender_id
    text = e.raw_text.strip()
    if user_id in waiting_phone:
        phone = text
        waiting_phone.pop(user_id)
        try:
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            sent = await client.send_code_request(phone)
            phone_clients[user_id] = {
                "client": client,
                "phone": phone,
                "phone_code_hash": sent.phone_code_hash
            }
            waiting_code[user_id] = True
            await e.reply(fancy_text("""
╔══════════════════════════╗
║        𝐋𝐎𝐆𝐈𝐍 𝐂𝐎𝐃𝐄      
╚══════════════════════════╝

✧ تم ارسال كود التحقق
✧ ارسل الكود اللي وصلك
""", "script"))
        except Exception as ex:
            await e.reply(fancy_text(f"✧ خطأ : {str(ex)}", "script"))
    elif user_id in waiting_code:
        code = text
        waiting_code.pop(user_id)
        client_data = phone_clients.get(user_id)
        if not client_data:
            await e.reply(fancy_text("✧ حصلت مشكلة", "script"))
            return
        client = client_data["client"]
        phone = client_data["phone"]
        phone_code_hash = client_data["phone_code_hash"]
        try:
            await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
            me = await client.get_me()
            session_key = str(uuid.uuid4())
            user_session = UserbotSession(client, user_id, session_key)
            user_session.source_enabled = True
            all_clients.append(user_session)
            if user_id not in user_clients:
                user_clients[user_id] = []
            user_clients[user_id].append(user_session)
            if user_id in phone_clients:
                del phone_clients[user_id]
            await e.reply(fancy_text(f"""
╔══════════════════════════╗
║        𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐀𝐃𝐃𝐄𝐃     
╚══════════════════════════╝

✧ تم تسجيل الدخول بنجاح
✧ الحساب ↤ {me.first_name}

✧ عشان تشوف الجلسات اكتب /sessions
""", "script"))
        except Exception as ex:
            err_str = str(ex)
            if "SessionPasswordNeededError" in err_str or "password" in err_str.lower():
                waiting_2fa[user_id] = True
                await e.reply(fancy_text("""
╔══════════════════════════╗
║       𝐓𝐖𝐎 𝐅𝐀𝐂𝐓𝐎𝐑 𝐀𝐔𝐓𝐇   
╚══════════════════════════╝

✧ حسابك يحتاج كلمة مرور التحقق الثنائي
✧ ارسل كلمة المرور
""", "script"))
            else:
                if user_id in phone_clients:
                    del phone_clients[user_id]
                await e.reply(fancy_text(f"✧ خطأ : {err_str}", "script"))
    elif user_id in waiting_2fa:
        password = text
        waiting_2fa.pop(user_id)
        client_data = phone_clients.get(user_id)
        if not client_data:
            await e.reply(fancy_text("✧ حصلت مشكلة", "script"))
            return
        client = client_data["client"]
        try:
            await client.sign_in(password=password)
            me = await client.get_me()
            session_key = str(uuid.uuid4())
            user_session = UserbotSession(client, user_id, session_key)
            user_session.source_enabled = True
            all_clients.append(user_session)
            if user_id not in user_clients:
                user_clients[user_id] = []
            user_clients[user_id].append(user_session)
            if user_id in phone_clients:
                del phone_clients[user_id]
            await e.reply(fancy_text(f"""
╔══════════════════════════╗
║        𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐀𝐃𝐃𝐄𝐃     
╚══════════════════════════╝

✧ تم تسجيل الدخول بنجاح
✧ الحساب ↤ {me.first_name}

✧ عشان تشوف الجلسات اكتب /sessions
""", "script"))
        except Exception as ex:
            if user_id in phone_clients:
                del phone_clients[user_id]
            await e.reply(fancy_text(f"✧ كلمة المرور غلط : {str(ex)}", "script"))

@bot.on(events.NewMessage)
async def handle_admin_requests(e):
    user_id = e.sender_id
    if user_id in waiting_user_add:
        try:
            target_user_id = int(e.raw_text.strip())
            allowed_users.add(target_user_id)
            waiting_user_add.remove(user_id)
            await e.reply(fancy_text(f"""
╔══════════════════════════╗
║          𝐔𝐒𝐄𝐑 𝐀𝐃𝐃𝐄𝐃      
╚══════════════════════════╝

✧ تم اضافة المستخدم {target_user_id} بنجاح
""", "script"))
        except:
            await e.reply(fancy_text("✧ ايدي غلط", "script"))
    elif user_id in waiting_user_ban:
        try:
            target_user_id = int(e.raw_text.strip())
            banned_users.add(target_user_id)
            waiting_user_ban.remove(user_id)
            await e.reply(fancy_text(f"""
╔══════════════════════════╗
║          𝐔𝐒𝐄𝐑 𝐁𝐀𝐍𝐍𝐄𝐃     
╚══════════════════════════╝

✧ تم حظر المستخدم {target_user_id} بنجاح
""", "script"))
        except:
            await e.reply(fancy_text("✧ ايدي غلط", "script"))
    elif user_id in waiting_user_unban:
        try:
            target_user_id = int(e.raw_text.strip())
            if target_user_id in banned_users:
                banned_users.remove(target_user_id)
            waiting_user_unban.remove(user_id)
            await e.reply(fancy_text(f"""
╔══════════════════════════╗
║        𝐔𝐒𝐄𝐑 𝐔𝐍𝐁𝐀𝐍𝐍𝐄𝐃     
╚══════════════════════════╝

✧ تم الغاء حظر المستخدم {target_user_id} بنجاح
""", "script"))
        except:
            await e.reply(fancy_text("✧ ايدي غلط", "script"))

@bot.on(events.CallbackQuery)
async def callback_handler(e):
    user_id = e.sender_id
    data = e.data.decode('utf-8')
    if data == "addsession":
        if user_id != OWNER_ID and user_id not in allowed_users:
            await e.answer("غير مسموح", alert=True)
            return
        waiting_sessions[user_id] = True
        await e.edit(fancy_text("""
╔══════════════════════════╗
║        𝐀𝐃𝐃 𝐒𝐄𝐒𝐒𝐈𝐎𝐍      
╚══════════════════════════╝

✧ ارسل سترنج الجلسه 
""", "script"))
    elif data == "adduser":
        if user_id != OWNER_ID:
            await e.answer("متاح فقط للمطور", alert=True)
            return
        waiting_user_add.add(user_id)
        await e.edit(fancy_text("""
╔══════════════════════════╗
║        𝐀𝐃𝐃 𝐔𝐒𝐄𝐑        
╚══════════════════════════╝

✧ ارسل ايدي المستخدم لتفعيله
""", "script"))
    elif data == "banuser":
        if user_id != OWNER_ID:
            await e.answer("متاح فقط للمطور", alert=True)
            return
        waiting_user_ban.add(user_id)
        await e.edit(fancy_text("""
╔══════════════════════════╗
║        𝐁𝐀𝐍 𝐔𝐒𝐄𝐑        
╚══════════════════════════╝

✧ ارسل ايدي المستخدم لحظره
""", "script"))
    elif data == "unbanuser":
        if user_id != OWNER_ID:
            await e.answer("متاح فقط للمطور", alert=True)
            return
        waiting_user_unban.add(user_id)
        await e.edit(fancy_text("""
╔══════════════════════════╗
║       𝐔𝐍𝐁𝐀𝐍 𝐔𝐒𝐄𝐑      
╚══════════════════════════╝

✧ ارسل ايدي المستخدم لفك الحظر
""", "script"))
    elif data.startswith("acc_"):
        if user_id != OWNER_ID:
            await e.answer("متاح فقط للمطور", alert=True)
            return
        target_user = int(data.split("_")[1])
        allowed_users.add(target_user)
        if target_user in pending_requests:
            del pending_requests[target_user]
        await e.edit(fancy_text(f"""
╔══════════════════════════╗
║        𝐀𝐂𝐂𝐄𝐏𝐓𝐄𝐃       
╚══════════════════════════╝

✧ تم تفعيل المستخدم {target_user}
""", "script"))
        try:
            await bot.send_message(target_user, fancy_text("""
╔══════════════════════════╗
║          𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅     
╚══════════════════════════╝

✧ تم تفعيل حسابك
✧ استخدم /start لتشغيل البوت
""", "script"))
        except:
            pass
    elif data.startswith("rej_"):
        if user_id != OWNER_ID:
            await e.answer("متاح فقط للمطور", alert=True)
            return
        target_user = int(data.split("_")[1])
        if target_user in pending_requests:
            del pending_requests[target_user]
        await e.edit(fancy_text(f"""
╔══════════════════════════╗
║        𝐑𝐄𝐉𝐄𝐂𝐓𝐄𝐃       
╚══════════════════════════╝

✧ تم رفض المستخدم {target_user}
""", "script"))
        try:
            await bot.send_message(target_user, fancy_text("""
╔══════════════════════════╗
║          𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐒𝐇𝐑𝐀𝐅     
╚══════════════════════════╝

✧ تم رفض طلبك       
✧ لمراسله المطور @C_GGV
""", "script"))
        except:
            pass
    elif data == "copy_source":
        await e.answer("تم النسخ", alert=True)
        await e.edit("```\n@esraf4\n```")
    elif data == "copy_channel":
        await e.answer("تم النسخ", alert=True)
        await e.edit("```\nhttps://t.me/esraf4\n```")
    elif data == "copy_bot":
        await e.answer("تم النسخ", alert=True)
        await e.edit("```\n@TelethonByKevobot\n```")
    elif data == "copy_dev":
        await e.answer("تم النسخ", alert=True)
        await e.edit("```\n@C_GGV\n```")
    elif data == "enable_source":
        if user_id != OWNER_ID and user_id not in allowed_users:
            await e.answer("غير مسموح", alert=True)
            return
        sessions = user_clients.get(user_id, [])
        if not sessions:
            await e.answer("مافي جلسات مضافه", alert=True)
            return
        for session in sessions:
            session.source_enabled = True
        await e.edit(fancy_text("""
╔══════════════════════════╗
║       𝐒𝐎𝐔𝐑𝐂𝐄 𝐄𝐍𝐀𝐁𝐋𝐄𝐃    
╚══════════════════════════╝

✧ تم تفعيل السورس
✧ كل الاوامر تعمل الان
""", "script"))
    elif data == "disable_source":
        if user_id != OWNER_ID and user_id not in allowed_users:
            await e.answer("غير مسموح", alert=True)
            return
        sessions = user_clients.get(user_id, [])
        if not sessions:
            await e.answer("مافي جلسات مضافه", alert=True)
            return
        for session in sessions:
            session.source_enabled = False
        await e.edit(fancy_text("""
╔══════════════════════════╗
║       𝐒𝐎𝐔𝐑𝐂𝐄 𝐃𝐈𝐒𝐀𝐁𝐋𝐄𝐃   
╚══════════════════════════╝

✧ تم تعطيل السورس
✧ الاوامر موقوفه
✧ اضغط تفعيل السورس لتشغيلها مره اخرى
""", "script"))
    elif data == "login_phone":
        if user_id != OWNER_ID and user_id not in allowed_users:
            await e.answer("غير مسموح", alert=True)
            return
        waiting_phone[user_id] = True
        await e.edit(fancy_text("""
╔══════════════════════════╗
║       𝐋𝐎𝐆𝐈𝐍 𝐁𝐘 𝐏𝐇𝐎𝐍𝐄    
╚══════════════════════════╝

✧ ارسل رقم الهاتف مع الكود الدولي
✧ مثال: +9665xxxxxxxx
""", "script"))
    elif data.startswith("del_session_"):
        if user_id != OWNER_ID and user_id not in allowed_users:
            await e.answer("غير مسموح", alert=True)
            return
        try:
            session_index = int(data.split("del_session_")[1])
            sessions = user_clients.get(user_id, [])
            if 0 <= session_index < len(sessions):
                session = sessions[session_index]
                try:
                    me = await session.get_me_safe()
                    acc_name = me.first_name if me else "الحساب"
                except:
                    acc_name = "الحساب"
                await session.stop()
                sessions.pop(session_index)
                if session in all_clients:
                    all_clients.remove(session)
                await e.edit(fancy_text(f"""
╔══════════════════════════╗
║      𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐃𝐄𝐋𝐄𝐓𝐄𝐃   
╚══════════════════════════╝

✧ تم حذف جلسة ↤ {acc_name} من الجذور
✧ تم إيقاف الوهمي اونلاين والساعة وكل المهام
✧ تم قطع الاتصال نهائياً
""", "script"))
            else:
                await e.answer("رقم الجلسة غلط", alert=True)
        except Exception as ex:
            await e.answer(f"خطأ: {str(ex)}", alert=True)
    elif data == "cancel_del":
        await e.edit(fancy_text("""
╔══════════════════════════╗
║          𝐂𝐀𝐍𝐂𝐄𝐋𝐋𝐄𝐃     
╚══════════════════════════╝

✧ تم الغاء الحذف
""", "script"))

print("تم تشغيل البوت بنجاح")
print("𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑 : @C_GGV")
print("Telethon By esraf")
bot.run_until_disconnected()