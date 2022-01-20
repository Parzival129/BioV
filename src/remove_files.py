import os
rootdir = '/Users/Russell/Dev/BioKey-Auth/src/testimgs/lfw/'
count = 0
for subdir, dirs, files in os.walk(rootdir):
    if count > 1:
        print(subdir)
        initial_count = 0
        breaknow = False
        for paths in os.listdir(subdir):
            if os.path.isfile(os.path.join(subdir, paths)):
                initial_count += 1
        print(initial_count)
        if initial_count == 1:
            os.remove(subdir)
    count += 1