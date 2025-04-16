import cv2
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets authentication
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Corrosion Detection Data").sheet1
    return sheet

# Function to detect if the object is metal
def is_metal(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = np.mean(hsv[:, :, 1])

    # Metal: High brightness & Low saturation
    return brightness > 110 and saturation < 80  # Adjust if needed

# Detect corrosion and log data to Google Sheets
def detect_corrosion_live():
    cap = cv2.VideoCapture(1)  # 0 for built-in webcam, 1 for external webcam
    if not cap.isOpened():
        print("Error: Could not access the webcam!")
        return

    sheet = authenticate_google_sheets()  # Authenticate and get the Google Sheet

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame!")
            break

        # Step 1: Detect Metal or Non-Metal
        if not is_metal(frame):
            corrosion_status = "Not Corroded (Plastic/Non-Metal)"
            corrosion_color = (0, 255, 0)  # Green
            cv2.putText(frame, corrosion_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, corrosion_color, 2)
            cv2.imshow("Live Corrosion Detection", frame)
            
            # Log the data to Google Sheets (Non-Metal)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([timestamp, corrosion_status, "N/A", "N/A", "N/A"])
        
        else:
            # Convert to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Rust color range
            lower_rust = np.array([5, 60, 40])
            upper_rust = np.array([35, 255, 255])

            # Rust Mask
            rust_mask = cv2.inRange(hsv, lower_rust, upper_rust)

            # Count rust pixels
            rust_pixels = cv2.countNonZero(rust_mask)
            total_pixels = frame.shape[0] * frame.shape[1]
            rust_ratio = (rust_pixels / total_pixels) * 100

            # Default corrosion status
            corrosion_status = "Not Corroded"
            corrosion_color = (0, 255, 0)  # Green

            # If corrosion is detected, apply edge detection
            if rust_ratio > 3:  # Rust detected (Threshold adjustable)
                corrosion_status = "Corroded"
                corrosion_color = (0, 0, 255)  # Red

                # Convert to grayscale and apply adaptive thresholding
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (3, 3), 0)
                edges = cv2.Canny(blurred, 20, 80)

                # Count edge pixels in rust area
                edge_pixels = cv2.countNonZero(edges)

                # Calculate more accurate edge density
                edge_density = (edge_pixels / rust_pixels) * 100 if rust_pixels > 0 else 0

                # Updated Edge Density Classification
                if edge_density < 1:
                    corrosion_severity = "Low Corrosion"
                    severity_color = (0, 255, 0)  # Green
                elif edge_density < 5:  # Lowered threshold for Medium Corrosion
                    corrosion_severity = "Medium Corrosion"
                    severity_color = (0, 165, 255)  # Orange
                else:
                    corrosion_severity = "High Corrosion"
                    severity_color = (0, 0, 255)  # Red

                # Display corrosion severity
                cv2.putText(frame, corrosion_severity, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, severity_color, 2)

                # Log data to Google Sheets
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.append_row([timestamp, corrosion_status, corrosion_severity, rust_ratio, edge_density])

                # Show edge detection output
                cv2.imshow("Edge Detection", edges)

            # Display corrosion status
            cv2.putText(frame, corrosion_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, corrosion_color, 2)
            cv2.imshow("Rust Mask", rust_mask)

        # Show live webcam feed with rust detection
        cv2.imshow("Live Corrosion Detection", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the live corrosion detection and logging
detect_corrosion_live()
