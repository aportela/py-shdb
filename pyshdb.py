import sys

from src.boot import Boot

boot = Boot()

running = True
while running:
    running = boot.loop()

boot.end()

sys.exit(0)
