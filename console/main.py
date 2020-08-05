import threading
from app.events import *


while True:
    try:
        threading.Thread(target=print('Hello world')).start()
    except KeyboardInterrupt:
        exit()