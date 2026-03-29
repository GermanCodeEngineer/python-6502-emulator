OPCODES = [
    #       0       |       1       |       2       |       3       |       4       |       5       |       6       |       7       |       8       |       9       |       A       |       B       |       C       |       D       |       E       |       F       |
    ("imp", "brk"), ("inx", "ora"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zp" , "ora"), ("zp" , "asl"), ("   ", "   "), ("imp", "php"), ("imm", "ora"), ("acc", "asl"), ("   ", "   "), ("   ", "   "), ("abs", "ora"), ("abs", "asl"), ("   ", "   "),  # 0
    ("rel", "bpl"), ("iny", "ora"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zpx", "ora"), ("zpx", "asl"), ("   ", "   "), ("imp", "clc"), ("aby", "ora"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("abx", "ora"), ("abx", "asl"), ("   ", "   "),  # 1
    ("abs", "jsr"), ("inx", "and"), ("   ", "   "), ("   ", "   "), ("zp" , "bit"), ("zp" , "and"), ("zp" , "rol"), ("   ", "   "), ("imp", "plp"), ("imm", "and"), ("acc", "rol"), ("   ", "   "), ("abs", "bit"), ("abs", "and"), ("abs", "rol"), ("   ", "   "),  # 2
    ("rel", "bmi"), ("iny", "and"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zpx", "and"), ("zpx", "rol"), ("   ", "   "), ("imp", "sec"), ("aby", "and"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("abx", "and"), ("abx", "rol"), ("   ", "   "),  # 3
    ("imp", "rti"), ("inx", "eor"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zp" , "eor"), ("zp" , "lsr"), ("   ", "   "), ("imp", "pha"), ("imm", "eor"), ("acc", "lsr"), ("   ", "   "), ("abs", "jmp"), ("abs", "eor"), ("abs", "lsr"), ("   ", "   "),  # 4
    ("rel", "bvc"), ("iny", "eor"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zpx", "eor"), ("zpx", "lsr"), ("   ", "   "), ("imp", "cli"), ("aby", "eor"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("abx", "eor"), ("abx", "lsr"), ("   ", "   "),  # 5
    ("imp", "rts"), ("inx", "adc"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zp" , "adc"), ("zp" , "ror"), ("   ", "   "), ("imp", "pla"), ("imm", "adc"), ("acc", "ror"), ("   ", "   "), ("ind", "jmp"), ("abs", "adc"), ("abs", "ror"), ("   ", "   "),  # 6
    ("rel", "bvs"), ("iny", "adc"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zpx", "adc"), ("zpx", "ror"), ("   ", "   "), ("imp", "sei"), ("aby", "adc"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("abx", "adc"), ("abx", "ror"), ("   ", "   "),  # 7
    ("   ", "   "), ("inx", "sta"), ("   ", "   "), ("   ", "   "), ("zp" , "sty"), ("zp" , "sta"), ("zp" , "stx"), ("   ", "   "), ("imp", "dey"), ("   ", "   "), ("imp", "txa"), ("   ", "   "), ("abs", "sty"), ("abs", "sta"), ("abs", "stx"), ("   ", "   "),  # 8
    ("rel", "bcc"), ("iny", "sta"), ("   ", "   "), ("   ", "   "), ("zpx", "sty"), ("zpx", "sta"), ("zpy", "stx"), ("   ", "   "), ("imp", "tya"), ("aby", "sta"), ("imp", "txs"), ("   ", "   "), ("   ", "   "), ("abx", "sta"), ("   ", "   "), ("   ", "   "),  # 9
    ("imm", "ldy"), ("inx", "lda"), ("imm", "ldx"), ("   ", "   "), ("zp" , "ldy"), ("zp" , "lda"), ("zp" , "ldx"), ("   ", "   "), ("imp", "tay"), ("imm", "lda"), ("imp", "tax"), ("   ", "   "), ("abs", "ldy"), ("abs", "lda"), ("abs", "ldx"), ("   ", "   "),  # A
    ("rel", "bcs"), ("iny", "lda"), ("   ", "   "), ("   ", "   "), ("zpx", "ldy"), ("zpx", "lda"), ("zpy", "ldx"), ("   ", "   "), ("imp", "clv"), ("aby", "lda"), ("imp", "tsx"), ("   ", "   "), ("abx", "ldy"), ("abx", "lda"), ("aby", "ldx"), ("   ", "   "),  # B
    ("imm", "cpy"), ("inx", "cmp"), ("   ", "   "), ("   ", "   "), ("zp" , "cpy"), ("zp" , "cmp"), ("zp" , "dec"), ("   ", "   "), ("imp", "iny"), ("imm", "cmp"), ("imp", "dex"), ("   ", "   "), ("abs", "cpy"), ("abs", "cmp"), ("abs", "dec"), ("   ", "   "),  # C
    ("rel", "bne"), ("iny", "cmp"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zpx", "cmp"), ("zpx", "dec"), ("   ", "   "), ("imp", "cld"), ("aby", "cmp"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("abx", "cmp"), ("abx", "dec"), ("   ", "   "),  # D
    ("imm", "cpx"), ("inx", "sbc"), ("   ", "   "), ("   ", "   "), ("zp" , "cpx"), ("zp" , "sbc"), ("zp" , "inc"), ("   ", "   "), ("imp", "inx"), ("imm", "sbc"), ("imp", "nop"), ("   ", "   "), ("abs", "cpx"), ("abs", "sbc"), ("abs", "inc"), ("   ", "   "),  # E
    ("rel", "beq"), ("iny", "sbc"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("zpx", "sbc"), ("zpx", "inc"), ("   ", "   "), ("imp", "sed"), ("aby", "sbc"), ("   ", "   "), ("   ", "   "), ("   ", "   "), ("abx", "sbc"), ("abx", "inc"), ("   ", "   "),  # F
]
OPCODE_NAMES = [i[1].upper() for i in OPCODES] + [i[1] for i in OPCODES]

BYTEORDER = "little"

def to_number(obj):
    if isinstance(obj, int): return obj
    
    try:
        new = int(obj, base=2)
    except ValueError: pass
    else: return new

    try:
        new = int(obj, base=10)
    except ValueError: pass
    else: return new
    
    try:
        new = int(obj, base=16)
    except ValueError: pass
    else: return new
    
    raise ValueError(f"Couldn't convert {repr(obj)} to number.")

import platform, os
def copy(string):
    if "ANDROID_ROOT" in os.environ or "android" in platform.system().lower():
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(string)
    else:
        import pyperclip
        pyperclip.copy(string)

from enum import Enum
class ParserState(Enum):
    NONE           = 0
    ALNUM          = 1
    HASHTAG        = 2
    DOLLAR         = 3
    HASHTAG_DOLLAR = 4
    DOT            = 5
    STRING         = 6

class Token:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return self.__class__.__name__.removesuffix("Token") + (("{"+str(self.value)+"}") if self.value != None else "")

class NewlineToken(Token):
    def __init__(self): super().__init__(value=None)

class AlnumToken(Token):
    def __init__(self, value): super().__init__(value=value)

class ImmediateOperandToken(Token):
    def __init__(self, value): super().__init__(value=value)

class AddressOperandToken(Token):
    def __init__(self, value): super().__init__(value=value)

class OpeningBracketToken(Token):
    def __init__(self): super().__init__(value=None)

class ClosingBracketToken(Token):
    def __init__(self): super().__init__(value=None)

class DirectiveToken(Token):
    def __init__(self, value): super().__init__(value=value)

class ImmediateStringToken(Token):
    def __init__(self, value): super().__init__(value=value)

class LabelReference:
    def __init__(self, name: str):
        self.name = name    

class AbsoluteLabelReference(LabelReference):
    def __init__(self, name: str):
        super().__init__(name=name)
    def __repr__(self):
        return f"AbsoluteLabelReference({self.name})"

class RelativeLabelReference(LabelReference):
    def __init__(self, name: str):
        super().__init__(name=name)
    def __repr__(self):
        return f"RelativeLabelReference({self.name})"

class PlaceHolder:
    def __init__(self): pass
    def __repr__(self): return "PlaceHolder"

class Label:
    def __init__(self, value: str):
        self.value = value

class InstructionLabel(Label):
    def __init__(self, value: str):
        super().__init__(value=value)
    def __repr__(self):
        return f"InstructionLabel({self.value})"
    def calculate_absolute(self, start_vector, byte_count):
        return start_vector + self.value

class MemoryLabel(Label):
    def __init__(self, value: str):
        super().__init__(value=value)
    def __repr__(self):
        return f"MemoryLabel({self.value})"
    def calculate_absolute(self, start_vector, byte_count):
        return start_vector + byte_count + self.value

def parse_assembly(assembly: str) -> list[list[Token]]:
    def endToken():
        nonlocal state, token_chars
        if   state == ParserState.NONE: pass
        elif state == ParserState.ALNUM:
            if token_chars != "":
                tokens.append(AlnumToken(token_chars))
                token_chars = ""
            state = ParserState.NONE
        elif state == ParserState.DOLLAR:
            if token_chars != "":
                value = int("0x" + token_chars, base=16)
                tokens.append(AddressOperandToken(value))
                token_chars = ""
            state = ParserState.NONE
        elif state == ParserState.HASHTAG:
            if token_chars != "":
                value = int(token_chars, base=10)
                tokens.append(ImmediateOperandToken(value))
                token_chars = ""
            state = ParserState.NONE
        elif state == ParserState.HASHTAG_DOLLAR:
            if token_chars != "":
                value = int("0x" + token_chars, base=16)
                tokens.append(ImmediateOperandToken(value))
                token_chars = ""
            state = ParserState.NONE
        elif state == ParserState.DOT:
            if token_chars != "":
                tokens.append(DirectiveToken(token_chars))
                token_chars = ""
            state = ParserState.NONE
        elif state == ParserState.STRING:
            tokens.append(ImmediateStringToken(token_chars))
            token_chars = ""
            state = ParserState.NONE
            is_escaped = False
        else: raise Exception(state)
    
    
    lines = assembly.splitlines()
    mod_assembly = ""
    for line in lines:
        if ";" in line:
            line = line[:line.index(";")]
        line = line.strip()
        if line == "": continue
        if mod_assembly != "":
            mod_assembly += "\n"
        mod_assembly += line

    lines = mod_assembly.splitlines()
    print(repr(assembly))
    print("jey", lines)
    token_chars = ""
    state = ParserState.NONE
    is_escaped = False
    tokens = []
    for line in lines:
        for i, char in enumerate(line):
            if state == ParserState.STRING:
                if   not(is_escaped) and (char == "\\"):
                    is_escaped = True
                elif not(is_escaped) and (char == '"'):
                    endToken()
                else:
                    token_chars += char
                    is_escaped = False

            elif char in {" ", ",", ":"}:
                endToken()
            
            elif char == '"':
                if   state == ParserState.NONE:
                    state = ParserState.STRING
                    is_escaped = False
                else: raise Exception(state)
                
            elif char == ".":
                if   state == ParserState.NONE:
                    state = ParserState.DOT
                else: raise Exception(state)
            
            elif char == "#":
                if   state == ParserState.NONE:
                    state = ParserState.HASHTAG
                else: raise Exception(state)
            
            elif char == "$":
                if   state == ParserState.NONE:
                    state = ParserState.DOLLAR
                elif state == ParserState.HASHTAG:
                    state = ParserState.HASHTAG_DOLLAR
                else: raise Exception(state)
            
            elif char == "(":
                if   state == ParserState.NONE:
                    tokens.append(OpeningBracketToken())
                else: raise Exception(state)
            elif char == ")":
                endToken()
                if   state == ParserState.NONE:
                    tokens.append(ClosingBracketToken())
                else: raise Exception(state)
    
            elif char.isalnum():
                if   state == ParserState.NONE:
                    state = ParserState.ALNUM
                elif state == ParserState.ALNUM: pass
                elif state == ParserState.DOLLAR: pass
                elif state == ParserState.HASHTAG: pass
                elif state == ParserState.HASHTAG_DOLLAR: pass
                elif state == ParserState.DOT: pass
                else: raise Exception(state)
    
                if state in {ParserState.ALNUM, ParserState.DOLLAR, ParserState.HASHTAG, ParserState.HASHTAG_DOLLAR, ParserState.DOT}:
                    token_chars += char
            
            else: raise Exception(repr(char))
            print(repr(char), state)
        endToken()
        tokens.append(NewlineToken())
    print(repr(mod_assembly))
    print(mod_assembly)
    print("one", tokens)

    ordered_tokens = []
    line_tokens = []
    for token in tokens:
        if isinstance(token, NewlineToken):
            if line_tokens != []:
                ordered_tokens.append(line_tokens)
            line_tokens = []
        else:
            line_tokens.append(token)
    print("ordered", ordered_tokens)
    return ordered_tokens

def generate_machine_code(
        ordered_tokens: list[list[Token]], 
        default_start_vector:int = 0x8000
    ) -> list[int]:
    
    def interpret_instruction():
        nonlocal bytes
        if   (isinstance(first_token, OpeningBracketToken) and isinstance(second_token, AddressOperandToken)
                    and (third_token_value == "X")         and isinstance(fourth_token, ClosingBracketToken)):
            addressing_mode = "inx"
            operand         = second_token_value
            operand_bits    = 8
        elif (isinstance(first_token, OpeningBracketToken) and isinstance(second_token, AddressOperandToken)
          and isinstance(third_token, ClosingBracketToken) and (fourth_token_value == "Y")):
            addressing_mode = "iny"
            operand         = second_token_value
            operand_bits    = 8
        elif (isinstance(first_token, OpeningBracketToken) and isinstance(second_token, AddressOperandToken)
          and isinstance(third_token, ClosingBracketToken) and (fourth_token is None)):
            addressing_mode = "ind"
            operand         = second_token_value
            operand_bits    = 16
        elif (third_token is None) and (fourth_token is None):
            if (first_token is None) and (second_token is None):
                addressing_mode = "imp"
                operand         = None
                operand_bits    = None 
            elif isinstance(first_token, ImmediateOperandToken) and (second_token is None):
                addressing_mode = "imm"
                operand         = first_token_value
                operand_bits    = 8
            elif isinstance(first_token, AddressOperandToken) and (second_token is None):
                if first_token_value < 0x100: addressing_mode, operand_bits = "zp" , 8 
                else                        : addressing_mode, operand_bits = "abs", 16
                operand = first_token_value
            elif isinstance(first_token, AddressOperandToken) and (second_token_value == "X"):
                if first_token_value < 0x100: addressing_mode, operand_bits  = "zpx", 8 
                else                        : addressing_mode, operand_bits  = "abx", 16
                operand = first_token_value
            elif isinstance(first_token, AddressOperandToken) and (second_token_value == "Y"):
                if first_token_value < 0x100: addressing_mode, operand_bits  = "zpy", 8 
                else                        : addressing_mode, operand_bits  = "aby", 16
                operand = first_token
            elif (first_token_value == "A") and (second_token is None):
                addressing_mode = "acc"
                operand         = None
            elif isinstance(first_token, AlnumToken) and (second_token is None):
                if opcode_name in ["bcc", "bcs", "beq", "bmi", "bne", "bpl", "bvc", "bvs"]:
                    addressing_mode = "rel"
                    operand         = RelativeLabelReference(first_token_value)
                else:
                    addressing_mode = "abs"
                    operand         = AbsoluteLabelReference(first_token_value)
            elif (first_token_value in label_data) and (second_token_value == "X"):
                addressing_mode = "abx"
                operand = AbsoluteLabelReference(first_token_value)
            elif (first_token_value in label_data) and (second_token_value == "Y"):
                addressing_mode = "aby"
                operand = AbsoluteLabelReference(first_token_value)
            else: raise Exception()
        else: raise Exception()
        id = (addressing_mode, opcode_name)
        if id not in OPCODES: raise Exception(id)
        
        instr_bytes = []
        opcode_num = OPCODES.index(id)
        instr_bytes.append(opcode_num)
        if isinstance(operand, int):
            if operand_bits == 8:
                if (operand >= 0xFF) or (operand < -0x80): raise ValueError()
                instr_bytes.append(operand)
            elif operand_bits == 16:
                if (operand >= 0xFFFF) or (operand < -0x8000): raise ValueError()
                if BYTEORDER == "little":
                    instr_bytes.append((operand >> 0) & 0xFF)
                    instr_bytes.append((operand >> 8) & 0xFF)
                else:
                    instr_bytes.append((operand >> 8) & 0xFF)
                    instr_bytes.append((operand >> 0) & 0xFF)
            else: raise Exception()
        elif isinstance(operand, LabelReference):
            instr_bytes.append(operand)
            # AbsoluteLabelReference will be replaced by 2 bytes, so use a placeholder to keep len(bytes) correct
            if isinstance(operand, AbsoluteLabelReference):
                instr_bytes.append(PlaceHolder())
            
        elif operand is None: pass
        else: raise Exception()
        bytes += instr_bytes
        print(label, instr_bytes)
    
    def interpret_directive():
        nonlocal option_start_vector, memory_bytes
        match opcode_name:
            case "org":
                assert len(remaining_tokens) == 1
                option_start_vector = to_number(first_token_value)
            case "byte"|"db":
                assert len(remaining_tokens) >= 1
                if isinstance(remaining_tokens[0], ImmediateStringToken):
                    assert len(remaining_tokens) == 2
                    assert isinstance(remaining_tokens[1], AlnumToken) and (remaining_tokens[1].value == "0")
                    directive_bytes = []
                    for char in remaining_tokens[0].value:
                        assert ord(char) in range(256)
                        directive_bytes.append(ord(char))
                    directive_bytes.append(0)
                else:
                    directive_bytes = []
                    for token in remaining_tokens:
                        byte = to_number(token.value)
                        assert not ((byte >= 0xFF) or (byte < -0x80))
                        directive_bytes.append(byte & 0xFF)
                memory_bytes += directive_bytes
            case _: raise Exception(opcode_name)
            
    
    option_start_vector = default_start_vector
    memory_bytes = []
    bytes = []
    label_data = {}
    for line_tokens in ordered_tokens:
        assert len(line_tokens) >= 1
        first_token  = line_tokens[0] if (0 in range(len(line_tokens))) else None
        second_token = line_tokens[1] if (1 in range(len(line_tokens))) else None
        first_token_value  = None if (first_token  is None) else first_token.value
        second_token_value = None if (second_token is None) else second_token.value
        if not isinstance(first_token, (AlnumToken, DirectiveToken)): raise Exception()
        
        compatible = isinstance(second_token, DirectiveToken) or (isinstance(second_token, AlnumToken) and (second_token_value in OPCODE_NAMES))
        if isinstance(first_token, AlnumToken) and compatible: # The instruction/directive has a label 
            label       = first_token_value
            opcode_name = second_token_value.lower()
            deciding_token = second_token
            remaining_tokens = line_tokens[2:]
        else:
            label       = None
            opcode_name = first_token_value.lower()
            deciding_token = first_token
            remaining_tokens = line_tokens[1:]
        
        first_token  = remaining_tokens[0] if (0 in range(len(remaining_tokens))) else None
        second_token = remaining_tokens[1] if (1 in range(len(remaining_tokens))) else None
        third_token  = remaining_tokens[2] if (2 in range(len(remaining_tokens))) else None
        fourth_token = remaining_tokens[3] if (3 in range(len(remaining_tokens))) else None
        first_token_value  = None if (first_token  is None) else first_token.value
        second_token_value = None if (second_token is None) else second_token.value
        third_token_value  = None if (third_token  is None) else third_token.value
        fourth_token_value = None if (fourth_token is None) else fourth_token.value
        print("rem", remaining_tokens, first_token, second_token, opcode_name)
        
        if label is not None:
            if isinstance(deciding_token, AlnumToken):
                label_data[label] = InstructionLabel(len(bytes))
            else:
                label_data[label] = MemoryLabel(len(memory_bytes))
            print("LABEL NEW", label_data)
        if isinstance(deciding_token, DirectiveToken):
            interpret_directive()
        elif isinstance(deciding_token, AlnumToken):
            assert len(remaining_tokens) <= 4
            interpret_instruction()
        print(label)
            
    print(bytes, label_data)
    final_bytes = []
    for i, item in enumerate(bytes+memory_bytes):
        if isinstance(item, AbsoluteLabelReference):
            label = label_data[item.name]
            address = label.calculate_absolute(
                start_vector=option_start_vector,
                byte_count=len(bytes),
            )
            print("REPLACE", item, address, hex(address))
            if (address >= 0xFFFF) or (address < -0x8000): raise ValueError()
            if BYTEORDER == "little":
                final_bytes.append((address >> 0) & 0xFF)
                final_bytes.append((address >> 8) & 0xFF)
            else:
                final_bytes.append((address >> 8) & 0xFF)
                final_bytes.append((address >> 0) & 0xFF)
        elif isinstance(item, RelativeLabelReference):
            label = label_data[item.name]
            assert isinstance(label, InstructionLabel) # Branching to a MemoryLabel makes no sense
            address = label.calculate_absolute(
                start_vector=0,
                byte_count=len(bytes),
            )
            print("REPLACE", item, address)
            relative_address = (address - i) - 1 # Adjust because PC will be i+1 because of the one byte operand
            print("I", i, "ADD", address, relative_address)
            
            if (relative_address >= 0xFF) or (relative_address < -0x80): raise ValueError()
            final_bytes.append((relative_address) & 0xFF)
        elif isinstance(item, PlaceHolder):
            pass
        else:
            final_bytes.append(item)
    print(final_bytes, label_data)
    options = {
        "START_VECTOR":  option_start_vector
    }
    return final_bytes, options

def generate_rom(machine_code, options):
    option_start_vector = options["START_VECTOR"]
    rom = {}
    if (option_start_vector >= 0xFFFF) or (option_start_vector < 0): raise ValueError()
    
    # Set the start vector
    if BYTEORDER == "little":
        rom[0xFFFC] = (option_start_vector >> 0) & 0xFF
        rom[0xFFFD] = (option_start_vector >> 8) & 0xFF
    else:
        rom[0xFFFC] = (option_start_vector >> 8) & 0xFF
        rom[0xFFFD] = (option_start_vector >> 0) & 0xFF
    
    # Set the program bytes
    for i, byte in enumerate(machine_code):
        rom[option_start_vector + i] = byte
    return dict(sorted(rom.items())) # My preference
#365 * 365
# 33 + 97
# 51 + 151
assembly = r"""
        LDA #5     ; set x
        STA $0200  ;
        LDA #3     ; set y
        STA $0201  ;
        LDA #1     ; set a to 1
        STA $0202  ;
        LDX #0     ; set i to 0

LOOP1a  LDA #0     ; set b to 0
        STA $0203  ;
        LDY #0     ; set j to 0

LOOP2   LDA $0203  ; add b to a
        CLC        ;
        ADC $0202  ;
        STA $0203  ;
        INY        ; increase j by 1
        CPY $0200  ; compare j and x
        BNE LOOP2  ; repeat LOOP2 as long as j != x

LOOP1b  LDA $0203  ; set a to b
        STA $0202  ;
        INX        ; increase i by 1
        CPX $0201  ; compare j and y
        BNE LOOP1a ; repeat LOOP1 as long as i != y

        LDA $0202
END     JMP END    ;
"""

tokens = parse_assembly(assembly)
machine_code, options = generate_machine_code(tokens)

print(" ".join([hex(i).removeprefix("0x").upper() for i in machine_code]))

import json
rom = generate_rom(machine_code, options)
print(json.dumps(rom))

string = 'set runtime var [memory] to (M___init__ [' + json.dumps(rom) + '])\n'
#copy(string)
print("Copied!")
