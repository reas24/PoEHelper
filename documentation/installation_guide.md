# Path of Exile Economy Analysis Tool - Installation Guide

This guide provides detailed instructions for installing and running the Path of Exile Economy Analysis Tool on different operating systems.

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+ recommended)
- **Python**: Version 3.8 or newer
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 200MB free space
- **Internet Connection**: Required for fetching real-time data from poe.ninja

## Windows Installation

### Step 1: Install Python (if not already installed)

1. Download the latest Python installer from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check the box that says "Add Python to PATH" during installation
4. Complete the installation

### Step 2: Download and Extract the Tool

1. Download the PoE_Economy_Analysis_Tool.zip file
2. Right-click the zip file and select "Extract All..."
3. Choose a destination folder and click "Extract"

### Step 3: Install Dependencies

1. Open Command Prompt (Press Win+R, type "cmd", and press Enter)
2. Navigate to the extracted directory:
   ```
   cd C:\path\to\extracted\folder
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Step 4: Run the Application

1. In the same Command Prompt window, run:
   ```
   python app.py
   ```
2. You should see output indicating the server has started
3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## macOS Installation

### Step 1: Install Python (if not already installed)

1. Download the latest Python installer from [python.org](https://www.python.org/downloads/)
2. Run the installer and follow the instructions
3. Complete the installation

### Step 2: Download and Extract the Tool

1. Download the PoE_Economy_Analysis_Tool.zip file
2. Double-click the zip file to extract it
3. Move the extracted folder to your desired location

### Step 3: Install Dependencies

1. Open Terminal (Applications > Utilities > Terminal)
2. Navigate to the extracted directory:
   ```
   cd /path/to/extracted/folder
   ```
3. Install required dependencies:
   ```
   pip3 install -r requirements.txt
   ```

### Step 4: Run the Application

1. In the same Terminal window, run:
   ```
   python3 app.py
   ```
2. You should see output indicating the server has started
3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Linux Installation

### Step 1: Install Python and pip (if not already installed)

For Ubuntu/Debian:
```
sudo apt update
sudo apt install python3 python3-pip
```

For Fedora:
```
sudo dnf install python3 python3-pip
```

### Step 2: Download and Extract the Tool

1. Download the PoE_Economy_Analysis_Tool.zip file
2. Extract it using the command:
   ```
   unzip PoE_Economy_Analysis_Tool.zip -d /path/to/destination
   ```
   Or use your desktop environment's archive manager

### Step 3: Install Dependencies

1. Open Terminal
2. Navigate to the extracted directory:
   ```
   cd /path/to/extracted/folder
   ```
3. Install required dependencies:
   ```
   pip3 install -r requirements.txt
   ```

### Step 4: Run the Application

1. In the same Terminal window, run:
   ```
   python3 app.py
   ```
2. You should see output indicating the server has started
3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Troubleshooting

### Common Issues

#### "Python is not recognized as an internal or external command"

This means Python is not in your PATH. Try:
- Reinstalling Python and make sure to check "Add Python to PATH"
- Or use the full path to Python: `C:\Path\to\Python\python.exe app.py`

#### "No module named 'flask'"

This means the dependencies were not installed correctly. Run:
```
pip install -r requirements.txt
```

#### "Address already in use"

This means port 5000 is already being used by another application. You can:
1. Close the other application
2. Or modify app.py to use a different port:
   ```python
   app.run(host='0.0.0.0', port=5001, debug=False)
   ```

#### "Connection refused" when accessing localhost:5000

This could mean:
- The application is not running
- A firewall is blocking the connection
- The application is running on a different port

#### "Cannot fetch data from poe.ninja"

This could mean:
- Your internet connection is down
- poe.ninja is down or has changed its API
- Your network is blocking access to poe.ninja

### Getting Help

If you encounter issues not covered here:
1. Check the console output for error messages
2. Refer to the developer documentation
3. Contact the developer with details about your issue

## Running as a Service

### Windows

To run the application as a service on Windows:

1. Install NSSM (Non-Sucking Service Manager):
   - Download from [nssm.cc](https://nssm.cc/download)
   - Extract to a folder

2. Open Command Prompt as Administrator
3. Navigate to the NSSM folder
4. Run:
   ```
   nssm install PoEEconomyTool
   ```
5. In the dialog:
   - Path: `C:\Path\to\Python\python.exe`
   - Startup directory: `C:\path\to\extracted\folder`
   - Arguments: `app.py`
6. Configure other settings as needed and click "Install service"

### Linux (systemd)

To run the application as a service on Linux:

1. Create a service file:
   ```
   sudo nano /etc/systemd/system/poe-economy-tool.service
   ```

2. Add the following content:
   ```
   [Unit]
   Description=Path of Exile Economy Analysis Tool
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/extracted/folder
   ExecStart=/usr/bin/python3 /path/to/extracted/folder/app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Save and exit (Ctrl+X, Y, Enter)
4. Enable and start the service:
   ```
   sudo systemctl enable poe-economy-tool
   sudo systemctl start poe-economy-tool
   ```

5. Check status:
   ```
   sudo systemctl status poe-economy-tool
   ```
