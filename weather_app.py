import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = 'bd5e378503939ddaee76f12ad7a97608'

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("420x580")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.main_frame = tk.Frame(root, bg="#0f172a")
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        self.title_label = tk.Label(
            self.main_frame, text="WEATHER ATMOSPHERE", 
            font=("Segoe UI", 10, "bold"), bg="#0f172a", fg="#38bdf8"
        )
        self.title_label.pack(anchor="w")

        self.brand_label = tk.Label(
            self.main_frame, text="Weather App", 
            font=("Segoe UI", 16, "bold"), bg="#0f172a", fg="#ffffff"
        )
        self.brand_label.pack(anchor="w", pady=(0, 20))

        self.search_container = tk.Frame(self.main_frame, bg="#1e293b", bd=0)
        self.search_container.pack(fill="x", pady=(0, 15))
        
        self.entry_pad = tk.Frame(self.search_container, bg="#1e293b")
        self.entry_pad.pack(side="left", fill="x", expand=True, padx=12, pady=8)

        self.city_entry = tk.Entry(
            self.entry_pad, font=("Segoe UI", 12), bg="#1e293b", fg="#ffffff",
            bd=0, insertbackground="white", highlightthickness=0
        )
        self.city_entry.pack(fill="x")
        self.city_entry.insert(0, "Detecting location...")

        self.search_btn = tk.Button(
            self.search_container, text="Search", font=("Segoe UI", 11, "bold"),
            bg="#38bdf8", fg="#0f172a", activebackground="#0ea5e9", activeforeground="#0f172a",
            command=self.search_city, relief="flat", padx=18, pady=6, cursor="hand2"
        )
        self.search_btn.pack(side="right")

        self.detect_btn = tk.Button(
            self.main_frame, text="⚡ Auto-Detect My Location", font=("Segoe UI", 10, "bold"),
            bg="#1e293b", fg="#94a3b8", activebackground="#334155", activeforeground="#ffffff",
            command=self.auto_detect, relief="flat", bd=0
        )
        self.detect_btn.pack(fill="x", pady=(0, 25))

        self.card = tk.Frame(self.main_frame, bg="#1e293b", highlightbackground="#334155", highlightthickness=1)
        self.card.pack(fill="both", expand=True)

        self.icon_lbl = tk.Label(self.card, text="✨", font=("Segoe UI", 56), bg="#1e293b", fg="#38bdf8")
        self.icon_lbl.pack(pady=(25, 5))

        self.temp_lbl = tk.Label(self.card, text="--°", font=("Segoe UI Semibold", 52), bg="#1e293b", fg="#ffffff")
        self.temp_lbl.pack()

        self.location_lbl = tk.Label(self.card, text="Location Syncing...", font=("Segoe UI", 15, "bold"), bg="#1e293b", fg="#ffffff")
        self.location_lbl.pack(pady=(5, 2))

        self.desc_lbl = tk.Label(self.card, text="Please wait", font=("Segoe UI", 11), bg="#1e293b", fg="#94a3b8")
        self.desc_lbl.pack(pady=(0, 25))

        self.metrics_frame = tk.Frame(self.card, bg="#0f172a", height=70)
        self.metrics_frame.pack(fill="x", side="bottom")
        self.metrics_frame.pack_propagate(False)

        self.hum_box = tk.Frame(self.metrics_frame, bg="#0f172a")
        self.hum_box.pack(side="left", fill="both", expand=True, pady=12)
        self.humidity_lbl = tk.Label(self.hum_box, text="--%", font=("Segoe UI", 13, "bold"), bg="#0f172a", fg="#ffffff")
        self.humidity_lbl.pack()
        self.hum_title = tk.Label(self.hum_box, text="HUMIDITY", font=("Segoe UI", 8, "bold"), bg="#0f172a", fg="#64748b")
        self.hum_title.pack()

        self.sep = tk.Frame(self.metrics_frame, bg="#1e293b", width=1)
        self.sep.pack(side="left", fill="y", pady=15)

        self.wind_box = tk.Frame(self.metrics_frame, bg="#0f172a")
        self.wind_box.pack(side="right", fill="both", expand=True, pady=12)
        self.wind_lbl = tk.Label(self.wind_box, text="-- m/s", font=("Segoe UI", 13, "bold"), bg="#0f172a", fg="#ffffff")
        self.wind_lbl.pack()
        self.wind_title = tk.Label(self.wind_box, text="WIND SPEED", font=("Segoe UI", 8, "bold"), bg="#0f172a", fg="#64748b")
        self.wind_title.pack()

        self.root.after(100, self.auto_detect)

    def select_icon(self, description):
        text = description.lower()
        if "cloud" in text: return "☁️"
        if "rain" in text or "drizzle" in text: return "🌧️"
        if "thunder" in text: return "⛈️"
        if "snow" in text: return "❄️"
        if "clear" in text or "sun" in text: return "☀️"
        if "mist" in text or "haze" in text or "fog" in text: return "🌫️"
        return "✨"

    def update_dashboard(self, data):
        city = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        self.location_lbl.config(text=f"{city}, {country}")
        self.temp_lbl.config(text=f"{round(temp)}°")
        self.desc_lbl.config(text=description.upper())
        self.humidity_lbl.config(text=f"{humidity}%")
        self.wind_lbl.config(text=f"{wind_speed} m/s")
        self.icon_lbl.config(text=self.select_icon(description))

    def get_weather(self, query, search_type="name"):
        try:
            if search_type == "coords":
                url = f"http://api.openweathermap.org/data/2.5/weather?lat={query[0]}&lon={query[1]}&appid={API_KEY}&units=metric"
            else:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}&units=metric"

            response = requests.get(url)
            weather_data = response.json()

            if weather_data.get("cod") == 200:
                self.update_dashboard(weather_data)
                self.city_entry.delete(0, tk.END)
                self.city_entry.insert(0, weather_data["name"])
            else:
                if search_type == "name":
                    messagebox.showerror("Error", f"City '{query.title()}' not found.")
        except requests.ConnectionError:
            messagebox.showerror("Network Error", "Please verify your internet connection.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def auto_detect(self):
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, "Locating...")
        self.root.update_idletasks()
        
        try:
            network_info = requests.get('http://ip-api.com/json/', timeout=4).json()
            
            if network_info.get("status") == "success":
                lat = network_info.get("lat")
                lon = network_info.get("lon")
                
                if 21.5 <= lat <= 24.5 and 84.5 <= lon <= 87.5:
                    lat, lon = 22.8046, 86.2029
                
                self.get_weather((lat, lon), search_type="coords")
            else:
                self.get_weather((22.8046, 86.2029), search_type="coords")
        except Exception:
            self.get_weather((22.8046, 86.2029), search_type="coords")

    def search_city(self):
        city = self.city_entry.get().strip()
        if city and city != "Locating...":
            self.get_weather(city)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()