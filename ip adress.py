import requests
import tkinter as tk
from tkinter import messagebox
import webbrowser  # To open Google Maps

# Ramnagar, Hanamkonda Coordinates
DEFAULT_LOCATION = {
    'ip': 'Your IP',
    'city': 'Ramnagar',
    'region': 'Telangana',
    'country': 'India',
    'zip': '506001',
    'isp': 'Your ISP',
    'lat': 17.9905,
    'lon': 79.5603
}

def display_default_location():
    info = f"""
===============================
📍 IP Geolocation Report 📍
===============================
IP Address      : {DEFAULT_LOCATION['ip']}
City            : {DEFAULT_LOCATION['city']}
Region          : {DEFAULT_LOCATION['region']}
Country         : {DEFAULT_LOCATION['country']}
ZIP Code        : {DEFAULT_LOCATION['zip']}
ISP             : {DEFAULT_LOCATION['isp']}
Coordinates     : {DEFAULT_LOCATION['lat']}, {DEFAULT_LOCATION['lon']}
===============================
✅ This is your current location.
===============================
"""
    result_label.config(text=info)

    # Open Google Maps automatically to default location
    maps_url = f"https://www.google.com/maps?q={DEFAULT_LOCATION['lat']},{DEFAULT_LOCATION['lon']}"
    webbrowser.open(maps_url)

def fetch_ip_location():
    ip_address = ip_entry.get().strip()

    if not ip_address:
        messagebox.showwarning("Input Required", "Please enter an IP address.")
        return

    try:
        location_response = requests.get(f"http://ip-api.com/json/{ip_address}")
        location_response.raise_for_status()
        location_data = location_response.json()

        if location_data.get('status') == 'fail':
            messagebox.showerror("Error", f"Invalid IP address: {ip_address}")
            return

        latitude = location_data.get('lat')
        longitude = location_data.get('lon')

        info = f"""
===============================
📍 IP Geolocation Report 📍
===============================
IP Address      : {ip_address}
City            : {location_data.get('city')}
Region          : {location_data.get('regionName')}
Country         : {location_data.get('country')}
ZIP Code        : {location_data.get('zip')}
ISP             : {location_data.get('isp')}
Coordinates     : {latitude}, {longitude}
===============================
✅ Data Fetched Successfully!
===============================
"""
        result_label.config(text=info)

        # Open Google Maps automatically
        maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
        webbrowser.open(maps_url)

    except Exception as e:
        messagebox.showerror("Error", f"❌ Error fetching location!\n\n{str(e)}")

# Create GUI Window
window = tk.Tk()
window.title("User IP Geolocation Finder")
window.geometry("550x600")
window.config(bg="#FFFBF0")
window.resizable(False, False)

# Header
header = tk.Label(window, text="🌍 Enter IP Address to Find Location 🌍", bg="#FFFBF0", fg="#3E4E50", font=("Arial", 16, "bold"))
header.pack(pady=20)

# Input Field
ip_entry = tk.Entry(window, width=30, font=("Arial", 14), bd=2, relief="solid", fg="#3E4E50")
ip_entry.pack(pady=10)

# Fetch Button
fetch_button = tk.Button(window, text="Get Geolocation", command=fetch_ip_location, bg="#27AE60", fg="white", font=("Arial", 14), padx=10, pady=5, activebackground="#1E8449")
fetch_button.pack(pady=20)

# Result Display Label
result_label = tk.Label(window, text="", bg="#FFFFFF", fg="#3E4E50", font=("Courier", 12), justify="left", anchor="w", bd=2, relief="solid", padx=10, pady=10)
result_label.pack(padx=20, pady=20, fill="both", expand=True)

# Show your location when the app starts
display_default_location()

# Run the GUI
window.mainloop()
