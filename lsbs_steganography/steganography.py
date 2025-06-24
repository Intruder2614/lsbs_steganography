import os
from PIL import Image
import argparse


class LSBSteganography:
    """
    A class to perform LSB (Least Significant Bit) steganography on images.
    This method hides data by modifying the least significant bit of each color channel.
    """
    
    def __init__(self):
        self.delimiter = "###END###"  # Delimiter to mark end of hidden message
    
    def _message_to_binary(self, message):
        """Convert message string to binary format."""
        return ''.join(format(ord(char), '08b') for char in message)
    
    def _binary_to_message(self, binary_data):
        """Convert binary data back to message string."""
        message = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                message += chr(int(byte, 2))
        return message
    
    def _modify_pixel(self, pixel, data_bit):
        """Modify the least significant bit of a pixel value."""
        # Convert pixel to binary, replace LSB, convert back to int
        pixel_bin = format(pixel, '08b')
        modified_pixel_bin = pixel_bin[:-1] + str(data_bit)
        return int(modified_pixel_bin, 2)
    
    def _extract_lsb(self, pixel):
        """Extract the least significant bit from a pixel value."""
        return format(pixel, '08b')[-1]
    
    def hide_message(self, image_path, message, output_path):
        """
        Hide a message in an image using LSB steganography.
        
        Args:
            image_path (str): Path to the input image
            message (str): Message to hide
            output_path (str): Path to save the output image
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open the image
            img = Image.open(image_path)
            img = img.convert('RGB')  # Ensure RGB format
            
            # Get image dimensions
            width, height = img.size
            pixels = list(img.getdata())
            
            # Add delimiter to message to mark its end
            full_message = message + self.delimiter
            binary_message = self._message_to_binary(full_message)
            
            # Check if image can hold the message
            total_pixels = width * height
            total_bits_available = total_pixels * 3  # RGB has 3 channels
            
            if len(binary_message) > total_bits_available:
                print(f"Error: Message too long! Image can hold {total_bits_available} bits, "
                      f"but message needs {len(binary_message)} bits.")
                return False
            
            # Hide the message
            data_index = 0
            modified_pixels = []
            
            for pixel in pixels:
                r, g, b = pixel
                
                # Modify red channel
                if data_index < len(binary_message):
                    r = self._modify_pixel(r, int(binary_message[data_index]))
                    data_index += 1
                
                # Modify green channel
                if data_index < len(binary_message):
                    g = self._modify_pixel(g, int(binary_message[data_index]))
                    data_index += 1
                
                # Modify blue channel
                if data_index < len(binary_message):
                    b = self._modify_pixel(b, int(binary_message[data_index]))
                    data_index += 1
                
                modified_pixels.append((r, g, b))
                
                # Stop if all message bits are embedded
                if data_index >= len(binary_message):
                    # Add remaining pixels unchanged
                    modified_pixels.extend(pixels[len(modified_pixels):])
                    break
            
            # Create new image with modified pixels
            new_img = Image.new('RGB', (width, height))
            new_img.putdata(modified_pixels)
            new_img.save(output_path)
            
            print(f"Message successfully hidden in '{output_path}'")
            print(f"Original image size: {os.path.getsize(image_path)} bytes")
            print(f"Steganographic image size: {os.path.getsize(output_path)} bytes")
            return True
            
        except Exception as e:
            print(f"Error hiding message: {str(e)}")
            return False
    
    def extract_message(self, image_path):
        """
        Extract a hidden message from an image using LSB steganography.
        
        Args:
            image_path (str): Path to the steganographic image
        
        Returns:
            str: The extracted message, or None if extraction fails
        """
        try:
            # Open the image
            img = Image.open(image_path)
            img = img.convert('RGB')
            pixels = list(img.getdata())
            
            # Extract binary data from LSBs
            binary_data = ""
            
            for pixel in pixels:
                r, g, b = pixel
                
                # Extract LSB from each channel
                binary_data += self._extract_lsb(r)
                binary_data += self._extract_lsb(g)
                binary_data += self._extract_lsb(b)
            
            # Convert binary data to message
            full_message = self._binary_to_message(binary_data)
            
            # Find the delimiter and extract the actual message
            if self.delimiter in full_message:
                message = full_message.split(self.delimiter)[0]
                return message
            else:
                print("Error: No hidden message found or message corrupted.")
                return None
                
        except Exception as e:
            print(f"Error extracting message: {str(e)}")
            return None
    
    def compare_images(self, original_path, stego_path):
        """
        Compare original and steganographic images for analysis.
        
        Args:
            original_path (str): Path to original image
            stego_path (str): Path to steganographic image
        """
        try:
            original = Image.open(original_path).convert('RGB')
            stego = Image.open(stego_path).convert('RGB')
            
            if original.size != stego.size:
                print("Images have different dimensions!")
                return
            
            orig_pixels = list(original.getdata())
            stego_pixels = list(stego.getdata())
            
            differences = 0
            max_diff = 0
            
            for i, (orig, stego) in enumerate(zip(orig_pixels, stego_pixels)):
                for j in range(3):  # RGB channels
                    diff = abs(orig[j] - stego[j])
                    if diff > 0:
                        differences += 1
                        max_diff = max(max_diff, diff)
            
            total_values = len(orig_pixels) * 3
            print(f"\nImage Comparison:")
            print(f"Total pixel values: {total_values}")
            print(f"Modified values: {differences}")
            print(f"Modification percentage: {(differences/total_values)*100:.2f}%")
            print(f"Maximum difference: {max_diff}")
            
        except Exception as e:
            print(f"Error comparing images: {str(e)}")


def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(description='LSB Steganography Tool')
    parser.add_argument('action', choices=['hide', 'extract', 'compare'], 
                       help='Action to perform')
    parser.add_argument('-i', '--input', required=True, 
                       help='Input image path')
    parser.add_argument('-o', '--output', 
                       help='Output image path (for hide action)')
    parser.add_argument('-m', '--message', 
                       help='Message to hide (for hide action)')
    parser.add_argument('-f', '--file', 
                       help='Text file containing message to hide')
    parser.add_argument('-c', '--compare', 
                       help='Second image path for comparison')
    
    args = parser.parse_args()
    
    stego = LSBSteganography()
    
    if args.action == 'hide':
        if not args.output:
            print("Error: Output path required for hide action")
            return
        
        message = ""
        if args.message:
            message = args.message
        elif args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    message = f.read()
            except Exception as e:
                print(f"Error reading file: {str(e)}")
                return
        else:
            message = input("Enter message to hide: ")
        
        if message:
            stego.hide_message(args.input, message, args.output)
        else:
            print("Error: No message provided")
    
    elif args.action == 'extract':
        message = stego.extract_message(args.input)
        if message:
            print(f"\nExtracted message:\n{message}")
        else:
            print("Failed to extract message")
    
    elif args.action == 'compare':
        if not args.compare:
            print("Error: Second image path required for comparison")
            return
        stego.compare_images(args.input, args.compare)


# Interactive mode functions
def interactive_mode():
    """Run the program in interactive mode."""
    stego = LSBSteganography()
    
    while True:
        print("\n" + "="*50)
        print("LSB Steganography Tool")
        print("="*50)
        print("1. Hide message in image")
        print("2. Extract message from image")
        print("3. Compare images")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            image_path = input("Enter path to input image: ").strip()
            if not os.path.exists(image_path):
                print("Error: Input image not found!")
                continue
            
            print("\nChoose message input method:")
            print("1. Type message")
            print("2. Load from file")
            msg_choice = input("Enter choice (1-2): ").strip()
            
            message = ""
            if msg_choice == '1':
                message = input("Enter message to hide: ")
            elif msg_choice == '2':
                file_path = input("Enter path to text file: ").strip()
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        message = f.read()
                    print(f"Loaded {len(message)} characters from file")
                except Exception as e:
                    print(f"Error reading file: {str(e)}")
                    continue
            else:
                print("Invalid choice!")
                continue
            
            output_path = input("Enter output image path: ").strip()
            if not output_path:
                base, ext = os.path.splitext(image_path)
                output_path = f"{base}_stego{ext}"
                print(f"Using default output path: {output_path}")
            
            success = stego.hide_message(image_path, message, output_path)
            if success:
                print(f"\nMessage hidden successfully!")
                print(f"Message length: {len(message)} characters")
        
        elif choice == '2':
            image_path = input("Enter path to steganographic image: ").strip()
            if not os.path.exists(image_path):
                print("Error: Image not found!")
                continue
            
            message = stego.extract_message(image_path)
            if message:
                print(f"\nExtracted message ({len(message)} characters):")
                print("-" * 40)
                print(message)
                print("-" * 40)
                
                save_choice = input("\nSave extracted message to file? (y/n): ").strip().lower()
                if save_choice == 'y':
                    filename = input("Enter filename (default: extracted_message.txt): ").strip()
                    if not filename:
                        filename = "extracted_message.txt"
                    
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(message)
                        print(f"Message saved to {filename}")
                    except Exception as e:
                        print(f"Error saving file: {str(e)}")
            else:
                print("Failed to extract message or no message found.")
        
        elif choice == '3':
            img1_path = input("Enter path to first image: ").strip()
            img2_path = input("Enter path to second image: ").strip()
            
            if not os.path.exists(img1_path):
                print("Error: First image not found!")
                continue
            if not os.path.exists(img2_path):
                print("Error: Second image not found!")
                continue
            
            stego.compare_images(img1_path, img2_path)
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please enter 1-4.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        main()
    else:
        # Interactive mode
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")