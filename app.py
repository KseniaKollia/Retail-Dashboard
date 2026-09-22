import streamlit as st
import pandas as pd

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(layout="wide", page_title="Store Stand Viewer")

# -------------------
# MOCK DATA GENERATOR
# -------------------
def get_mock_data():
    return pd.DataFrame({
        "Ημερομηνία Επίσκεψης": ["01/03/2026", "05/03/2026", "12/03/2026", "18/03/2026"],
        "Προϊόν": ["Προϊόν Α", "Προϊόν Β", "Προϊόν Α", "Προϊόν Γ"],
        "Ενημέρωση": ["Update 1", "Update 1", "Update 2", "Update 1"],
        "Αλυσίδα": ["Supermarket Alpha", "Supermarket Beta", "Supermarket Alpha", "Supermarket Gamma"],
        "Διεύθυνση Καταστήματος": ["Λεωφ. Κηφισίας 100", "Εγνατία 50", "Πανεπιστημίου 20", "Τσιμισκή 10"],
        "Πόλη": ["Αθήνα", "Θεσσαλονίκη", "Αθήνα", "Θεσσαλονίκη"],
        "Παρατηρήσεις": [
            "Πλήρης τοποθέτηση στο σταντ", 
            "Χρειάζεται αναπλήρωση σε 2 κωδικούς", 
            "Τοποθετήθηκε νέο προωθητικό υλικό", 
            "Καλή παρουσίαση στην είσοδο"
        ],
        "Φωτογραφία Merchandiser 1": [
            "https://picsum.photos/id/10/400/500",
            "https://picsum.photos/id/20/400/500",
            "https://picsum.photos/id/30/400/500",
            "https://picsum.photos/id/40/400/500"
        ],
        "Φωτογραφία Merchandiser 2": [
            "https://picsum.photos/id/15/400/500",
            "",
            "https://picsum.photos/id/35/400/500",
            ""
        ]
    })

# -------------------
# LOAD DATA (Mock)
# -------------------
df = get_mock_data()
df.columns = df.columns.str.strip()

# -------------------
# DATE PARSING
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
st.title(" Store Stand Viewer (Portfolio Demo)")

# -------------------
# SEARCH
# -------------------
search = st.text_input("🔍 Αναζήτηση (αλυσίδα, πόλη, παρατήρηση...)")

# -------------------
# FILTERS
# -------------------
col1, col2, col3 = st.columns(3)

with col1:
    months_available = ["Όλοι"] + sorted(df["Μήνας"].dropna().unique().tolist())
    month = st.selectbox("Μήνας", months_available)

with col2:
    products_available = ["Όλα"] + df["Προϊόν"].dropna().unique().tolist()
    product = st.selectbox("Προϊόν", products_available)

with col3:
    updates_available = ["Όλες"] + df["Ενημέρωση"].dropna().unique().tolist()
    update_no = st.selectbox("Ενημέρωση", updates_available)

# -------------------
# FILTER DATA
# -------------------
filtered = df.copy()

if month != "Όλοι":
    filtered = filtered[filtered["Μήνας"] == month]
if product != "Όλα":
    filtered = filtered[filtered["Προϊόν"] == product]
if update_no != "Όλες":
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
    "Φωτογραφία Merchandiser 1", 
    "Φωτογραφία Merchandiser 2"
]

# -------------------
# STATE
# -------------------
if "selected_row" not in st.session_state:
    st.session_state.selected_row = None

if st.session_state.selected_row is None:
    st.info("👉 Πάτησε σε μια φωτογραφία για να δεις λεπτομέρειες στο sidebar")

# -------------------
# GRID DISPLAY
# -------------------
st.subheader("📸 Φωτογραφίες Stand")

all_images = []

for _, row in filtered.iterrows():
    for col_name in image_cols:
        img = row.get(col_name)
        if pd.notna(img) and str(img).strip():
            all_images.append((img, row))

if all_images:
    cols = st.columns(4)
    for i, (img, row) in enumerate(all_images):
        with cols[i % 4]:
            st.image(str(img).strip(), use_container_width=True)
            if st.button("📌 Details", key=f"img_{i}"):
                st.session_state.selected_row = row.to_dict()
else:
    st.warning("Δεν βρέθηκαν αποτελέσματα για τα επιλεγμένα φίλτρα.")

# -------------------
# SIDEBAR DETAILS
# -------------------
if st.session_state.selected_row:
    d = st.session_state.selected_row

    st.sidebar.title("📌 Λεπτομέρειες Stand")
    st.sidebar.write(f"🏬 **Αλυσίδα:** {d.get('Αλυσίδα', '-')}")
    st.sidebar.write(f"📍 **Διεύθυνση:** {d.get('Διεύθυνση Καταστήματος', '-')}")
    st.sidebar.write(f"🏙️ **Πόλη:** {d.get('Πόλη', '-')}")
    st.sidebar.write(f"🔢 **Ενημέρωση:** {d.get('Ενημέρωση', '-')}")
    
    date_val = d.get('Ημερομηνία Επίσκεψης', '-')
    if pd.notna(date_val):
        date_str = pd.to_datetime(date_val).strftime('%d/%m/%Y')
    else:
        date_str = '-'
        
    st.sidebar.write(f"📅 **Ημερομηνία:** {date_str}")
    st.sidebar.write(f"📝 **Παρατηρήσεις:** {d.get('Παρατηρήσεις', '-')}")
