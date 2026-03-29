class CPU6502:
    def __init__(self):
        self.A = 0          # Accumulator
        self.X = 0          # X register
        self.Y = 0          # Y register
        self.PC = 0x0000    # Program Counter
        self.C = 0          # Carry Flag
        self.V = 0          # Overflow Flag
        self.Z = 0          # Zero Flag
        self.N = 0          # Negative Flag
        self.D = 0          # Decimal Mode Flag
        self.memory = [0] * 65536  # 64KB Memory

    def set_flags(self, result, value):
        self.C = 1 if result > 0xFF else 0
        self.Z = 1 if (result & 0xFF) == 0 else 0
        self.N = 1 if (result & 0x80) != 0 else 0
        self.V = 1 if (~(self.A ^ value) & (self.A ^ result) & 0x80) else 0

    def adc(self, value):
        if self.D:  # Decimal Mode
            lo = (self.A & 0x0F) + (value & 0x0F) + self.C
            if lo > 9:
                lo += 6
            hi = (self.A >> 4) + (value >> 4) + (lo > 0x0F)
            if hi > 9:
                hi += 6
            result = (hi << 4) | (lo & 0x0F)
        else:  # Binary Mode
            result = self.A + value + self.C

        self.set_flags(result, value)
        self.A = result & 0xFF

    def fetch_operand(self, mode):
        if mode == 'immediate':
            return self.memory[self.PC + 1]
        elif mode == 'zeropage':
            addr = self.memory[self.PC + 1]
            return self.memory[addr]
        elif mode == 'zeropage,X':
            addr = (self.memory[self.PC + 1] + self.X) & 0xFF  # Wrap within zero-page
            return self.memory[addr]
        elif mode == 'absolute':
            addr = self.memory[self.PC + 1] | (self.memory[self.PC + 2] << 8)
            return self.memory[addr]
        elif mode == 'absolute,X':
            addr = (self.memory[self.PC + 1] | (self.memory[self.PC + 2] << 8)) + self.X
            return self.memory[addr]
        elif mode == 'absolute,Y':
            addr = (self.memory[self.PC + 1] | (self.memory[self.PC + 2] << 8)) + self.Y
            return self.memory[addr]
        elif mode == '(indirect,X)':
            zp_addr = (self.memory[self.PC + 1] + self.X) & 0xFF
            addr = self.memory[zp_addr] | (self.memory[(zp_addr + 1) & 0xFF] << 8)
            return self.memory[addr]
        elif mode == '(indirect),Y':
            zp_addr = self.memory[self.PC + 1]
            base_addr = self.memory[zp_addr] | (self.memory[(zp_addr + 1) & 0xFF] << 8)
            return self.memory[base_addr + self.Y]
        else:
            raise ValueError("Unsupported addressing mode")

    def execute_adc(self, mode):
        operand = self.fetch_operand(mode)
        self.adc(operand)
        self.PC += 2 if mode in ['immediate', 'zeropage', 'zeropage,X', '(indirect,X)', '(indirect),Y'] else 3

# Example usage:
cpu = CPU6502()
cpu.memory[0x00] = 0x69  # ADC #$05 (Immediate Mode)
cpu.memory[0x01] = 0x05
cpu.execute_adc('immediate')
print(f"A: {cpu.A:02X}, C: {cpu.C}, Z: {cpu.Z}, N: {cpu.N}, V: {cpu.V}, D: {cpu.D}")


# AND
class CPU6502:
    def __init__(self):
        self.A = 0x00  # Accumulator
        self.X = 0x00  # X Register
        self.Y = 0x00  # Y Register
        self.PC = 0x0000  # Program Counter
        self.flags = {"Z": 0, "N": 0}  # Zero and Negative flags
        self.memory = [0] * 65536  # 64K Memory

    def fetch_byte(self):
        """Fetches a byte and increments the program counter"""
        value = self.memory[self.PC]
        self.PC += 1
        return value

    def fetch_word(self):
        """Fetches a word (16-bit) in little-endian format and increments the PC"""
        low = self.fetch_byte()
        high = self.fetch_byte()
        return (high << 8) | low

    def read_byte(self, address):
        """Reads a byte from memory"""
        return self.memory[address]

    def write_byte(self, address, value):
        """Writes a byte to memory"""
        self.memory[address] = value & 0xFF  # Ensure 8-bit value

    def update_flags(self):
        """Updates the Zero and Negative flags based on the Accumulator"""
        self.flags["Z"] = 1 if self.A == 0 else 0
        self.flags["N"] = 1 if (self.A & 0x80) != 0 else 0

    def AND(self, opcode):
        """Executes the AND instruction for different addressing modes"""
        if opcode == 0x21:  # (indx) - Indexed Indirect (pre-indexed X)
            zp_addr = (self.fetch_byte() + self.X) & 0xFF
            effective_addr = self.read_byte(zp_addr) | (self.read_byte(zp_addr + 1) << 8)
            operand = self.read_byte(effective_addr)

        elif opcode == 0x25:  # zp - Zero Page
            zp_addr = self.fetch_byte()
            operand = self.read_byte(zp_addr)

        elif opcode == 0x29:  # imm - Immediate
            operand = self.fetch_byte()

        elif opcode == 0x2D:  # abs - Absolute
            effective_addr = self.fetch_word()
            operand = self.read_byte(effective_addr)

        elif opcode == 0x31:  # (indy) - Indirect Indexed (post-indexed Y)
            zp_addr = self.fetch_byte()
            base_addr = self.read_byte(zp_addr) | (self.read_byte(zp_addr + 1) << 8)
            effective_addr = (base_addr + self.Y) & 0xFFFF
            operand = self.read_byte(effective_addr)

        elif opcode == 0x35:  # zpx - Zero Page, X
            zp_addr = (self.fetch_byte() + self.X) & 0xFF
            operand = self.read_byte(zp_addr)

        elif opcode == 0x39:  # aby - Absolute, Y
            base_addr = self.fetch_word()
            effective_addr = (base_addr + self.Y) & 0xFFFF
            operand = self.read_byte(effective_addr)

        elif opcode == 0x3D:  # abx - Absolute, X
            base_addr = self.fetch_word()
            effective_addr = (base_addr + self.X) & 0xFFFF
            operand = self.read_byte(effective_addr)

        else:
            raise ValueError(f"Unsupported AND opcode: {hex(opcode)}")

        # Perform AND operation
        self.A &= operand

        # Update flags
        self.update_flags()

