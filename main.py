from gauss_bot.managers.main_manager import OpsManager, MatricesManager, VectoresManager

if __name__ == "__main__":
    manager = OpsManager(MatricesManager(), VectoresManager())
    manager.start_exec_loop()
