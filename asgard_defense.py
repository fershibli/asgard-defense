# -*- coding: cp1252 -*-
import pyTreeBee,pygame,sys,os
from pygame.locals import*
'''
Testes de compilação:
    teste na versão 006 com a versão recente do pyTreeBee:
        compilação : OK
    inimigoAlvo e torreGuerreiro removidos:
        erro de compilação permanece
    comandos setVisible do mouse removidos:
        erro de compilação permanece
    matriz3D retrocedida e depois expandida por append:
        erro de compilação permanece
    matriz3D retrocedida a uma array com endereçamentos de memoria para outras duas matrizes comuns:
        erro de compilação permanece
    camadas de matriz removidas:
        erro de compilação permanece
    removido o ciclo duplo de desenho na tela:
        erro de compilação permanece
    

'''
frame_atual=0
class animacaoSprite(object):
    def __init__(self,spritesheet,spritesize,stepnextsprite,rewind):
        self.sheet=spritesheet
        self.size=spritesize
        self.x=0
        self.y=0
        self.step=stepnextsprite
        self.rewind=rewind
        self.next=1
    def setLine(self, line):
        if line>=0 and line<int(self.sheet.get_height()/self.size[1]): self.y=line
    def getNextImage(self):
        global frame_atual
        if frame_atual%self.step==0:
            if int(((self.x+1)*self.size[0])/self.sheet.get_width())>=1 or (self.x+1)<=0:
                if self.rewind:
                    self.next=self.next*(-1)
                else:
                    self.x=0
            else:
                self.x+=self.next
            
        return self.sheet.subsurface((self.x*self.size[0],self.y*self.size[1]),self.size)

class blocoTabuleiro(object):
    def __init__(self,numid,cor):
        self.numID=numid
        self.cor=cor
        self.piece=None
    def addPiece(self,piece):
        self.piece=piece
class quadradoControlavel(object):
    def __init__(self,size):
        self.x=1
        self.y=1
        self.sprite=animacaoSprite(pygame.image.load("selecao.png"),(40,40),6,False)
        self.size=size
        self.buttonup=False
        self.dentro=True
    def blitOn(self,screen):
        screen.blit(self.sprite.getNextImage(),(self.x*self.size,self.y*self.size))
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
                if mapa[self.y][self.x].numID==1 or mapa[self.y][self.x].numID==2:
                    if self.dentro:
                        mapa[self.y][self.x].addPiece(animacaoSprite(pygame.image.load("viking_a_spritesheet.png"),(60,50),10,False))
            
        

class mapaLimitavel(object):
    def __init__(self):
        self.alingment=(0,0)
        self.mapa=[[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
                   [2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2],
                   [3,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,4],
                   [3,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,4],
                   [1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1],
                   [1,2,2,2,2,2,2,0,0,1,1,0,0,2,2,2,2,2,2,1],
                   [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
                   [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
                   [1,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]#13
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[y])):
                if self.mapa[y][x]==8: cor=(34,57,65)
                if self.mapa[y][x]==0: cor=pygame.image.load("mapacaminho4.png")#(0,255,0)
                if self.mapa[y][x]==3: cor=pygame.image.load("mapaentrada.png")#(0,0,255)
                if self.mapa[y][x]==4: cor=pygame.transform.flip(pygame.image.load("mapaentrada.png"),True,False)#cor=(255,0,0)
                if self.mapa[y][x]==1: cor=pygame.image.load("mapagrama4.png")#(0,200,100)
                if self.mapa[y][x]==2: cor=pygame.image.load("mapagramawterra3.png")#(0,200,100)
                try:
                    self.mapa[y][x]=blocoTabuleiro(self.mapa[y][x],cor)
                except:
                    pass
        self.size=40
        self.selecao=quadradoControlavel(self.size)
    def blitOn(self,screen):
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[y])):
                #sprite=False
                try:
                    screen.blit(self.mapa[y][x].cor,(self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size)))
                except:
                    screen.fill(self.mapa[y][x].cor,pygame.Rect(self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size),self.size,self.size))
                try:
                    if self.mapa[y][x].piece!=None:
                        alinhaspriteX=(self.size/2)-(self.mapa[y][x].piece.size[0]/2)
                        screen.blit(self.mapa[y][x].piece.getNextImage(), (self.alingment[0]+(x*self.size)+alinhaspriteX,self.alingment[1]+(y*self.size)))
                        #screen.blit(pygame.transform.scale(self.mapa[y][x].getNextImage(),(40,33)), (self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size)))
                except:
                    pass

        self.selecao.blitOn(screen)
        
    def keyControls(self,event):
        self.selecao.keyControls(event,self.mapa, self.alingment)
        

class controlesExtras(object):
    def __init__(self,tela):
        self.tela=tela
    def blitOn(self,screen):
        global frame_atual
        frame_atual+=1
    def keyControls(self,event):
        if event.type==KEYUP:
            if event.key==K_ESCAPE:
                self.tela.storedlink=None
                self.tela.running=False
        return None


fase_1 = pyTreeBee.dynamicScreen((800,600),60,(78,133,154),mapaLimitavel())
fase_1.addItem(controlesExtras(fase_1))


botao_1=pyTreeBee.linkedButton(fase_1,pygame.font.SysFont(None,20),["Fase 1","Jardim de Valhalha"],pygame.Rect(100,100,280,192),-20,200,"logo_fase1.png")
botao_1.setEach_BarSize((-20,-5),(-20,-10),(-20,-15))
selecao_fase = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_1)
tela_inicial = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),pyTreeBee.linkedButton(selecao_fase,pygame.font.SysFont(None,50),["   ASGARD DEFENSE","Clique aqui para jogar"],pygame.Rect(0,0,800,600),250,250))
selecao_fase.addItem(pyTreeBee.linkedButton(tela_inicial,pygame.font.SysFont(None,20),["Voltar"],pygame.Rect(740,570,50,20),0,0))
fase_1.addItem(pyTreeBee.linkedButton(selecao_fase,pygame.font.SysFont(None,20),["Voltar"],pygame.Rect(740,570,50,20),0,0))
pyTreeBee.treeBeeStart(tela_inicial)

