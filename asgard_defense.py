# -*- coding: cp1252 -*-
import pyTreeBee,pygame,sys,os
from pygame.locals import*
infoObject = pygame.display.Info()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((infoObject.current_w//2)-400, (infoObject.current_h//2)-300)
temporarydisplay=pygame.display.set_mode((800,600))
frame_atual=0
arial=pygame.font.SysFont("Arial",12)
class blocoTabuleiro(object):
    def __init__(self,numid,cor):
        self.numID=numid
        self.cor=cor
        self.piece=None
    def addPiece(self,piece):
        self.piece=piece

class moveOject(object):
    def __init__(self, origem,item, pos_ini, destino, velocidade):
        self.item=item
        self.origem=origem
        self.pos_ini=pos_ini
        self.destino=destino
        self.step=((destino[0]-pos_ini[0])/velocidade,(destino[1]-pos_ini[1])/velocidae)
    def keyControls(self,event):
        try:
            if self.destino[0]!=self.item.pos[0]:
                self.item.pos[0]+=self.step[0]
            if self.destino[1]!=self.item.pos[1]:
                self.item.pos[1]+=self.step[1]
            if self.destino[0]==self.item.pos[0] and self.destino[1]==self.item.pos[1]:
                self.origem.count-=1
                self=None
        except:
            if self.destino[0]!=self.item.x:
                self.item.x+=self.step[0]
            if self.destino[1]!=self.item.y:
                self.item.y+=self.step[1]
            if self.destino[0]==self.item.x and self.destino[1]==self.item.y:
                self.origem.count-=1
                self=None
    def blitOn(self,scr):pass

class itemCounter(object):
    def __init__(self,link,count):
        self.link=link
        self.count=count
    def keyControls(self,event):
        retorno=None
        if self.count==0: retorno=self.link
        return retorno
    def blitOn(self,scr):pass

def fadeIn(scr, *itens):
    scr.addItem(itemCounter(scr,len(self.itens)))
    origem=scr.itens[len(itens)-1]
    for item in itens:
        try:
            scr.addItem(moveObject(origem,item[0], (item[0].pos[0],item[0].pos[0]), item[1], item[2]))#item,posicao inicial,destino,velocidade
        except:
            scr.addItem(moveObject(origem,item[0], (item[0].x,item[0].y), item[1], item[2]))
        

class fadeOut(object):
    def __init__(self, link, *itens):
        self.link=link
        self.itens=list(itens)
    def linkReply(self,prevscr):
        prevscr.addItem(itemCounter(self.link,len(self.itens)))
        origem=prevscr.itens[len(itens)-1]
        for item in self.itens:
            try:
                prevscr.addItem(moveObject(origem,item[0], (item[0].pos[0],item[0].pos[0]), item[1], item[2]))#item,posicao inicial,destino,velocidade
            except:
                prevscr.addItem(moveObject(origem,item[0], (item[0].x,item[0].y), item[1], item[2]))
        return prevscr
            

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
    def __init__(self,sprite,size,nextsprite,rewind,atk,vel,hp, x,y , movimento, sentidox,sentidoy):
        self.sprite=animacaoSprite(sprite,size,nextsprite,rewind)
        self.pos=[x,y]
        self.pixelpos=[0,0]
        self.atk=atk
        self.vel=vel
        self.hp=hp
        self.hpmax=0;self.hpmax+=hp
        self.sentido=[sentidox,sentidoy]#(1,0)horizontal,vertical
        self.parede=[0,0]
        self.colidiu=False
        self.movimento=movimento
        self.vectorpos=0
        self.vectorstep=1
        self.rewind=False
        self.repeat=False
    def movimentoPadrao(self,mapa,size):
        if len(self.movimento)>0:

            #segue movimento definido
            
            next_tile=mapa[0][self.pos[1]+self.movimento[self.vectorpos][1]][self.pos[0]+self.movimento[self.vectorpos][0]]
            if self.vectorpos<len(self.movimento)-1 and self.vectorpos>=(1-self.vectorstep)/2:
                if abs(self.pixelpos[0])>=size or abs(self.pixelpos[1])>=size:
                    #muda de tile
                    next_tile.piece = mapa[0][self.pos[1]][self.pos[0]].piece
                    #next_tile.cor=(255,0,0)
                    mapa[0][self.pos[1]][self.pos[0]].piece=None
                    self.pos[0]+=self.movimento[self.vectorpos][0]
                    self.pos[1]+=self.movimento[self.vectorpos][1]
                    self.vectorpos+=self.vectorstep
                    if self.pixelpos[0]>=size:
                        self.pixelpos[0]-=size
                    if self.pixelpos[1]>=size:
                        self.pixelpos[1]-=size
                        
                    if self.pixelpos[0]<=-size:
                        self.pixelpos[0]+=size
                    if self.pixelpos[1]<=-size:
                        self.pixelpos[1]+=size
                else:
                    self.pixelpos[0]+=self.vel*self.movimento[self.vectorpos][0]
                    self.pixelpos[1]+=self.vel*self.movimento[self.vectorpos][1]
            else:
                if self.rewind: self.vectorstep*=-1
                elif self.repeat: self.vectorpos=0
        else:pass
            ###segue paredes###
        
    

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
    def movimentoPadrao(self,mapa,size):#ataque circular
        global frame_atual
        if self.aim==None:
           for y in range(len(mapa[0])):
               for x in range(len(mapa[0][y])):
                   if mapa[0][y][x].piece!=None:
                       x_a=(mapa[0][y][x].piece.pos[0]*size) + mapa[0][y][x].piece.pixelpos[0]
                       y_a=(mapa[0][y][x].piece.pos[1]*size) + mapa[0][y][x].piece.pixelpos[1]
                       if abs(pow(  (pow((self.x*size)-x_a,2) + pow((self.y*size)-y_a,2)),0.5))<self.rng*size:
                           print str(pow(  (pow((self.x*size)-x_a,2) + pow((self.y*size)-y_a,2)),0.5))+" "+str(self.rng*size)
                           if self.sprite.y!=1: self.sprite.setLine(1)
                           self.aim=mapa[0][y][x]
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
    def fightControls_anterior(self,mapa):
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


class charSelected(object):
    def __init__(self,mouse,sprite,size,nextsprite,rewind,atk,vel,rng):
        self.mouse=mouse
        self.sprite=sprite
        self.size=size
        self.nextsprite=nextsprite
        self.rewind=rewind
        self.atk=atk
        self.vel=vel
        self.rng=rng
    def linkReply(self,prevscr):
        self.mouse.setSelection(self.sprite,self.size,self.nextsprite,self.rewind,self.atk,self.vel,self.rng)
        return prevscr

class quadradoControlavel(object):
    def __init__(self,size):
        self.x=1
        self.y=1
        self.sprite=animacaoSprite(pygame.image.load("selecao3.png"),(40,40),9,True)
        self.size=size
        self.buttonup=False
        self.dentro=True
        self.torre=pygame.image.load("viking_spritesheet.png")
        self.inimigo=pygame.image.load("inimigo01sheet2.png")
        self.botaodireito=False
        self.botaoesquerdo=False
        
        self.char_sprite=None
        self.char_size=None
        self.nextsprite=None
        self.rewind=None
        self.atk=None
        self.vel=None
        self.rng=None
    def setSelection(self,sprite,size,nextsprite,rewind,atk,vel,rng):
        self.char_sprite=sprite
        self.char_size=size
        self.nextsprite=nextsprite
        self.rewind=rewind
        self.atk=atk
        self.vel=vel
        self.rng=rng
    def nullSelection(self):
        self.char_sprite=None
        self.char_size=None
        self.nextsprite=None
        self.rewind=None
        self.atk=None
        self.vel=None
        self.rng=None
    def blitOn(self,screen):
        if self.char_sprite!=None:
            try: screen.blit(self.char_sprite.subsurface(((0,0),self.char_size)),((self.x*self.size)-(self.char_size[0]/2)+(self.size/2),self.y*self.size) )
            except:pass
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
                if self.char_sprite!=None:
                    if mapa[1][self.y][self.x].piece==None:
                        if mapa[1][self.y][self.x].numID>=3 and mapa[1][self.y][self.x].numID<=11:
                            mapa[1][self.y][self.x].addPiece(torreGuerreiro(self.char_sprite,self.char_size,self.nextsprite,self.rewind,self.atk,self.vel,self.rng, self.x,self.y))
                            self.nullSelection()#isso apaga a info do mouse depois de colocar a torre - voce pode realocar
                '''
                else:
                    if mapa[1][self.y][self.x].piece==None:
                        if mapa[1][self.y][self.x].numID>=3 and mapa[1][self.y][self.x].numID<=11:
                            mapa[1][self.y][self.x].addPiece(torreGuerreiro(self.torre,(60,50),6,False,10,10,1,self.x,self.y))
                '''
        if self.botaodireito:
            if mapa[0][self.y][self.x].numID==0:
                if self.dentro:
                    mapa[0][self.y][self.x].addPiece(inimigoAlvo(self.inimigo,(20,20),10,False,1,1,10,self.x,self.y,[],1,0))
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
            
class lifeTarget(object):
    def __init__(self,pos, sentido=None):
        self.pos=pos
        self.sentido=sentido
    def fightControls(self,mapa):
        if self.sentido==None:
            for x in range(-1,2):
                for y in range(-1,2):
                    around=mapa[0][self.pos[1]+y][self.pos[0]+x]
                    if around.piece!=None:
                        around.piece=None
        else:
            point=mapa[0][self.pos[1]+self.sentido[1]][self.pos[0]+self.sentido[0]]
            if point.piece!=None:
                point.piece=None
                

class spawnInimigo(object):
    def __init__(self,pos,time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,movimento,sentidos,quantidades):
        self.spawntime=time
        self.spawn=where
        self.pos=pos
        
        self.movimento=movimento

        self.sprite=sprites
        self.size=tamanhos
        self.next=nextsprites
        self.rewind=rewinds
        self.atk=forcas
        self.vel=velocidades
        self.hp=vidas
        self.sentido=sentidos
        self.quantidade=[0,quantidades]
        self.contador=0
    def fightControls(self,mapa):
        global frame_atual
        if self.contador<len(self.sprite):
            if frame_atual%self.spawntime[self.contador]==0:
                if self.quantidade[0]<self.quantidade[1][self.contador]:
                    sc=self.contador# (self,sprite,size,nextsprite,rewind,atk,vel,hp, x,y , movimento, sentidox,sentidoy)
                    #print str(self.sprite[sc])+" , "+str(self.size[sc])+" , "+str(self.next[sc])+" , "+str(self.rewind[sc])+" , "+str(self.atk[sc])+" , "+str(self.vel[sc])+" , "+str(self.hp[sc])+" , "+str(self.pos[0]+self.spawn[0])+" , "+str(self.pos[1]+self.spawn[1])+" , "+str(self.sentido[sc])
                    #print str(self.sprite)+" , "+str(self.size)+" , "+str(self.next)+" , "+str(self.rewind)+" , "+str(self.atk)+" , "+str(self.vel)+" , "+str(self.hp)+" , "+str(self.pos[0]+self.spawn[0])+" , "+str(self.pos[1]+self.spawn[1])+" , "+str(self.sentido)
                    inimigo=inimigoAlvo(self.sprite[sc],self.size[sc],self.next[sc], self.rewind[sc], self.atk[sc],self.vel[sc],self.hp[sc], (self.pos[0]+self.spawn[0]), (self.pos[1]+self.spawn[1]), self.movimento[sc], self.sentido[sc][0], self.sentido[sc][1])
                    
                    mapa[0][self.pos[1]+self.spawn[1]][self.pos[0]+self.spawn[0]].piece=inimigo
                    self.quantidade[0]+=1
                    #print self.quantidade
                else:
                    self.contador+=1
                    self.quantidade[0]=0
                
class mapaLimitavel(object):
    def __init__(self, mapa,imagens,size):
        self.alingment=(0,0)
        self.mapa=mapa
        for z in range(len(self.mapa)):
            for y in range(len(self.mapa[z])):
                for x in range(len(self.mapa[z][y])):
                    try:
                        if self.mapa[z][y][x]<len(imagens) and self.mapa[z][y][x]>=0:
                            self.mapa[z][y][x]=blocoTabuleiro(self.mapa[z][y][x],imagens[self.mapa[z][y][x]])
                        else:
                            self.mapa[z][y][x]=blocoTabuleiro(self.mapa[z][y][x],None)
                    except:
                        pass
        self.size=size
        self.selecao=quadradoControlavel(self.size)
    def addSpawn(self,pos,time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,movimento,sentidos,quantidades):
        self.mapa[1][pos[1]][pos[0]].piece=spawnInimigo(pos,time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,movimento,sentidos,quantidades)
    def addTarget(self,pos, sentido=None):
        self.mapa[1][pos[1]][pos[0]].piece=lifeTarget(pos,sentido)
    def blitOn(self,screen):
        for z in range(len(self.mapa)):                                
            for y in range(len(self.mapa[z])):
                for x in range(len(self.mapa[z][y])):
                    if self.mapa[z][y][x].piece!=None:
                        try:
                            self.mapa[z][y][x].piece.movimentoPadrao(self.mapa,self.size)
                        except:
                            self.mapa[z][y][x].piece.fightControls(self.mapa)
                    #sprite=False
                    try:
                        screen.blit(self.mapa[z][y][x].cor,(self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size)))
                    except:
                        try:
                            screen.fill(self.mapa[z][y][x].cor,pygame.Rect(self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size),self.size,self.size))
                        except:pass
        for y in range(len(self.mapa[1])):
            for x in range(len(self.mapa[1][y])):
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
                    pass #print "erro desenhar inimigo"
                try:
                    if self.mapa[1][y][x].piece!=None:
                        alinhaspriteX=(self.size/2)-(self.mapa[1][y][x].piece.sprite.size[0]/2)
                        screen.blit(self.mapa[1][y][x].piece.sprite.getNextImage(), (self.alingment[0]+(x*self.size)+alinhaspriteX,self.alingment[1]+(y*self.size)))
                        #screen.blit(pygame.transform.scale(self.mapa[y][x].getNextImage(),(40,33)), (self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size)))
                except:
                    pass #print "erro desenhar torre"

        self.selecao.blitOn(screen)
        
    def keyControls(self,event):
        self.selecao.keyControls(event,self.mapa, self.alingment)
        

