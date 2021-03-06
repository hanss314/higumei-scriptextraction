"""
Given a higumei script, extracts all the lines containing text which is shown to the player.
Useful for translation.
Also prefixes each line with the command index, for integrating the translated text back into the commands.
Outputs in the following format

<command index>:
<Speaker>
<Line 1>
<Line 2> ...

Each command is separated by two newlines.
"""
import csv

from sys import argv, stdout
from base_processor import BaseScriptProcessor

tl_dict = {    
"千雨":   "Chisame",
"一穂":   "Kazuho",
"梨花":   "Rika",
"羽入":   "Hanyuu",
"魅音":   "Mion",
"美雪":   "Miyuki",
"沙都子": "Satoko",
"悟史":   "Satoshi",
"夏美":   "Natsumi",
"レナ":   "Rena",
"菜央":   "Nao",

'私服':   'Casual',
# To be completed
}

def tl_name(name):
    if name == '：': return ''
    name = name.split('：')
    if len(name) == 1:
        name.append(None)
    name, outfit = name

    name = tl_dict.get(name, name)
    outfit = tl_dict.get(outfit, outfit)
    #outfit = tl_dict[outfit]
    if outfit is None:
        return f'{name}'
    else:
        return f'{name} ({outfit})'



class ExtractLines(BaseScriptProcessor):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.linecount = 0
        self.rows = []

    def showtext(self, chara, text):
        self.rows.append((self.linecount, tl_name(chara), text))
        self.linecount += 1

    def handle_default(self, cmd, raw):
        self.linecount += 1

    def run(self):
        self.process_file(self.filename)

    def print(self):
        writer = csv.writer(stdout)
        writer.writerow(('index', 'chara', 'jp', 'en'))
        for row in self.rows: writer.writerow(row)


if __name__ == '__main__':
    print(argv[1])
    e = ExtractLines(argv[1])
    e.run()
    e.print()
    
