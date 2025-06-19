def create_position_mask(positions):
    # Calculate how many bytes we need (highest position / 8, rounded up)
    max_pos = max(positions)
    mask_size = (max_pos + 8) // 8
    
    # Create empty mask
    mask = [0] * mask_size
    
    # Set bits for special positions
    for pos in positions:
        byte_index = pos >> 3  # Divide by 8
        bit_position = pos & 7  # Remainder of 8
        mask[byte_index] |= (1 << bit_position)
    
    # Format output as C array
    output = "const uint8_t PROGMEM POSITION_MASK[] = {\n"
    for i in range(0, len(mask), 8):
        line = ", ".join(f"0b{bin(b)[2:].zfill(8)}" for b in mask[i:i+8])
        output += f"    {line},\n"
    output += "};\n"
    return output

# LED positions
positions = []
leds = [
    [19, 20, 30, 69, 70, 169, 179, 180],
    [200, 201, 210, 218, 219, 220, 379, 380],
    [488, 489, 490, 500, 580, 599],
    [619, 620, 779, 780, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799],
    [820, 839, 900, 910, 919, 920, 930, 931, 960, 979, 980, 990]
]
for output_port in leds:
    for led in output_port:
        position = led * 2 - output_port.index(led)
        positions.append(position)

print(create_position_mask(positions))