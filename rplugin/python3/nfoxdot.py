import pynvim

#import FoxDot
from FoxDot import FoxDotCode

@pynvim.plugin
class NeoFoxDot(object):

    def __init__(self, vim):
        self.vim=vim
        self._editor_split=vim.current.window
        self._env=None
        self._fd_win=None
        #print("nfoxdot loaded")

    def findBlock(self):
        if len(self.vim.current.line)==0:
            return (-1,-1)
        res=[]
        begin,end=-1,-1
        buffs=self.vim.current.buffer
        current=self.vim.current.window.cursor[0]-1
        for i in range(current, 0, -1):
            if len(buffs[i].strip())==0:
                begin=i
                break
        for i in range(current, len(buffs)):
            if len(buffs[i].strip())==0:
                end=i
                break
        end=end if end!=-1 else len(buffs)
        begin=begin if begin!=-1 else 0
        return (begin, end)

    @pynvim.command("StartFoxDot")
    def start_foxdot(self):
        self.vim.command("set splitbelow")
        self.vim.command("sp logs")
        self._fd_win = self.vim.windows[1]
        self.vim.current.window= self.vim.windows[0]
        if self._env is None:
            self._env=FoxDotCode()


    @pynvim.command("FDRunBlock")
    def foxdot_handler(self):
        if self._env is None:
            self.start_foxdot()
        begin, end = self.findBlock()
        if begin!=-1 and end!=-1:
            buff=self.vim.current.buffer
            for i in range(begin, end):
                if i>=0 and i<len(buff):
                    self.play_line(buff[i])

    @pynvim.command("FDRunLine")
    def foxdot_line(self):
        if self._env is None:
            self.start_foxdot()
        line=self.vim.current.line
        self.play_line(line)

    def play_line(self, line):
        if len(line)!=0:
            ret = self._env(line)
            self._fd_win.buffer.append(ret)
            pos=self._fd_win.cursor[0]
            self._fd_win.cursor=[pos+1,1]

    @pynvim.command("FDClearClock")
    def clear_clock(self):
        if self._env is None:
            self.start_foxdot()
        self._env("Clock.clear()")
