
# Copy As Python Request Extension
A working burpsuite extension for copying raw HTTP as python request (The one on bApp store is pretty buggy). This one uses a modified parser from curl.trillworks.com, instead of writing my own parser. 

# Usage
1. download jython and link it on burp > extender > options 
2. Go to jython directory and run the command below to install additional package
```
java -jar jython-standalone-2.7.2.jar -m ensurepip
java -jar jython-standalone-2.7.2.jar -m pip install requests
```
3. load the extension on burpsuite, extender > add > select python