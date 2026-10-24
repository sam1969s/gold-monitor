import streamlit as st
import time
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime

# إعدادات الصفحة الخارجية
st.set_page_config(page_title="منظومة مراقبة الذهب الاحترافية", layout="wide")

# فرض التنسيق العربي الصحيح (RTL)
st.markdown(
    """
    <style>
    .stApp { direction: RTL; text-align: right; }
    .stMetric { text-align: right; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>⚡ منظومة المراقبة والتحليل الثلاثي للذهب</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>نظام فلترة الفترات الثابتة مع حماية ميكانيكية ضد الطوارئ والعواجل المفاجئة</p>", unsafe_allow_html=True)

def get_market_data():
    try:
        tickers = {"Gold": "GC=F", "DXY": "DX-Y.NYB", "US10Y": "^TNX", "NVDA": "NVDA"}
        data = {}
        for name, ticker in tickers.items():
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            data[name] = hist['Close'].iloc[-1]
            if name == "Gold":
                data["Gold_High"] = hist['High'].iloc[-1]
                data["Gold_Low"] = hist['Low'].iloc[-1]
                data["Gold_Open"] = hist['Open'].iloc[-1]
        return data
    except:
        return None

def get_breaking_news_rss():
    try:
        url = "https://reutersagency.com"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        articles = []
        for item in soup.find_all('item')[:5]:
            articles.append(item.title.text)
        return articles
    except:
        return ["تعذر الاتصال بخلاصة الأخبار الفورية حالياً"]

market = get_market_data()
news = get_breaking_news_rss()

if market:
    # 1. نظام رصد الطوارئ التلقائي (Emergency Circuit Breaker)
    danger_words = ["margin call", "rate hike", "liquidation", "debt crisis", "fed hawkish", "france"]
    emergency_news_detected = any(any(word in title.lower() for word in danger_words) for title in news)
    
    # قياس التذبذب اللحظي العنيف (إذا تحرك السعر بأكثر من 15$ عن الافتتاح)
    price_deviation = abs(market['Gold'] - market['Gold_Open'])
    volatile_emergency = price_deviation > 15.0
    
    is_emergency = emergency_news_detected or volatile_emergency

    # عرض الأسعار الرئيسية في كروت علوية
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="✨ الذهب الفوري", value=f"{market['Gold']:.2f} $")
    col2.metric(label="💵 مؤشر الدولار (DXY)", value=f"{market['DXY']:.2f}")
    col3.metric(label="📈 سندات أمريكا 10Y", value=f"{market['US10Y']:.2f} %")
    col4.metric(label="🤖 سهم نفيديا AI", value=f"{market['NVDA']:.2f} $")
    
    st.markdown("---")

    # 2. تفعيل وضع الطوارئ أو إدارة الفترات
    if is_emergency:
        st.markdown(
            f"<div style='background-color:#FF4B4B; padding:15px; border-radius:10px; text-align:center; color:white; font-size:22px; font-weight:bold; direction: rtl;'>"
            f"🚨 تفعيل وضع كسر الحماية الطارئ! تذبذب حاد أو عواجل تسييل نشطة الآن. تجميد الفترات العادية والتحول للمراقبة اللحظية.<br>"
            f"تكتيك مضاربي عاجل: ترقب سلوك السعر حول مستويات الاستسلام البيعي عند القاع التاريخي 3,950$ إلى 3,942$. لا تندفع بالشراء."
            f"</div>", 
            unsafe_allow_html=True
        )
    else:
        # حساب مستويات الدعم والمقاومة اليومية الثابتة للفترات
        pivot = (market['Gold_High'] + market['Gold_Low'] + market['Gold']) / 3
        r1, s1 = (2 * pivot) - market['Gold_Low'], (2 * pivot) - market['Gold_High']
        r2, s2 = pivot + (market['Gold_High'] - market['Gold_Low']), pivot - (market['Gold_High'] - market['Gold_Low'])

        # عرض التبويبات الثلاثة المعتمدة بناءً على ساعات دمشق
        current_hour = datetime.now().hour
        
        tab1, tab2, tab3 = st.tabs(["🕒 التحليل الصباحي (الأوروبي)", "🌤️ منتصف اليوم (الأمريكي)", "🌌 التحليل المسائي (الإغلاق)"])
        
        with tab1:
            st.markdown("### 📋 تقرير الفترة الصباحية (ثابت)")
            st.write(f"**نقطة الارتكاز المحورية لليوم:** {pivot:.2f} $")
            st.write(f"**كمين الشراء الصباحي المقترح (الدعم الأول S1):** {s1:.2f} $")
            st.write(f"**مستهدف البيع الصباحي (المقاومة الأولى R1):** {r1:.2f} $")
            if current_hour >= 9 and current_hour < 15:
                st.info("💡 هذه الفترة نشطة حالياً بناءً على توقيت الجلسة الأوروبية.")

        with tab2:
            st.markdown("### 📋 تقرير فترة منتصف اليوم (دخول سيولة نيويورك والـ AI)")
            st.write(f"**نطاق حماية الجلسة الأمريكية (الدعم الثاني S2):** {s2:.2f} $")
            st.write(f"**أقصى مستهدف صاعد متوقع للجلسة (المقاومة الثانية R2):** {r2:.2f} $")
            if current_hour >= 15 and current_hour < 21:
                st.info("💡 هذه الفترة نشطة حالياً. تدفق سيولة أمريكية مكثف في السوق.")

        with tab3:
            st.markdown("### 📋 التقييم المسائي وإغلاق المحافظ")
            if market['Gold'] > 4000:
                st.success("🟢 الذهب أغلق فوق الدعم النفسي 4000$. مؤشر أمان نسبي للاحتفاظ بالمراكز الفورية بدون رافعة.")
            else:
                st.warning("⚠️ الذهب تحت مستويات الـ 4000$. يفضل تسييل جزء من العقود المضاربية كاش لتجنب فجوات الصباح.")
            if current_hour >= 21 or current_hour < 9:
                st.info("💡 الأسواق في مرحلة التقييم المسائي والاستعداد لجلسة الغد.")

    st.markdown("---")
    
    # عرض الأخبار العاجلة بالأسفل كمرجع دائم
    st.subheader("📰 خلاصة عواجل رويترز الاقتصادية لليوم:")
    for title in news:
        if any(word in title.lower() for word in danger_words):
            st.markdown(f"• <span style='color:#FF4B4B; font-weight:bold;'>[حرج] {title}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"• {title}")
            
    st.caption(f"آخر تحديث تلقائي آمن للموقع: {time.strftime('%H:%M:%S')}")

time.sleep(30)
st.rerun()
