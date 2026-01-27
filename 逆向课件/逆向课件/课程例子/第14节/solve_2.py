#!/usr/bin/env python3

import base64

correct = b''


get = base64.b64decode(correct)
for item in get:
    item = (item - 16) % 256
    print(chr(item ^ 32), end="")
    

