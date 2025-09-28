import os

from utils.util.util import remove_blank_lines

if __name__ == '__main__':
    pass
    dir_path = r"D:\LongHe\01-PHD\999-temp\0729\add_non_vul_data"
    # remove_blank_lines
    for root, dirs, files in os.walk(dir_path):
        for d in dirs:
            if d == 'contracts':
                src_dir_path = os.path.join(root, d)
                for file_name in os.listdir(src_dir_path):
                    full_path = os.path.join(src_dir_path, file_name)
                    if os.path.isfile(full_path):
                        print(full_path)
                        remove_blank_lines(full_path)

