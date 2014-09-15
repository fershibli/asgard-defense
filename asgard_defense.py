# -*- coding: cp1252 -*-
import pyTreeBee,pygame,sys,os,math
from pygame.locals import*
temporarydisplay=pygame.display.set_mode((800,600))
frame_atual=0
arial12=pygame.font.SysFont("Arial",12)
class blocoTabuleiro(object):
    def __init__(self,numid,cor):
        self.numID=numid
        self.cor=cor
        self.piece=None
    def addPiece(self,piece):
        self.piece=piece

class animacaoSprite(object):
    def __init__(self,spritesheet,spritesize,stepnextsprite,rewind,pos=(0,0)):
        self.sheet=spritesheet
        self.size=spritesize
        self.x=0
        self.y=0
        self.step=stepnextsprite
        self.rewind=rewind
        self.next=1
        self.pos=pos
    def setLine(self, line):
        if line>=0 and line<int(self.sheet.get_height()/self.size[1]): self.y=line
    def getNextImage(self):
        global frame_atual
        if frame_atual%self.step==0:
            if int(((self.x+1)*self.size[0])/self.sheet.get_width())>=1 or (self.x+1)<=(-self.next+1)/2:
                if self.rewind:
                    self.next=(-1)
                    self.x=int(self.sheet.get_width()/self.size[0])-2
                    self.rewind=False
                else:
                    self.x=(-self.next+1)/2
                    if self.next==(-1):
                        self.next=1
                        self.rewind=True
            else:
                self.x+=self.next
            
        return self.sheet.subsurface((self.x*self.size[0],self.y*self.size[1]),self.size)
    def blitOn(self,screen):
        screen.blit(self.getNextImage(),self.pos)
    def keyControls(self,event):pass


class inimigoAlvo(object):#inimigoAlvo(pygame.image.load("inimigo01sheet2.png"),(20,20),10,False,1,1,1,
    def __init__(self,sprite,size,nextsprite,rewind,atk,vel,hp, x,y , sentidox,sentidoy):
        self.sprite=animacaoSprite(sprite,size,nextsprite,rewind)
        self.pos=[x,y]
        self.pixelpos=[0,0]
        self.atk=atk
        self.vel=vel
        self.hp=hp
        self.hpmax=0;self.hpmax+=hp
        self.sentido=[sentidox,sentidoy]#(1,0)horizontal,vertical
        self.parede=[0,0]
    def movimentoPadrao(self,mapa,size):'''
        if mapa[0][self.pos[1]+self.parede[1]][self.pos[0]+self.parede[0]]==0:
            self.sentido=self.parede
        if mapa[0][self.pos[1]+1][self.pos[0]].numID!=0: self.parede = [0,1];mapa[0][self.pos[1]+1][self.pos[0]].cor=(0,255,0)
        if mapa[0][self.pos[1]-1][self.pos[0]].numID!=0: self.parede = [0,-1];mapa[0][self.pos[1]-1][self.pos[0]].cor=(0,255,0)
        if mapa[0][self.pos[1]][self.pos[0]+1].numID!=0: self.parede = [1,0];mapa[0][self.pos[1]][self.pos[0]+1].cor=(0,255,0)
        if mapa[0][self.pos[1]][self.pos[0]-1].numID!=0: self.parede = [-1,0];mapa[0][self.pos[1]][self.pos[0]-1].cor=(0,255,0)
        
        #mapa[0][self.pos[1]+self.parede[1]][self.pos[0]+self.parede[0]].cor=(255,0,0)
        
        next_tile=mapa[0][self.pos[1]+self.sentido[1]][self.pos[0]+self.sentido[0]]
        if next_tile.numID==0 and next_tile.piece==None:
            if self.pixelpos[0]>=size or self.pixelpos[1]>=size:
                #muda de tile
                mapa[0][self.pos[1]+self.sentido[1]][self.pos[0]+self.sentido[0]].piece = mapa[0][self.pos[1]][self.pos[0]].piece
                mapa[0][self.pos[1]][self.pos[0]].piece=None
                self.pos[0]+=self.sentido[0]
                self.pos[1]+=self.sentido[1]
                if self.pixelpos[0]>=size: self.pixelpos[0]-=size
                if self.pixelpos[1]>=size: self.pixelpos[1]-=size
            else:
                if self.sentido[0]==1: self.pixelpos[0]+=self.vel
                if self.sentido[0]==-1: self.pixelpos[0]-=self.vel
                if self.sentido[1]==1: self.pixelpos[1]+=self.vel
                if self.sentido[1]==-1: self.pixelpos[1]-=self.vel
        else:
            if mapa[0][self.pos[1]+1][self.pos[0]].numID==0 and self.sentido!=[0,-1]: self.sentido = [0,1]
            if mapa[0][self.pos[1]-1][self.pos[0]].numID==0 and self.sentido!=[0,1]: self.sentido = [0,-1]
            if mapa[0][self.pos[1]][self.pos[0]+1].numID==0 and self.sentido!=[-1,0]: self.sentido = [1,0]
            if mapa[0][self.pos[1]][self.pos[0]-1].numID==0 and self.sentido!=[1,0]: self.sentido = [-1,0]'''
        
    

