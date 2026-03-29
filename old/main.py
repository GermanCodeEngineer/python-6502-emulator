from m6502 import *

START = 0xFCE2
#BYTECODE = "A9 05 8D 00 02 CE 00 02 AD 00 02 D0 FA 00"
BYTECODE = "A9 05 18 69 02 D0 FC"
# LDA #5
# CLC
# loop: ADC #2
# BNE loop


memory = M___init__()
for i, byte in enumerate(BYTECODE.split(" ")):
    print("*", hex(START+i), byte)
    memory = M___setitem__(memory, START+i, int(byte, base=16))
cpu = P___init__(memory)
cpu, _ = P_reset(cpu)
cpu, _ = P_execute(cpu, instructions=1000, debug=True)

