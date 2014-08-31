# -*- coding: cp1252 -*-
import pyTreeBee,pygame,sys,os
from pygame.locals import*

frame_atual=0
class animacaoSprite(object):
    def __init__(self,spritesheet,spritesize,stepnextsprite,rewind):
        self.sheet=spritesheet
        self.size=spritesize
        self.pos=(0,0)
        self.step=stepnextsprite
        self.rewind=rewind
        self.next=1
    def setLine(self, line):
        if line>0 and line<int(self.sheet.get_size()[1]/self.size[1]): self.pos[1]=line
    def getNextImage(self):
        global frame_atual
        if frame_atual%self.step==0:
            if self.pos[0]<=int(self.sheet.get_size()[0]/self.size[0]):
                self.pos[0]+=int(self.next)
            else:
                if self.rewind:
                    self.next*=(-1)
                else:
                    self.pos[0]=0
        return self.sheet.subsurface(self.pos,self.size)

class quadradoControlavel(object):
    def __init__(self,size):
        self.x=1
        self.y=1
        self.size=size
        self.buttonup=False
        self.dentro=True
    def blitOn(self,screen):
        screen.fill((0,0,0),pygame.Rect(self.x*self.size,self.y*self.size,self.size,self.size))
    def keyControls(self,event,mapa,alingment):
        if event.type==MOUSEMOTION:
            x,y=event.pos
            self.x=int(x/self.size)
            self.y=int(y/self.size)
            alnX=int(alingment[0]/self.size)
            alnY=int(alingment[1]/self.size)
            self.dentro=True
            if self.y>alnY+len(mapa)-1 or self.x>alnX+len(mapa[self.y])-1 or self.y<alnY or self.x<alnX:
                self.dentro=False
            
            if self.y>alnY+len(mapa)-1: # ta dando erro nesse IF
                self.y=alnY+len(mapa)-1 # nao esqueca da copia desse IF no IF acima quando corrigir
            if self.y<alnY:
                self.y=alnY
            if self.x>alnX+len(mapa[self.y])-1:
                self.x=alnX+len(mapa[self.y])-1
            if self.x<alnX:
                self.x=alnX
        if event.type==MOUSEBUTTONDOWN:
            if event.button==1:
                if mapa[self.y][self.x]==3 or mapa[self.y][self.x]==2:
                    mapa[self.y][self.x]=4
                    #mapa[self.y][self.x]=animacaoSprite(pygame.image.load("viking_a_spritesheet.png"),(60,50),6,False)

class mapaLimitavel(object):
    def __init__(self):
        self.alingment=(0,0)
        self.mapa=[[3,2,3,2,3,2,3,2,3,2,3,2,3,2,3,2,3,2,3,2],
                   [0,1,0,1,0,1,0,1,0,3,2,1,0,1,0,1,0,1,0,1],
                   [1,0,1,0,1,0,1,0,1,2,3,0,1,0,1,0,1,0,1,0],
                   [2,3,2,3,2,3,2,1,0,3,2,1,0,3,2,3,2,3,2,3],
                   [3,2,3,2,3,2,3,0,1,2,3,0,1,2,3,2,3,2,3,2],
                   [2,1,0,1,0,1,0,1,0,3,2,1,0,1,0,1,0,1,0,3],
                   [3,0,1,0,1,0,1,0,1,2,3,0,1,0,1,0,1,0,1,2],
                   [2,1,0,3,2,3,2,3,2,3,2,3,2,3,2,3,2,1,0,3],
                   [3,0,1,2,3,2,3,2,3,2,3,2,3,2,3,2,3,0,1,2],
                   [2,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,3],
                   [3,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,2],
                   [2,3,2,3,2,3,2,3,2,3,2,3,2,3,2,3,2,3,2,3]]
        self.size=40
        self.selecao=quadradoControlavel(self.size)
    def blitOn(self,screen):
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[y])):
                cor=(255,255,255)
                sprite=False
                if self.mapa[y][x]==0: cor=(0,255,0)
                if self.mapa[y][x]==2: cor=(0,0,255)
                if self.mapa[y][x]==3: cor=(255,0,0)
                if self.mapa[y][x]==1: cor=(0,200,100)
                if self.mapa[y][x]==4: cor=(200,200,0)
                if self.mapa[y][x].__class__.__name__=="animacaoSprite": sprite=True
                if sprite: screen.blit(self.mapa[y][x].getNextImage(),(self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size)))
                else:screen.fill(cor,pygame.Rect(self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size),self.size,self.size))
        self.selecao.blitOn(screen)
    def keyControls(self,event):
        self.selecao.keyControls(event,self.mapa, self.alingment)
        

class controlesExtras(object):
    def __init__(self,tela):
        self.tela=tela
    def blitOn(self,screen): pass
    def keyControls(self,event):
        global frame_atual
        frame_atual+=1
        if event.type==KEYUP:
            if event.key==K_ESCAPE:
                self.tela.storedlink=None
                self.tela.running=False

tela_inicial = pyTreeBee.dynamicScreen((0,0),30,(255,255,255),mapaLimitavel())
tela_inicial.addItem(controlesExtras(tela_inicial))
tela_inicial.setFULLSCREEN()
pyTreeBee.treeBeeStart(tela_inicial)

