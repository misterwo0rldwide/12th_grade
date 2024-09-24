#  SHELL semulator python - Omer Kfir יב'3

import subprocess, os, shutil, sys, re
from colorama import Fore, Style

MY_PATH = [os.getcwd() + "\\" + "scripts\\"]
internal_commands = ["cd", "set", "dir", "type", "copy", "del", "help"]
currentPath = ""


class CMDcommand:
    
    stdout = None
    stdin = None
    stderr = None
    proc_stdout = None
    
    
    def __init__(self, stdout, stdin, stderr):
        
        self.stdout = stdout
        self.stdin = stdin
        self.stderr = stderr
    
    
    def _execute():
        pass
        


class dirCommand(CMDcommand):
    
    args = ""
    
    def __init__(self, stdout, stdin, stderr, args):
        super().__init__(stdout, stdin, stderr)
        self.args = args


    def __list_directories(self, path):
        """
            List all directories in a path
        """
        
        directories = []
        
        try:
            os.listdir(path)
        
        except PermissionError as e:
            self.stderr += e
            return -1
        
        for d in os.listdir(path):
            
            try:
            
                if os.path.isdir(os.path.join(path, d)):
                    directories.append(d)
            
            except PermissionError as e:
                self.stderr += e
        
        return directories


    def print_directory(self, directory, regex_search) -> str:
        """
            Print all directory files, directories
        """
        
        lst_directory = []
    
        for entry in os.scandir(path=directory):
            
            #  If user didnt specify any regex_search
            if regex_search == "":
            
                if os.path.isdir(directory + entry.name):
                    lst_directory.append("<DIR>  " + entry.name)
                
                else:
                    lst_directory.append("<FILE>  " + entry.name)
            
            else:
                
                if os.path.isfile(directory + "\\" + entry.name) and re.search(regex_search, entry.name):
                    lst_directory.append("<FILE>  " + entry.name)
            
    
        return lst_directory

    
    def print_all_subdirectories(self, path, regex_search):
        """
            Prints the info of all subdirectories
        """
        
        directories = self.__list_directories(path)
        lst_directory = self.print_directory(path, regex_search)

        if lst_directory:
            self.stdout += f"\n  Directory of {path}\n"
            self.stdout += "\n".join(lst_directory)
        
        if directories != -1 and len(directories) != 0:
            
            for directory in directories:
                new_path = path + "\\" + directory
                self.print_all_subdirectories(new_path, regex_search)



    def __convert_wildcard_to_regex(self, wildcard):
        """
            Convert cmd wildcard to valid regex
        """

        regex_pattern = wildcard.replace('*', '.*')
        regex_pattern = regex_pattern.replace('.', r'\.')

        return regex_pattern


    def _execute(self) -> None:
        """
            'dir' command in windows, prints directory information
        """
        
        self.args = self.args
        directory_search = ""
        regex_search = ""
        flag = ""
        wild_card = "."
        self.args = self.args.split()
        
        if len(self.args) > 3:
            self.stderr = "The syntax of the command is incorrect.\n"
            return
        
        
        if len(self.args) > 0:    
            #  We only have one flag so we can find it only by its name
            if "/S" in self.args:
                flag = self.args.index("/S")
                flag = self.args[flag]
                self.args.remove(flag)

            #  Find the regex, it will have to specify a dot
            regex_search = next((i for i, s in enumerate(self.args) if wild_card in s), -1)
            
            #  If found regex specified by user
            if regex_search != -1:
                regex_search = self.args[regex_search]
                self.args.remove(regex_search)
            
            else:
                regex_search = ""

            #  If user specified path
            if self.args:
                directory_search = self.args[0]
        
        regex_search = self.__convert_wildcard_to_regex(regex_search)
        
        #  If path is nothing
        if directory_search == "":
            directory_search = currentPath
        
        #  Check wether its a valid path
        if not os.path.isdir(directory_search):
            #  If not a valid path we try to add full path to see if user input local path
            
            directory_search = currentPath + "\\" + directory_search + "\\"
        
            #  Strictly not valid path
            if not os.path.isdir(directory_search):
                self.stderr = "\nDirectory does not exists\n"
                return
            
        #  Recurive 'dir' command
        if flag == "/S":
            self.print_all_subdirectories(directory_search, regex_search)
        
        else:
            lst_directory = self.print_directory(directory_search, regex_search)
            
            if lst_directory:
                self.stdout = "\n".join(lst_directory)
        
        
