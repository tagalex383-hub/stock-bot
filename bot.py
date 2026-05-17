from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8601537948:AAGM0xHurRn1wsSO0_2agA2sAuyix_JsKcg"

# =========================
# تحليل احترافي خفيف
# =========================
def analyze(open_price, high, low, close):

    # =========================
    # Pivot Point
    # =========================
    pivot = (high + low + close) / 3

    # Supports & Resistance
    s1 = (2 * pivot) - high
    r1 = (2 * pivot) - low

    # =========================
    # الاتجاه
    # =========================
    trend = "📈 صاعد" if close > pivot else "📉 هابط"

    # =========================
    # RSI مبسط
    # =========================
    movement = close - open_price

    if movement > 0.03:
        rsi = 70
    elif movement < -0.03:
        rsi = 30
    else:
        rsi = 50

    # =========================
    # MACD مبسط
    # =========================
    macd = "📈 إيجابي" if close > open_price else "📉 سلبي"

    # =========================
    # إشارة التداول
    # =========================
    if close > pivot and rsi < 70:
        signal = "🟢 BUY"
    elif close < pivot:
        signal = "🔴 SELL"
    else:
        signal = "🟡 WAIT"

    # =========================
    # نقطة الدخول
    # =========================
    entry = pivot

    # =========================
    # وقف الخسارة
    # =========================
    stop_loss = low - 0.02

    # =========================
    # الأهداف
    # =========================
    target1 = r1
    target2 = r1 + 0.03
    target3 = r1 + 0.05

    # =========================
    # نقطة الخروج
    # =========================
    exit_point = target1

    # =========================
    # متوسط السعر
    # =========================
    average_price = (high + low + close) / 3

    # =========================
    # Risk / Reward
    # =========================
    risk = abs(entry - stop_loss)
    reward = abs(target1 - entry)

    if risk != 0:
        rr = reward / risk
    else:
        rr = 0

    # =========================
    # تقييم الصفقة
    # =========================
    if rr >= 2:
        rating = "🔥 ممتازة"
    elif rr >= 1:
        rating = "✅ جيدة"
    else:
        rating = "⚠ ضعيفة"

    # =========================
    # قوة الحركة
    # =========================
    strength = abs(high - low)

    if strength > 0.10:
        strength_text = "🔥 قوية"
    else:
        strength_text = "⚡ متوسطة"

    # =========================
    # النتيجة النهائية
    # =========================
    return f"""
📊 EGX ULTIMATE ANALYSIS

💰 Open: {open_price}
📈 High: {high}
📉 Low: {low}
🔚 Close: {close}

🔵 Pivot: {pivot:.2f}

📉 Support S1: {s1:.2f}
📈 Resistance R1: {r1:.2f}

📊 Trend: {trend}
🔥 Strength: {strength_text}

📈 RSI: {rsi}
📊 MACD: {macd}

🎯 Signal: {signal}

🟢 Entry Point: {entry:.2f}

🛑 Stop Loss: {stop_loss:.2f}

🎯 Target 1: {target1:.2f}
🚀 Target 2: {target2:.2f}
🚀 Target 3: {target3:.2f}

🔚 Exit Point: {exit_point:.2f}

📈 Average Price: {average_price:.2f}

⚖ Risk/Reward: 1:{rr:.2f}

🏆 Trade Rating: {rating}
"""


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📊 تحليل سهم", callback_data="analysis")],
        [InlineKeyboardButton("📚 شرح المؤشرات", callback_data="learn")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "⚡ EGX ULTIMATE BOT\nاختر:",
        reply_markup=reply_markup
    )


# =========================
# BUTTON HANDLER
# =========================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "analysis":

        await query.message.reply_text(
            "✍️ اكتب البيانات بهذا الشكل:\n\n"
            "Open High Low Close\n\n"
            "مثال:\n"
            "1.93 1.94 1.89 1.91"
        )

    elif query.data == "learn":

        await query.message.reply_text(
            "📚 شرح سريع:\n\n"
            "🔵 Pivot = نقطة ارتكاز\n"
            "📉 S1 = دعم\n"
            "📈 R1 = مقاومة\n"
            "🟢 BUY = شراء\n"
            "🔴 SELL = بيع\n"
            "🛑 Stop Loss = وقف خسارة"
        )


# =========================
# استقبال البيانات
# =========================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    try:

        values = text.split()

        if len(values) != 4:
            raise ValueError

        open_price = float(values[0])
        high = float(values[1])
        low = float(values[2])
        close = float(values[3])

        result = analyze(open_price, high, low, close)

        await update.message.reply_text(result)

    except:

        await update.message.reply_text(
            "❌ صيغة خاطئة\n\n"
            "اكتب:\n"
            "Open High Low Close"
        )


# =========================
# تشغيل البوت
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("⚡ EGX ULTIMATE BOT RUNNING")

app.run_polling()
