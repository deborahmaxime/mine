import streamlit as st
import sqlite3
from datetime import datetime

conn = sqlite3.connect("minesafe.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker TEXT,
    incident TEXT,
    severity TEXT,
    location TEXT,
    timestamp TEXT
)
""")
conn.commit()

st.set_page_config(page_title="MineSafe", layout="centered")

st.title("⛏️ MineSafe – Mining Safety System")
st.caption("Report and monitor mining site incidents in real time")

menu = st.sidebar.selectbox("Choose Action", ["Report Incident", "Dashboard"])

if menu == "Report Incident":
    st.subheader("🚨 Report an Incident")

    worker = st.text_input("Worker Name")
    incident = st.text_area("Describe the Incident")
    severity = st.selectbox("Severity Level", ["Low", "Medium", "High", "Critical"])
    location = st.text_input("Mine Location / Section")

    if st.button("Submit Report"):
        if worker and incident and location:
            c.execute("""
                INSERT INTO incidents (worker, incident, severity, location, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (worker, incident, severity, location, str(datetime.now())))
            conn.commit()
            st.success("Incident successfully recorded!")
        else:
            st.error("Please fill all fields")

elif menu == "Dashboard":
    st.subheader("📊 Live Incident Dashboard")

    data = c.execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()

    if len(data) == 0:
        st.info("No incidents reported yet.")
    else:
        for row in data:
            color = {
                "Low": "🟢",
                "Medium": "🟡",
                "High": "🟠",
                "Critical": "🔴"
            }

            st.markdown(f"""
### {color.get(row[3], "⚪")} {row[3]} Severity Incident
- 👷 Worker: **{row[1]}**
- 📝 Description: {row[2]}
- 📍 Location: {row[4]}
- ⏰ Time: {row[5]}
---
""")
