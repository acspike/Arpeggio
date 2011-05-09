import Tkinter as tk
from ScrolledText import ScrolledText
from configobj import unrepr

class ValidatingEntry(tk.Entry):
    def __init__(self, master, value='', **kw):
        apply(tk.Entry.__init__, (self, master), kw)
        self.__value = value
        self.__variable = tk.StringVar()
        self.__variable.set(value)
        self.__variable.trace('w', self.__callback)
        self.config(textvariable=self.__variable)
    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.__value)
        elif newvalue != value:
            self.__value = newvalue
            self.__variable.set(self.newvalue)
        else:
            self.__value = value
    def set(self, value):
        self.__variable.set(value)
    def get(self):
        return self.__variable.get()
    def validate(self, value):
        # override: return value, new value, or None if invalid
        return value

class DotEntry(ValidatingEntry):
    def validate(self, value):
        if len(value):
            self.config(bg='#00ffff')
        else:
            self.config(bg='white')
        return value

class App(tk.Frame):
    def __init__(self, master=None, frets=17, strings=6):
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH,expand=True)
        self.master.title('FB Dots')
        
        self.frets = frets + 1
        self.strings = strings
        
        tframe = tk.Frame(self)
        tframe.pack(expand=False, anchor=tk.W)
        for i in range(self.frets):
            tk.Label(tframe, text=str(i)).grid(row=0, column=i)
        self.dots = []
        for i in range(self.strings):
            dots = []
            for j in range(self.frets):
                x = DotEntry(tframe, width=3)
                x.grid(row=(i + 1), column=j, sticky=(tk.E+tk.W))
                dots.append(x)
            self.dots.append(dots)
            
        bframe = tk.Frame(self)
        bframe.pack(expand=False, anchor=tk.W)
        tk.Button(bframe, text='Load', command=self.load).grid(row=0, column=0, sticky=(tk.E+tk.W))
        tk.Button(bframe, text='Save', command=self.save).grid(row=0, column=1, sticky=(tk.E+tk.W))
        tk.Button(bframe, text='Clear', command=self.clear).grid(row=0, column=2, sticky=(tk.E+tk.W))
        tk.Label(bframe, text=' Ring Character: ').grid(row=0, column=3, sticky=(tk.E+tk.W))
        self.ring_character = tk.StringVar()
        self.ring_character.set('.')
        tk.Entry(bframe, textvariable=self.ring_character, width=2).grid(row=0, column=4, sticky=(tk.E+tk.W))
        tk.Button(bframe, text='Down', command=self.move_down).grid(row=0, column=5, sticky=(tk.E+tk.W))
        tk.Button(bframe, text='Up', command=self.move_up).grid(row=0, column=6, sticky=(tk.E+tk.W))
        
        self.io = ScrolledText(self)
        self.io.pack(fill=tk.BOTH, expand=True, anchor=tk.N)
    def load(self):
        rc = self.ring_character.get()
        v = self.io.get(1.0, tk.END)
        val = unrepr(v)
        for d in val:
            s,f,t,r = d
            s = s - 1
            out = t
            if r:
                out += rc
            if not out:
                out += ' '
            self.dots[s][f].set(out)
    def save(self):
        rc = self.ring_character.get()
        val = []
        for i in range(self.strings):
            for j in range(self.frets):
                v = self.dots[i][j].get()

                if len(v) == 0:
                    continue
                    
                if rc in v:
                    r = 1
                else:
                    r = 0
                
                v = ''.join([x for x in v if x not in [rc, ' ']])
                
                val.append(((i + 1), j, v, r))
                
        self.io.delete(1.0, tk.END)
        self.io.insert(tk.END, str(val))
    def clear(self):
        for s in self.dots:
            for f in s:
                f.set('')
    def move(self, offset):
        self.save()
        self.clear()
        v = self.io.get(1.0, tk.END)
        val = unrepr(v)
        new_val = []
        for d in val:
            s,f,t,r = d
            f += offset
            if 0 <= f < self.frets:
                new_val.append((s,f,t,r))
            else:
                print f
        self.io.delete(1.0, tk.END)
        self.io.insert(tk.END, str(new_val))
        self.load()
    def move_up(self):
        self.move(1)
    def move_down(self):
        self.move(-1)

        
if __name__=='__main__':
    app = App(frets=19)
    app.mainloop()
