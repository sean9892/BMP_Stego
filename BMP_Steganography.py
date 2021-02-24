import os
import struct
import tkinter as tk
from tkinter import filedialog
from gmpy2 import iroot


# Convert Integer to Hex(Little Endian)
def hexLE(x):
    return struct.pack('l', x).hex()


def fileChoose():
    root = tk.Tk()
    root.withdraw()
    pth = filedialog.askopenfilename()
    assert pth != '', "No file choosed"
    return pth


def findFactor(k):
    r = []
    f = 1
    while f * f <= k:
        if k % f == 0:
            r.append(f)
            r.append(k // f)
        f += 1
    return tuple(set(r))


def main():
    pth = fileChoose()
    with open(pth, "rb") as f:
        binary = f.read()
    L = len(binary)
    wid = None
    if L % 3 != 0:
        binary = os.urandom(3 - L % 3) + binary
        L = len(binary)
    if iroot(L // 3, 2)[1]:
        wid = int(iroot(L // 3, 2)[0])
    else:
        wid = int(iroot(L // 3, 2)[0]) + 1
        binary = os.urandom(3 * (wid ** 2 - L // 3)) + binary
        L = len(binary)

    assert L % 3 == 0, "Data cannot be RGB raw data"
    assert L == len(binary), "L must be length of binary"

    # BITMAPFILEHEADER
    bfType     = b'BM'
    bfSize     = bytes.fromhex(hexLE(L + 0x8A))
    bfReserved = bytes.fromhex("00000000")
    bfOffBits  = bytes.fromhex("8A000000")

    FILEHEADER = bfType + bfSize + bfReserved + bfOffBits

    # BITMAPINFOHEADER
    biSize          = bytes.fromhex("7C000000")
    biWidth         = bytes.fromhex(hexLE(wid)) # Need to change
    biHeight        = bytes.fromhex(hexLE(wid)) # Need to change
    biPlanes        = bytes.fromhex("0100")
    biBitCount      = bytes.fromhex("1800")
    biCompression   = bytes.fromhex("00000000")
    biSizeImage     = bytes.fromhex(hexLE(L))
    biXPelsPerMeter = bytes.fromhex("27000000")
    biYPelsPerMeter = bytes.fromhex("27000000")
    biClrUsed       = bytes.fromhex("00000000")
    biClrImportant  = bytes.fromhex("00000000")

    INFOHEADER = biSize + biWidth + biHeight + biPlanes + biBitCount + biCompression + biSizeImage + biXPelsPerMeter + biYPelsPerMeter + biClrUsed + biClrImportant

    DUMMY = os.urandom(84)

    npth = pth
    filename = npth.split("/")[-1]
    if filename.find(".") == -1:
        npth = npth + ".bmp"
    else:
        filename = '.'.join(filename.split(".")[:-1]) + ".bmp"
        npth = '/'.join(npth.split("/")[:-1]) + "/" + filename

    with open(npth, "wb") as f:
        DATA = FILEHEADER + INFOHEADER + DUMMY + binary
        f.write(DATA)

if __name__ == '__main__':
    main()
