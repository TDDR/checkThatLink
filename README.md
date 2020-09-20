# checkThatLink

This is a CLI tool used to check an html file for the status of the url's it contains.

To use, run the application using.
  ```$  checkThatLink.py```

The application requires the path to an html file as it's first positioanl argument.
  ```$  checkThatLink.py index.html```

The status of the url will be shown by colour
  - Green = good link
  - Red = bad link
  - Grey = Unknown link
  
You can also use the optional flag argument -s to indicate that you want to see if the supplied http url's
will work using https instead.
 ``` $  checkThatLink.py index.html -s```
 
