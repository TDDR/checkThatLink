# checkThatLink

This is a CLI tool used to check an html file for the status of the URL's it contains. In order to install and use this tool on your 
computer you can run the following command. 

*note, you must have python installed to use this tool, if you do not, check out thier [installation guide](https://wiki.python.org/moin/BeginnersGuide/Download)*

```pip install Check-That-Link```

The application can now be run from the command line with the abriviated form like.

```$  clt [fileName]```

*requires the path to a file as it's first positional argument.*

The status of the URL will be shown by colour
  - Green = good link
  - Cyan = secured link
  - Red = bad link
  - Grey = unknown link
  
### Options

|Optional argument| Descritption |
|-----------------|--------------|
| -s, --secureHttp | Indicates that you want to see if the supplied http URL's will work using https instead. |
| -j, --json | Output will be displayed as JSON |
| -a, --all | Show results for all links in file (default behaviour) |
| -g, --good | Show results for good links only |
| -b, --bad | Show results for bad links only |
| -i [file], --ignore [file] | this option requiers a file that contains a list or URL's to ignore. *Note 1*|
| -t, --telescope | Check the status of the latest 10 Telescope posts.|

*Note 1* - The format of an ignored URLs text file is as follows:
- URLs must be placed on separate lines and begin with either `http` or `https`
- Any line that begins with `#` is a comment and will not be parsed 

*Note 2* - You must have Telescope's backend running locally in order to use this feature
