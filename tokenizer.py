import os
import glob

class Tokenizer:
    def read_file(self,file_path):
        encodings = ['utf-8', 'utf-16']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    temp = file.read()
                    return temp
            except UnicodeDecodeError:
                continue
            except Exception as e:
                if encoding == encodings[-1]:  # Only print error if it's the last encoding tried
                    return f"Error reading {file_path} with encoding {encoding}: {e}"
        return ""

    def process_file_contents(self,directory):
        final_str = ''
        print(". . . . . . . . . G A R B A G E   F R O M   T O K E N I Z E R . . . . . . . . .")
        print(glob.glob(os.path.join(directory, '*')))
        print(". . . . . . . . . E N D   T O K E N I Z E R . . . . . . . . .")
        for file_path in glob.glob(os.path.join(directory, '*')):
            if os.path.isfile(file_path):
                final_str += "Contents of "+file_path+":"+'\n'
                try:
                    contents = self.read_file(file_path)
                    final_str += contents+'\n'
                except Exception as e:
                    final_str += "Could not read "+file_path+":"+'\n'
                final_str += ('-' * 20) +'\n' # Separator between files
            else:
                final_str += "Entering directory "+file_path+":"+'\n'
                self.process_file_contents(file_path)  # Recursively handle subdirectories
        
        return final_str

# directory_path = input('Enter directory to read: ')
# ob = Tokenizer()
# got = ob.process_file_contents(directory_path)
# with open('output_file.txt', 'w', encoding='utf-8') as new_file:
#     new_file.write(got)
# # print(got)
# print('Size:',len(got))
# print('Chunks:',len(got)/127500)