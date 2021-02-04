import pynvim

#import FoxDot
from FoxDot import FoxDotCode

@pynvim.plugin
class NFoxDot(object):

    def __init__(self, vim):
        self.vim=vim
        self._editor_split=vim.current.window
        self._env=None
        self._fd_win=None
        print("nfoxdot loaded")

    def findBlock(self):
        if len(self.vim.current.line)==0:
            return []
        begin,end=-1,-1
        buffs=self.vim.current.buffer
        current=self.vim.current.window.cursor[0]-1
        for i in range(current, len(buffs)):
            if len(buffs[i].strip())==0:
                end=i
        end = (len(buffs)+1 if end==-1 else end)
        for i in range(current,0, -1):
            if len(buffs[i].strip())==0:
                begin=i
        if begin==-1:
            begin = current-1 if current>0 else current
        if begin==end:
            ret=[buffs[begin]]
        else:
            ret=[buffs[i] for i in range(begin, end)]
        return ret

    @pynvim.command("StartFoxDot")
    def start_foxdot(self):
        self.vim.command("30split logs")
        self._fd_win = self.vim.windows[1]
        if self._env is None:
            self._env=FoxDotCode()

    @pynvim.command("FDRunBlock")
    def foxdot_handler(self):
        if self._env is None:
            self.start_foxdot()
        block = self.findBlock()
        if len(block)!=0:
            for l in block:
                if l:
                    ret=self._env(l)
                    self._fd_win.buffer.append(ret)
                    self._fd_win.cursor=[self._fd_win.row,0]

    @pynvim.command("FDRunLine")
    def foxdot_line(self):
        if self._env is None:
            self.start_foxdot()
        line = self.vim.current.buffer[self.vim.current.window.cursor[0]-1]
        if len(line)!=0:
            ret = self._env(line)
            self._fd_win.buffer.append(ret)
            self._fd_win.cursor=[self._fd_win.row,0]

    @pynvim.command("FDClearClock")
    def clear_clock(self):
        if self._env is None:
            self.start_foxdot()
        self._env("Clock.clear()")
