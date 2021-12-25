import PIL
import numpy
import math
import imghdr
import binascii

from PIL import Image

def to_bin(astring):

    letter_to_hex = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}

    hex_astring = (astring.encode("utf-8")).hex()
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

def decode(file):
    if imghdr.what(file) != 'png':
        return "Invalid file extension! This type of steganopgrahy only works with uncompressed image formats"
    
    img = Image.open(file)
    
    pixels = img.load()
    pixel_list = numpy.array(img)
    
    lsb_of_each_pixel = ""
    
    for i in range(len(pixel_list)): #Indíce da altura
            
            for j in range(len(pixel_list[i])):
                
                for w in range(3):
                    
                    lsb_of_each_pixel += str(last_bit(pixel_list[i][j][w]))
                    
    number_of_bytes = int(lsb_of_each_pixel).bit_length() + 7 // 8
    array_of_bytes = int(lsb_of_each_pixel).to_bytes(number_of_bytes, "big")
    
    ascii_representation = array_of_bytes.decode()
    
    return ascii_representation
    
def encode(file):

    img = Image.open(file)

    width, height = img.size
    number_of_pixels = width * height

    message = str(input("Qual é a mensagem que pretende enviar? "))
    
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

print(decode("linus_encoded.png"))