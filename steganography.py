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

def list_to_tuple(alist):
    
    alist_tuple = tuple()
    
    for element in alist:
        alist_tuple += (tuple(element), )
        
    return list(alist_tuple)

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
    
    for i in range(len(pixel_list)):
            
            for j in range(len(pixel_list[i])):
                
                for w in range(3):
                    
                    lsb_of_each_pixel += str(last_bit(pixel_list[i][j][w]))
                    
    delimiter_string_bin = to_bin("$$EOM")
    
    if delimiter_string_bin in lsb_of_each_pixel:
        lsb_of_each_pixel = lsb_of_each_pixel.split(delimiter_string_bin)[0]
    
    decoded_text = ""
    
    for i in range(0, len(lsb_of_each_pixel), 8):
        
        try:
            binary_int = int(lsb_of_each_pixel[i:i+8], 2)
            byte_number = binary_int.bit_length() + 7 // 8
            binary_array = binary_int.to_bytes(byte_number, "big")
            decoded_text += binary_array.decode('unicode_escape')
        except:
            decoded_text += ""       
            
    trimmed_decoded_text = decoded_text.replace("\\u2610", "")
    
    return f"Decoded message: {trimmed_decoded_text}\n"
    
    
def encode():
    
    while True:
        try:
            file = str(input("Image to encode: "))
            img = Image.open(file)
            break
        except:
            print("Image couldn't be loaded")
        

    width, height = img.size
    number_of_pixels = width * height

    message = str(input("What is the message you want to encode?"))
    
    bin_message = to_bin(message)
    
    message_bits_lower_than_pixels = False

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
        
    if message_bits_lower_than_pixels:
        bin_message += to_bin("$$EOM")
        
    pixels = img.load()
    pixel_list = numpy.array(img)
    
    message_divided_by_three_parts = []
    new_pixel_list = []
    
    for i in range(0, len(bin_message), 3):
        
        if len(bin_message[i:i+3]) != 3:
                message_divided_by_three_parts.append(bin_message[i:i+3] + " " * (3 - len(bin_message[i:i+3])))
        elif len(bin_message[i:i+3]) == 0:
            break
        else:
            message_divided_by_three_parts.append(bin_message[i:i+3])
    
    #Cada conjunto dentro da array message_divided_by_three_parts representa um pixel
    #Logo, só irá ser necessário considerar a altura caso o número de conjuntos (len(message...)) for maior do que a width
    
    times_to_change_row = math.ceil(len(message_divided_by_three_parts) / width)
    number_of_pixels_to_change = len(message_divided_by_three_parts)
    
    change_pixels = True
    
    image_type = imghdr.what(file)
    
    while change_pixels:
        
        for i in range(times_to_change_row): #Indíce da altura
        
            if not(change_pixels):
                break
            
            for j in range(len(pixel_list[i])):
                
                if not(change_pixels):
                    break
                
                for w in range(3):
                    
                    lsb = last_bit(pixel_list[i][j][w])
                    
                    if message_divided_by_three_parts[j][w]== "1" and lsb == 0:
                        pixel_list[i][j][w] += 1
                    elif message_divided_by_three_parts[j][w] == "0" and lsb == 1:
                        pixel_list[i][j][w] -= 1
                
                number_of_pixels_to_change -= 1
                
                if number_of_pixels_to_change == 0:
                    
                    change_pixels = False
                   
    encoded_image = Image.fromarray(pixel_list)
    encoded_image.save(f"{file.split('.')[0]}_encoded.{file.split('.')[1]}")
    
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
    
