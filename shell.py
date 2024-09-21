#  SHELL semulator python - Omer Kfir יב'3

import subprocess, os, shutil
from colorama import Fore, Style

class CMD:
    
    #  Current cmd variables
    userName = ""
    computerName = ""
    currentPath = ""
    
    def __init__(self, userName=os.environ['USERNAME'], computerName=os.environ['COMPUTERNAME'], currentPath=os.getcwd()):
        
        self.userName = userName
        self.computerName = computerName
        self.currentPath = currentPath
        
        
    def print_prompt(self) -> None:
        """
            Prints the cmd prompt before every input from user
        """
        
        print(fr"{Fore.GREEN}{self.userName}@{self.computerName}{Fore.WHITE}:{Fore.LIGHTBLUE_EX}\{self.currentPath}{Style.RESET_ALL}$", end=" ")
    
    
    def __parse_path(self, path) -> str:
        """
            Returns a parsed path
        """
        
        build_path = []
        current_destination = path.split("\\")
        for d in current_destination:
            
            if d  == "..":
                build_path.pop()
            
            elif d != ".":
                build_path.append(d)
        
        build_path = "\\".join(build_path)
        return build_path

    
    def change_directory(self, destination) -> None:
        """
            Changes current working directory to be destination
        """
        
        #  If destination is None print the current working directory
        
        if len(destination) == 1:
            #  cd command without argss
            print(self.currentPath)
        
        else:
            
            #  Check if its a valid directory
            #  We also check for user_path since it can be a full path
            
            fullPath = os.path.join(self.currentPath, destination[1])
            user_path = destination[1]
            
            if os.path.isdir(fullPath):
                    
                self.currentPath = self.__parse_path(fullPath)
            
            elif os.path.isdir(user_path):
            
                self.currentPath = self.__parse_path(user_path)
            
            elif os.path.isfile(fullPath):
                print("The directory name is invalid.")
               
            elif os.path.isfile(user_path):
                print("The directory name is invalid.")
            
            else:
                print("The system cannot find the path specified.")
    
    
    def set_environment_variables(self, variable) -> None:
        """
            'set' command in windows, handles environment variables
        """
        
        if len(variable) == 1:
            #  set command without args
            print(*[f"{key}={value}" for key, value in os.environ.items()], sep='\n')
            return
        
        
        #  The set command does not split by whitespace
        #  It splits by the equal char
        
        environ_variable = variable[1].split("=")
        variable_name = environ_variable[0]
        
        if len(environ_variable) == 1:
            
            try:
                content = os.environ[variable_name]
                
                #  Get the original name of the environment variable
                
                for key in os.environ:
                    if key.lower() == variable_name.lower():
                        variable_name = key
                        break
                
                print(f"{variable_name}={content}")
            
            except KeyError:
                print(f"Environment variable {variable_name} not defined")
        
        else:
            
            #  Since '=' can be in the value itself we need to
            #  Return it from the split
            
            environ_variable_value = "".join(environ_variable[1:])  
            
            if environ_variable_value == "":
                try:
                    #  If variable does not exists it will return an error
                    
                    del os.environ[variable_name]
                    
                except KeyError:
                    #  In set, if variable does not exists and we delete it
                    #  It will not display any message
                    
                    pass
            
            else:
                os.environ[variable_name] = environ_variable_value
    
    
    def get_directory_variables(self, directory) -> None:
        """
            'dir' command in windows, prints directory information
        """
        
        if len(directory) == 1:
            directory = self.currentPath + "\\" + "."
        
        else:
            directory = directory[1]

        if not os.path.isdir(directory):
            directory = self.currentPath + "\\" + directory + "\\"
        
        if not os.path.isdir(directory):
            print("\nDirectory does not exists\n")
            
        else:
            print()
            print(*["<DIR>  " + entry.name if os.path.isdir(directory + entry.name) else "<FILE>  " + entry.name for entry in os.scandir(path=directory)], sep="\n")
            print()
    
    
    def get_file_content(self, path) -> None:
        """
            'type' command in windows, prints directory information
        """
        
        if len(path) == 1:
            print("The syntax of the command is incorrect.\n")
        
        else:
            #  Path can be a couple of files
            path = path[1]
            path = path.split()
            
            for file in path:
                
                #  We will also support ',' seperation
                for file in file.split(','):
                    
                    if file != "":
                        
                        if not os.path.isfile(file):
                            file = self.currentPath + "\\" + file
                        
                        if not os.path.isfile(file):
                            print(f"\nThe system cannot find the file specified.\nError occurred while processing: {file}.\n")
                            continue
                        
                        with open(file, 'r') as f:
                            print(f.read())


    def copy_file(self, files) -> None:
        """
            'copy' command in windows, copies one file to another location
        """
        
        files = files[1]
        files = files.split()
        
        if len(files) < 2:
            print("\nThe syntax of the command is incorrect.\n")
        
        else:
            #  Copy all files to the destination directory
            
            destination = files[1]
            file = files[0]
            
            #  Check if a directory, if so check if directory exists
            if "\\" in destination and not os.path.isdir(destination) and not os.path.isdir(self.currentPath + destination):
                print("\nThe system cannot find the directory specified.\n")
                return
                
            #  Check if the file is infact a file
            if not os.path.isfile(file) and not os.path.isfile(self.currentPath + file):
                print("\nThe system cannot find the file specified.\n")
                return
            
            shutil.copy(file, destination)
            print("\n        1 file copied.\n")
     
    
    def delete_files(self, files):
        """
            'del' command in windows, copies one file to another location
        """
        
        if len(files) == 1:
            print("\nThe syntax of the command is incorrect.\n")
        
        else:
            files = files[1:]
            
            for file in files:
                
                #  We will also support ',' seperation
                for file in file.split(','):
                    
                    if file != "":
                        
                        if "\\" not in file:
                            file = self.currentPath + "\\" + file
                        
                        if not os.path.isfile(file):
                            print(f"\nThe system cannot find {file} file.\n")
                            continue
                        
                        os.remove(file)
            


    def get_help(self, command) -> None:
        """
            Prints help on how to use different commands
        """
        
        if len(command) == 1:
            #  User typed only help
            #  Print help for all commands
            pass
    
        else:
            #  Print help for certain command
            
            command = command[1]
            command = command.split()
            
            #  Check for more then two commands (Not valid usage)
            if len(command) > 1:
                self.help_screen()
            
            else:
                #  Print help screen for the different commands
                
                command = command[0]
                command = command.lower()
                
                if command == "cd":
                    self.change_directory_help_screen()
                
                elif command == "exit":
                    self.exit_help_screen()
                
                elif command == "set":
                    self.set_help_screen()
                 
                elif command == "dir":
                    self.dir_help_screen()
                
                elif command == "type":
                    self.type_help_screen()
                
                elif command == "copy":
                    self.copy_help_screen()
                
                elif command == "del":
                    self.delete_help_screen()
                
                elif command == "help":
                    self.help_screen()
                    
                else:
                    self.help_screen_command_not_found()
                    
        
        
    def command_not_exists(self, command) -> None:
        """
            Print Error message, command does not exists
        """
        
        print(f"'{command}' is not recognized as an internal or external command or operable program")


    def help_screen(self):
        """
            Prints help window to the help command
        """
        
        print("\nProvides help information for OK commands.\n\nHELP [command]\n\n" \
              "    command - displays help information on that command.\n")
    
    
    def change_directory_help_screen(self):
        """
            Prints help window to the cd command
        """
        
        print("\nDisplays the name of or changes the current directory.\n\nCD [..]\n\n" \
              "    Type CD without parameters to display the current drive and directory.\n")
    
    
    def exit_help_screen(self):
        """
            Prints help window to the exit command
        """
        
        print("\nQuits the CMD.EXE program (command interpreter)\n")


    def set_help_screen(self):
        """
            Prints help window to the set command
        """
        
        print("\nDisplays, sets, or removes cmd.exe environment variables.\n\nSET [variable=[string]]\n" \
              "    variable  Specifies the environment-variable name.\n" \
              "    string    Specifies a series of characters to assign to the variable.\n\n" \
              "Type SET without parameters to display the current environment variables.\n")
    
    
    def dir_help_screen(self):
        """
            Prints help window to the dir command
        """
        
        print("\nDisplays a list of files and subdirectories in a directory.\n\n    DIR [path]\n")
    
    
    def type_help_screen(self):
        """
            Prints help window to the dir command
        """
        
        print("\nDisplays the contents of a text file or files.\n\n    TYPE [path]filename\n")
    
    
    def copy_help_screen(self):
        """
            Prints help window to the copy command
        """
        
        print("\nCopies one or more files to another location.\n\n    COPY source destination\n")
    
    
    def delete_help_screen(self):
        """
            Prints help window to the delete command
        """
        
        print("\nDeletes one or more files.\n\n    DEL names\n")
    

    def help_screen_command_not_found(self):
        """
            Prints command not found in help format
        """
        
        print("\nThis command is not supported by the help utility.\n")


