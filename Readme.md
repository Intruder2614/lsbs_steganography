# LSB Steganography Tool

A Python-based steganographic tool that conceals data in images using the Least Significant Bit (LSB) method. This project allows you to hide secret messages within image files with minimal visual distortion.

##  Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Interactive Mode](#interactive-mode)
  - [Command Line Mode](#command-line-mode)
- [How It Works](#how-it-works)
- [Examples](#examples)
- [Technical Details](#technical-details)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

##  Overview

This steganography tool implements the LSB (Least Significant Bit) technique to hide text messages within digital images. The LSB method modifies the least significant bit of each color channel (RGB) in an image to store binary data representing your secret message.

The tool is designed to be:
- **User-friendly**: Both command-line and interactive interfaces
- **Robust**: Comprehensive error handling and validation
- **Secure**: Minimal visual distortion with delimiter-based message detection
- **Versatile**: Support for various image formats and message input methods

##  Features

- **Hide Messages**: Embed text messages or files into images
- **Extract Messages**: Retrieve hidden messages from steganographic images
- **Multiple Input Methods**: 
  - Direct text input
  - Load messages from text files
- **Image Comparison**: Analyze differences between original and steganographic images
- **Format Support**: Works with common image formats (JPEG, PNG, BMP, etc.)
- **Dual Interface**: Command-line arguments or interactive menu
- **Capacity Checking**: Validates if an image can hold the desired message
- **Error Handling**: Comprehensive validation and error reporting

##  Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Install Dependencies

```bash
pip install Pillow
```

### Download the Tool

1. Clone this repository or download the `lsb_steganography.py` file
2. Ensure the file has execute permissions (Unix/Linux/macOS):
   ```bash
   chmod +x lsb_steganography.py
   ```

##  Usage

The tool can be used in two modes: Interactive Mode (menu-driven) or Command Line Mode (with arguments).

### Interactive Mode

Run the script without any arguments to enter interactive mode:

```bash
python lsb_steganography.py
```

This will present a user-friendly menu with the following options:
1. Hide message in image
2. Extract message from image
3. Compare images
4. Exit

### Command Line Mode

Use command-line arguments for automation or scripting:

#### Hide a Message

```bash
# Hide a typed message
python lsb_steganography.py hide -i input_image.jpg -o output_image.jpg -m "Your secret message"

# Hide message from a text file
python lsb_steganography.py hide -i input_image.jpg -o output_image.jpg -f message.txt
```

#### Extract a Message

```bash
python lsb_steganography.py extract -i steganographic_image.jpg
```

#### Compare Images

```bash
python lsb_steganography.py compare -i original_image.jpg -c steganographic_image.jpg
```

### Command Line Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `action` | Action to perform: `hide`, `extract`, or `compare` | Yes |
| `-i, --input` | Input image path | Yes |
| `-o, --output` | Output image path (for hide action) | For hide |
| `-m, --message` | Message to hide | Optional |
| `-f, --file` | Text file containing message to hide | Optional |
| `-c, --compare` | Second image path for comparison | For compare |

##  How It Works

### LSB Steganography Technique

1. **Message Encoding**: The text message is converted to binary format
2. **Pixel Modification**: Each bit of the message replaces the least significant bit of RGB color channels
3. **Delimiter Addition**: A special delimiter (`###END###`) marks the end of the hidden message
4. **Image Reconstruction**: Modified pixels are reassembled into the output image

### Capacity Calculation

The maximum message length depends on the image dimensions:
```
Max characters ≈ (Width × Height × 3) ÷ 8
```

For example, a 1920×1080 image can hide approximately 777,600 characters.

## 💡 Examples

### Example 1: Basic Message Hiding

```bash
# Hide a simple message
python lsb_steganography.py hide -i family_photo.jpg -o hidden_message.jpg -m "Meet me at midnight"

# Extract the message
python lsb_steganography.py extract -i hidden_message.jpg
```

Output:
```
Message successfully hidden in 'hidden_message.jpg'
Original image size: 2048576 bytes
Steganographic image size: 2048576 bytes

Extracted message:
Meet me at midnight
```

### Example 2: Hiding a File

Create a text file with your message:
```bash
echo "This is a longer secret message that spans multiple lines.
It can contain any text content you want to hide.
The tool will handle it automatically." > secret.txt

# Hide the file contents
python lsb_steganography.py hide -i landscape.png -o stego_landscape.png -f secret.txt
```

### Example 3: Image Analysis

```bash
python lsb_steganography.py compare -i original.jpg -c steganographic.jpg
```

Output:
```
Image Comparison:
Total pixel values: 6220800
Modified values: 1152
Modification percentage: 0.02%
Maximum difference: 1
```

##  Technical Details

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- And other formats supported by PIL

### Algorithm Specifications

- **Method**: LSB substitution in RGB channels
- **Bit Order**: Sequential (R→G→B→R→G→B...)
- **Delimiter**: `###END###` (marks message end)
- **Encoding**: UTF-8 for text messages

### Performance Characteristics

- **Visual Impact**: Minimal (changes only LSBs)
- **Size Impact**: No increase in file size
- **Processing Speed**: Linear with image size
- **Memory Usage**: Loads entire image into memory

##  Security Considerations

### Strengths

- **Invisible to Naked Eye**: LSB changes are imperceptible
- **Format Preservation**: Maintains original image format
- **No Size Increase**: File size remains unchanged

### Limitations

- **Statistical Detection**: Vulnerable to chi-square and other statistical tests
- **Compression Sensitivity**: JPEG compression may corrupt hidden data
- **No Encryption**: Messages are hidden but not encrypted
- **Known Format**: Standard LSB implementation

### Security Recommendations

1. **Use PNG format** for better data preservation
2. **Encrypt messages** before hiding them
3. **Use cover images** with natural noise/complexity
4. **Avoid consecutive hiding** in the same image
5. **Consider file metadata** cleaning

##  Troubleshooting

### Common Issues

#### "Message too long" Error
```
Error: Message too long! Image can hold X bits, but message needs Y bits.
```
**Solution**: Use a larger image or shorter message

#### "No hidden message found"
```
Error: No hidden message found or message corrupted.
```
**Solutions**:
- Ensure the image contains a hidden message
- Check if the image was compressed after steganography
- Verify the image wasn't modified

#### PIL/Pillow Installation Issues
```bash
# Try upgrading pip first
pip install --upgrade pip

# Install Pillow
pip install Pillow

# If issues persist, try:
pip install --upgrade Pillow
```

#### File Permission Errors
```bash
# Unix/Linux/macOS
chmod 644 input_image.jpg
chmod 755 output_directory/

# Or run with appropriate permissions
sudo python lsb_steganography.py ...
```

### Performance Issues

For large images (>10MB), consider:
- Using smaller images when possible
- Ensuring sufficient RAM availability
- Processing on systems with adequate memory

##  Contributing

Contributions are welcome! Here are ways you can help:

1. **Bug Reports**: Submit detailed bug reports with reproduction steps
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit pull requests with enhancements
4. **Documentation**: Improve documentation and examples
5. **Testing**: Test with different image formats and sizes

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd lsb-steganography

# Install dependencies
pip install Pillow

# Run tests (if available)
python -m pytest tests/
```

##  License

This project is released under the MIT License. See the LICENSE file for details.

## Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing issues in the repository
3. Create a new issue with detailed information
4. Include sample images and error messages when possible

##  Acknowledgments

- **Python Imaging Library (PIL/Pillow)** for image processing capabilities
- **Steganography research community** for LSB technique documentation
- **Contributors** who have helped improve this tool

---

** Disclaimer**: This tool is for educational and legitimate purposes only. Users are responsible for complying with applicable laws and regulations regarding data hiding and privacy.