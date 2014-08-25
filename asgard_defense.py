# -*- coding: cp1252 -*-
import pyTreeBee,pygame,sys,os
from pygame.locals import*

class quadradoControlavel(object):
    def __init__(self,size):
        self.x=1
        self.y=1
        self.size=size
        self.right=False
        self.left=False
        self.up=False
        self.down=False
    def blitOn(self,screen):
        screen.fill((0,0,0),pygame.Rect(self.x*self.size,self.y*self.size,self.size,self.size))
    def keyControls(self,event,mapa):
        if self.right:
            if mapa[self.y][self.x+1]==0: self.x+=1
        if self.left:
            if mapa[self.y][self.x-1]==0: self.x-=1
        if self.down:
            if mapa[self.y+1][self.x]==0: self.y+=1
        if self.up:
            if mapa[self.y-1][self.x]==0: self.y-=1
        
        if event.type==KEYDOWN:
            if event.key==K_RIGHT:
                self.right=True
            if event.key==K_LEFT:
                self.left=True
            if event.key==K_UP:
                self.up=True
            if event.key==K_DOWN:
                self.down=True
        if event.type==KEYUP:
            if event.key==K_RIGHT:
                self.right=False
            if event.key==K_LEFT:
                self.left=False
            if event.key==K_UP:
                self.up=False
            if event.key==K_DOWN:
                self.down=False

class mapaLimitavel(object):
    def __init__(self):
        self.mapa=[[1,2,1,1,1,1,1,1,1,1,1],
                   [1,0,1,0,0,0,1,0,0,0,1],
                   [1,0,1,0,1,0,1,0,1,0,1],
                   [1,0,1,0,1,0,1,0,1,0,1],
                   [1,0,0,0,1,0,0,0,1,0,1],
                   [1,1,1,1,1,1,1,1,1,3,1]]
        self.size=50
        self.selecao=quadradoControlavel(self.size)
    def blitOn(self,screen):
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[y])):
                cor=(255,255,255)
                if self.mapa[y][x]==0: cor=(0,255,0)
                if self.mapa[y][x]==2: cor=(0,0,255)
                if self.mapa[y][x]==3: cor=(255,0,0)
                if self.mapa[y][x]==1: cor=(0,200,100)
                screen.fill(cor,pygame.Rect(x*self.size,y*self.size,self.size,self.size))
        self.selecao.blitOn(screen)
    def keyControls(self,event):
        self.selecao.keyControls(event,self.mapa)
        
                

tela_inicial = pyTreeBee.dynamicScreen((600,600),60,(255,255,255),mapaLimitavel())
#tela_inicial.setFULLSCREEN()
pyTreeBee.treeBeeStart(tela_inicial)

