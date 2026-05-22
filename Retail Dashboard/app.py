import streamlit as st
import pandas as pd

# -------------------
# LOAD DATA
# -------------------

sheet_url = "https://docs.google.com/spreadsheets/d/1Gjmuj5GZRqa-8JegtUIhnei-rPgEoBSB7qlqwxWeMgg/export?format=csv&gid=0"
df = pd.read_csv(sheet_url)

# fix column spaces (ΠΟΛΥ ΣΗΜΑΝΤΙΚΟ)
df.columns = df.columns.str.strip()

st.title("Nestle Dashboard")

# -------------------
# FILTERS
# -------------------

product = st.selectbox("Προϊόν", df["Προϊόν"].unique())

date = st.date_input("Ημερομηνία Επίσκεψης")

filtered = df[df["Προϊόν"] == product]

if date:
    filtered = filtered[filtered["Ημερομηνία Επίσκεψης"] == str(date)]

# -------------------
# IMAGE COLUMNS
# -------------------

image_cols = [
    "Φωτογραφία Merchandiser 1","Φωτογραφία Merchandiser 2","Φωτογραφία Merchandiser 3","Φωτογραφία Merchandiser 4","Φωτογραφία Merchandiser 5",
    "Φωτογραφία Πωλητή 1","Φωτογραφία Πωλητή 2","Φωτογραφία Πωλητή 3","Φωτογραφία Πωλητή 4","Φωτογραφία Πωλητή 5"
]

# -------------------
# DISPLAY
# -------------------

st.subheader("Ενημερώσεις")

for _, row in filtered.iterrows():

    st.markdown(f"""
    ### Ενημέρωση #{row['Ενημέρωση']}
    - Αλυσίδα: {row['Αλυσίδα']}
    - Οδός: {row['Διεύθυνση Καταστήματος']}
    - Πόλη: {row['Πόλη']}
    - Παρατήρηση: {row['Παρατηρήσεις']}
    """)

    cols = st.columns(5)
    i = 0

    for col_name in image_cols:
        img = row.get(col_name)

        if pd.notna(img) and str(img).strip() != "":
            cols[i % 5].image(str(img).strip(), width=150)
            i += 1

    st.divider()