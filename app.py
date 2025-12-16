import streamlit as st
from groq import Groq
import json
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AWKUM Lost & Found",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend Configuration - Secure API Key Loading
GROQ_API_KEY = None

# Try to load from Streamlit secrets (for cloud deployment)
try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
except:
    pass

# If not in secrets, try environment variable (for local development)
if not GROQ_API_KEY:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Initialize Groq client
client = None
if GROQ_API_KEY and GROQ_API_KEY != "YOUR_GROQ_API_KEY_HERE":
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        st.sidebar.warning(f"⚠️ AI initialization failed")
        client = None
else:
    st.sidebar.info("ℹ️ AI chat disabled: Configure GROQ_API_KEY to enable")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Crimson Text', 'Times New Roman', serif !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    .main {
        background-color: #f8f9fa;
        padding: 0 !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        max-width: 1400px !important;
    }
    
    .awkum-header {
        background: linear-gradient(135deg, #800000, #a00000);
        padding: 2rem 3rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin: -1rem -1rem 0 -1rem;
    }
    
    .awkum-header h1 {
        color: white !important;
        font-size: 2.8rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .awkum-header p {
        color: #FFC72C !important;
        font-size: 1.3rem;
        margin: 0.5rem 0 0 0;
        font-weight: 600;
    }
    
    .content-wrapper {
        background: white;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    .section-title {
        color: #800000;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid #FFC72C;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #800000, #a00000) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(128,0,0,0.3) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #a00000, #c00000) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(128,0,0,0.4) !important;
    }
    
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 0.6rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #800000 !important;
        box-shadow: 0 0 0 3px rgba(128,0,0,0.1) !important;
    }
    
    .info-card {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #17a2b8;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #28a745;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #800000;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(128,0,0,0.2);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #800000, #a00000);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 15px rgba(128,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(128,0,0,0.4);
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: bold;
        color: #FFC72C;
        margin: 1rem 0;
    }
    
    .stat-label {
        font-size: 1.2rem;
        color: white;
        font-weight: 600;
    }
    
    .chat-container {
        background: white;
        border: 2px solid #FFC72C;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #800000, #a00000);
        color: white;
        margin-left: 15%;
    }
    
    .assistant-message {
        background: #f8f9fa;
        color: #333;
        border: 2px solid #e0e0e0;
        margin-right: 15%;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        background: white;
        border-top: 3px solid #FFC72C;
        margin-top: 3rem;
    }
    
    @media (max-width: 768px) {
        .stat-number {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'lost_items_db' not in st.session_state:
    st.session_state.lost_items_db = []
if 'found_items_db' not in st.session_state:
    st.session_state.found_items_db = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Database Functions
def save_data():
    data = {
        'lost': st.session_state.lost_items_db,
        'found': st.session_state.found_items_db
    }
    try:
        with open('lost_found_data.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        pass

def load_data():
    try:
        with open('lost_found_data.json', 'r') as f:
            data = json.load(f)
            st.session_state.lost_items_db = data.get('lost', [])
            st.session_state.found_items_db = data.get('found', [])
    except:
        pass

def report_lost(name, contact, category, description, location):
    item = {
        "id": len(st.session_state.lost_items_db) + 1,
        "name": name,
        "contact": contact,
        "category": category,
        "description": description,
        "location": location,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.lost_items_db.append(item)
    save_data()
    return f"✅ Report LOST-{item['id']} saved successfully!"

def report_found(name, contact, category, description, location):
    item = {
        "id": len(st.session_state.found_items_db) + 1,
        "name": name,
        "contact": contact,
        "category": category,
        "description": description,
        "location": location,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.found_items_db.append(item)
    save_data()
    return f"✅ Report FOUND-{item['id']} saved successfully!"

def search_items(query, search_type):
    db = st.session_state.lost_items_db if search_type == "Lost Items" else st.session_state.found_items_db
    if not db:
        return []
    results = []
    q = query.lower() if query else ""
    for item in db:
        if not q or q in item['description'].lower() or q in item['category'].lower() or q in item['location'].lower():
            results.append(item)
    return results

def ai_chat(message):
    if not message:
        return
    
    st.session_state.chat_history.append({"role": "user", "content": message})
    
    if client is None:
        bot_response = "⚠️ AI service is currently unavailable. Please configure your Groq API key."
    else:
        try:
            api_messages = [
                {"role": "system", "content": "You are the AWKUM Lost & Found AI Assistant. Be helpful, friendly, and concise. Location: Abdul Wali Khan University Mardan, Pakistan. Help users with lost and found queries, guide them on using the system, and provide relevant information."},
            ] + st.session_state.chat_history
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                max_tokens=300,
                temperature=0.7
            )
            bot_response = response.choices[0].message.content
        except Exception as e:
            bot_response = f"❌ I encountered an error. Please check your API key and try again."
    
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Load data
load_data()

# Header
st.markdown("""
<div class="awkum-header">
    <h1>🎓 AWKUM Lost & Found</h1>
    <p>Official AI-Powered Recovery System</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Navigation
pages = ["Home", "Report Lost", "Report Found", "Search", "Statistics", "AI Chat"]
cols = st.columns(len(pages))
for idx, page in enumerate(pages):
    with cols[idx]:
        if st.button(page, key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Main Content
if st.session_state.current_page == "Home":
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Welcome to AWKUM Lost & Found</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3 style="color: #17a2b8; margin-top: 0;">📢 Lost Something?</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Report your lost item with detailed description. Our system will help connect you with anyone who finds it.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-card">
            <h3 style="color: #28a745; margin-top: 0;">🎉 Found Something?</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Report the found item and help someone recover their belongings. Be a hero today!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Lost Items Reported</div>
            <div class="stat-number">{len(st.session_state.lost_items_db)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Found Items Reported</div>
            <div class="stat-number">{len(st.session_state.found_items_db)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "Report Lost":
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">📢 Report Lost Item</h2>', unsafe_allow_html=True)
    
    with st.form("lost_form"):
        col1, col2 = st.columns(2)
        with col1:
            l_name = st.text_input("Your Full Name *", placeholder="Enter your full name")
        with col2:
            l_contact = st.text_input("Contact Number *", placeholder="e.g., 03XX-XXXXXXX")
        
        col1, col2 = st.columns(2)
        with col1:
            l_category = st.selectbox("Item Category *", ["Mobile", "Wallet", "Keys", "Laptop", "Bag", "ID Card", "Books", "Charger", "Headphones", "Other"])
        with col2:
            l_location = st.text_input("Location Lost *", placeholder="e.g., Main Library, CS Department")
        
        l_description = st.text_area("Detailed Description *", placeholder="Provide detailed description (color, brand, model, distinctive features, etc.)", height=120)
        
        submitted = st.form_submit_button("📝 Submit Lost Report", use_container_width=True)
        
        if submitted:
            if not l_name or not l_contact or not l_description or not l_location:
                st.error("❌ Please fill all required fields!")
            else:
                result = report_lost(l_name, l_contact, l_category, l_description, l_location)
                st.success(result)
                st.balloons()
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "Report Found":
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🎉 Report Found Item</h2>', unsafe_allow_html=True)
    
    with st.form("found_form"):
        col1, col2 = st.columns(2)
        with col1:
            f_name = st.text_input("Your Full Name *", placeholder="Enter your full name")
        with col2:
            f_contact = st.text_input("Contact Number *", placeholder="e.g., 03XX-XXXXXXX")
        
        col1, col2 = st.columns(2)
        with col1:
            f_category = st.selectbox("Item Category *", ["Mobile", "Wallet", "Keys", "Laptop", "Bag", "ID Card", "Books", "Charger", "Headphones", "Other"])
        with col2:
            f_location = st.text_input("Location Found *", placeholder="e.g., Main Library, CS Department")
        
        f_description = st.text_area("Detailed Description *", placeholder="Provide detailed description (color, brand, model, distinctive features, etc.)", height=120)
        
        submitted = st.form_submit_button("📝 Submit Found Report", use_container_width=True)
        
        if submitted:
            if not f_name or not f_contact or not f_description or not f_location:
                st.error("❌ Please fill all required fields!")
            else:
                result = report_found(f_name, f_contact, f_category, f_description, f_location)
                st.success(result)
                st.balloons()
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "Search":
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🔎 Search Database</h2>', unsafe_allow_html=True)
    
    search_type = st.radio("Search In:", ["Found Items", "Lost Items"], horizontal=True)
    search_query = st.text_input("🔍 Enter keywords to search", placeholder="e.g., Wallet, iPhone, Keys, Blue Bag...")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_btn = st.button("🔍 Search Now", use_container_width=True)
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            st.rerun()
    
    if search_btn or search_query:
        results = search_items(search_query, search_type)
        
        if not results:
            st.warning("📭 No matching items found. Try different keywords or check other category.")
        else:
            st.success(f"✅ Found {len(results)} matching item(s)")
            st.markdown("<br>", unsafe_allow_html=True)
            
            for item in results:
                contact_label = "Finder Contact" if search_type == "Found Items" else "Owner Contact"
                st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h3 style="color: #800000; margin: 0 0 0.5rem 0;">🆔 ID: {item["id"]} - {item["category"]}</h3>
                            <p style="margin: 0.3rem 0;"><strong>📝 Description:</strong> {item["description"]}</p>
                            <p style="margin: 0.3rem 0;"><strong>📍 Location:</strong> {item["location"]}</p>
                            <p style="margin: 0.3rem 0;"><strong>📞 {contact_label}:</strong> {item["contact"]}</p>
                            <p style="margin: 0.3rem 0; color: #666; font-size: 0.9rem;"><strong>🕐 Reported:</strong> {item.get("timestamp", "N/A")}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "Statistics":
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">📊 System Statistics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Lost Items</div>
            <div class="stat-number">{len(st.session_state.lost_items_db)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Found Items</div>
            <div class="stat-number">{len(st.session_state.found_items_db)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total = len(st.session_state.lost_items_db) + len(st.session_state.found_items_db)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Reports</div>
            <div class="stat-number">{total}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h3 style="color: #800000; border-bottom: 2px solid #FFC72C; padding-bottom: 0.5rem;">📝 Recent Activity</h3>', unsafe_allow_html=True)
    
    all_items = []
    for item in st.session_state.lost_items_db:
        item_copy = item.copy()
        item_copy['type'] = 'Lost'
        all_items.append(item_copy)
    
    for item in st.session_state.found_items_db:
        item_copy = item.copy()
        item_copy['type'] = 'Found'
        all_items.append(item_copy)
    
    all_items.sort(key=lambda x: x.get('id', 0), reverse=True)
    
    if not all_items:
        st.info("📭 No activity yet. Be the first to report an item!")
    else:
        for item in all_items[:10]:
            icon = "📢" if item['type'] == 'Lost' else "🎉"
            st.markdown(f"""
            <div class="result-card">
                {icon} <strong>{item['type']}:</strong> {item['category']} - {item['description'][:80]}{'...' if len(item['description']) > 80 else ''}
                <span style="color: #666; font-size: 0.9rem; float: right;">🕐 {item.get('timestamp', 'N/A')}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "AI Chat":
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🤖 AI Assistant</h2>', unsafe_allow_html=True)
    
    if client is None:
        st.warning("⚠️ AI chat requires a valid Groq API key. Add GROQ_API_KEY to your environment or Streamlit secrets.")
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="assistant-message">
            <strong>🤖 Assistant:</strong> Hi! I'm your AWKUM Lost & Found AI Assistant. How can I help you today?
        </div>
        """, unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        css_class = "user-message" if msg["role"] == "user" else "assistant-message"
        label = "You" if msg["role"] == "user" else "🤖 Assistant"
        st.markdown(f"""
        <div class="chat-message {css_class}">
            <strong>{label}:</strong> {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message...", key="chat_input", label_visibility="collapsed")
    with col2:
        send_btn = st.button("Send", use_container_width=True)
    
    if send_btn and user_input:
        ai_chat(user_input)
        st.rerun()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <h3 style="color: #800000; margin-bottom: 0.5rem;">🎓 Abdul Wali Khan University Mardan</h3>
    <p style="font-size: 1.1rem; margin: 0.3rem 0;">Lost & Found Management System</p>
    <p style="font-size: 0.95rem; color: #888;">Powered by AI | Built with ❤️ for AWKUM Community</p>
</div>
""", unsafe_allow_html=True)