class torreGuerreiro(object):
    def __init__(self,sprite,size,nextsprite,rewind,atk,vel,rng, x,y):
        self.sprite=animacaoSprite(sprite,size,nextsprite,rewind)
        self.atk=atk
        self.vel=vel
        self.rng=rng
        self.aim=None
        self.x=x
        self.y=y
    def getNextImage(self): self.sprite.getNextImage()
    def fightControls(self,mapa):
        global frame_atual
        if self.aim==None:
            for i in range(-self.rng,1+self.rng):
                for e in range(-self.rng,1+self.rng):
                    '''
                    try:
                        mapa[0][self.y+e][self.x+i].cor=(255,0,0)
                    except:
                        pass
                    '''
                    try:
                        if mapa[0][self.y+e][self.x+i].piece!=None:
                            if self.sprite.y!=1: self.sprite.setLine(1)
                            self.aim=mapa[0][self.y+e][self.x+i]
                    except:
                        pass
        else:            
            if frame_atual%self.vel==0:
                try:
                    self.aim.piece.hp-=self.atk
                    if self.aim.piece.hp<=0:
                        self.aim.addPiece(None)
                        self.aim=None
                        if self.sprite.y!=0: self.sprite.setLine(0)
                except:
                    self.aim=None
                    self.sprite.setLine(0)
        
class quadradoControlavel(object):
    def __init__(self,size):
        self.x=1
        self.y=1
        self.sprite=animacaoSprite(pygame.image.load("selecao2.png"),(40,40),9,True)
        self.size=size
        self.buttonup=False
        self.dentro=True
        self.torre=pygame.image.load("viking_spritesheet.png")
        self.inimigo=pygame.image.load("inimigo01sheet2.png")
        self.botaodireito=False
        self.botaoesquerdo=False
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
            if self.y>alnY+len(mapa[0])-1 or self.x>alnX+len(mapa[0][self.y])-1 or self.y<alnY or self.x<alnX:
                self.dentro=False

            if self.y>alnY+len(mapa[0])-1: # ta dando erro nesse IF
                self.y=alnY+len(mapa[0])-1 # nao esqueca da copia desse IF no IF acima quando corrigir
            if self.y<alnY:
                self.y=alnY
            if self.x>alnX+len(mapa[0][self.y])-1:
                self.x=alnX+len(mapa[0][self.y])-1
            if self.x<alnX:
                self.x=alnX
        if self.botaoesquerdo:
            if self.dentro:
                if mapa[0][self.y][self.x].numID==1 or mapa[0][self.y][self.x].numID==2:                
                    mapa[1][self.y][self.x].addPiece(torreGuerreiro(self.torre,(60,50),6,False,2,2,2,self.x,self.y))
                if mapa[0][self.y][self.x].numID==0:
                    mapa[0][self.y][self.x].addPiece(inimigoAlvo(self.inimigo,(20,20),10,False,1,1,1000,self.x,self.y,1,0))
        if self.botaodireito:
            if mapa[0][self.y][self.x].numID==0:
                if self.dentro:
                    mapa[0][self.y][self.x].addPiece(inimigoAlvo(self.inimigo,(20,20),10,False,1,1,100000,self.x,self.y,1,0))
        if event.type==MOUSEBUTTONDOWN:
            if event.button==1:
                self.botaoesquerdo=True
            if event.button==3:
                self.botaodireito=True
        if event.type==MOUSEBUTTONUP:
            if event.button==1:
                self.botaoesquerdo=False
            if event.button==3:
                self.botaodireito=False
        if self.dentro:
            try:
                pygame.mouse.set_visible(False)
            except:
                print "can't set invisible"
        else:
            try:
                pygame.mouse.set_visible(True)
            except:
                print "can't set visible"
            
        

