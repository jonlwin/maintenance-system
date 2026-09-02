import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Enterprise Maintenance & Fixed Asset Management System", page_icon="🛠️", layout="wide")

# Custom Styling for Professional Look
st.markdown("""
    <style>
    .main-header {font-size: 28px; font-weight: bold; color: #1E3A8A;}
    .sub-text {font-size: 14px; color: #4B5563;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🛠️ Enterprise Maintenance & Fixed Asset Management System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">ဌာနဆိုင်ရာ ပစ္စည်းကိရိယာများ၊ ပုံသေပိုင်ပစ္စည်းများ (Fixed Assets) နှင့် ပြုပြင်ထိန်းသိမ်းမှု အချိန်ဇယားများ စီမံခန့်ခွဲမှုစနစ်</p>', unsafe_allow_html=True)
st.markdown("---")

# Initialize Session State Data with updated Departments and Fixed Assets
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        ["AC-001", "Server Room Air Con 3-Ton", "Air Conditioner", "IT", "Server Room", "2025-01-15", "Active"],
        ["GEN-001", "Office Backup Generator 50KVA", "Generator", "Office", "Compound", "2024-06-10", "Active"],
        ["EL-001", "Main Distribution Board (MDB)", "Electrical", "M&E", "Ground Floor", "2024-01-01", "Active"]
    ], columns=["Asset_ID", "Asset_Name", "Category", "Department", "Location", "Purchase_Date", "Status"])

if 'fixed_assets' not in st.session_state:
    st.session_state.fixed_assets = pd.DataFrame([
        ["FA-001", "Executive Office Desk Set", "Furniture", "Admin Executive", "Level 2 Office", "1,200,000 MMK", "Good"],
        ["FA-002", "Conference Room Smart TV 75\"", "Electronics", "Office", "Meeting Room", "3,500,000 MMK", "Excellent"],
        ["FA-003", "Network Core Switch Cisco", "IT Hardware", "IT", "Server Room", "4,500,000 MMK", "Good"]
    ], columns=["Asset_Code", "Item_Name", "Asset_Category", "Department", "Location", "Original_Value", "Condition"])

if 'schedules' not in st.session_state:
    st.session_state.schedules = pd.DataFrame([
        ["SCH-001", "AC-001", "Clean filter, check gas pressure", "Monthly", "2026-08-01", "2026-09-01", "IT", "Technician Team A"],
        ["SCH-002", "GEN-001", "Change engine oil, filter", "Quarterly", "2026-06-01", "2026-09-01", "Office", "External Vendor"],
        ["SCH-003", "EL-001", "Thermal scanning and tighten terminals", "Every 6 Months", "2026-03-01", "2026-09-01", "M&E", "Electrician"]
    ], columns=["Schedule_ID", "Asset_ID", "Task_Description", "Frequency", "Last_Date", "Next_Due_Date", "Department", "Assignee"])

if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame([
        ["LOG-001", "SCH-001", "2026-08-01", "Kyaw Kyaw", 15000, "Filter cleaned and tested OK", "Completed"],
        ["LOG-002", "SCH-002", "2026-06-01", "U Ba", 150000, "Oil and filters replaced successfully", "Completed"]
    ], columns=["Log_ID", "Schedule_ID", "Check_Date", "Technician", "Cost_MMK", "Remarks", "Status"])

# Updated Departments list
dept_options = ["Office", "M&E", "IT", "Admin Asst 1", "Admin Asst 2", "Admin Executive"]

# Sidebar Navigation
menu = st.sidebar.selectbox("Navigation Menu", [
    "📊 Dashboard", 
    "📦 Assets Management", 
    "🏛️ Fixed Assets Register", 
    "📅 Maintenance Schedules", 
    "📝 Maintenance Logs"
])

if menu == "📊 Dashboard":
    st.subheader("📊 Executive Summary Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Equipment Assets", len(st.session_state.assets))
    col2.metric("Fixed Assets Registered", len(st.session_state.fixed_assets))
    col3.metric("Active Schedules", len(st.session_state.schedules))
    col4.metric("Completed Logs", len(st.session_state.logs))
    
    st.markdown("---")
    st.subheader("⏰ Upcoming Maintenance Schedules")
    st.dataframe(st.session_state.schedules, use_container_width=True)

elif menu == "📦 Assets Management":
    st.subheader("📦 Equipment & Machinery Assets")
    st.dataframe(st.session_state.assets, use_container_width=True)
    
    with st.expander("➕ Add New Equipment Asset"):
        with st.form("asset_form"):
            aid = st.text_input("Asset ID (e.g., AC-002)")
            aname = st.text_input("Asset Name")
            cat = st.text_input("Category")
            dept = st.selectbox("Department", dept_options)
            loc = st.text_input("Location")
            pdate = st.date_input("Purchase Date")
            submit = st.form_submit_button("Save Asset")
            if submit:
                new_row = pd.DataFrame([[aid, aname, cat, dept, loc, str(pdate), "Active"]], 
                                       columns=st.session_state.assets.columns)
                st.session_state.assets = pd.concat([st.session_state.assets, new_row], ignore_index=True)
                st.success("New equipment asset successfully added!")

elif menu == "🏛️ Fixed Assets Register":
    st.subheader("🏛️ Fixed Assets (ပုံသေပိုင်ပစ္စည်းများ စာရင်း)")
    st.dataframe(st.session_state.fixed_assets, use_container_width=True)
    
    with st.expander("➕ Add New Fixed Asset"):
        with st.form("fixed_asset_form"):
            fcode = st.text_input("Asset Code (e.g., FA-004)")
            fname = st.text_input("Item Name")
            fcat = st.text_input("Asset Category")
            fdept = st.selectbox("Department", dept_options, key="fa_dept")
            floc = st.text_input("Location", key="fa_loc")
            fval = st.text_input("Original Value (e.g., 500,000 MMK)")
            fcond = st.selectbox("Condition", ["Excellent", "Good", "Fair", "Needs Repair"])
            f_submit = st.form_submit_button("Save Fixed Asset")
            if f_submit:
                new_fa = pd.DataFrame([[fcode, fname, fcat, fdept, floc, fval, fcond]], 
                                      columns=st.session_state.fixed_assets.columns)
                st.session_state.fixed_assets = pd.concat([st.session_state.fixed_assets, new_fa], ignore_index=True)
                st.success("New fixed asset successfully registered!")

elif menu == "📅 Maintenance Schedules":
    st.subheader("📅 Maintenance Schedules (ပြုပြင်ရန် အချိန်ဇယားများ)")
    st.dataframe(st.session_state.schedules, use_container_width=True)

elif menu == "📝 Maintenance Logs":
    st.subheader("📝 Maintenance Execution Logs (ပြုပြင်ပြီးစီးမှု မှတ်တမ်းများ)")
    st.dataframe(st.session_state.logs, use_container_width=True)
