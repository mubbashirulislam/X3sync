
# X3sync

## Overview

X3sync Tool is a Python script that allows users to synchronize their browser data—including bookmarks, cookies, and passwords—across multiple browsers to a USB drive. This tool is particularly useful for users who frequently switch between different devices and want to keep their browser settings consistent. 

### Supported Browsers

The tool currently supports the following browsers:
- **Brave**
- **Google Chrome**
- **Microsoft Edge**
- **Mozilla Firefox**

## Key Features

- **Data Extraction**: The script extracts bookmarks, cookies, and passwords from the supported browsers.
- **USB Drive Backup**: Automatically saves the extracted data to a connected USB drive.
- **Logging**: Keeps a detailed log of its operations, making it easy to track what was synchronized and any errors that may have occurred.

### Important Note

This script handles sensitive data, including passwords. Users should exercise caution and ensure compliance with all relevant laws and regulations when using this tool.

## How It Works

1. **USB Drive Detection**: The script checks for a connected USB drive using the Windows File System Object.
2. **Data Extraction Process**:
   - It accesses specific data paths for each supported browser.
   - Extracts bookmarks, cookies, and passwords from the respective database files.
3. **Data Storage**: The script saves the extracted data in both HTML and JSON formats on the USB drive for easy access.

### Data Structure

- **Bookmarks**: Saved as HTML files for easy viewing and importing into other browsers.
- **Cookies**: Saved in JSON format, which can be parsed easily by other tools if needed.
- **Passwords**: Also saved in JSON format. Users should handle this file with care to prevent unauthorized access.

## Installation

To run this script, you need to have Python installed on your system. Follow these steps to set it up:

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/downloads/).
2. **Install Required Packages**: Open your command line or terminal and run the following command to install the required package:
   ```bash
   pip install pywin32
   ```

## Usage

### Step-by-Step Instructions

1. **Connect a USB Drive**: Make sure your USB drive is plugged into your computer. Note the drive letter assigned to it (e.g., `E:\`).
2. **Download the Script**: Clone this repository or download the script file (`browser_data_sync.py`) to your local machine.
3. **Run the Script**: Open your command line or terminal and navigate to the directory where the script is located. Run the script using:
   ```bash
   python browser_data_sync.py
   ```
4. **Check Logs**: After execution, the script generates a log file named `browser_data_sync.log` in the same directory. This file provides a record of the synchronization process, including any errors or warnings encountered.

## Sensitivity Disclaimer

This script handles sensitive data. The author is not responsible for any misuse, data breaches, or violations of privacy that may arise from using this tool. Users should take appropriate measures to secure their data.

### Recommended Practices

- **Backup Data Regularly**: Regularly use the tool to keep your browser data backed up on your USB drive.
- **Secure Your USB Drive**: Ensure that your USB drive is secure and protected with a password if it contains sensitive information.
- **Review Log Files**: Periodically check the log files for any issues or anomalies during the synchronization process.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! If you'd like to improve this tool, feel free to fork the repository and submit a pull request. Please ensure your code follows best practices and is well-documented.

## Acknowledgments

This script was developed by me, utilizing my knowledge and the help of AI, to address the need for seamless synchronization of browser data across devices. Thank you to the open-source community for providing the tools and libraries that made this project possible.

## Contact

For questions or feedback regarding the Browser Data Sync Tool, please reach out to me at [imsabbirahmed.info@gmail.com].
```
