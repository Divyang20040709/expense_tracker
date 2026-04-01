import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")

st.markdown("""
<style>
body {
    background: linear-gradient(to right, #141e30, #243b55);
}
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "categories" not in st.session_state:
    st.session_state.categories = ["Food", "Transport", "Entertainment", "Utilities", "Other"]

if "income" not in st.session_state:
    st.session_state.income = 0

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Add Expense", "View Expenses", "Analysis", "Categories"],
    icons=["house", "plus", "list", "bar-chart", "gear"],
    orientation="horizontal"
)

st.title("💸 Expense Tracker")
st.caption("Smart finance management system ")

if selected == "Dashboard":

    col1, col2 = st.columns([2,1])

    with col1:
        income_input = st.number_input("Monthly Income (₹)", min_value=0.0, step=100.0)

        if st.button("Save Income"):
            st.session_state.income = income_input

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        df["Date"] = pd.to_datetime(df["Date"])

        month = st.selectbox("Select Month", df["Date"].dt.month.unique())
        df = df[df["Date"].dt.month == month]

        total_expense = df["Amount"].sum()
        income = st.session_state.income
        savings = income - total_expense

        m1, m2, m3 = st.columns(3)
        m1.metric("Income", f"₹{income:.0f}")
        m2.metric("Expense", f"₹{total_expense:.0f}")
        m3.metric("Savings", f"₹{savings:.0f}")

        if income > 0:
            percent = (total_expense / income) * 100
            st.progress(min(int(percent), 100))

        st.subheader("Spending Distribution")
        cat = df.groupby("Category")["Amount"].sum()

        fig1, ax1 = plt.subplots()
        ax1.pie(cat, labels=cat.index, autopct='%1.1f%%')
        st.pyplot(fig1)

        st.subheader("Expense Trend")
        trend = df.groupby("Date")["Amount"].sum()

        fig2, ax2 = plt.subplots()
        trend.plot(ax=ax2)
        st.pyplot(fig2)

    else:
        st.info("No data yet")

elif selected == "Add Expense":

    with st.form("form"):
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date")
            category = st.selectbox("Category", st.session_state.categories)

        with col2:
            amount = st.number_input("Amount", min_value=0.0)
            desc = st.text_input("Description")

        if st.form_submit_button("Add"):
            st.session_state.expenses.append({
                "Date": date,
                "Category": category,
                "Amount": amount,
                "Description": desc
            })
            st.success("Added!")

elif selected == "View Expenses":

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)

        st.dataframe(df)

        csv = df.to_csv(index=False).encode()
        st.download_button("Download CSV", csv, "expenses.csv", "text/csv")

    else:
        st.info("No data")

elif selected == "Analysis":

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        cat = df.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()
        cat.plot(kind="bar", ax=ax)
        st.pyplot(fig)

elif selected == "Categories":

    new = st.text_input("New Category")

    if st.button("Add Category"):
        if new and new not in st.session_state.categories:
            st.session_state.categories.append(new)

    st.write(st.session_state.categories)