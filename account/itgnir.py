import subprocess


class ITGNIR:
    def __init__(self, path):
        self.path = path

    def check_network(self):
        output = subprocess.check_output('tasklist', shell=True, text=True)
        if "ITGNIR_original.exe" in output:
            return True

    def start_network(self):
        try:
            subprocess.run(f'{self.path} network', shell=True, check=True)
            print(f"ITGNIR has been started")
        except FileNotFoundError:
            print(f"{self.path} does not exist")
        except subprocess.CalledProcessError:
            print(f"Failed to start ITGNIR network")


path = 'ITGNIR.lnk'
itgnir = ITGNIR(path)

if itgnir.check_network():
    print("ITGNIR is already running")
else:
    itgnir.start_network()