class cd(CMDcommand):

    args = ""
    
    def __init__(self, stdout, stdin, stderr, args):
        super().__init__(stdout, stdin, stderr)
        self.args = args
    
    
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

    
    def _execute(self) -> None:
        """
            Changes current working directory to be destination
        """
        
        global currentPath
        
        #  If destination is None print the current working directory
        
        if len(self.args) == 0:
            #  cd command without args
            self.stdout = currentPath
        
        else:
            
            #  Check if its a valid directory
            #  We also check for user_path since it can be a full path
            
            fullPath = os.path.join(currentPath, self.args)
            user_path = self.args
            
            if os.path.isdir(fullPath):
                    
                currentPath = self.__parse_path(fullPath)
            
            elif os.path.isdir(user_path):
            
                currentPath = self.__parse_path(user_path)
            
            elif os.path.isfile(fullPath):
                self.stderr += "The directory name is invalid."
               
            elif os.path.isfile(user_path):
                self.stderr += "The directory name is invalid."
            
            else:
                self.stderr += "The system cannot find the path specified."
    
    
class setCommand(CMDcommand):

    args = ""
    
    def __init__(self, stdout, stdin, stderr, args):
        super().__init__(stdout, stdin, stderr)
        self.args = args
    
    
    def _execute(self) -> None:
        """
            'set' command in windows, handles environment variables
        """
        
        if len(self.args) == 0:
            #  set command without args
            self.stdout = "\n".join([f"{key}={value}" for key, value in os.environ.items()])
            return
        
        
        #  The set command does not split by whitespace
        #  It splits by the equal char
        
        environ_variable = self.args.split("=")
        variable_name = environ_variable[0]
        
        if len(environ_variable) == 1:
            
            try:
                content = os.environ[variable_name]
                
                #  Get the original name of the environment variable
                
                for key in os.environ:
                    if key.lower() == variable_name.lower():
                        variable_name = key
                        break
                
                self.stdout = f"{variable_name}={content}"
            
            except KeyError:
                self.stderr = f"Environment variable {variable_name} not defined"
        
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


class typeCommand(CMDcommand):

    args = ""
    
    def __init__(self, stdout, stdin, stderr, args):
        super().__init__(stdout, stdin, stderr)
        self.args = args
    
    
    def _execute(self) -> None:
        """
            'type' command in windows, prints directory information
        """
        
        if len(self.args) == 0:
            self.stdout = "The syntax of the command is incorrect.\n"
        
        else:
            #  Path can be a couple of files
            self.args = self.args.split()
            
            for file in self.args:
                
                #  We will also support ',' seperation
                for file in file.split(','):
                    
                    if file != "":
                        
                        if not os.path.isfile(file):
                            file = currentPath + "\\" + file
                        
                        if not os.path.isfile(file):
                            self.stderr += f"\nThe system cannot find the file specified.\nError occurred while processing: {file}.\n"
                            continue
                        
                        with open(file, 'r') as f:
                            self.stdout += f.read() + "\n"


class copy(CMDcommand):

    args = ""
    
    def __init__(self, stdout, stdin, stderr, args):
        super().__init__(stdout, stdin, stderr)
        self.args = args
    
    
    def _execute(self) -> None:
        """
            'copy' command in windows, copies one file to another location
        """
        
        self.args = self.args.split()
        
        if len(self.args) < 2:
            self.stderr = "\nThe syntax of the command is incorrect.\n"
        
        else:
            #  Copy all files to the destination directory
            
            destination = self.args[1]
            file = self.args[0]
            
            #  Check if a directory, if so check if directory exists
            if "\\" in destination and not os.path.isdir(destination) and not os.path.isdir(currentPath + destination):
                self.stderr = "\nThe system cannot find the directory specified.\n"
                return
                
            #  Check if the file is infact a file
            if not os.path.isfile(file) and not os.path.isfile(currentPath + file):
                self.stderr = "\nThe system cannot find the file specified.\n"
                return
            
            shutil.copy(file, destination)
            self.stdin = "\n        1 file copied.\n"


class delCommand(CMDcommand):
    
    args = ""
    
    def __init__(self, stdout, stdin, stderr, args):
        super().__init__(stdout, stdin, stderr)
        self.args = args
    
    
    def _execute(self):
        """
            'del' command in windows, copies one file to another location
        """
        
        if len(self.args) == 0:
            self.stderr = "\nThe syntax of the command is incorrect.\n"
        
        else:
            files = self.args.split()
            
            for file in files:
                
                #  We will also support ',' seperation
                for file in file.split(','):
                    
                    if file != "":
                        
                        if "\\" not in file:
                            file = currentPath + "\\" + file
                        
                        if not os.path.isfile(file):
                            self.stderr = f"\nThe system cannot find {file} file.\n"
                        
                        else:
                            os.remove(file)
            

