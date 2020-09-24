# checkThatLink

This is a CLI tool used to check an html file for the status of the URL's it contains.

This application requires Python version 3.0 or higher. It also requires that you install urllib3 by using the following command.

```$ pip install urllib3 ```

To use, run the application using.

```$  checkThatLink.py```

The application requires the path to a file as it's first positional argument.

```$  checkThatLink.py [fileName]```

You can also use the optional flag argument -s or --secureHttp to indicate that you want to see if the supplied http URL's
will work using https instead.

``` $  checkThatLink.py [fileName] -s```

The status of the URL will be shown by colour
  - Green = good link
  - Cyan = secured link
  - Red = bad link
  - Grey = unknown link
  

