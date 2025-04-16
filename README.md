# Smart Corrosion Detection System (IoT-Simulated)

This project simulates a smart corrosion detection system using Python and OpenCV. It mimics an IoT device that captures live camera feed, analyzes corrosion status and severity, and logs the output data to a live Google Sheet using Google Sheets API.

---

## 📌 Features

- Real-time video feed from webcam
- Rust/corrosion detection using HSV color filtering
- Edge-based severity classification (`Low`, `Medium`, `High`)
- Logs timestamp, corrosion status, severity, and edge density to Google Sheets
- Simulates an IoT-based data pipeline

---

## 🔧 Technologies Used

- Python
- OpenCV
- Google Sheets API
- OAuth2 (Service Account Authentication)

---

## ⚙️ How It Works

1. Captures live webcam input
2. Detects if the surface is metallic (for relevance)
3. Identifies rust-colored regions using color filtering
4. Calculates edge density to assess corrosion severity
5. Logs real-time data into a connected Google Sheet

---

## 📥 Output Parameters Logged

- **Timestamp**
- **Corrosion Status** (`Corroded` / `Not Corroded`)
- **Corrosion Severity** (`Low`, `Medium`, `High`)
- **Edge Density** (in %)

---

## 🖼️ Sample Output

The `outputs/` folder contains:
- `corrosion_sample_1.png` – Snapshot showing detected rust on metal surface
- `google_sheet_log.png` – Screenshot of data logged to Google Sheet

---

## 🚀 Run the Project

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Install dependencies
pip install -r requirements.txt
🔐 Google API Credentials Required
⚠️ For security reasons, the actual credentials.json is not included in this repository.
Please use your own Google service account key file and place it in the project’s root folder.

To understand the required format, a sample file credentials_sample.json is provided for reference.

# Run the project
python main.py
