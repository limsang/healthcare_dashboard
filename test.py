import os.path
folder = os.getcwd()

print('Current folder : %s' % folder)

for path, dirs, files in os.walk(folder):
    print('\nFolder: ', path)
    if files:
        for filename in files:
            print(filename)

