# neuralut
neuralut

# setup
dependencies:
- pyenv 
	- https://github.com/pyenv/pyenv#installation
	- `curl https://pyenv.run | bash`
- pipenv
	- https://pipenv.pypa.io/en/latest/#install-pipenv-today
	- `pip install --user pipenv` ~~(I normally drop --user and install globally)~~ (don't do that)

setup:
- `pipenv install`
	- if pipenv didn't detect pyenv and prompt to install the correct version of python, might need to run `pyenv install` first
- `pipenv run python tkintertest.py`
	- might need to install system tkinter, readline, bz2, sqlite dev libraries (if python not compiled with them, if using pyenv this is usually because the appropriate libraries are not installed)

notes:
2/18/2021
- new build command is `pyinstaller neuralut.exe.spec`
- tkintertest is getting the the point where it will need cleaned up. possibly after v 0.1.0


2/12/2021
- kivy sucks for everything. back to tkinter, looks 90s AF but we good
- new command is `pyinstaller -F -w tkintertest.py --icon neuralut.ico -n neuralut.exe`


2/10/2021
- there might be a problem with openlut, look into alternatives
- build command `pyinstaller -F -w kivytest.py --icon neuralut.ico -n neuralut.exe`
- trying to get command `pyinstaller kivytest.spec` to create an exe that actually shows the ui... turns out it worked. I was just doing it wrong it's far too late to be working on this
