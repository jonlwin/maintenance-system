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

# Initialize Empty DataFrames
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame(columns=["Asset_ID", "Asset_Name", "Category", "Department", "Location", "Purchase_Date", "Status"])

if 'fixed_assets' not in st.session_state:
    st.session_state.fixed_assets = pd.DataFrame(columns=["Asset_Code", "Item_Name", "Asset_Category", "Department", "Location", "Original_Value", "Condition"])

if 'schedules' not in st.session_state:
    st.session_state.schedules = pd.DataFrame(columns=["Schedule_ID", "Asset_ID", "Task_Description", "Frequency", "Last_Date", "Next_Due_Date", "Department", "Assignee"])

if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame(columns=["Log_ID", "Schedule_ID", "Check_Date", "Technician", "Cost_MMK", "Remarks", "Status"])

# Departments list
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
    if not st.session_state.schedules.empty:
        st.dataframe(st.session_state.schedules, use_container_width=True)
    else:
        st.info("ပြုပြင်ရန် အချိန်ဇယားများ မရှိသေးပါ။")

elif menu == "📦 Assets Management":
    st.subheader("📦 Equipment & Machinery Assets")
    if not st.session_state.assets.empty:
        st.dataframe(st.session_state.assets, use_container_width=True)
    else:
        st.info("ပစ္စည်းစာရင်းများ မရှိသေးပါ။")
    
    with st.expander("➕ Add New Equipment Asset"):
        with st.form("asset_form"):
            aid = st.text_input("Asset ID (ဥပမာ- AC-001)")
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
                st.success("ပစ္စည်းအသစ် အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ!")

elif menu == "🏛️ Fixed Assets Register":
    st.subheader("🏛️ Fixed Assets (ပုံသေပိုင်ပစ္စည်းများ စာရင်း)")
    if not st.session_state.fixed_assets.empty:
        st.dataframe(st.session_state.fixed_assets, use_container_width=True)
    else:
        st.info("ပုံသေပိုင်ပစ္စည်း စာရင်းများ မရှိသေးပါ။")
    
    with st.expander("➕ Add New Fixed Asset"):
        with st.form("fixed_asset_form"):
            fcode = st.text_input("Asset Code (ဥပမာ- FA-001)")
            fname = st.text_input("Item Name")
            fcat = st.text_input("Asset Category")
            fdept = st.selectbox("Department", dept_options, key="fa_dept")
            floc = st.text_input("Location", key="fa_loc")
            fval = st.text_input("Original Value (ဥပမာ- 1,200,000 MMK)")
            fcond = st.selectbox("Condition", ["Excellent", "Good", "Fair", "Needs Repair"])
            f_submit = st.form_submit_button("Save Fixed Asset")
            if f_submit:
                new_fa = pd.DataFrame([[fcode, fname, fcat, fdept, floc, fval, fcond]], 
                                      columns=st.session_state.fixed_assets.columns)
                st.session_state.fixed_assets = pd.concat([st.session_state.fixed_assets, new_fa], ignore_index=True)
                st.success("ပုံသေပိုင်ပစ္စည်း အောင်မြင်စွာ မှတ်တမ်းတင်ပြီးပါပြီ!")

elif menu == "📅 Maintenance Schedules":
    st.subheader("📅 Maintenance Schedules (ပြုပြင်ရန် အချိန်ဇယားများ)")
    if not st.session_state.schedules.empty:
        st.dataframe(st.session_state.schedules, use_container_width=True)
    else:
        st.info("အချိန်ဇယားများ မရှိသေးပါ။")
    
    with st.expander("➕ Add New Maintenance Schedule"):
        with st.form("schedule_form"):
            sch_id = st.text_input("Schedule ID (ဥပမာ- SCH-001)")
            asset_id_ref = st.text_input("Asset ID (သက်ဆိုင်ရာ ပစ္စည်းကုဒ်)")
            task_desc = st.text_area("Task Description (လုပ်ဆောင်ရမည့် လုပ်ငန်းစဉ်)")
            freq = st.selectbox("Frequency", ["Weekly", "Monthly", "Quarterly", "Every 6 Months", "Yearly"])
            last_dt = st.date_input("Last Service Date")
            next_dt = st.date_input("Next Due Date")
            sch_dept = st.selectbox("Department", dept_options, key="sch_dept")
            assignee = st.text_input("Assignee (တာဝန်ခံ Technician / Vendor)")
            sch_submit = st.form_submit_button("Save Schedule")
            if sch_submit:
                new_sch = pd.DataFrame([[sch_id, asset_id_ref, task_desc, freq, str(last_dt), str(next_dt), sch_dept, assignee]], 
                                       columns=st.session_state.schedules.columns)
                st.session_state.schedules = pd.concat([st.session_state.schedules, new_sch], ignore_index=True)
                st.success("ပြုပြင်ရန် အချိန်ဇယား အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ!")

elif menu == "📝 Maintenance Logs":
    st.subheader("📝 Maintenance Execution Logs (ပြုပြင်ပြီးစီးမှု မှတ်တမ်းများ)")
    if not st.session_state.logs.empty:
        st.dataframe(st.session_state.logs, use_container_width=True)
    else:
        st.info("ပြုပြင်ပြီးစီးမှု မှတ်တမ်းများ မရှိသေးပါ။")
    
    with st.expander("➕ Add New Maintenance Log"):
        with st.form("log_form"):
            log_id = st.text_input("Log ID (ဥပမာ- LOG-001)")
            sch_id_ref = st.text_input("Schedule ID (သက်ဆိုင်ရာ အချိန်ဇယားကုဒ်)")
            chk_date = st.date_input("Check Date (စစ်ဆေးပြုပြင်သည့်ရက်)")
            tech = st.text_input("Technician Name")
            cost = st.number_input("Cost (MMK - ကုန်ကျစရိတ်)", min_value=0, step=1000)
            remarks = st.text_area("Remarks (မှတ်ချက်/ဆောင်ရွက်ချက်)")
            log_status = st.selectbox("Status", ["Completed", "Pending", "In Progress"])
            log_submit = st.form_submit_button("Save Log")
            if log_submit:
                new_log = pd.DataFrame([[log_id, sch_id_ref, str(chk_date), tech, cost, remarks, log_status]], 
                                       columns=st.session_state.logs.columns)
                st.session_state.logs = pd.concat([st.session_state.logs, new_log], ignore_index=True)
                st.success("ပြုပြင်ပြီးစီးမှု မှတ်တမ်း အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")