class controlesExtras(object):
    def __init__(self,tela):
        self.tela=tela
        self.scroll=[0,0]
        self.frame_skip=1
    def blitOn(self,screen):
        global frame_atual
        if frame_atual>=pow(10,4)-self.frame_skip:
            frame_atual=0
            print 'zerou'
        else:
            frame_atual+=self.frame_skip
        screen.scroll(self.scroll[0],self.scroll[1])
    def keyControls(self,event):
        if event.type==KEYUP:
            if event.key==K_ESCAPE:
                self.tela.storedlink=None
                self.tela.running=False
            if event.key==K_DOWN:
                self.scroll[1]+=10
            if event.key==K_RIGHT:
                self.scroll[0]+=10
            if event.key==K_UP:
                self.scroll[1]-=10
            if event.key==K_LEFT:
                self.scroll[0]-=10
            if event.key==K_EQUALS:
                self.tela.fps+=10
            if event.key==K_MINUS:
                self.tela.fps-=10
        return None

        
#matriz seletora de tiles da fase 1
matriz_fase_1=[[[12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [ 1, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 2],
              [ 1, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 2],
              [-1,-1,-1,-1,-1,-1, 0, 0, 0,-1,-1, 0, 0, 0,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1, 0, 0, 0,-1,-1, 0, 0, 0,-1,-1,-1,-1,-1,-1],
              [-1, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1],
              [-1, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1],
              [-1, 0, 0, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 0, 0, 0,-1],
              [-1, 0, 0, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 0, 0, 0,-1],
              [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1],
              [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]],#13
             [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [ 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1, 4,10,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1, 4,10,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [ 6, 6, 6, 6, 6, 6, 9,-1,-1, 4,10,-1,-1, 3, 6, 6, 6, 6, 6, 6],
              [ 7, 8, 8, 8, 8, 8,11,-1,-1, 4,10,-1,-1, 5, 8, 8, 8, 8, 8, 7],
              [10,-1,-1,-1,-1,-1,-1,-1,-1, 4,10,-1,-1,-1,-1,-1,-1,-1,-1, 4],
              [10,-1,-1,-1,-1,-1,-1,-1,-1, 4,10,-1,-1,-1,-1,-1,-1,-1,-1, 4],
              [10,-1,-1, 3, 6, 6, 6, 6, 6, 7, 7, 6, 6, 6, 6, 6, 9,-1,-1, 4],
              [10,-1,-1, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,11,-1,-1, 4],
              [10,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 4],
              [10,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 4],
              [ 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7]],
             [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]]
#loading dos tiles
tile_grama=pygame.image.load("tileset_grama.png").convert()
tiles_fase_1=[pygame.image.load("mapacaminho5.png").convert(),pygame.image.load("mapaentrada2.png").convert(),pygame.image.load("mapasaida.png").convert()]#,tile_grama.subsurface((40,40),(40,40)),tile_grama.subsurface((40,80),(40,40)),tile_grama.subsurface((0,80),(40,40)),tile_grama.subsurface((80,80),(40,40)),tile_grama.subsurface((80,0),(40,40)),tile_grama.subsurface((0,0),(40,40)),tile_grama.subsurface((40,40),(0,40)),tile_grama.subsurface((40,0),(40,40)),tile_grama.subsurface(
for w in range(3):
    for h in range(3):
        tiles_fase_1.append(tile_grama.subsurface((w*40,h*40),(40,40)))
tiles_fase_1.append((34,57,65))
mapa_fase_1 = mapaLimitavel(matriz_fase_1, tiles_fase_1,40)
#spawn gerador de hordaS
enemyimg=pygame.image.load("inimigo01sheet2.png")
mov_y3=[(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,1),(0,1),(0,1),(0,1),(0,1),
        (1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
        (0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)]
mov_y2=[(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(0,1),(0,1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,1),(0,1),(0,1),
        (1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
        (0,-1),(0,-1),(0,-1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)]
mapa_fase_1.addSpawn( (0,3) , [120,150] , (1,0) , [enemyimg,enemyimg] , [(20,20),(20,20)] , [8,10] , [True,True] , [1,1] , [0.5,0.3] , [100,300] , [mov_y3,mov_y3] , [(1,0),(1,0)] , [20,20])
mapa_fase_1.addSpawn( (0,2) , [120,150] , (1,0) , [enemyimg,enemyimg] , [(20,20),(20,20)] , [8,10] , [True,True] , [1,1] , [0.5,0.3] , [100,300] , [mov_y2,mov_y2] , [(1,0),(1,0)] , [20,20])
#alvo para o inimigo dar pontos de dano
mapa_fase_1.addTarget((19,3),(-1,0))
mapa_fase_1.addTarget((19,2),(-1,0))
#botoes de personagens
viking_image=pygame.image.load("viking_spritesheet.png")
viking_lvl_1=charSelected(mapa_fase_1.selecao,viking_image,(60,50),6,False,10,10,1)
valkyria_lvl_1=charSelected(mapa_fase_1.selecao,viking_image,(60,50),2,True,10,10,8)
botao_viking = pyTreeBee.linkedButton(viking_lvl_1,arial,["1 range"],pygame.Rect(25,535,50,50),0,0)
botao_valkyria = pyTreeBee.linkedButton(valkyria_lvl_1,arial,["8 range"],pygame.Rect(100,535,50,50),0,0)
#fase 1
fase_1 = pyTreeBee.dynamicScreen((800,600), 60,(78,133,154),mapa_fase_1,botao_viking,botao_valkyria)
fase_1.addItem(controlesExtras(fase_1))
#seleção de fases
botao_1=pyTreeBee.linkedButton(fase_1,arial,["Fase 1","Jardim de Valhalla"],pygame.Rect(100,100,280,192),-20,200,pygame.image.load("logo_fase1.png").convert())
botao_1.setEach_BarSize((-20,-5),(-20,-10),(-20,-15))
selecao_fase = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_1)
#tela inicial
botao_start=pyTreeBee.linkedButton(selecao_fase,arial,[""],pygame.Rect(0,0,800,600),250,250,pygame.image.load("Abertura copy.png").convert())
tela_inicial = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_start)
#botões de voltar adicionados às telas anteriores
selecao_fase.addItem(pyTreeBee.linkedButton(tela_inicial,arial,["Voltar"],pygame.Rect(740,570,50,20),0,0))
fase_1.addItem(pyTreeBee.linkedButton(selecao_fase,arial,["Voltar"],pygame.Rect(740,570,50,20),0,0))
#início dos ciclos
pyTreeBee.treeBeeStart(tela_inicial)


