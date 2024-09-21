import re, sys
import os


def main():
    if len(sys.argv) == 0:
        print("\ngrep.py pattern [filename]\ngrep.py pattern")

    pattern = sys.argv[1]

    if len(sys.argv) == 3:
        file = sys.argv[2]
        
        if os.path.isfile(file) or os.path.isfile(os.getcwd() + "\\" + file):
            with open(file, "r") as f:
                lines = f.read().split("\n")
                for line in lines:
                    if re.search(pattern, line):
                        print(line)
        else:
            print("\nCould not find specified file\n")
        
    else:
        try:
            while True:
                line = input()
                if re.search(pattern, line):
                    print(line)
        except EOFError:
            pass


if __name__ == "__main__":
    main()