class mapaLimitavel(object):
    def __init__(self):
        self.alingment=(0,0)
        self.mapa=[[[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
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
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]],#13
                   [[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]],
                   [[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]]]
        imagens=[pygame.image.load("mapacaminho4.png").convert(),pygame.image.load("mapaentrada.png").convert(),pygame.image.load("mapagrama4.png").convert(),pygame.image.load("mapagramawterra3.png").convert()]
        imagens.append(pygame.transform.flip(imagens[1],True,False))
        for z in range(len(self.mapa)):
            for y in range(len(self.mapa[z])):
                for x in range(len(self.mapa[z][y])):
                    if self.mapa[z][y][x]==8: cor=(34,57,65)
                    if self.mapa[z][y][x]==0: cor=imagens[0]
                    if self.mapa[z][y][x]==3: cor=imagens[1]
                    if self.mapa[z][y][x]==4: cor=imagens[4]
                    if self.mapa[z][y][x]==1: cor=imagens[2]
                    if self.mapa[z][y][x]==2: cor=imagens[3]
                    try:
                        self.mapa[z][y][x]=blocoTabuleiro(self.mapa[z][y][x],cor)
                        if y==3 and x==3:self.mapa[0][y][x].piece=inimigoAlvo(pygame.image.load("inimigo01sheet2.png"),(20,20),20,False,1,1,1000,x,y,1,0)
                        if y==2 and x==2:self.mapa[0][y][x].piece=inimigoAlvo(pygame.image.load("inimigo01sheet2.png"),(20,20),20,False,1,1,2000,x,y,1,0)
                    except:
                        pass
        self.size=40
        self.selecao=quadradoControlavel(self.size)
    def blitOn(self,screen):
                                
        for y in range(len(self.mapa[0])):
            for x in range(len(self.mapa[0][y])):
                if self.mapa[0][y][x].piece!=None:
                    self.mapa[0][y][x].piece.movimentoPadrao(self.mapa,self.size)
                #sprite=False
                try:
                    screen.blit(self.mapa[0][y][x].cor,(self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size)))
                except:
                    screen.fill(self.mapa[0][y][x].cor,pygame.Rect(self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size),self.size,self.size))
        for y in range(len(self.mapa[1])):
            for x in range(len(self.mapa[1][y])):
                if self.mapa[1][y][x].piece!=None:
                    self.mapa[1][y][x].piece.fightControls(self.mapa)
                try:
                    if self.mapa[0][y][x].piece!=None:
                        alinhaspriteX=(self.size/2)-(self.mapa[0][y][x].piece.sprite.size[0]/2)
                        posx=self.alingment[0]+(x*self.size)+self.mapa[0][y][x].piece.pixelpos[0]
                        posy=self.alingment[1]+((1+y)*self.size)-10+self.mapa[0][y][x].piece.pixelpos[1]
                        screen.blit(self.mapa[0][y][x].piece.sprite.getNextImage(), (posx+alinhaspriteX,self.alingment[1]+(y*self.size)+self.mapa[0][y][x].piece.pixelpos[1]))

                        screen.fill((0,0,0),pygame.Rect(posx+2,posy,self.size-4,8))
                        screen.fill((255,0,0),pygame.Rect(posx+4,posy+2,self.size-8,4))
                        
                        life=self.size-((self.mapa[0][y][x].piece.hpmax-self.mapa[0][y][x].piece.hp)*self.size/self.mapa[0][y][x].piece.hpmax)

                        screen.fill((255,255,255),pygame.Rect(posx+4,posy+2,life-8,4))
                except:
                    print "erro desenhar inimigo"
                try:
                    if self.mapa[1][y][x].piece!=None:
                        alinhaspriteX=(self.size/2)-(self.mapa[1][y][x].piece.sprite.size[0]/2)
                        screen.blit(self.mapa[1][y][x].piece.sprite.getNextImage(), (self.alingment[0]+(x*self.size)+alinhaspriteX,self.alingment[1]+(y*self.size)))
                        #screen.blit(pygame.transform.scale(self.mapa[y][x].getNextImage(),(40,33)), (self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size)))
                except:
                    print "erro desenhar torre"

        self.selecao.blitOn(screen)
        
    def keyControls(self,event):
        self.selecao.keyControls(event,self.mapa, self.alingment)
        

