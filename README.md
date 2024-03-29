<h1>FINDXSS</h1>

## installation:
```sh
git clone https://github.com/ali64x/HackingStuff.git
```
```sh
cd HackingStuff/
```
```sh
pip install .
```
you may need to install termcolor manually to do that use:
```sh
pip install termcolor --upgrade
```

## Description:

This tool facilitates XSS testing on multiple URLs, systematically searching all parameters for potential XSS injections with ease. You have control over its speed, allowing you to slow it down for programs that do not permit scanning or speed it up for larger files. Additionally, providing your email allows the tool to send you progress updates.

## Features:

- **Parameter Scanning:** Scans all parameters for possible XSS vulnerabilities.
- **Speed Control:** Adjust the scanning speed to match the requirements of the target system.
- **Email Notifications:** Sends email updates on the progress of your job, including finished, error, and other status notifications.
- **Results Reporting:** Vulnerable URLs are stored in a file named `foundxss.txt` in the same directory as the tool.
- **Error Handling:** URLs terminated due to errors are recorded in the `exceptions.txt` file.

## Usage:

1. Provide a list of URLs to test.
2. Adjust the scanning speed as needed.
3. Provide your email for progress updates.

## Output Files:

- `foundxss.txt`: Contains all vulnerable URLs.
- `exceptions.txt`: Stores URLs that encountered errors during scanning.

## HOW TO USE IT:
all you have to do is just provide a file containing the urls formated as follow : "<a><b>https://www.example.com?parameter=ok</b></a>" one url per line .
you can use the "<a href="https://github.com/ali64x/does.git">does</a>" tool to format the urls properly </h6><br><br>
Or using flags ,type `findxss -h` to see all the available options .
<br><br>
<h3>Run :</h3>
open the newly installed folder or use cd command to navigate to it ,then type : <strong>python3 findxss.py</strong>
<br>
Follow the instructions provided there and good luck 🙂
