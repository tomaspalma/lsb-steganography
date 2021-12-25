import PIL
import numpy
import math

from PIL import Image

def to_bin(astring):

    letter_to_hex = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}

    hex_astring = (astring.encode("utf-8")).hex()
    bin_astring = ""

    for char in hex_astring:
        if char in list(letter_to_hex.keys()):
            bin_astring +=  "".join(bin(int(letter_to_hex[char])).split("0b"))
        else:
            bin_astring +=  "".join(bin(int(char)).split("0b"))

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
    file_extension = file.split(".")[1]
    if file_extension != "png":
        return f"Este tipo de técnica de esteganografia não suporta ficheiros .{file_extension}"

    img = Image.open(file)
    pixels = img.load()

    width, height = img.size

    return pixels[0,2]

def encode(file):

    img = Image.open(file)

    width, height = img.size
    number_of_pixels = width * height

    message = str(input("Qual é a mensagem que pretende enviar? "))

    bin_message = to_bin(message)

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
    
    for i in range(len(message_divided_by_three_parts)):
        
        pixel_to_alter = list(pixels[i,0])
        new_pixel_list += (pixel_to_alter, )
            
            
                
    new_pixel_list = list_to_tuple(new_pixel_list)
    
                
    encoded_image = Image.fromarray(pixel_list)
    encoded_image.save(f"{file.split('.')[0]}_encoded.{file.split('.')[1]}")
    
    return pixel_list[0][0][1]

print(encode("linus5.png"))
