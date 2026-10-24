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

st.markdown("<h1 style='text-align: center; color: #FFD700;'>⚡ منظومة المراقبة والتحليل الثلاثي المطور للذهب</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>النسخة المضبوطة هندسياً: فلترة الفترات الثابتة المستقلة مع فحص الأخبار الفردية بالذكاء الاصطناعي</p>", unsafe_allow_html=True)

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

def analyze_single_news_with_ai(title):
    """
    تحليل كل خبر بمفرده وبشكل مستقل لتحديد تصنيفه الدقيق بدون دمج أو خلط
    """
    api_url = "https://huggingface.co"
    candidate_labels = ["financial panic or interest rates", "war or geopolitical conflict", "inflation or economic debt crisis", "normal business news"]
    payload = {"inputs": title, "parameters": {"candidate_labels": candidate_labels}}
    try:
        response = requests.post(api_url, json=payload, timeout=4)
        result = response.json()
        top_label = result['labels'][0]
        top_score = result['scores'][0]
        
        if top_score > 0.45:
            if top_label == "financial panic or interest rates": return "financial"
            elif top_label == "war or geopolitical conflict": return "geopolitical"
            elif top_label == "inflation or economic debt crisis": return "macro"
        return "normal"
    except:
        return "normal"

market = get_market_data()
news = get_breaking_news_rss()

if market:
    # قياس التذبذب السعري الحاد المفاجئ (حارس الأمان الميكانيكي على الشارت)
    price_deviation = abs(market['Gold'] - market['Gold_Open'])
    volatile_emergency = price_deviation > 15.0

    # 1. عرض الأسعار اللحظية للأصول الحاكمة للسيولة دائماً في الأعلى
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="✨ الذهب الفوري", value=f"{market['Gold']:.2f} $")
    col2.metric(label="💵 مؤشر الدولار (DXY)", value=f"{market['DXY']:.2f}")
    col3.metric(label="📈 سندات أمريكا 10Y", value=f"{market['US10Y']:.2f} %")
    col4.metric(label="🤖 سهم نفيديا AI", value=f"{market['NVDA']:.2f} $")
    
    st.markdown("---")

    # 2. يافطة كسر الحماية الطارئ (تشتعل فقط وفقط إذا تحرك السعر بعنف على الشارت)
    if volatile_emergency:
        st.markdown(
            f"<div style='background-color:#FF4B4B; padding:15px; border-radius:10px; text-align:center; color:white; font-size:18px; font-weight:bold; direction: rtl; margin-bottom:20px;'>"
            f"🚨 تنبيه تذبذب حاد! الذهب يتحرك بنطاق يتجاوز 15$ حالياً. يرجى توخي الحذر الصارم في العقود اللحظية وتجنب الملاحقة العاطفية السعرية."
            f"</div>", unsafe_allow_html=True
        )

    # 3. عرض الفترات الثلاث الثابتة (مستقلة تماماً وتظهر بشكل دائم ومستمر)
    pivot = (market['Gold_High'] + market['Gold_Low'] + market['Gold']) / 3
    r1, s1 = (2 * pivot) - market['Gold_Low'], (2 * pivot) - market['Gold_High']
    r2, s2 = pivot + (market['Gold_High'] - market['Gold_Low']), pivot - (market['Gold_High'] - market['Gold_Low'])
    current_hour = datetime.now().hour
    
    tab1, tab2, tab3 = st.tabs(["🕒 التحليل الصباحي (الأوروبي)", "🌤️ منتصف اليوم (الأمريكي)", "🌌 التحليل المسائي (الإغلاق)"])
    
    with tab1:
        st.markdown("### 📋 تقرير الفترة الصباحية الثابت")
        st.write(f"**نقطة الارتكاز المحورية الحالية لليوم:** {pivot:.2f} $")
        st.write(f"**كمين الشراء الصباحي المقترح (الدعم الأول S1):** {s1:.2f} $")
        st.write(f"**مستهدف جني الأرباح الصباحي (المقاومة الأولى R1):** {r1:.2f} $")

    with tab2:
        st.markdown("### 📋 تقرير فترة منتصف اليوم (سيولة نيويورك والـ AI)")
        st.write(f"**نطاق حماية الجلسة الأمريكية العميق (الدعم الثاني S2):** {s2:.2f} $")
        st.write(f"**أقصى مستهدف صاعد متوقع للجلسة (المقاومة الثانية R2):** {r2:.2f} $")

    with tab3:
        st.markdown("### 📋 التقييم المسائي وإغلاق المحافظ")
        if market['Gold'] > 4000:
            st.success("🟢 الذهب مستقر فوق الدعم النفسي 4000$. إشارة أمان نسبي للاحتفاظ بالمراكز الفورية.")
        else:
            st.warning("⚠️ الذهب تحت مستويات 4000$. يفضل تسييل جزء من المراكز لتجنب فجوات الصباح.")

    st.markdown("---")
    
    # 4. خلاصة الأخبار مع الفحص الفردي الملون بالذكاء الاصطناعي لكل خبر على حدة
    st.subheader("📰 رادار عواجل رويترز المصفى بالذكاء الاصطناعي اللحظي:")
    
    for title in news:
        if title == "تعذر الاتصال بخلاصة الأخبار الفورية حالياً":
            st.markdown(f"• {title}")
            continue
            
        # فحص الخبر الحالي بمفرده لمعرفة تصنيفه
        single_analysis = analyze_single_news_with_ai(title)
        
        if single_analysis == "financial":
            st.markdown(f"• <span style='color:#FF4B4B; font-weight:bold;'>[خطر مالي/فائدة]</span> {title}", unsafe_allow_html=True)
        elif single_analysis == "geopolitical":
            st.markdown(f"• <span style='color:#FF8C00; font-weight:bold;'>[خطر جيوسياسي/حرب]</span> {title}", unsafe_allow_html=True)
        elif single_analysis == "macro":
            st.markdown(f"• <span style='color:#FFD700; background-color:#333; padding:1px 4px; border-radius:3px; font-weight:bold;'>[خطر اقتصادي/ديون]</span> {title}", unsafe_allow_html=True)
        else:
            st.markdown(f"• <span style='color:#888;'>[أخبار شركات عامة]</span> {title}", unsafe_allow_html=True)
            
    st.caption(f"آخر تحديث ميكانيكي مضبوط للموقع: {time.strftime('%H:%M:%S')}")

time.sleep(30)
st.rerun()
