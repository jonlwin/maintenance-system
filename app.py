import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Maintenance Management System", page_icon="🛠️", layout="wide")

st.title("🛠️ Department Maintenance Schedule System")
st.write("ဌာနဆိုင်ရာ ပစ္စည်းကိရိယာများနှင့် ပြုပြင်ထိန်းသိမ်းမှု အချိန်ဇယားများကို စီမံခန့်ခွဲရန် စနစ်။")

# Initialize Session State Data (Assets, Schedules, Logs)
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        ["AC-001", "Server Room Air Con 3-Ton", "Air Conditioner", "အိုင်တီဌာန", "Server Room", "2025-01-15", "Active"],
        ["GEN-001", "Office Backup Generator 50KVA", "Generator", "အုပ်ချုပ်ရေးဌာန", "Compound", "2024-06-10", "Active"],
        ["EL-001", "Main Distribution Board (MDB)", "Electrical", "အုပ်ချုပ်ရေးဌာန", "Ground Floor", "2024-01-01", "Active"]
    ], columns=["Asset_ID", "Asset_Name", "Category", "Department", "Location", "Purchase_Date", "Status"])

if 'schedules' not in st.session_state:
    st.session_state.schedules = pd.DataFrame([
        ["SCH-001", "AC-001", "Clean filter, check gas pressure", "Monthly", "2026-08-01", "2026-09-01", "အိုင်တီဌာန", "Technician Team A"],
        ["SCH-002", "GEN-001", "Change engine oil, filter", "Quarterly", "2026-06-01", "2026-09-01", "အုပ်ချုပ်ရေးဌာန", "External Vendor"],
        ["SCH-003", "EL-001", "Thermal scanning and tighten terminals", "Every 6 Months", "2026-03-01", "2026-09-01", "အုပ်ချုပ်ရေးဌာန", "Electrician"]
    ], columns=["Schedule_ID", "Asset_ID", "Task_Description", "Frequency", "Last_Date", "Next_Due_Date", "Department", "Assignee"])

if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame([
        ["LOG-001", "SCH-001", "2026-08-01", "Kyaw Kyaw", 15000, "Filter cleaned and tested OK", "Completed"],
        ["LOG-002", "SCH-002", "2026-06-01", "U Ba", 150000, "Oil and filters replaced successfully", "Completed"]
    ], columns=["Log_ID", "Schedule_ID", "Check_Date", "Technician", "Cost_MMK", "Remarks", "Status"])

# Sidebar Navigation
menu = st.sidebar.selectbox("Navigation Menu", ["📊 Dashboard", "📦 Assets Management", "📅 Maintenance Schedules", "📝 Maintenance Logs"])

if menu == "📊 Dashboard":
    st.subheader("📊 Maintenance Summary Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Assets", len(st.session_state.assets))
    col2.metric("Active Schedules", len(st.session_state.schedules))
    col3.metric("Completed Logs", len(st.session_state.logs))
    
    st.markdown("---")
    st.subheader("Upcoming Schedules (စစ်ဆေးရန်ရှိသည်များ)")
    st.dataframe(st.session_state.schedules)

elif menu == "📦 Assets Management":
    st.subheader("📦 ပစ္စည်း/စက်ယន្តတရား စာရင်း (Assets)")
    st.dataframe(st.session_state.assets)
    
    with st.expander("➕ ပစ္စည်းအသစ် ထည့်သွင်းရန်"):
        with st.form("asset_form"):
            aid = st.text_input("Asset ID (ဥပမာ- AC-002)")
            aname = st.text_input("Asset Name")
            cat = st.text_input("Category")
            dept = st.selectbox("Department", ["အုပ်ချုပ်ရေးဌာန", "အိုင်တီဌာန", "ហိတ္တုနှင့် ထောက်ပံ့ရေး"])
            loc = st.text_input("Location")
            pdate = st.date_input("Purchase Date")
            submit = st.form_submit_button("Save Asset")
            if submit:
                new_row = pd.DataFrame([[aid, aname, cat, dept, loc, str(pdate), "Active"]], 
                                       columns=st.session_state.assets.columns)
                st.session_state.assets = pd.concat([st.session_state.assets, new_row], ignore_index=True)
                st.success("ပစ္စည်းအသစ် အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ!")

elif menu == "📅 Maintenance Schedules":
    st.subheader("📅 ပြုပြင်ရန် အချိန်ဇယားများ (Schedules)")
    st.dataframe(st.session_state.schedules)

elif menu == "📝 Maintenance Logs":
    st.subheader("📝 ပြုပြင်ပြီးစီးမှု မှတ်တမ်းများ (Maintenance Logs)")
    st.dataframe(st.session_state.logs)