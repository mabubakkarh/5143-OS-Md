# Assignment 2: Implementing a Basic Shell* in Python
## Date: 2/20/2022
###### *Shell must run in the terminal
##### Group Member: Md Abubakkar, Parker Hagmaier & Sabin Dhekee.
##### In this project we have created a basic terminal using python 3
##### 👉A full list of the functions and commands can be found in the commands.md page
##### 👉All of our commands/functions work and are able to be redirected/piped and or recieve input from both pipes and redirects 
##### 👉Not all of the code is perfect, for example our ls does not display the way ls is displayed sorted into rows in columns in a real terminal but 
##### 👉Everything else does work. Also it should be noted our delete function does not function perfectly either and I don't know why but at one point it worked
##### in Ubuntu and I tried to change it for mac and cannot remeber what was chnaged but it does technically delete but the characters don't show 
##### as being deleted if you write over them the change is reflected but until then it just looks like the cursor is moving backwards 
##### it is most likley a simple mistake.
##### 👉Another problem is if a list is nested not all commands/functions will remove the outer brackets and this will effect commands such as sort
##### 👉The shell.py file contains the actual shell which is what takes user input and calls commands or at least calls the fnction that calls commands
##### 👉The shell.py is the shell part but the work of sending the commands to get called and dealing with pipe or redirects is done in the parse.py file which then
##### calls the call() function which uses a dictionary that has all our functions imported into it
##### 👉our parse uses reccursion to deal with pipeing and or redirection constantly calling itself without the pipe or redirect and then feeding that in as input to the 
##### 👉next command this is more thourgly explained in the comments of each specific command/function 
##### 👉The Ls command is where we recieved the most help since we were clueless on how to accomplish this and it will be cited bellow along with others


##### Sources:
###### 1. LS Command source this was the source I most used and took from: 🔗 [Carl Tashian Youtube channel](https://www.youtube.com/watch?v=VTNrfcDrP_U&t=107s) 
###### 2. For Colors 🔗 [Stackoverflow question](https://stackoverflow.com/questions/63768372/color-codes-for-discord-py) (Used almost in its entirety since it is just the codes on how to change the color)
###### 3. The sort in Ls along with the sort in my sort function to sort by lowercase is from this 🔗 [stackoverflow help](https://stackoverflow.com/questions/28136374/python-sort-strings-alphabetically-lowercase-first)
###### 4. rm and rm dir. 🔗 [How to use shutil to remove directories/files](https://www.geeksforgeeks.org/delete-a-directory-or-file-using-python/)
###### 5. Cd 🔗 [how to change directories in python](https://www.geeksforgeeks.org/change-current-working-directory-with-python/)
###### 6. Pwd 🔗[how to get the current working directory python](https://www.tutorialspoint.com/How-to-know-current-working-directory-in-Python)
