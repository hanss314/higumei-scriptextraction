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


outfits = set()
bgs = set()
bgm = set()
ses = set()
shaders = set()


class ExtractLines(BaseScriptProcessor):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.linecount = 0
        self.rows = []

    def charaload(self, raw, cmd, chara):
        outfits.add(chara)

    def se2(self, raw, cmd, thing, _=0):
        ses.add(thing)

    def background(self, raw, cmd, thing):
        bgs.add(thing)

    def bgm(self, raw, cmd, thing):
        bgm.add(thing)

    def shader(self, raw, cmd, shader):
        shaders.add(shader)

    def run(self):
        self.process_file(self.filename)


if __name__ == '__main__':
    for arg in argv[1:]:
        ExtractLines(arg).run()
    print('Outfits:')
    print('\n'.join(outfits))
    print('\nBackgrounds:')
    print('\n'.join(bgs))
    print('\nMusic:')
    print('\n'.join(bgm))
    print('\nSound Effects:')
    print('\n'.join(ses))

   # print('\n'.join(shaders))
