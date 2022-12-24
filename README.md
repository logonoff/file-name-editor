# vscode but for file names
quick script that helps you mass-edit file names with vscode

**motivation**: i wanted to multi-cursor edit my file names but didn't see anything that let me do that

### how to use
0. install vscode (optional), and python 3
1. install the package using pip: `pip install vs-rename`
2. open the program `ren-vs`. if no arguments for path are supplied it will use the cwd
3. vscode will open with a list of the file names in that directory. change those as you please
4. save the file and close it
5. the files will be renamed according to how you changed it in vscode
6. hopefully nothing broke
