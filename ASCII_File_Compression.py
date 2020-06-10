#Compression
import time as time
import array as ar
import os
from heapq import heappush, heappop, heapify
import pickle
import numpy as np
from io import StringIO

def characters(file):
    with open(file,'r') as f:
        return [character for line in f.readlines() for character in line]
def characterset(file): #lists all characters used in text
    characterset=set(characters(file))
    return(characterset)
def character_dictionary(file): #dictionary of characters
    characterdictionary={}
    for i in characterset(file):
        characterdictionary.update({i:characters(file).count(i)})
    return(characterdictionary)
def encodehuffman(symb2freq): #frequency count and builds tree
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt,[sym,""]] for sym, wt in symb2freq.items() ]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key = lambda p: (len(p[-1]),p))
def huffman(file): # uses tree to encode files
    time_initial=time.time()
    huffman_info=[]
    code=encodehuffman(character_dictionary(file))
    finaldict = {}
    codedict = {}
    j = 0
    while j<len(code):
        codedict.update({code[j][0]:code[j][1]})
        j=j+1
    k=0
    while k<len(code):
        finaldict.update({code[k][1]:code[k][0]})
        k=k+1
    final=''
    for i in characters(file):
        final = final+str(codedict[i])
    finallist =[]
    for i in final:
        finallist.append(i)
    final = str(final)
    k=0
    anotherlist=[]
    while k<len(finallist)-8:
        anotherlist.append(str(''.join(finallist[k:k+8])))
        k=k+8
    else:
        number=(str(''.join(finallist[k:len(finallist)]) ) )
        extrabits=8-len(number)
        while len(number)!=8:
            number+='0'
        anotherlist.append(number)
    with open('decompressionkey.pickle', 'wb') as handle:
        pickle.dump(finaldict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bin_array=ar.array('B')
    for i in anotherlist:
        bin_array.append(int(i,2))
    size=(len(bin_array))
    f = open('newfile.txt','wb')
    bin_array.tofile(f)
    f.close()
    f1=open('filesize.txt','w')
    f1.write( (str(size)+','+str(extrabits) ))
    f1.close()
    time_final=time.time()
    time_difference=time_final - time_initial
    size_huffman=os.path.getsize("newfile.txt")
    huffman_info.append(size_huffman)
    huffman_info.append(time_difference)
    return(huffman_info)
def runlengthcode(file):
    run_length_info=[]
    time_initial=time.time()
    characterlist=characters(file)
    lettersdictionary=[]
    i=0
    n=1
    while i<len(characterlist)-n:
        while i+n<len(characterlist) and characterlist[i]==characterlist[i+n]:
            n+=1
        else:
            lettersdictionary.append(str(len(characterlist[i:i+n])))
            lettersdictionary.append(characterlist[i])
            i+=n
            n=1
    final=''.join(lettersdictionary)
    run_length_file = open("runlengthcompressed.txt","w")
    run_length_file.write(final)
    run_length_file.close()
    size_run_length=os.path.getsize("runlengthcompressed.txt")
    time_final=time.time()
    time_difference=time_final - time_initial
    run_length_info.append(size_run_length)
    run_length_info.append(time_difference)
    return(run_length_info)
def lempelziv(file):
    time_initial=time.time()
    lempelziv_info=[]
    dictionary_lempel_ziv = {}
    ascii = 256
    i =0
    while i < ascii:
        dictionary_lempel_ziv.update({chr(i):i})
        i+=1
    current = ""
    text = ar.array('H')
    for i in ''.join(characters(file)):
        currentnext = current +i
        if currentnext in dictionary_lempel_ziv:
            current = currentnext
        elif currentnext not in dictionary_lempel_ziv:
            text.append(dictionary_lempel_ziv[current])
            dictionary_lempel_ziv[currentnext] = ascii
            ascii = ascii + 1
            current = i
    text.append(dictionary_lempel_ziv[current])
    print('Compressed machine/ASCII values:')
    print(text)
    lempel_ziv_file = open('compressed_text','wb')
    text.tofile(lempel_ziv_file)
    lempel_ziv_file.close()
    size_lempel_ziv=os.path.getsize("compressed_text")
    time_final =time.time()
    time_difference = time_final - time_initial
    lempelziv_info.append(size_lempel_ziv)
    lempelziv_info.append(time_difference)
    return(lempelziv_info)

#Images

def brl(file): # contains code for compression of images
    time_intial=time.time()
    ddict=bytearray()
    bufsize = 255
    f = open(file,'rb')
    buf = bytearray(f.read(bufsize))
    while len(buf):
        i = 0
        n = 1
        while i < len(buf)-n:
            while i+n<len(buf) and buf[i]==buf[i+n]:
                n+=1
            else:
                ddict.append(len(buf[i:i+n]))
                ddict.append(buf[i])
                if i+n == len(buf) - 1:
                    ddict.append(1)
                    ddict.append(buf[i+n])
                i = i + n
                n=1
        buf = bytearray(f.read(bufsize))
    run_length_file = open("brlcmp.bin","wb")
    run_length_file.write(ddict)
    run_length_file.close()

    org_size = os.path.getsize(file)
    size_run_length = os.path.getsize("brlcmp.bin")
    time_final = time.time()
    time_difference = time_final - time_initial

    run_length_info = {}
    run_length_info['original size'] = org_size
    run_length_info['compressed size'] = size_run_length
    run_length_info['compression rate'] = org_size/ size_run_length
    run_length_info['time difference'] = time_difference
    print(run_length_info)

# Decompression

#HUFFMAN

def huffman_decompression():
    time_initial= time.time()
    f= open('newfile.txt', 'rb')
    ra = ar.array('B')
    sizefile=open('filesize.txt', 'r+')
    sizefileline = sizefile.readline()
    size = ''
    while len(sizefileline)!=0:
        for i in sizefileline:
            size=size+str(i)
        sizefileline = sizefile.readline()
    size=size.split(',')
    sizeoffile=int(size[0])
    extrabits=int(size[1])
    ra.fromfile(f,int(sizeoffile))
    result=[]
    for c in ra:
        result.append('{0:08b}'.format(c))
    binarycode = result
    result=''.join(result)
    with open('decompressionkey.pickle', 'rb') as handle:
        b = pickle.load(handle)
    decompressionkey = b
    binary={}
    for i in decompressionkey.keys():
        binary.update({i:len(i)})
    maxlength = max(binary.values())
    minlength = min(binary.values())
    finaltext = ''
    p = 0
    k = minlength
    while p+k<= len(result)-extrabits:
        if result[p:p+k] not in binary:
            k+=1
        else:
            finaltext+=str(decompressionkey[result[p:p+k]])
            p+=k
            k=minlength
    file = open("decompressed_huffman.txt","w")
    file.write(finaltext)
    file.close()

#Run length encoding

def RLE_decompression():
    file=open('runlengthcompressed.txt',"r+")
    mystring=file.readline(100)
    mystringlist=[]
    i = 0
    while i < len(mystring)-1:
        mystringlist.append([int(mystring[i]),mystring[i+1]])
        i+=2

    decompression=[]
    for i in mystringlist:
        y = i[0]
        while y>0:
            decompression.append(i[1])
            y=y-1
        
    decompression=''.join(decompression)
    print(decompression)

#Lempel-Ziv

def LZ_decompression():
    f=open('compressed_text','rb')
    ra=ar.array('H')
    while True:
        try:
            ra.fromfile(f,100)
        except EOFError:
            break
    print("Compressed ASCII: ")
    print(ra)
    text=ra.tolist()
    dictionary = {}
    ascii =256
    i=0
    while i <ascii:
        dictionary.update({i:chr(i)})
        i+=1
    decompressed = StringIO()
    w = chr(text.pop(0))
    decompressed.write(w)
    for k in text:
        if k in dictionary:
            entry = dictionary[k]
        elif k == ascii:
            entry = w + w[0]
        decompressed.write(entry)
        dictionary[ascii] = w + entry[0]
        ascii += 1
        w = entry
    
    file = open("Decompressed_LZ.txt","w")
    file.write(decompressed.getvalue())
    print(decompressed.getvalue())
    file.close()

#IMAGES LZ

def LZ_images_decompress():
    time_initial=time.time()
    file=open("brlcmp.bin","rb")
    decompression = bytearray()
    buff=bytearray(file.read(1024))
    while len(buff)!=0:
        i=0
        n=1
        while i < len(buff)-1:
            counter=int(buff[i])
            while counter!=0:
                decompression.append(buff[i+1])
                counter-=1
            i+=2
        buff=bytearray(file.read(255))
    file=open("decompressed.bmp","wb")
    file.write(decompression)
    file.close()
    

              