class helpCommand(CMDcommand):

    args = ""
    
    def __init__(self, stdout, stdin, stderr, args):
        super().__init__(stdout, stdin, stderr)
        self.args = args


    def __print_help(self):
        """
            Calls all help functions
        """

        self.stdout += "CD: \n"
        self.change_directory_help_screen()
        
        self.stdout += "EXIT: \n"
        self.exit_help_screen()
        
        self.stdout += "SET: \n"
        self.set_help_screen()
        
        self.stdout += "DIR: \n"
        self.dir_help_screen()

        self.stdout += "TYPE: \n"
        self.type_help_screen()
        
        self.stdout += "COPY: \n"
        self.copy_help_screen()
        
        self.stdout += "DEL: \n"
        self.delete_help_screen()

        self.stdout += "HELP: \n"
        self.help_screen()

    
    def __help_table(self, command):
        """
            Calls the help function for each command
        """

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


    def _execute(self) -> None:
        """
            Prints help on how to use different commands
        """
        
        if len(self.args) == 0:
            #  User typed only help
            #  Print help for all commands

            self.__print_help()

        else:
            #  Print help for certain command
            
            command = self.args.split()
            
            #  Check for more then two commands (Not valid usage)
            if len(command) > 1:
                self.help_screen()
            
            else:
                #  Print help screen for the different commands
                self.__help_table(command)    
        
        
    def command_not_exists(self, command) -> None:
        """
            Print Error message, command does not exists
        """
        
        self.stdout += f"'{command}' is not recognized as an internal or external command or operable program"


    def help_screen(self):
        """
            Prints help window to the help command
        """
        
        self.stdout += "\nProvides help information for OK commands.\n\nHELP [command]\n\n" \
              "    command - displays help information on that command.\n"
    
    
    def change_directory_help_screen(self):
        """
            Prints help window to the cd command
        """
        
        self.stdout += "\nDisplays the name of or changes the current directory.\n\nCD [..]\n\n" \
              "    Type CD without parameters to display the current drive and directory.\n"
    
    
    def exit_help_screen(self):
        """
            Prints help window to the exit command
        """
        
        self.stdout += "\nQuits the CMD.EXE program (command interpreter)\n"


    def set_help_screen(self):
        """
            Prints help window to the set command
        """
        
        self.stdout += "\nDisplays, sets, or removes cmd.exe environment variables.\n\nSET [variable=[string]]\n" \
              "    variable  Specifies the environment-variable name.\n" \
              "    string    Specifies a series of characters to assign to the variable.\n\n" \
              "Type SET without parameters to display the current environment variables.\n"
    
    
    def dir_help_screen(self):
        """
            Prints help window to the dir command
        """
        
        self.stdout += "\nDisplays a list of files and subdirectories in a directory.\n\n    DIR [path]\n" \
              "\n/S          Displays files in specified directory and all subdirectories.\n"
    
    
    def type_help_screen(self):
        """
            Prints help window to the dir command
        """
        
        self.stdout += "\nDisplays the contents of a text file or files.\n\n    TYPE [path]filename\n"
    
    
    def copy_help_screen(self):
        """
            Prints help window to the copy command
        """
        
        self.stdout += "\nCopies one or more files to another location.\n\n    COPY source destination\n"
    
    
    def delete_help_screen(self):
        """
            Prints help window to the delete command
        """
        
        self.stdout += "\nDeletes one or more files.\n\n    DEL names\n"
    

    def help_screen_command_not_found(self):
        """
            Prints command not found in help format
        """
        
        self.stdout += "\nThis command is not supported by the help utility.\n"
    

