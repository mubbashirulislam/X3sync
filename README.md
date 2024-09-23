
# X3sync

showcase.gif

## Overview

**X3sync** is a powerful Python tool designed to synchronize your browser data—including bookmarks, cookies, and passwords—across multiple browsers to a USB drive. This utility is especially beneficial for users who frequently switch between different devices and wish to maintain consistent browser settings.

### Supported Browsers

The tool currently supports the following browsers:
- **Brave**
- **Google Chrome**
- **Microsoft Edge**
- **Mozilla Firefox**

## Key Features

- **Data Extraction**: Efficiently extracts bookmarks, cookies, and passwords from the supported browsers.
- **USB Drive Backup**: Automatically saves the extracted data to a connected USB drive for easy portability.
- **Detailed Logging**: Maintains comprehensive logs of operations, allowing users to track synchronization events and errors.

### Important Note

This script handles sensitive data, including passwords. Users should exercise caution and ensure compliance with all relevant laws and regulations when using this tool.

## How It Works

1. **USB Drive Detection**: The script verifies the presence of a connected USB drive using the Windows File System Object.
2. **Data Extraction Process**:
   - Accesses specific data paths for each supported browser.
   - Extracts bookmarks, cookies, and passwords from the respective database files.
3. **Data Storage**: Saves the extracted data in both HTML and JSON formats on the USB drive for straightforward access.

### Data Structure

- **Bookmarks**: Stored as HTML files for easy viewing and importing into other browsers.
- **Cookies**: Saved in JSON format, facilitating parsing by other tools if necessary.
- **Passwords**: Stored in JSON format. Users should handle this file with care to prevent unauthorized access.

## Installation

To run this script, you must have Python installed on your system. Follow these steps to set it up:

1. **Install Python**: Download and install Python from the official site: [python.org](https://www.python.org/downloads/).
   
2. **Install Required Packages**: Open your command line (CMD) or terminal and execute the following command to install the necessary package:
   ```bash
   pip install pywin32
   ```

## Usage

### Step-by-Step Instructions

1. **Connect a USB Drive**: Ensure your USB drive is plugged into your computer. Note the assigned drive letter (e.g., `E:\`).
   
2. **Download the Script**: Clone this repository or download the script file (`browser_data_sync.py`) to your local machine.

3. **Run the Script**: Open your command line or terminal, navigate to the directory where the script is located, and execute:
   ```bash
   python browser_data_sync.py
   ```

4. **Check Logs**: After execution, the script generates a log file named `browser_data_sync.log` in the same directory. This file records the synchronization process, including any encountered errors or warnings.

## Sensitivity Disclaimer

This script handles sensitive data. The author is not responsible for any misuse, data breaches, or privacy violations that may occur from using this tool. Users must take appropriate measures to secure their data.

### Recommended Practices

- **Backup Data Regularly**: Utilize the tool frequently to keep your browser data backed up on your USB drive.
- **Secure Your USB Drive**: Ensure your USB drive is secured and protected with a password if it contains sensitive information.
- **Review Log Files**: Periodically check the log files for any issues or anomalies during the synchronization process.

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

## Contributing

Contributions are welcome! If you'd like to enhance this tool, feel free to fork the repository and submit a pull request. Please ensure your code adheres to best practices and is well-documented.

## Acknowledgments

This script was developed by me, utilizing my knowledge and the assistance of AI, to address the need for seamless synchronization of browser data across devices. Special thanks to the open-source community for providing the tools and libraries that made this project possible.

## Contact

For questions or feedback regarding the X3sync tool, please reach out to me at [imsabbirahmed.info@gmail.com].
