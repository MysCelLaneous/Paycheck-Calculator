
import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from io import BytesIO

# --- Simple password gate ---
password = st.text_input("Enter password to access the calculator:", type="password")
if password != "DFTA2020":
    st.warning("Incorrect password. Please try again.")
    st.stop()

# --- Full Step Table with 43 Steps ---
data = {
    "Step": list(range(1, 44)),
    "60 College": [20, 20.75, 21.5, 22.32, 23.04, 23.79, 24.54, 25.14, 25.76, 26.4, 26.78, 26.78, 26.78, 26.78, 27.29, 27.84, 27.84, 27.84, 27.84, 27.84, 28.36, 28.36, 28.36, 29.18, 29.18, 29.67, 29.67, 29.67, 29.67, 29.67, 29.78, 29.78, 29.78, 29.78, 29.78, 29.91, 29.91, 29.91, 29.91, 29.91, 29.91, 29.91, 29.91],
    "61-90 College": [21.5, 22.25, 23, 23.82, 24.54, 25.29, 26.04, 26.67, 27.32, 27.99, 28.4, 28.4, 28.4, 28.4, 29.01, 29.51, 29.51, 29.51, 29.51, 29.51, 30.1, 30.1, 30.1, 30.1, 30.1, 30.56, 30.56, 30.56, 30.56, 30.56, 30.67, 30.67, 30.67, 30.67, 30.67, 30.79, 30.79, 30.79, 30.79, 30.79, 30.79, 30.79, 30.79],
    "91+ College": [22.87, 23.62, 24.37, 25.19, 25.91, 26.66, 27.41, 28.07, 28.74, 29.45, 29.89, 29.89, 29.89, 29.89, 30.51, 31.05, 31.05, 31.05, 31.05, 31.05, 31.66, 31.66, 31.66, 31.66, 31.66, 32.14, 32.14, 32.14, 32.14, 32.14, 32.25, 32.25, 32.25, 32.25, 32.25, 32.37, 32.37, 32.37, 32.37, 32.37, 32.37, 32.37, 32.37],
    "BA College": [24.35, 25.1, 25.85, 26.67, 27.39, 28.14, 28.89, 29.58, 30.28, 31.02, 31.5, 31.5, 31.5, 31.5, 32.1, 32.65, 32.65, 32.65, 32.65, 32.65, 33.29, 33.29, 33.29, 33.29, 33.29, 33.76, 33.76, 33.76, 33.76, 33.76, 33.89, 33.89, 33.89, 33.89, 33.89, 34.01, 34.01, 34.01, 34.01, 34.01, 34.01, 34.01, 34.01],
    "Sign/LPN": [24.37, 25.12, 25.87, 26.69, 27.41, 28.16, 28.91, 29.34, 29.79, 30.24, 30.69, 30.69, 30.69, 30.69, 31.31, 31.85, 31.85, 31.85, 31.85, 31.85, 31.85, 31.85, 31.85, 32.47, 32.47, 32.94, 32.94, 32.94, 32.94, 32.94, 33.07, 33.07, 33.07, 33.07, 33.07, 33.2, 33.2, 33.2, 33.2, 33.2, 33.2, 33.2, 33.2]
}
df = pd.DataFrame(data)

st.title("Paycheck Calculator with Leave Summary")

step = st.selectbox("Step", df["Step"])
role = st.selectbox("Education/Role", df.columns[1:])
hours_per_week = st.selectbox("Hours per Week", [20, 25, 30, 32.5, 35, 40])
months_worked = st.selectbox("Months Worked", [8, 9, 10, 12])
pay_periods = st.selectbox("Number of Pay Periods", [18, 20, 22, 24, 26])
daily_hours = st.selectbox("Daily Hours Worked", [6, 6.25, 6.5])

hourly_rate = df.loc[df["Step"] == step, role].values[0]
weeks_worked = months_worked * 4.33
total_hours = hours_per_week * weeks_worked
total_gross = hourly_rate * total_hours
gross_per_check = total_gross / pay_periods
gross_per_month = total_gross / months_worked

sick_hours = 10 * daily_hours
personal_hours = 4 * daily_hours

st.subheader("Results")
st.write(f"**Hourly Rate:** ${hourly_rate:.2f}")
st.write(f"**Total Hours Worked:** {total_hours:.2f}")
st.write(f"**Total Gross Pay:** ${total_gross:,.2f}")
st.write(f"**Gross Pay Per Check:** ${gross_per_check:,.2f}")
st.write(f"**Gross Pay Per Month:** ${gross_per_month:,.2f}")
st.write(f"**Sick Leave (Hours):** {sick_hours}")
st.write(f"**Personal Leave (Hours):** {personal_hours}")

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Paycheck Summary Report", ln=True, align="C")
    pdf.ln(5)
    fields = {
        "Step": step,
        "Role": role,
        "Hourly Rate": f"${hourly_rate:.2f}",
        "Hours/Week": hours_per_week,
        "Months Worked": months_worked,
        "Pay Periods": pay_periods,
        "Daily Hours": daily_hours,
        "Total Hours": f"{total_hours:.2f}",
        "Total Gross Pay": f"${total_gross:,.2f}",
        "Gross Per Paycheck": f"${gross_per_check:,.2f}",
        "Gross Per Month": f"${gross_per_month:,.2f}",
        "Sick Leave Hours": sick_hours,
        "Personal Leave Hours": personal_hours
    }
    for k, v in fields.items():
        pdf.cell(200, 8, f"{k}: {v}", ln=True)
    pdf_output = pdf.output(dest="S").encode("latin1")
    return BytesIO(pdf_output)

pdf_file = generate_pdf()
b64_pdf = base64.b64encode(pdf_file.read()).decode()
href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="paycheck_summary.pdf">📄 Download PDF Report</a>'
st.markdown(href, unsafe_allow_html=True)
