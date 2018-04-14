import os
import sys

path = os.path.dirname(__file__)
path = os.path.join(os.path.dirname(path), 'meowth')
print(path)

if path not in sys.path:
    sys.path.append(path)