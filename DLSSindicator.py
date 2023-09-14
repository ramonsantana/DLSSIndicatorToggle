import tkinter as tk
import winreg

# Define colors and fonts
dark_bg = "#2D2D2D"
dark_fg = "#FFFFFF"
button_hover_color = "#3D3D3D"
font_style = ("Helvetica", 14)

def add_button_border(button):
    # Configure button appearance with border and hover effects
    button.config(
        relief="solid",
        borderwidth=2,
        font=font_style,
        bg=dark_bg,
        fg=dark_fg,
    )
    # Button hover effect on mouse enter
    button.bind("<Enter>", lambda e: button.config(bg=button_hover_color))
    button.bind("<Leave>", lambda e: button.config(bg=dark_bg))

class DLSSIndicatorApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("DLSS Indicator Toggle")
        self.geometry("400x260")
        self.configure(bg=dark_bg)

        main_frame = tk.Frame(self, bg=dark_bg)
        main_frame.pack()

        title_label = tk.Label(main_frame, text="DLSS Indicator On/Off", font=("Helvetica", 24), bg=dark_bg, fg=dark_fg)
        toggle_button = tk.Button(main_frame, text="Toggle", command=self.toggle_dlss_indicator, justify="center")
        self.indicator_label = tk.Label(main_frame, text="", font=("Helvetica", 18), bg=dark_bg, fg=dark_fg)
        close_button = tk.Button(main_frame, text="Close", command=self.close_app, justify="center")

        add_button_border(toggle_button)
        add_button_border(close_button)

        title_label.pack(pady=20)
        toggle_button.pack(pady=10)
        self.indicator_label.pack()
        close_button.pack(pady=10)

        # Preventing the File from Being Detected as a Trojan:
        # To avoid false positive detections and ensure proper execution,
        # I've removed any code related to the fade effect, which was
        # previously associated with trojan-like behavior. 

        initial_state = self.get_dlss_indicator_state()
        self.update_title_label(initial_state)

    def get_dlss_indicator_state(self):
        try:
            key_path = r"SOFTWARE\NVIDIA Corporation\Global\NGXCore"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ) as key:
                return winreg.QueryValueEx(key, "ShowDlssIndicator")[0]
        except Exception as e:
            # Log and handle any error when reading the DLSS Indicator state
            print(f"Error reading DLSS Indicator state: {str(e)}")
            return 0  # Default to "Off"

    def toggle_dlss_indicator(self):
        try:
            key_path = r"SOFTWARE\NVIDIA Corporation\Global\NGXCore"
            current_state = self.get_dlss_indicator_state()
            new_state = 0 if current_state == 0x400 else 0x400  # Toggle between "On" (0x400) and "Off" (0)

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                # Set the DLSS Indicator state in the Windows registry
                winreg.SetValueEx(key, "ShowDlssIndicator", 0, winreg.REG_DWORD, new_state)
                self.update_title_label(new_state)

        except Exception as e:
            # Log and handle any error when toggling the DLSS Indicator
            print(f"Failed to toggle DLSS Indicator: {str(e)}")

    def close_app(self):
        # Close the application
        self.destroy()

    def update_title_label(self, new_value):
        # Update the label to display the current DLSS Indicator state
        self.indicator_label.config(text=f"DLSS Indicator is {'On' if new_value == 0x400 else 'Off'}")

if __name__ == "__main__":
    app = DLSSIndicatorApp()
    app.mainloop()
