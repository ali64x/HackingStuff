<h1>FINDXSS</h1>
<h6>
This tool allows you to run xss test on multiple urls , searching all the parameters for possible xss injections with ease , you can control its speed slow it down 
for programs that doesn't allow scanning ,or speed it up for very big files .
provide it with your email and it will send you the progress of your job
sends email of the vulrenable urls , the progress of the running job (finished , error ,...)
all vulrnable urls can be found in the file named foundxss.txt in the same directory of the tool 
all urls that got terminated due to  any kind of errors and didn't get checked propperly by the tool are stored in the file named exceptions.txt

<h3>HOW TO USE IT:</h3>
all you have to do is just provide a file containing the urls formated as follow : "https://www.example.com?parameter=ok" one url per line .
you can use the "<a href="https://github.com/ali64x/does.git">does</a>" tool to format the urls properly </h6>
<br><br>
<h3>Installation:</h3>
create a new folder , open the terminal in that directory , type : git clone https://github.com/ali64x/HackingStuff.git
<br><br>
<h3>Run :</h3>
open the newly installed folder or use cd command to navigate to it ,then type : python3 findxss.py
<br>
Follow the instruction provided there and good luck 🙂
