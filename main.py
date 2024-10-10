from gauss_bot.operaciones import OpsManager, MatricesManager, VectoresManager

if __name__ == "__main__":
    manager = OpsManager(MatricesManager(), VectoresManager())
    manager.start_exec_loop()
    input("Cerrando programa...")
