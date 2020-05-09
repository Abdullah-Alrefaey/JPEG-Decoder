from PIL import Image, JpegImagePlugin
from io import BytesIO

MARKER = {
    b'\xff\xc4': ("DHT", "Define Huffman table"),
    b'\xff\xc2': ("SOF2", "Progressive DCT"),
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
    scans= []
    with open(fp, 'rb') as rData:

        stream = b''
        END = False
        counterData = 0

        while not END:
            #
            # Continuously parsing the image file till
            # the end of the end of the image
            #

            current_Byte = rData.read(1)  # Read one byte at a time
            stream += current_Byte  # Update Stream

            if current_Byte == b'\xff':
                # Check for marker start

                current_pos = rData.tell()
                indicator = current_Byte + rData.read(1)  # Read the next byte
                rData.seek(current_pos) # Reset stream Position

                if indicator in MARKER: # If False -- Ignore Spacings and Junk
                    mode = MARKER[indicator]

                    if mode[0] == "SOF2":  # Identify Progressive marker
                        print(mode[1])

                    if mode[0] == "EOI":   # Identify image end
                        END = True

                    if mode[0] == "SOS":   # Start of huffman

                        current_pos = rData.tell()
                        stream += rData.read(1)

                        if counterData == 0: # if first Occurance Ignore
                            counterData = 1
                            continue

                        if counterData == 1: # if second time the scan ended and save
                            # TODO : Check for case with multiple dhts
                            rData.seek(current_pos-1)
                            scan = stream[:-1] + b'\xd9'
                            stream = stream[:-2]
                            scans.append(scan)
                            counterData = 0


    return scans










if __name__ == '__main__':
    # READ a file
    fp = open("progress.jpg", 'rb')

    data= fp.read()
    print(data.hex())
    #
    # stream = BytesIO(data[:-10])
    # print(stream)
    #
    # image = Image.open(stream)
    #
    # print(image)
    import matplotlib.pyplot as plt
    data = progress("progress.jpg")
    for i in data:
        print(i.hex())
    # print(data[])
    #
    # s = BytesIO(data)
    # print(type(s))
    # image = Image.open(s)
    #
    # print(image)
    #
    # plt.imshow(image)



