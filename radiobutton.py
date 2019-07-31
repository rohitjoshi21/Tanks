import pygame as pg


class Radio:
    def __init__(self,x,y,group = None,**kwargs):
        self.group = group
        self.center = (x,y)
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "checkbox":False,
                    "outer_radius":10,
                    "inner_radius":7,
                    "main_color" : pg.Color("green"),
                    "selected_color":pg.Color("black"),
                    "outline_color" : pg.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pg.Color("blue")}
        
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))

        self.__dict__.update(defaults)
        
    def get_event(self,event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x,y = event.pos
            h,k = self.center
            r = self.outer_radius
            if (x-h)**2 + (y-k)**2 <= r**2:
                self.execute()
                
    def execute(self):
        if self.active and self.checkbox:
            self.active = False

        else:
            if self.group:
                for butt in self.group:
                    butt.active = False
            self.active = True
        
        if self.command:
            self.command(self.main_color,self.active)

    def draw(self,surface):
        #print(self.outline_color,self.main_color,self.center,int(self.outer_radius+self.outline_width))
        pg.draw.circle(surface,self.outline_color,self.center,int(self.outer_radius+self.outline_width))
        pg.draw.circle(surface,self.main_color,self.center,self.outer_radius)
        if self.active:
            pg.draw.circle(surface,self.selected_color,self.center,self.inner_radius)
        
            