class executableCMD(CMDcommand):

    args = ""
    
    def __init__(self, stdout, stdin, stderr, args, pipe_next, prev_proc):
        super().__init__(stdout, stdin, stderr)
        self.args = args
        self.pipe_next = pipe_next
        self.prev_proc = prev_proc
        

    def _execute(self):
        """
            Executes an executble with specified path
        """
        
        try:
            
            std = None
            if self.stdin != None and self.stdin != "":
                std = self.stdin
            elif self.prev_proc != None:
                std = self.prev_proc.stdout

            proc = subprocess.Popen(args=self.args, stdin=std, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

            if self.prev_proc != None:
                self.prev_proc.stdout.close()

            if self.pipe_next == ">":
                self.stdout = ""
                for line in proc.stdout:
                    self.stdout += line

            elif self.pipe_next == "":
                for line in proc.stdout:
                    print(line, end="")

            return proc

        except FileNotFoundError as e:
            self.stderr += str(e)

def activate_command(command, args, stdin, pipe_next, prev_proc) -> CMDcommand:
    """
        Buisness logic for internal commands
    """

    obj = ""
    path = command_in_path(command + ".py")

    if command == "cd":
        obj = cd("", stdin, "", args)
    
    elif command == "set":
        obj = setCommand("", stdin, "", args)
    
    elif command == "dir":
        obj = dirCommand("", stdin, "", args)
    
    elif command == "type":
        obj = typeCommand("", stdin, "", args)
    
    elif command == "copy":
        obj = copy("", stdin, "", args)
     
    elif command == "del":
        obj = delCommand("", stdin, "", args)
    
    elif command == "help":
        obj = helpCommand("", stdin, "", args)
    
    elif path != "":
        stdin = stdin if stdin != "" else None
        obj = executableCMD(None, stdin, None, "python " + path + "\\" + command + ".py " + args, pipe_next, prev_proc)
    
    else:
        stdin = stdin if stdin != "" else None
        obj = executableCMD(None, stdin, None, command + " " + args, pipe_next, prev_proc)

    return obj


def spill_input_to_redirect(filePath, stdin):
    """
        Handles redirect of type '>'
    """

    with open(filePath, "w", encoding="utf-8") as file:
        file.write(stdin)


def command_in_path(command):
    """
        Searches the external command in the 'MY_PATH'
    """
    
    for directory in MY_PATH:
    
        if os.path.isfile(directory + command):
            return directory
    
    return ""


def print_prompt(userName, computerName, currentPath) -> None:
    """
        Prints the cmd prompt before every input from user
    """
    
    print(fr"{Fore.GREEN}{userName}@{computerName}{Fore.WHITE}:{Fore.LIGHTBLUE_EX}\{currentPath}{Style.RESET_ALL}$", end=" ")


def parse_command(command) -> tuple:
    """
        Returns a command split into command and args
    """
    
    command = command.lstrip().split(" ", 1)
    args = command[1] if len(command) == 2 else ""
    command = command[0]
    
    return command, args


def restore_default():
    """
        Returns the default variables form
    """

    prev_command = CMDcommand("", "", "")
    prev_delimiter = ""
    ret_proc = None

    return prev_command, prev_delimiter, ret_proc

def user_requests() -> None:
    """
        Handle user requests in the terminal
    """
    
    global currentPath
    
    userName=os.environ['USERNAME']
    computerName=os.environ['COMPUTERNAME']
    currentPath=os.getcwd()
    
    pattern = r'([^|><]+)([|><]?)'
    
    while True:
        print_prompt(userName, computerName, currentPath)
        commands = re.findall(pattern ,input())

        prev_command, prev_delimiter, ret_proc = restore_default()
    
        for index, command in enumerate(commands):

            command, delimiter = command
            comm, args = parse_command(command)
            
            if comm == "exit":
                return
            
            if prev_delimiter == ">":
                spill_input_to_redirect(comm, prev_command.stdout)
                prev_command, prev_delimiter, ret_proc = restore_default()

            else:
                prev_command = activate_command(comm.lower(), args, prev_command.stdout, delimiter, ret_proc)
                ret_proc = prev_command._execute()

            prev_delimiter = delimiter

        if prev_command.stdout != None:
            print(prev_command.stdout, prev_command.stderr)
        
        elif ret_proc.wait():
            output, err = ret_proc.communicate()
            print(output, err)
                


def print_giraffe():
    """
        Prints the start logo of this shell
    """

    with open('giraffe.txt', 'r') as f:
        print(f.read())


def print_dragon():
    """
        Prints the end logo of this shell
    """

    with open('dragon.txt', 'r') as f:
        print("\n\n\n" + f.read() + "\n\n\n")


def main():
    print("Omer Kfir Shell [Version 10.0.22631.4169]\n" \
          "(c) Ophir Shavit Corporation. All rights reserved.\n\n")
    
    print_giraffe()

    user_requests()
    
    print_dragon()
    

if __name__ == "__main__":
    main()