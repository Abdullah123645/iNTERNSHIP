import customtkinter as ctk
from model import predict_rain
from utils import show_pie, show_box, show_heatmap

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("500x650")
root.title("🌧 Rainfall Prediction System")

title = ctk.CTkLabel(root, text="Rainfall Prediction", font=("Poppins", 22, "bold"))
title.pack(pady=20)

# Inputs
entries = {}


fields = [
"pressure","humidity","dew_point","cloud",
"sunshine","wind_direction","wind_speed"
]

for field in fields:
    label = ctk.CTkLabel(root, text=field)
    label.pack()

    entry = ctk.CTkEntry(root)
    entry.pack(pady=5)

    entries[field] = entry 

entry = ctk.CTkEntry(root, placeholder_text=f"Enter {field}")



# Prediction
result_label = ctk.CTkLabel(root, text="")
result_label.pack(pady=20)
def predict():

    try:
        data = []

        for f in fields:
            value = entries[f].get().strip()   # 🔥 strip added

            if value == "":
                result_label.configure(text=f"{f} is empty ❌")
                return

            try:
                num = float(value)
            except:
                result_label.configure(text=f"{f} must be number ❌")
                return

            data.append(num)

        print("Input Data:", data)  # DEBUG

        result = predict_rain(data)

        if result == 1:
            result_label.configure(text="🌧 Rain Expected", text_color="green")
        else:
            result_label.configure(text="☀ No Rain", text_color="orange")

    except Exception as e:
        print("Error:", e)
        result_label.configure(text="Error Occurred ❌")

# Buttons
ctk.CTkButton(root, text="Predict Rainfall", command=predict).pack(pady=10)
ctk.CTkButton(root, text="Show Pie Chart", command=show_pie).pack(pady=10)
ctk.CTkButton(root, text="Show Box Plot", command=show_box).pack(pady=10)
ctk.CTkButton(root, text="Show Heatmap", command=show_heatmap).pack(pady=10)

root.mainloop()