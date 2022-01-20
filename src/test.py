"""
A testing function for testing
facial recognition performance
"""

from icrawler.builtin import BingImageCrawler
from rich.console import Console
from facialRecog2 import comparemodel2img2, create
import shutil
import os

console = Console()
rootdir = 'testimgs/lfw'

tolerance = input("what tolerance? > ")
amount = input("how many faces? > ")
amount = int(amount) + 1
count = 0


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

YES = 0
NO = 0
ERROR = 0
"""
Looping throuh lfw database
"""
print("==================")
print("Checking Positives")
print("==================")
people_tested_correct = []
people_tested_incorrect = []
for subdir in os.walk(rootdir):
    if count <= int(amount):
        if count > 1:
            name = subdir[0][13:]
            console.print("[bold cyan]" + name)
            initial_count = 0
            dir = 'testimgs/lfw/' + name + '/'
            breaknow = False
            for paths in os.listdir(dir):
                if os.path.isfile(os.path.join(dir, paths)):
                    initial_count += 1
            if int(initial_count) < 3:
                console.print("[bold red] Insufficient training data")
                ERROR += 1
                breaknow = True
            print(subdir[0])
            classes=[name.replace('-',' ')]
            number=1
            for c in classes:
                if breaknow == True:
                    break
                # bing_crawler=BingImageCrawler(storage={'root_dir':f'testimgs/scraped/{c.replace(" ","-")}/'})
                # # downloads an image to testimgs/scraped/[name]/
                # bing_crawler.crawl(keyword=c,filters=None,max_num=number,offset=0)
                path = 'testimgs/lfw/' + name + '/'
                initial_count = 0
                dir = path
                cppath = 'testimgs/person/person'
                shutil.copyfile(dir + name + '_0003.jpg', 'scraped/person.jpg')
                copytree(path, cppath)
                print("----------------------")
                print(path)
                print(name)
                print("----------------------")
                # TODO: the people images miust be in a folder in the persons name folder!!
                if create(name, 'testimgs/person') == False:
                    ERROR += 1
                else:
                    try:
                        res = comparemodel2img2('scraped/person.jpg', "testimgs/person/person/" + name + '.clf', distance=float(tolerance))
                        console.print("[bold cyan]" + str(res))
                        if res == True:
                            YES += 1
                            people_tested_correct.append(name)
                        if res == False:
                            NO += 1
                            people_tested_incorrect.append(name)
                    except Exception as e:

                        console.print('[bold red]' + str(e))
                        ERROR += 1
                dir = cppath
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))
        count += 1
    else:
        break


# show stats
print("Positive Stats")
console.print ("[bold green]CORRECT: " + str(YES))
console.print ("[bold red]INCORRECT: " + str(NO))
console.print ("[bold purple]ERROR: " + str(ERROR))
console.print ("[bold cyan]TOTAL: " + str(amount - 1))
print("Correct %: " + str(((YES/((amount - 1) - ERROR))) * 100) + "%")
console.print('[bold green]Correct People:')
for i in people_tested_correct:
    print(i)
console.print('[bold red]Incorrect People:')
for i in people_tested_incorrect:
    print(i)