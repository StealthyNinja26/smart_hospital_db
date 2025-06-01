import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import joblib

# Page setup
st.set_page_config(page_title="Smart Hospital Dashboard", layout="wide")

# DB connection
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="Smart_Hospital_DB",
        user="postgres",
        password="Praveen2001!",
        port=5432
    )

conn = get_connection()

@st.cache_data
def run_query(query):
    return pd.read_sql(query, conn)

# Load ML model and preprocessor
@st.cache_resource
def load_model():
    return joblib.load("length_of_stay_model.pkl")

model = load_model()


# --- UI Start ---
st.title("🏥 Smart Hospital Admin Dashboard")

# Added Insights tab
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🧑‍💼 Patients", "👨‍⚕️ Staff", "📈 Insights", "🧮 Length of Stay Estimator"])

# --- OVERVIEW TAB ---
with tab1:
    st.subheader("Hospital Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    total_patients = run_query("SELECT COUNT(*) FROM patient").iloc[0, 0]
    total_physicians = run_query("SELECT COUNT(*) FROM physician").iloc[0, 0]
    total_nurses = run_query("SELECT COUNT(*) FROM nurse").iloc[0, 0]
    total_rooms = run_query("SELECT COUNT(*) FROM room").iloc[0, 0]

    col1.metric("Total Patients", total_patients)
    col2.metric("Physicians", total_physicians)
    col3.metric("Nurses", total_nurses)
    col4.metric("Rooms", total_rooms)

    st.markdown("---")
    st.subheader("Room Availability")
    rooms = run_query("SELECT roomnumber, roomtype, unavailable FROM room ORDER BY roomnumber")
    st.dataframe(rooms.set_index("roomnumber"))

# --- PATIENTS TAB ---
with tab2:
    st.subheader("Patient Records")

    search_name = st.text_input("Search by name")
    if search_name:
        query = f"SELECT * FROM patient WHERE name ILIKE '%{search_name}%'"
    else:
        query = "SELECT * FROM patient LIMIT 100"

    patients = run_query(query)
    st.dataframe(patients.set_index("ssn"))

# --- STAFF TAB ---
with tab3:
    subtab1, subtab2 = st.tabs(["Physicians", "Nurses"])

    with subtab1:
        st.subheader("👨‍⚕️ Physicians")
        physicians = run_query("SELECT * FROM physician ORDER BY name")
        st.dataframe(physicians.set_index("employeeid"))

    with subtab2:
        st.subheader("🧑‍⚕️ Nurses")
        nurses = run_query("SELECT * FROM nurse ORDER BY name")
        st.dataframe(nurses.set_index("employeeid"))

# --- INSIGHTS TAB ---
with tab4:
    st.subheader("📈 Hospital Data Insights")

    # --- 2. Top Prescribed Medications ---
    st.markdown("### 💊 Most Prescribed Medications")
    top_meds = run_query("""
        SELECT medication.name, COUNT(*) AS count
        FROM medication
        JOIN prescribes ON medication.code = prescribes.medication
        GROUP BY medication.name
        ORDER BY count DESC
        LIMIT 10
    """)
    if not top_meds.empty:
        fig2 = px.bar(top_meds, x="name", y="count", title="Top 10 Prescribed Medications")
        st.plotly_chart(fig2, use_container_width=True)

    # --- 3. Department Workload ---
    st.markdown("### 🏥 Department Workload (Appointments)")

    dept_workload = run_query("""
        SELECT d.name AS department, COUNT(a.appointmentid) AS count
        FROM appointment a
        JOIN physician p ON a.physician = p.employeeid
        JOIN affiliated_with aw ON p.employeeid = aw.physician
        JOIN department d ON aw.department = d.departmentid
        GROUP BY d.name
    """)

    if not dept_workload.empty:
        fig3 = px.pie(dept_workload, names="department", values="count", title="Appointments by Department")
        st.plotly_chart(fig3, use_container_width=True)


    # --- 4. Room Occupancy Rate ---
    st.markdown("### 🚪 Room Occupancy Rate")
    room_stats = run_query("""
        SELECT 
            COUNT(*) AS total_rooms,
            SUM(CASE WHEN unavailable THEN 1 ELSE 0 END) AS occupied_rooms
        FROM room
    """)
    if not room_stats.empty:
        total = room_stats['total_rooms'][0]
        occupied = room_stats['occupied_rooms'][0]
        fig4 = px.pie(
            names=["Occupied", "Available"], 
            values=[occupied, total - occupied],
            title="Room Occupancy"
        )
        st.plotly_chart(fig4, use_container_width=True)

# --- LENGTH OF STAY ESTIMATOR TAB ---
with tab5:
    st.subheader("🧮 Predict Length of Stay")

    with st.form("stay_form"):
        col1, col2 = st.columns(2)

        roomtype = col1.selectbox("Room Type", options=["ICU", "Private", "Semi-Private", "General"])
        insuranceid = col2.text_input("Insurance ID")
        num_procedures = col1.number_input("Number of Procedures", min_value=0, step=1)
        num_diagnoses = col2.number_input("Number of Diagnoses", min_value=0, step=1)

        submitted = st.form_submit_button("Estimate Length of Stay")

    if submitted:
        try:
            input_df = pd.DataFrame([{
                "roomtype": roomtype,
                "insuranceid": insuranceid,
                "num_procedures": num_procedures,
                "num_diagnoses": num_diagnoses
            }])

            prediction = model.predict(input_df)[0]

            st.success(f"🛏️ Estimated Length of Stay: {prediction:.2f} days")
        except Exception as e:
            st.error(f"Prediction failed: {e}")


# Footer
st.markdown("---")
st.caption("Smart Hospital DBMS · Admin Dashboard · Developed by Praveen Shanmuga Sundaram · 2025")