import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Enterprise Maintenance & Fixed Asset Management System", page_icon="🛠️", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main-header {font-size: 28px; font-weight: bold; color: #1E3A8A;}
    .sub-text {font-size: 14px; color: #4B5563;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🛠️ Enterprise Maintenance & Fixed Asset Management System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">ဌာနဆိုင်ရာ ပစ္စည်းကိရိယာများ၊ ပုံသေပိုင်ပစ္စည်းများ (Fixed Assets) နှင့် ပြုပြင်ထိန်းသိမ်းမှု အချိန်ဇယားများ စီမံခန့်ခွဲမှုစနစ်</p>', unsafe_allow_html=True)
st.markdown("---")

# Initialize DataFrames with identical professional schema for both Equipment Assets and Fixed Assets
asset_schema = [
    'Timestamp', 'ပစ္စည်းအမည် (Asset Name)', 'Location', 'Deparment (ဌာန)', 
    'ပစ္စည်းအမျိုးအစား (Category)', 'စက်ပစ္စည်းကိရိယာများ', 'ပရိဘောဂပစ္စည်းများ', 
    'ကွန်ပျူတာနှင့် ဆက်စပ်ပစ္စည်းများ', 'လျှပ်စစ်ပစ္စည်းများ', 'အီလက်ထရောနစ်ပစ္စည်းများ', 
    'ရုံးသုံးပစ္စည်းများ', 'လက်ရှိအခြေအနေ (Current Condition)', 'Asset Code', 
    'Asset NEW Code', 'photo', 'ဝယ်ယူသည့်နေ့ (Acquisition Date)', 
    'ဝယ်ယူဈေးနှုန်း ($) (Acquisition Cost)', 'အသုံးဝင်မည့်နှစ် (Useful Life in Years)', 
    'ကျန်ရှိမည့်တန်ဖိုး ($) (Salvage Value)', 'စုစုပေါင်း တန်ဖိုးလျော့ကျမှု ($) (Accumulated Depreciation)', 
    'လက်ရှိတန်ဖိုး ($) (Net Book Value)', 'နောက်ဆုံးပြုပြင်ခဲ့သည့်နေ့ (Last Maintenance Date)', 
    'ရောင်းချ/ဖျက်သိမ်းသည့်နေ့ (Disposal Date)', 'ရောင်းချ/ဖျက်သိမ်းမှု တန်ဖိုး ($) (Disposal Value)', 
    'ရောင်းချ/ဖျက်သိမ်းရသည့် အကြောင်းအရင်း (Reason for Disposal)'
]

if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame(columns=asset_schema)

if 'fixed_assets' not in st.session_state:
    st.session_state.fixed_assets = pd.DataFrame(columns=asset_schema)

if 'schedules' not in st.session_state:
    st.session_state.schedules = pd.DataFrame(columns=["Schedule_ID", "Asset_ID", "Task_Description", "Frequency", "Last_Date", "Next_Due_Date", "Department", "Assignee"])

if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame(columns=["Log_ID", "Schedule_ID", "Check_Date", "Technician", "Cost_MMK", "Remarks", "Status"])

# Updated Departments and Categories options
dept_options = [
    "BOD", "Marketing (MKT)", "စာရင်းစစ်ဌာန (AUD)", "စီမံရေးရာဌာန (AMD)", 
    "ဘဏ္ဏာရေးဌာန (FND)", "ဝန်ထမ်းရေးရာဌာန (HRD)", "ဝယ်ယူရေးဌာန (PRD)", 
    "သိုလှောင်ရေးဌာန (INV)", "အရောင်းဌာန (SED)", "သိုလှောင်ရေးဌာန (REC)", 
    "သိုလှောင်ရေးဌာန (LNE)", "သိုလှောင်ရေးဌာန (LOD)", "သိုလှောင်ရေးဌာန (LOG)"
]

category_options = [
    "ကွန်ပျူတာနှင့်ဆက်စပ်ပစ္စည်းများ (CP)", 
    "စက်ပစ္စည်းကိရိယာများ (MY)", 
    "ပရိဘောဂပစ္စည်းများ (FR)", 
    "ရုံးသုံးပစ္စည်းများ (OU)", 
    "ရုံးသုံးဖုန်းများ (PH)", 
    "လျှပ်စစ်ပစ္စည်းများ (EC)", 
    "အီလက်ထရောနစ်ပစ္စည်းများ (ET)"
]

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
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Equipment Assets", len(st.session_state.assets))
    col2.metric("Fixed Assets", len(st.session_state.fixed_assets))
    col3.metric("Active Schedules", len(st.session_state.schedules))
    col4.metric("Completed Logs", len(st.session_state.logs))
    
    total_cost = st.session_state.logs['Cost_MMK'].sum() if not st.session_state.logs.empty else 0
    col5.metric("Total Maint. Cost (MMK)", f"{total_cost:,} MMK")
    
    st.markdown("---")
    st.subheader("📦 Recent Equipment & Machinery Assets")
    if not st.session_state.assets.empty:
        st.dataframe(st.session_state.assets[['Asset Code', 'ပစ္စည်းအမည် (Asset Name)', 'Deparment (ဌာန)', 'ပစ္စည်းအမျိုးအစား (Category)', 'ဝယ်ယူဈေးနှုန်း ($) (Acquisition Cost)']], use_container_width=True)
    else:
        st.info("ပစ္စည်းစာရင်းများ မရှိသေးပါ။")

    st.subheader("🏛️ Recent Fixed Assets Summary")
    if not st.session_state.fixed_assets.empty:
        st.dataframe(st.session_state.fixed_assets[['Asset Code', 'ပစ္စည်းအမည် (Asset Name)', 'Deparment (ဌာန)', 'ပစ္စည်းအမျိုးအစား (Category)', 'ဝယ်ယူဈေးနှုန်း ($) (Acquisition Cost)']], use_container_width=True)
    else:
        st.info("ပုံသေပိုင်ပစ္စည်း မှတ်တမ်းများ မရှိသေးပါ။")
        
    st.subheader("⏰ Upcoming Maintenance Schedules")
    if not st.session_state.schedules.empty:
        st.dataframe(st.session_state.schedules, use_container_width=True)
    else:
        st.info("ပြုပြင်ရန် အချိန်ဇယားများ မရှိသေးပါ။")

elif menu == "📦 Assets Management":
    st.subheader("📦 Equipment & Machinery Assets Management")
    if not st.session_state.assets.empty:
        st.dataframe(st.session_state.assets, use_container_width=True)
    else:
        st.info("စက်ပစ္စည်းကိရိယာ မှတ်တမ်းများ မရှိသေးပါ။ (အောက်ပါပုံစံမှတစ်ဆင့် အသစ်ထည့်သွင်းနိုင်ပါသည်)")
    
    with st.expander("➕ Add New Equipment & Machinery Asset"):
        with st.form("equipment_asset_form"):
            eq_name = st.text_input("ပစ္စည်းအမည် (Asset Name)")
            eq_loc = st.text_input("Location (တည်နေရာ)", value="HTY-20")
            eq_dept = st.selectbox("Deparment (ဌာန)", dept_options, key="eq_dept")
            eq_cat = st.selectbox("ပစ္စည်းအမျိုးအစား (Category)", category_options, key="eq_cat")
            eq_cond = st.selectbox("လက်ရှိအခြေအနေ (Current Condition)", ["ကောင်းမွန်သည် (Good)", "အသင့်အတင့်", "ပြင်ဆင်ရန်လိုအပ်သည်"], key="eq_cond")
            eq_code = st.text_input("Asset Code", key="eq_code")
            eq_new_code = st.text_input("Asset NEW Code", key="eq_new_code")
            eq_photo = st.text_input("Photo Link", key="eq_photo")
            eq_pdate = st.date_input("ဝယ်ယူသည့်နေ့ (Acquisition Date)", key="eq_pdate")
            eq_cost = st.number_input("ဝယ်ယူဈေးနှုန်း ($) (Acquisition Cost)", min_value=0.0, step=10.0, key="eq_cost")
            eq_life = st.number_input("အသုံးဝင်မည့်နှစ် (Useful Life in Years)", min_value=1, value=5, key="eq_life")
            eq_salvage = st.number_input("ကျန်ရှိမည့်တန်ဖိုး ($) (Salvage Value)", min_value=0.0, step=10.0, key="eq_salvage")
            
            eq_submit = st.form_submit_button("Save Equipment Asset")
            if eq_submit:
                new_eq = pd.DataFrame([[
                    str(datetime.now()), eq_name, eq_loc, eq_dept, eq_cat, 
                    "", "", "", "", "", "", eq_cond, eq_code, eq_new_code, eq_photo, 
                    str(eq_pdate), eq_cost, eq_life, eq_salvage, 
                    (eq_cost - eq_salvage) / eq_life if eq_life > 0 else 0, 
                    eq_cost, "", "", 0.0, ""
                ]], columns=st.session_state.assets.columns)
                
                st.session_state.assets = pd.concat([st.session_state.assets, new_eq], ignore_index=True)
                st.success("စက်ပစ္စည်းကိရိယာ အောင်မြင်စွာ မှတ်တမ်းတင်ပြီးပါပြီ!")

elif menu == "🏛️ Fixed Assets Register":
    st.subheader("🏛️ Fixed Assets Register (ပုံသေပိုင်ပစ္စည်းများ စာရင်း)")
    if not st.session_state.fixed_assets.empty:
        st.dataframe(st.session_state.fixed_assets, use_container_width=True)
    else:
        st.info("ယခုလက်တလော မှတ်တမ်းတင်ထားသော ပုံသေပိုင်ပစ္စည်း ဒေတာများ မရှိသေးပါ။")
    
    with st.expander("➕ Add New Fixed Asset Record"):
        with st.form("fixed_asset_form"):
            fa_name = st.text_input("ပစ္စည်းအမည် (Asset Name)")
            fa_loc = st.text_input("Location (တည်နေရာ)", value="HTY-20")
            fa_dept = st.selectbox("Deparment (ဌာန)", dept_options)
            fa_cat = st.selectbox("ပစ္စည်းအမျိုးအစား (Category)", category_options)
            fa_cond = st.selectbox("လက်ရှိအခြေအနေ (Current Condition)", ["ကောင်းမွန်သည် (Good)", "အသင့်အတင့်", "ပြင်ဆင်ရန်လိုအပ်သည်"])
            fa_code = st.text_input("Asset Code")
            fa_new_code = st.text_input("Asset NEW Code")
            fa_photo = st.text_input("Photo Link")
            fa_pdate = st.date_input("ဝယ်ယူသည့်နေ့ (Acquisition Date)")
            fa_cost = st.number_input("ဝယ်ယူဈေးနှုန်း ($) (Acquisition Cost)", min_value=0.0, step=10.0)
            fa_life = st.number_input("အသုံးဝင်မည့်နှစ် (Useful Life in Years)", min_value=1, value=5)
            fa_salvage = st.number_input("ကျန်ရှိမည့်တန်ဖိုး ($) (Salvage Value)", min_value=0.0, step=10.0)
            
            f_submit = st.form_submit_button("Save Fixed Asset")
            if f_submit:
                new_fa = pd.DataFrame([[
                    str(datetime.now()), fa_name, fa_loc, fa_dept, fa_cat, 
                    "", "", "", "", "", "", fa_cond, fa_code, fa_new_code, fa_photo, 
                    str(fa_pdate), fa_cost, fa_life, fa_salvage, 
                    (fa_cost - fa_salvage) / fa_life if fa_life > 0 else 0, 
                    fa_cost, "", "", 0.0, ""
                ]], columns=st.session_state.fixed_assets.columns)
                
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
            asset_id_ref = st.text_input("Asset ID")
            task_desc = st.text_area("Task Description")
            freq = st.selectbox("Frequency", ["Weekly", "Monthly", "Quarterly", "Every 6 Months", "Yearly"])
            last_dt = st.date_input("Last Service Date")
            next_dt = st.date_input("Next Due Date")
            sch_dept = st.selectbox("Department", dept_options, key="sch_dept")
            assignee = st.text_input("Assignee")
            sch_submit = st.form_submit_button("Save Schedule")
            if sch_submit:
                new_sch = pd.DataFrame([[sch_id, asset_id_ref, task_desc, freq, str(last_dt), str(next_dt), sch_dept, assignee]], 
                                       columns=st.session_state.schedules.columns)
                st.session_state.schedules = pd.concat([st.session_state.schedules, new_sch], ignore_index=True)
                st.success("အချိန်ဇယား အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ!")

elif menu == "📝 Maintenance Logs":
    st.subheader("📝 Maintenance Execution Logs (ပြုပြင်ပြီးစီးမှု မှတ်တမ်းများ)")
    if not st.session_state.logs.empty:
        st.dataframe(st.session_state.logs, use_container_width=True)
    else:
        st.info("ပြုပြင်ပြီးစီးမှု မှတ်တမ်းများ မရှိသေးပါ။")
    
    with st.expander("➕ Add New Maintenance Log"):
        with st.form("log_form"):
            log_id = st.text_input("Log ID (ဥပမာ- LOG-001)")
            sch_id_ref = st.text_input("Schedule ID")
            chk_date = st.date_input("Check Date")
            tech = st.text_input("Technician Name")
            cost = st.number_input("Cost (MMK)", min_value=0, step=1000)
            remarks = st.text_area("Remarks")
            log_status = st.selectbox("Status", ["Completed", "Pending", "In Progress"])
            log_submit = st.form_submit_button("Save Log")
            if log_submit:
                new_log = pd.DataFrame([[log_id, sch_id_ref, str(chk_date), tech, cost, remarks, log_status]], 
                                       columns=st.session_state.logs.columns)
                st.session_state.logs = pd.concat([st.session_state.logs, new_log], ignore_index=True)
                st.success("မှတ်တမ်း အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")
