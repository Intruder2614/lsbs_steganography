import os
import argparse
import sys
from .steganography import LSBSteganography


def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(description='LSB Steganography Tool')
    parser.add_argument('action', choices=['hide', 'extract', 'compare', 'capacity'], 
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
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # If interactive mode requested or no arguments, run interactive mode
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return
    
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
    
    elif args.action == 'capacity':
        capacity_info = stego.get_capacity(args.input)
        if capacity_info:
            print(f"\nImage Capacity Information:")
            print(f"Dimensions: {capacity_info['width']} x {capacity_info['height']}")
            print(f"Total pixels: {capacity_info['total_pixels']:,}")
            print(f"Total available bits: {capacity_info['total_bits']:,}")
            print(f"Maximum characters: {capacity_info['max_characters']:,}")
            print(f"Delimiter overhead: {capacity_info['delimiter_overhead']} bits")


def interactive_mode():
    """Run the program in interactive mode."""
    stego = LSBSteganography()
    
    print("="*60)
    print("LSB Steganography Tool - Interactive Mode")
    print("="*60)
    
    while True:
        print("\n" + "="*50)
        print("Available Actions:")
        print("="*50)
        print("1. Hide message in image")
        print("2. Extract message from image")
        print("3. Compare images")
        print("4. Check image capacity")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            image_path = input("Enter path to input image: ").strip()
            if not os.path.exists(image_path):
                print("Error: Input image not found!")
                continue
            
            # Check capacity first
            capacity_info = stego.get_capacity(image_path)
            if capacity_info:
                print(f"\nImage can hold up to {capacity_info['max_characters']:,} characters")
            
            print("\nChoose message input method:")
            print("1. Type message directly")
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
            
            if not message:
                print("Error: No message provided!")
                continue
            
            # Check if message fits
            if capacity_info and len(message) > capacity_info['max_characters']:
                print(f"Error: Message too long ({len(message)} chars > {capacity_info['max_characters']} max)")
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
            
            print("Extracting message... This may take a moment.")
            message = stego.extract_message(image_path)
            if message:
                print(f"\nExtracted message ({len(message)} characters):")
                print("-" * 60)
                print(message)
                print("-" * 60)
                
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
            image_path = input("Enter path to image: ").strip()
            if not os.path.exists(image_path):
                print("Error: Image not found!")
                continue
            
            capacity_info = stego.get_capacity(image_path)
            if capacity_info:
                print(f"\nImage Capacity Information:")
                print(f"File: {os.path.basename(image_path)}")
                print(f"Dimensions: {capacity_info['width']} x {capacity_info['height']}")
                print(f"Total pixels: {capacity_info['total_pixels']:,}")
                print(f"Available storage bits: {capacity_info['available_bits']:,}")
                print(f"Maximum message length: {capacity_info['max_characters']:,} characters")
                print(f"Delimiter overhead: {capacity_info['delimiter_overhead']} bits")
                
                # Calculate some example sizes
                print(f"\nExample storage capacities:")
                print(f"- Tweet (280 chars): {'✓' if capacity_info['max_characters'] >= 280 else '✗'}")
                print(f"- Short email (~1KB): {'✓' if capacity_info['max_characters'] >= 1000 else '✗'}")
                print(f"- Long document (~10KB): {'✓' if capacity_info['max_characters'] >= 10000 else '✗'}")
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please enter 1-5.")
            
        # Ask if user wants to continue
        if choice in ['1', '2', '3', '4']:
            continue_choice = input("\nPerform another operation? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("Goodbye!")
                break


if __name__ == "__main__":
    main()