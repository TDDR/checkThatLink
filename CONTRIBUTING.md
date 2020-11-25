## Contributing

First of all, thank you for wanting to contribute to my repository. You can create an issue or just send a PR and I'll get to it as soon as possible.

### Setup

This application requires Python version 3.0 or higher. It also requires a few dependandices which can be installed with the following command.

`$ pip install urllib3 pytest pytest-cov `

To use, run the application using.

`$ checkThatLink.py`

The application requires the path to a file as it's first positional argument.

`$ checkThatLink.py [fileName]`

### Auto Formatting with Visual Studio Code

If you are using Visual Studio code both Black and Flake8 will be run automatically on your
work every time you save the file.

### For All editors

If you are not using Visual Studio code, or even if you are, there is a pre-commit hook that
will run both Black and Flake8 when you make a commit.

If you don't want to wait until a commit to check you can always run either option
from the command line

#### Formatting with Black

You can run the following command from the root directory to check all the files at once.

`$ black . `

#### Checking for lint with Flake8

Like with Black, you can run this command from the root directory to check all relevant .py files

`$ flake8 . `

## Testing

to insure continuos integration there are GitHub Actions tied to this repo. They will automatically perform tests to make 
sure a PR does not break anything in the master branch. If you would like to write some tests, or just run the test before making a PR, the you can do the following. 

- To run the test suite simply run the folling command from the root of the repository. There is a (-v)erbose option as well<br>
`$ pytest`

- You can also see the coverage of the tests by using:<br>
`$ pytest --cov=.`
