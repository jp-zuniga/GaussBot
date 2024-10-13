from customtkinter import CTkFrame as ctkFrame, CTkButton as ctkButton

class HomeFrame(ctkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # Add settings button
        self.settings_button = ctkButton(self, text="Opciones", command=self.open_settings)
        self.settings_button.grid(row=3, column=0, padx=20, pady=10)

        # Add close program button
        self.close_button = ctkButton(self, text="Cerrar aplicación", command=self.close_program)
        self.close_button.grid(row=4, column=0, padx=20, pady=10)

    def open_settings(self):
        # Placeholder for settings button functionality
        self.app.select_frame_by_name("settings")

    def close_program(self):
        # Close the application
        self.app.quit()