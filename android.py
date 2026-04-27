# termux-api integration
def share(text):
    subprocess.run(f"termux-share -t 'Nano AI' -c '{text}'")

def toast(msg):
    subprocess.run(f"termux-toast '{msg}'")