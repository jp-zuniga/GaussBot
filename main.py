from gauss_bot.gui import GaussUI

if __name__ == "__main__":
    app = GaussUI()
    app.after(0, lambda: app.state("zoomed"))  # maximizar ventana
    app.mainloop()  # ejecutar aplicacion
