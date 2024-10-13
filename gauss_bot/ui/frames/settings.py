from customtkinter import CTkFrame as ctkFrame, CTkButton as ctkButton

class SettingsFrame(ctkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Add buttons for changing settings
        self.change_theme_button = ctkButton(self, text="Change Theme", command=self.change_theme)
        self.change_theme_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.change_mode_button = ctkButton(self, text="Change Mode", command=self.change_mode)
        self.change_mode_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    def change_theme(self):
        # Placeholder for changing theme functionality
        print("Change Theme button clicked")

    def change_mode(self):
        # Placeholder for changing mode functionality
        print("Change Mode button clicked")