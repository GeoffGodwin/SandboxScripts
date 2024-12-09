# This program takes in a list of up to 8 integer numbers between 1 and 8 inclusive. Inputting a blank will stop the input and start the calculation. This list of numbers signify the bit position in an 8 bit byte. We combine those given positions to make the byte and return its decimal value.
# So 1 and 3 would be 00000101 which is 5 in decimal.
# 1 and 4 would be 00001001 which is 9 in decimal.
# 1, 2 and 5 would be 00010011 which is 19 in decimal.
# Created by: Geoff Godwin

# Function to combine the list (max 8) of positions and return the decimal value of the byte.
def stone_puzzle_problem(stone_positions):
    # Initialize the byte to 0
    byte = 0
    # Loop through the list of positions
    for position in stone_positions:
        # Add the position to the byte
        byte += 2 ** (position - 1)
    # Return the decimal value of the byte
    return byte
    
# Main function to take in the input and call the stone_puzzle_problem function.
def main():
    # Initialize the list of stone positions
    stone_positions = []
    # Loop to take in the input
    while True:
        # Take in the input
        stone_position = input("Enter the stone position (1-8) or blank to stop: ")
        # Check if the input is blank
        if stone_position == "":
            # Break the loop
            break
        # Add the stone position to the list
        stone_positions.append(int(stone_position))
    # Call the stone_puzzle_problem function and print the result
    print("Decimal value of the byte is:", stone_puzzle_problem(stone_positions))


# Call the main function
if __name__ == "__main__":
    main()

# End of Program