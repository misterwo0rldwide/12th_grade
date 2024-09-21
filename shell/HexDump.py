import sys, os

def main():
    if len(sys.argv) == 0:
        print("\nHexDump.py [filename]\n")
        
    elif os.path.isfile(sys.argv[1]) or os.path.isfile(os.getcwd() + "\\" + sys.argv[1]):

        with open(sys.argv[1], "rb") as file:
        
            offset = 0
            index = 0
            current_stream = ""
            cont = True
            content = file.read()
            
            while cont:
            
                print(hex(offset)[2:].zfill(8) + ": ", end="")
                current_stream = ""
                
                for index in range(0, 16, 2):
                    
                    if offset + index + 2 <= len(content):
                        current_stream = current_stream + chr(content[offset + index]) if 32 <= content[offset + index] < 128 else current_stream + "."
                        current_stream = current_stream + chr(content[offset + index + 1]) if 32 <= content[offset + index + 1] < 128 else current_stream + "."
                        print(hex(content[offset + index])[2:].zfill(2) + hex(content[offset + index + 1])[2:].zfill(2), end=" ")
                    
                    else:
                        cont = False
                        break

                if cont == False and offset + index + 1 < len(content):
                    current_stream = current_stream + chr(content[offset + index + 1]) if 32 <= content[offset + index + 1] < 128 else current_stream + "."
                    print(hex(content[offset + index + 1])[2:].zfill(2), end=" ")

                offset += 16
                print(current_stream)


    else:
        print("File does not exists")
    
    
if __name__ == "__main__":
    main()