import PIL
import numpy
import math
import imghdr

from PIL import Image

def to_bin(astring):

    hex_astring = (astring.encode("unicode_escape")).hex()
    bin_astring = bin(int('1' + hex_astring, 16))[3:]

    return bin_astring

def last_bit(integer):

    lsb = str(bin(integer))

    return int(lsb[len(lsb)-1])
    
def decode():

    while True:
        file = str(input("Image to decode:"))
        if imghdr.what(file) != 'png':
            print(f"Este tipo de steganograpfia não funciona com o formato .{imghdr.what(file)}")
        else:
            try:
                img = Image.open(file)
                break
            except:
                print("Image couldn't be loaded")

    pixels = img.load()
    pixel_list = numpy.array(img)

    lsb_of_each_pixel = ""
    
    pixel_depth = 0
    
    if img.mode == "RGBA":
        pixel_depth = 4
    else:
        pixel_depth = 3

    for i in range(len(pixel_list)):

            for j in range(len(pixel_list[i])):

                for w in range(pixel_depth):

                    lsb_of_each_pixel += str(last_bit(pixel_list[i][j][w]))

    delimiter_string_bin = to_bin("$$EOM")

    #We keep the left side which contains a valid message before the delimiter telling that the message has ended
    if delimiter_string_bin in lsb_of_each_pixel:
        lsb_of_each_pixel = lsb_of_each_pixel.split(delimiter_string_bin)[0]

    decoded_text = ""

    for i in range(0, len(lsb_of_each_pixel), 8):

        try:
            #Convert message into text
            binary_int = int(lsb_of_each_pixel[i:i+8], 2)
            byte_number = binary_int.bit_length() + 7 // 8
            binary_array = binary_int.to_bytes(byte_number, "big")
            decoded_text += binary_array.decode('unicode_escape')
        except:
            #If a certain binary sequence is not a valid character, we add a "" to the decoded_text
            decoded_text += ""

    trimmed_decoded_text = decoded_text.replace("\\u2610", "")

    return f"Decoded message: {trimmed_decoded_text}\n"


def encode():

    while True:
        #Check if the image that the user chose is an image the program can open
        try:
            file = str(input("Image to encode: "))
            img = Image.open(file)
            break
        except:
            print("Image couldn't be loaded")


    width, height = img.size
    number_of_pixels = width * height

    message = str(input("What is the message you want to encode?"))

    #Convert the message into bits
    bin_message = to_bin(message)

    message_bits_lower_than_pixels = False

    #If the message is too big to be represented in the image, we need to increase its size
    if math.ceil(len(bin_message) / 3) > number_of_pixels:
        print("A mensagem é demasiado longa para esta imagem")
        while True:
            auto_resize = str(input("Pretende aumentar manualmente a imagem ou que o programa aumente automaticamente? (M / A) "))

            if auto_resize == "M":
                return
            elif auto_resize == "A":
                img = img.resize((math.ceil(math.sqrt(math.ceil(len(bin_message) / 3))), math.ceil(math.sqrt(math.ceil(len(bin_message) / 3)))))
                width, height = img.size
                break
    else:
        message_bits_lower_than_pixels = True

    #Add a delimiter string so the decoder knows where the message stop
    if message_bits_lower_than_pixels:
        bin_message += to_bin("$$EOM")

    pixels = img.load()
    pixel_list = numpy.array(img)

    #Initialize array containing each transformation that is going to be performed to each rgb value of each pixel
    message_divided_by_parts = []
    
    pixel_depth = 0
    
    if img.mode == "RGBA":
        pixel_depth = 4
    elif img.mode == "RGB":
        pixel_depth = 3

    #The range is spaced by three because we are going to change up to three values of each pixel, so each element of the representation of the transformations the programs
    #is going to make is 3 digits long.
    for i in range(0, len(bin_message), pixel_depth):

        if len(bin_message[i:i+pixel_depth]) != pixel_depth:
                message_divided_by_parts.append(bin_message[i:i+pixel_depth] + " " * (pixel_depth - len(bin_message[i:i+pixel_depth])))
        elif len(bin_message[i:i+pixel_depth]) == 0:
            break
        else:
            message_divided_by_parts.append(bin_message[i:i+pixel_depth])

    #Each string inside the array represents the transformations for each rgb value of each pixel
    #Hence, we only need to loop through one more line of width if the division between the len of message_divided_by_three_parts is bigger than the width

    times_to_change_row = math.ceil(len(message_divided_by_parts) / width)
    number_of_pixels_to_change = len(message_divided_by_parts)

    keep_changing_pixels = True
    
    while keep_changing_pixels:

        for i in range(times_to_change_row): #Indíce da altura

            if not(keep_changing_pixels):
                break

            for j in range(len(pixel_list[i])):

                if not(keep_changing_pixels):
                    break

                for w in range(pixel_depth):

                    lsb = last_bit(pixel_list[i][j][w])

                    if message_divided_by_parts[j][w]== "1" and lsb == 0:
                        pixel_list[i][j][w] += 1
                    elif message_divided_by_parts[j][w] == "0" and lsb == 1:
                        pixel_list[i][j][w] -= 1

                number_of_pixels_to_change -= 1

                if number_of_pixels_to_change == 0:

                    keep_changing_pixels = False

    encoded_image = Image.fromarray(pixel_list)
    encoded_image.save(f"{file.split('.')[0]}_encoded.{file.split('.')[1]}")
    
    return img.mode

def interface():

    print("----------------------------------------------")
    print("LSB Steganography Encoder & Decoder")
    print("----------------------------------------------")
    print("Notice: This program only works with english characters.\n")
    print("In order to encode or decode an image, you have to store it inside the directory of this program.\n")

    print("1. Encode\n2. Decode\n3. Exit\n")

    #Block the program from quitting when non integer input is given by user
    while True:
        try:
            option = int(input("Choose an option (1, 2 or 3): "))
        except:
            print("Choose a number from the options.")

        if option == 1:
            print(encode())
            break
        elif option == 2:
            print(decode())
        elif option == 3:
            quit()
        else:
            print("Choose a number from the options")


interface()
