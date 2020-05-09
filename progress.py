from PIL import Image, JpegImagePlugin
from io import BytesIO

MARKER = {
    b'\xff\xc4': ("DHT", "Define Huffman table"),
    b'\xff\xd9' : ("EOI", "End of image"),
    b'\xff\xda': ("SOS", "Start of scan"),
}

def progress(fp: str):
    """
    Reads from path and convert to BytesIO Object then
    convert to Image object from PIL

    =================================================

    **Arguments**

    - **fp** :  A str file path

    """
    # rData = open(fp, 'rb')
    scans= []
    with open(fp, 'rb') as rData:
        # l = len(rData.read())
        # rData.seek(0)
        stream = b''
        END = False
        counter = 0

        while not END:
            current_Byte = rData.read(1)
            stream += current_Byte

            if int.from_bytes(current_Byte, 'big') == 255:
                current_pos = rData.tell()
                indicator = current_Byte + rData.read(1)
                rData.seek(current_pos)

                if indicator in MARKER:
                    mode = MARKER[indicator]
                    if mode[0] == "EOI":
                        END = True
                    elif mode[0] == "SOS":
                        stream += rData.read(1)
                        if counter == 0:
                            counter = 1
                            continue
                        else:
                            counter = 0
                            # END = True
                            scan = stream[:-1] + b'\xd9'
                            scans.append(scan)
                            # print(stream)

    return scans










if __name__ == '__main__':
    # READ a file
    fp = open("huff_simple0-progressive.jpeg", 'rb')

    data= fp.read()
    print(data)
    #
    # stream = BytesIO(data[:-10])
    # print(stream)
    #
    # image = Image.open(stream)
    #
    # print(image)
    import matplotlib.pyplot as plt
    data = progress("huff_simple0-progressive.jpeg")
    for i in data:
        print(i)
    # print(data))
    #
    # s = BytesIO(data)
    # print(type(s))
    # image = Image.open(s)
    #
    # print(image)
    #
    # plt.imshow(image)



