# SQUSeatStealer

**SQUSeatStealer** is a Python desktop application that automates the process of quickly enrolling in full or nearly full courses at **Sultan Qaboos University (SQU)**.  
It monitors the course seat availability in real time and instantly registers the course when a seat becomes available.

> **Important Note:**: Since the university website has been changed and updated, this tool no longer works.

## Features

- 🎓 **Login to SQU SIS**: Authenticate securely using your student credentials.
- 📚 **Monitor Course Seats**: Automatically monitor real-time available seats for a specific course.
- ⚡ **Auto Registration**: Instantly register when a seat is detected.
- 🌐 **Arabic and English Support**: Two versions are available – `main_en.py` for English, and `main_ar.py` for Arabic interface.
- 🖥️ **Modern Dark Theme**: GUI built with `tkinter` and styled with `sv-ttk`.
- 🔒 **User Validation**: Only authorized users can use the tool.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/SQUSeatStealer.git
   cd SQUSeatStealer
   ```

2. **Install Dependencies**

   Make sure you have Python 3 installed, then install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   - For English:
     ```bash
     python main_en.py
     ```

   - For Arabic:
     ```bash
     python main_ar.py
     ```

## Usage

1. Launch either the English or Arabic version.
2. Enter your **Username**, **Password**, and **Course Information**:
   - Example input: `COMP3202 10`
   - Format: `COURSE_CODE SECTION_NUMBER`
3. Click **Register**.
4. The app will continuously monitor the course and automatically register when a seat becomes available.

## Code Overview

- **`main_en.py`**: English GUI interface for seat monitoring and auto-registration.
- **`main_ar.py`**: Arabic GUI interface.
- **`functions.py`**: Core backend functions for:
  - Logging into the SIS system
  - Checking and adding courses
  - Scraping seat availability
- **`requirements.txt`**: List of dependencies.
