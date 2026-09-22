🏬 Store Stand Viewer

A streamlined, interactive Streamlit dashboard designed for retail operations, field sales representatives, and trade marketing teams to inspect product stand installations, review store visit logs, and analyze merchandise display photos across various retail chains.

🌟 Key Features

Interactive Photo Grid: Dynamically loads and presents store stand images in an organized grid layout.

Detailed Sidebar Inspection: Click on any photo to view detailed store context (retail chain, address, city, visit date, update round, and merchandiser field notes).

Multi-Filter System: Filter dataset records simultaneously by Month, Product line, and Update number.

Global Text Search: Instantly search across all fields (store names, cities, specific remarks, etc.).

Zero External Dependencies: Built with built-in mock data generation (picsum.photos integration) for seamless standalone demonstration without requiring database/API credentials.

🛠️ Tech Stack & Dependencies

Python 3.10+

Streamlit: Web application framework for data apps.

Pandas: Data manipulation and processing.

📁 Project Structure

Store-Stand-Viewer/
│
├── app.py              # Main Streamlit application entry point
├── requirements.txt    # Python dependencies
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation


🚀 Getting Started (Run Locally)

Follow these steps to run the application on your local machine:

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/Retail-Dashboard.git
cd Retail-Dashboard


2. Create and Activate a Virtual Environment

# On macOS / Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate


3. Install Requirements

Create a requirements.txt file (if not present) with the following contents:

streamlit
pandas


Then run:

pip install -r requirements.txt


4. Launch the App

streamlit run app.py


The application will open automatically in your browser at http://localhost:8501.

🔌 Architecture & Data Sources

This application is built with flexibility in mind:

Standalone Mock Mode (Default): Generates structured sample retail data on the fly. Ideal for portfolio demonstrations, UI testing, and public deployment without exposing sensitive client data.

Production / Google Sheets Integration: Can easily be adapted to read directly from a live Google Sheet or CSV URL by linking a private URL inside .streamlit/secrets.toml.

📝 License

Distributed under the MIT License. See LICENSE for more information.
