import streamlit as st
import time
import requests
import yfinance as yf
from bs4 import BeautifulSoup

# إعدادات الصفحة الخارجية
st.set_page_config(page_title="لوحة مراقبة الذهب", layout="wide")

# سطر برمجي لفرض التنسيق العربي الصحيح من اليمين إلى اليسار (RTL)
st.markdown(
    """
    <style>
    .stApp {
        direction: RTL;
        text-align: right;
    }
    .stMetric {
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>⚡ منظومة المراقبة والمضاربة اللحظية للذهب (نسخة سوريا)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>تحليل تلقائي متجدد لتدفقات السيولة والأخبار الأساسية</p>", unsafe_allow_html=True)

def get_market_data():
    try:
        tickers = {
            "Gold": "GC=F",
            "DXY": "DX-Y.NYB",
            "US10Y": "^TNX",
            "NVDA": "NVDA"
        }
        data = {}
        for name, ticker in tickers.items():
            t = yf.Ticker(ticker)
            data[name] = t.history(period="1d")['Close'].iloc[-1]
        return data
    except:
        return None

def get_crypto_panic_index():
    try:
        url = "https://alternative.me"
        response = requests.get(url).json()
        return response['data']['value'], response['data']['value_classification']
    except:
        return "50", "Neutral"

def get_breaking_news_rss():
    try:
        url = "https://reutersagency.com"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        articles = []
        items = soup.find_all('item')
        for item in items[:5]:
            articles.append(item.title.text)
        return articles
    except:
        return ["تعذر الاتصال بخلاصة الأخبار الفورية حالياً"]

market = get_market_data()
news = get_breaking_news_rss()
panic_val, panic_status = get_crypto_panic_index()

if market:
    danger_words = ["margin call", "rate hike", "liquidation", "debt crisis", "fed hawkish", "france"]
    margin_risk_detected = any(any(word in title.lower() for word in danger_words) for title in news)
    
    # تحديد القرار المضاربي ميكانيكياً
    if market['DXY'] > 105 and market['Gold'] < 4000:
        if margin_risk_detected:
            decision_text = "❌ إشارة: نداءات هامش نشطة (Margin Calls)! الدولار يلتهم السيولة. انتظر قاع 3,950$ ولا تشتري الآن."
            decision_color = "#FF4B4B"
        else:
            decision_text = "⚠️ إشارة: الذهب تحت الـ 4000$ والدولار مرتفع، ترقب سلوك السعر عند الدعم الحالي."
            decision_color = "#FFA500"
    elif market['DXY'] < 104 and market['Gold'] >= 3950:
        decision_text = "🟢 إشارة شراء: انحسار موجة الذعر وهبوط الدولار. فرصة ارتداد مضاربي صاعد قوية للذهب."
        decision_color = "#00D26A"
    else:
        decision_text = "🔵 إشارة: الأسواق مستقرة نسبياً في نطاق عرضي بانتظار قرار الفيدرالي يوم الأربعاء."
        decision_color = "#0080FF"

    # عرض الأسعار في كروت منسقة متوافقة مع اليمين
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="✨ الذهب الفوري", value=f"{market['Gold']:.2f} $")
    col2.metric(label="💵 مؤشر الدولار (DXY)", value=f"{market['DXY']:.2f}")
    col3.metric(label="📈 سندات أمريكا 10Y", value=f"{market['US10Y']:.2f} %")
    col4.metric(label="🤖 سهم نفيديا AI", value=f"{market['NVDA']:.2f} $")
    col5.metric(label="😨 مؤشر ذعر الأسواق", value=f"{panic_val} ({panic_status})")
    
    st.markdown("---")
    st.markdown(f"<div style='background-color:{decision_color}; padding:15px; border-radius:10px; text-align:center; color:white; font-size:20px; font-weight:bold; direction: rtl;'>{decision_text}</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("📰 آخر العواجل الاقتصادية من رويترز:")
    for title in news:
        st.markdown(f"• {title}")
        
    st.caption(f"آخر تحديث تلقائي: {time.strftime('%H:%M:%S')}")

time.sleep(30)
st.rerun()
