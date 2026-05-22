import streamlit as st
import pandas as pd

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(layout="wide")

# -------------------
# LOAD DATA
# -------------------

sheet_url = "https://docs.google.com/spreadsheets/d/1Gjmuj5GZRqa-8JegtUIhnei-rPgEoBSB7qlqwxWeMgg/export?format=csv&gid=0"
df = pd.read_csv(sheet_url)

df.columns = df.columns.str.strip()

# -------------------
# DATE PARSING (Greek format)
# -------------------

df["Ημερομηνία Επίσκεψης"] = pd.to_datetime(
    df["Ημερομηνία Επίσκεψης"],
    dayfirst=True,
    errors="coerce"
)

# -------------------
# MONTH → GREEK NAMES
# -------------------

month_map = {
    1: "Ιανουάριος",
    2: "Φεβρουάριος",
    3: "Μάρτιος",
    4: "Απρίλιος",
    5: "Μάιος",
    6: "Ιούνιος",
    7: "Ιούλιος",
    8: "Αύγουστος",
    9: "Σεπτέμβριος",
    10: "Οκτώβριος",
    11: "Νοέμβριος",
    12: "Δεκέμβριος"
}

df["Μήνας"] = df["Ημερομηνία Επίσκεψης"].dt.month.map(month_map)

# -------------------
# TITLE
# -------------------

st.title("Nestle Stand Viewer")

# -------------------
# SEARCH
# -------------------

search = st.text_input("🔍 Αναζήτηση (αλυσίδα, πόλη, παρατήρηση...)")

# -------------------
# FILTERS (ONE ROW)
# -------------------

col1, col2, col3 = st.columns(3)

with col1:
    month = st.selectbox(
        "Μήνας",
        sorted(df["Μήνας"].dropna().unique())
    )

with col2:
    product = st.selectbox(
        "Προϊόν",
        df["Προϊόν"].unique()
    )

with col3:
    update_no = st.selectbox(
        "Ενημέρωση",
        df["Ενημέρωση"].unique()
    )

# -------------------
# FILTER DATA
# -------------------

filtered = df[
    (df["Προϊόν"] == product) &
    (df["Μήνας"] == month) &
    (df["Ενημέρωση"] == update_no)
]

# -------------------
# SEARCH FILTER
# -------------------

if search:
    filtered = filtered[
        filtered.astype(str).apply(
            lambda row: search.lower() in row.to_string().lower(),
            axis=1
        )
    ]

# -------------------
# IMAGE COLUMNS
# -------------------

image_cols = [
    "Φωτογραφία Merchandiser 1",
    "Φωτογραφία Merchandiser 2",
    "Φωτογραφία Merchandiser 3",
    "Φωτογραφία Merchandiser 4",
    "Φωτογραφία Merchandiser 5",
    "Φωτογραφία Πωλητή 1",
    "Φωτογραφία Πωλητή 2",
    "Φωτογραφία Πωλητή 3",
    "Φωτογραφία Πωλητή 4",
    "Φωτογραφία Πωλητή 5"
]

# -------------------
# STATE
# -------------------

if "selected_row" not in st.session_state:
    st.session_state.selected_row = None

# -------------------
# INFO
# -------------------

if st.session_state.selected_row is None:
    st.info("👉 Πάτησε σε μια φωτογραφία για να δεις details")

# -------------------
# GRID FIXED
# -------------------

st.subheader("📸 Stand Photos")

all_images = []

for _, row in filtered.iterrows():
    for col_name in image_cols:
        img = row.get(col_name)

        if pd.notna(img) and str(img).strip():
            all_images.append((img, row))

cols = st.columns(5)

for i, (img, row) in enumerate(all_images):

    with cols[i % 5]:

        st.image(str(img).strip(), use_container_width=True)

        if st.button("📌 See Details", key=f"img_{i}"):
            st.session_state.selected_row = row.to_dict()

# -------------------
# SIDEBAR DETAILS
# -------------------

if st.session_state.selected_row:
    d = st.session_state.selected_row

    st.sidebar.title("📌 Details")

    st.sidebar.write(f"🏬 Αλυσίδα: {d['Αλυσίδα']}")
    st.sidebar.write(f"📍 Οδός: {d['Διεύθυνση Καταστήματος']}")
    st.sidebar.write(f"🏙️ Πόλη: {d['Πόλη']}")
    st.sidebar.write(f"🔢 Ενημέρωση: {d['Ενημέρωση']}")
    st.sidebar.write(f"📅 Ημερομηνία: {d['Ημερομηνία Επίσκεψης']}")
    st.sidebar.write(f"📝 Παρατηρήσεις: {d['Παρατηρήσεις']}")
