import json
import sys

from inspect import getcallargs

class BaseScriptProcessor:


   """General handler functions. Override these in your subclass.
        Parameter names
        ----------
        raw: Raw command, as a dictionary
        cmd: name of command, either cmd0 or cmd1 in the raw command
        motion: some type of motion, value is usually in japanese.
        filename: not actually a filename, but a name referring to a resource to be used by the command
        zoom: I don't actually know what this does, this is a guess
        color: Probably a color, only value I've seen for this is 黑
        chara: A character sprite, probably
        a,b,c,d,x,y: No idea what these do.

        sometimes ints can be RANDOM, DOWN, UP or something else like that
        set_var takes two variable names, a target and a source. 
        it sets the value of the target to the value of the source with an offset (I assume)
   """
    def shakeset(self, raw, cmd, motion, a:int, b:int, c:int, d:int): self.handle_default(raw, cmd)
    def zoom(self, raw, cmd, zoom:float, position, x:int, y:int): self.handle_default(raw, cmd)
    def charaload(self, raw, cmd, chara): self.handle_default(raw, cmd)
    def set_var(self, raw, cmd, name, value, shift:int=0): self.handle_default(raw, cmd)
    def background(self, raw, cmd, filename): self.handle_default(raw, cmd)
    def bgm(self, raw, cmd, filename): self.handle_default(raw, cmd)
    def fadein(self, raw, cmd, speed:int): self.handle_default(raw, cmd)
    def motion(self, raw, cmd, chara, motion): self.handle_default(raw, cmd)
    def hide(self, raw, cmd, chara, speed:int=0): self.handle_default(raw, cmd)
    def chara(self, raw, cmd, chara, motion, position, x:int, y:int): self.handle_default(raw, cmd)
    def fadeout(self, raw, cmd, color, speed:int): self.handle_default(raw, cmd)
    def shakedisp(self, raw, cmd, motion): self.handle_default(raw, cmd)
    def shakechara(self, raw, cmd, chara, motion): self.handle_default(raw, cmd)
    def se2(self, raw, cmd, filename): self.handle_default(raw, cmd)
    def wait(self, raw, cmd, time:int): self.handle_default(raw, cmd)
    def serifclose(self, raw, cmd): self.handle_default(raw, cmd)

    def handle_default(self, raw, cmd): 
        print(f'No handler for {cmd} falling back to default.', file=sys.stderr)

    
    def showtext(self, chara, text): 
        """chara says text"""
        self.handle_default('showtext', '')
    
    def __init__(self):
        self.command_dict = {
            'charaload': self.charaload,
            '変数': self.set_var,
            'shakeset': self.shakeset,
            '背景': self.background,
            'bgm2': self.bgm,
            'fadein': self.fadein,
            'motion': self.motion,
            'hide': self.hide,
            'chara': self.chara,
            'fadeout': self.fadeout,
            'zoom': self.zoom,
            'shakedisp': self.shakedisp,
            'shakechara': self.shakechara,
            'se2': self.se2,
            'wait': self.wait,
            'serifclose': self.serifclose,
        }

    def process_list(self, cmds : [dict]):
        for command in cmds:
            self.process_command(command)

    @staticmethod
    def extract_cmd(command):
        if 'cmd0' in command:
            cmd = command['cmd0']
            cmd_num = 0
        elif 'cmd1' in command:
            cmd = command['cmd1']
            cmd_num = 1
        else:
            raise ValueError('Command not found')

        return cmd, cmd_num

    @staticmethod
    def get_arg_list(command):
        args = []
        for i in range(10):
            if f'arg{i}' in command:
                args.append(command[f'arg{i}'])

        return args

    def call_func(self, f, *args):
        callargs = getcallargs(f, *args)
        del callargs['self']
        for k in callargs:
            if k in f.__annotations__:
                try: callargs[k] = f.__annotations__[k](callargs[k])
                except ValueError: pass

        return f(**callargs)

    def process_command(self, command):
        cmd, cmd_num = self.extract_cmd(command)
        if '：' in cmd: 
            self.showtext(cmd, command['arg1'])
        elif cmd in self.command_dict:
            self.call_func(self.command_dict[cmd], command, cmd, *self.get_arg_list(command))
        elif 'arg1' in command and 'arg0' not in command:
            self.showtext(cmd, command['arg1'])
        else:
            self.default_handler(command, cmd)

    def process_file(self, filename: str):
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        if 'scr' not in data:
            raise ValueError('Expected "scr" field in json')

        self.process_list(data['scr'])

if __name__ == '__main__':
    BaseScriptProcessor().process_file(sys.argv[1])
