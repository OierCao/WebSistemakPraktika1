import psutil
import time
def cpu_ram():
    while True:
        # KODEA: psutil liburutegia erabiliz, %CPU eta %RAM atera
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
        time.sleep(5)

if __name__ == "__main__":
    cpu_ram()