def user_requests(currentCMD: CMD) -> None:
    """
        Handle user requests in the terminal
    """
    
    currentCMD.print_prompt()
    
    userInput = input()
    userInput = userInput.split(' ', 1)
    userInput[0] = userInput[0].lower()
    command = userInput[0]
    
    while command != "exit":
        #  Buisness logic
        
        if command == "cd":
            currentCMD.change_directory(userInput)
        
        elif command == "set":
            currentCMD.set_environment_variables(userInput)
        
        elif command == "dir":
            currentCMD.get_directory_variables(userInput)
        
        elif command == "type":
            currentCMD.get_file_content(userInput)
        
        elif command == "copy":
            currentCMD.copy_file(userInput)
         
        elif command == "del":
            currentCMD.delete_files(userInput)
        
        elif command == "help":
            currentCMD.get_help(userInput)
        
        else:
            currentCMD.command_not_exists(command)


        currentCMD.print_prompt()
        
        userInput = input()
        userInput = userInput.split(' ', 1)
        userInput[0] = userInput[0].lower()    
        command = userInput[0]


def print_giraffe():
    with open('ascii.txt', 'r') as f:
        print(f.read())


def main():
    print("Omer Kfir Shell [Version 10.0.22631.4169]\n" \
          "(c) Ophir Shavit Corporation. All rights reserved.\n\n")
    
    print_giraffe()
    cmd = CMD()
    
    user_requests(cmd)
    

if __name__ == "__main__":
    main()