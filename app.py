import streamlit as st
import pandas as pd

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(layout="wide")

# -------------------
# MOCK DATA GENERATOR (Fallback)
# -------------------
def get_mock_data():
    return pd.DataFrame({
        "Ημερομηνία Επίσκεψης": ["01/03/2026", "15/03/2026"],
        "Προϊόν": ["Προϊόν Α", "Προϊόν Β"],
        "Ενημέρωση": ["Update 1", "Update 1"],
        "Αλυσίδα": ["Supermarket A", "Supermarket B"],
        "Διεύθυνση Καταστήματος": ["Λεωφ. Κηφισίας 100", "Εγνατία 50"],
        "Πόλη": ["Αθήνα", "Θεσσαλονίκη"],
        "Παρατηρήσεις": ["Όλα καλά", "Χρειάζεται αναπλήρωση"],
        "Φωτογραφία Merchandiser 1": [
            "https://via.placeholder.com/300x400.png?text=Stand+1",
            "https://via.placeholder.com/300x400.png?text=Stand+2"
        ]
    })

# -------------------
# LOAD DATA
# -------------------
# Διαβάζει το URL από τα secrets (.streamlit/secrets.toml)
# Αν δεν υπάρχει, χρησιμοποιεί dummy δεδομένα για επίδειξη
if "DATA_URL" in st.secrets:
    sheet_url = st.secrets["DATA_URL"]
    df = pd.read_csv(sheet_url)
else:
    df = get_mock_data()

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
    1: "Ιανουάριος", 2: "Φεβρουάριος", 3: "Μάρτιος", 4: "Απρίλιος",
    5: "Μάιος", 6: "Ιούνιος", 7: "Ιούλιος", 8: "Αύγουστος",
    9: "Σεπτέμβριος", 10: "Οκτώβριος", 11: "Νοέμβριος", 12: "Δεκέμβριος"
}

df["Μήνας"] = df["Ημερομηνία Επίσκεψης"].dt.month.map(month_map)

# -------------------
# TITLE
# -------------------
st.title("Store Stand Viewer")

# -------------------
# SEARCH
# -------------------
search = st.text_input("🔍 Αναζήτηση (αλυσίδα, πόλη, παρατήρηση...)")

# -------------------
# FILTERS (ONE ROW)
# -------------------
col1, col2, col3 = st.columns(3)

with col1:
    months_available = sorted(df["Μήνας"].dropna().unique())
    month = st.selectbox("Μήνας", months_available) if months_available else None

with col2:
    products_available = df["Προϊόν"].dropna().unique()
    product = st.selectbox("Προϊόν", products_available) if len(products_available) > 0 else None

with col3:
    updates_available = df["Ενημέρωση"].dropna().unique()
    update_no = st.selectbox("Ενημέρωση", updates_available) if len(updates_available) > 0 else None

# -------------------
# FILTER DATA
# -------------------
filtered = df.copy()

if month:
    filtered = filtered[filtered["Μήνας"] == month]
if product:
    filtered = filtered[filtered["Προϊόν"] == product]
if update_no:
    filtered = filtered[filtered["Ενημέρωση"] == update_no]

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
    "Φωτογραφία Merchandiser 1", "Φωτογραφία Merchandiser 2",
    "Φωτογραφία Merchandiser 3", "Φωτογραφία Merchandiser 4",
    "Φωτογραφία Merchandiser 5", "Φωτογραφία Πωλητή 1",
    "Φωτογραφία Πωλητή 2", "Φωτογραφία Πωλητή 3",
    "Φωτογραφία Πωλητή 4", "Φωτογραφία Πωλητή 5"
]

# Keep only image columns that exist in the dataframe
image_cols = [c for c in image_cols if c in filtered.columns]

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

if all_images:
    cols = st.columns(5)
    for i, (img, row) in enumerate(all_images):
        with cols[i % 5]:
            st.image(str(img).strip(), use_container_width=True)
            if st.button("📌 See Details", key=f"img_{i}"):
                st.session_state.selected_row = row.to_dict()
else:
    st.warning("Δεν βρέθηκαν φωτογραφίες με τα επιλεγμένα κριτήρια.")

# -------------------
# SIDEBAR DETAILS
# -------------------
if st.session_state.selected_row:
    d = st.session_state.selected_row

    st.sidebar.title("📌 Details")
    st.sidebar.write(f"🏬 Αλυσίδα: {d.get('Αλυσίδα', '-')}")
    st.sidebar.write(f"📍 Οδός: {d.get('Διεύθυνση Καταστήματος', '-')}")
    st.sidebar.write(f"🏙️ Πόλη: {d.get('Πόλη', '-')}")
    st.sidebar.write(f"🔢 Ενημέρωση: {d.get('Ενημέρωση', '-')}")
    st.sidebar.write(f"📅 Ημερομηνία: {d.get('Ημερομηνία Επίσκεψης', '-')}")
    st.sidebar.write(f"📝 Παρατηρήσεις: {d.get('Παρατηρήσεις', '-')}")