class controlesExtras(object):
    def __init__(self,tela):
        self.tela=tela
        self.rng=2
        self.x=9
        self.y=9
    def blitOn(self,screen):
        global frame_atual
        frame_atual+=1
    def keyControls(self,event):
        if event.type==KEYUP:
            if event.key==K_ESCAPE:
                self.tela.storedlink=None
                self.tela.running=False
            if event.key==K_SPACE:
                for i in range(-self.rng,1+self.rng):
                    for e in range(-self.rng,1+self.rng):
                        self.tela.itens[0].mapa[0][self.x+i][self.y+e].cor=(255,0,0)
                
                self.tela.itens[0].mapa[0][self.x][self.y].cor=(0,0,255)
        return None


fase_1 = pyTreeBee.dynamicScreen((800,600),60,(78,133,154),mapaLimitavel())
fase_1.addItem(controlesExtras(fase_1))


botao_1=pyTreeBee.linkedButton(fase_1,arial12,["Fase 1","Jardim de Valhalha"],pygame.Rect(100,100,280,192),-20,200,pygame.image.load("logo_fase1.png").convert())
botao_1.setEach_BarSize((-20,-5),(-20,-10),(-20,-15))
selecao_fase = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_1)
tela_inicial = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),pyTreeBee.linkedButton(selecao_fase,arial12,[""],pygame.Rect(0,0,800,600),250,250,pygame.image.load("Abertura copy.png").convert()))
selecao_fase.addItem(pyTreeBee.linkedButton(tela_inicial,arial12,["Voltar"],pygame.Rect(740,570,50,20),0,0))
fase_1.addItem(pyTreeBee.linkedButton(selecao_fase,arial12,["Voltar"],pygame.Rect(740,570,50,20),0,0))
'''
tela_inicial.addItem(controlesExtras(tela_inicial))
wakkanigga=pygame.image.load("viking_a_spritesheet.png")

mod=0
tela_inicial.addItem(animacaoSprite(wakkanigga,(60,50),4,True,(200,260)))
for soda in range(8):
    for sprite in range(12):
        if sprite==0 and soda==4: mod=80;wakkanigga=pygame.image.load("viking_s_spritesheet.png")
        tela_inicial.addItem(animacaoSprite(wakkanigga,(60,50),24-soda,False,(40+(sprite*60),50+mod+(soda*50))))

'''
pyTreeBee.treeBeeStart(tela_inicial)


