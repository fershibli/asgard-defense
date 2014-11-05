# -*- coding: cp1252 -*-
import pyTreeBee,pygame,sys,os,time, pygame.mixer, copy
import cPickle as pickle
from pygame.locals import*
infoObject = pygame.display.Info()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((infoObject.current_w//2)-400, (infoObject.current_h//2)-300)
temporarydisplay=pygame.display.set_mode((800,600))
dinB_22=pygame.font.Font("DIN-Black.otf",22)
dinBd_32=pygame.font.Font("DIN-Bold.otf",32)

loading=dinB_22.render("LOADING...",True,(255,255,255))
temporarydisplay.blit(loading,(370,278))
pygame.display.update()

frame_atual=0
din_12=pygame.font.Font("DIN-Medium.otf",12)
dinB_12=pygame.font.Font("DIN-Black.otf",12)
pygame.mixer.init()

#musica inicial, precisa dela pros botões de voltar cuidarem disso.
pygame.mixer.music.load("Five Armies.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(5)
'''
class hiddenStages(object):
    def __init__(self,selec_scr,*linkedButton_stage):
        self.stages=list(linkedButton_stage)
        self.locked=[False]*len(self.stages)
        self.added=[False]*len(self.stages)
    def unlockStage(self,number):
'''
class deleteSave(object):
    def __init__(self,tela):
        self.tela=tela
    def linkReply(self,prevscr):
        arq=open('game.ages','w')
        arq.write('''
lavhalsvnxlvkasfh
''')
        arq.close
        for liberada in load_fases_liberadas:
            liberada.stateClear()
        return self.tela
    
class lockedButton(object):
    def __init__(self,linkedButton,id_str):
        self.linkedButton=linkedButton
        self.unlocked=False
        self.id_str=id_str
    def blitOn(self,scr):
        if self.unlocked: self.linkedButton.blitOn(scr)
    def keyControls(self,event):
        retorno=False
        if self.unlocked: retorno=self.linkedButton.keyControls(event)
        return retorno
    def unlockButton(self):#na vitoria
        self.unlocked=True
    def stateLoad(self):#no inicio        
        arq=open('Data\game'+self.id_str+'.ages','rb')
        self.unlocked=pickle.load(arq)
        arq.close
    def stateClear(self):
        self.unlocked=False
        self.stateDump()
    def stateDump(self):#no fim
        arq=open('Data\game'+self.id_str+'.ages','wb')
        pickle.dump(self.unlocked,arq)
        arq.close

class linkedMusic(object):
    def __init__(self, link, music, repeat, start_time):
        self.link=link
        self.music=music
        self.repeat=repeat
        self.start_time=start_time
    def linkReply(self,prevscr):
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(self.music)
        except:
            print "can't load music"
        try:
            pygame.mixer.music.play(self.repeat,self.start_time)
        except:
            print "can't play music"
        self.link.stored_music=self.music
        return self.link

class moveObject(object):
    def __init__(self, origem,item, pos_ini, destino, velocidade):
        self.item=item
        self.origem=origem
        self.pos_ini=pos_ini
        self.destino=destino
        self.step=(((destino[0]-pos_ini[0])/velocidade),((destino[1]-pos_ini[1])/velocidade))
    def keyControls(self,event):
        return False
    def blitOn(self,scr):
        try:
            if self.destino[0]!=self.item.x:
                self.item.x+=self.step[0]
            if self.destino[1]!=self.item.y:
                self.item.y+=self.step[1]
            if self.destino[0]==self.item.x and self.destino[1]==self.item.y:
                self.origem.count-=1
                self=None            
        except:
            try:
                if self.destino[0]!=self.item.pos[0]:
                    self.item.pos[0]+=self.step[0]
                if self.destino[1]!=self.item.pos[1]:
                    self.item.pos[1]+=self.step[1]
                if self.destino[0]==self.item.pos[0] and self.destino[1]==self.item.pos[1]:
                    self.origem.count-=1
                    self=None
            except:
                pass

class itemCounter(object):
    def __init__(self,scr,link,count):
        self.scr=scr
        self.link=link
        self.count=count
    def keyControls(self,event):pass
    def blitOn(self,scr):
        if self.count==0:
            self.scr.linkcalled=self.link
'''
class fadeIn(object):
    def __init__(self,
'''
def fadeIn(scr,link, *itens):
    origem=itemCounter(scr,link,len(itens))
    scr.addItem(origem)
    for item in itens:
        try:
            scr.addItem(moveObject(origem,item[0], (item[0].x,item[0].y), item[1], item[2]))
        except:
            try:
                scr.addItem(moveObject(origem,item[0], (item[0].pos[0],item[0].pos[0]), item[1], item[2]))#item,posicao inicial,destino,velocidade
            except:
                pass
        

class fadeOut(object):
    def __init__(self,scr, link, *itens):
        self.scr=scr
        self.link=link
        self.itens=list(itens)
    def linkReply(self,prevscr):
        origem=itemCounter(self.scr,self.link,len(self.itens))
        self.scr.addItem(origem)
        for item in self.itens:
            try:
                self.scr.addItem(moveObject(origem,item[0], (item[0].x,item[0].y), item[1], item[2]))
            except:
                self.scr.addItem(moveObject(origem,item[0], (item[0].pos[0],item[0].pos[0]), item[1], item[2]))#item,posicao inicial,destino,velocidade
        return self.scr


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
        self.x_sheet=0
        self.y_sheet=0
        self.x=pos[0]
        self.y=pos[1]
        self.step=stepnextsprite
        self.rewind=rewind
        self.next=1
        self.pause_time=0
        self.repeats=0
        self.stop=False
        self.wait=False
        self.invert=[False,False]
        #self.pos=pos
    def setPause(self,pause):
        self.pause_time=pause
    def setStop(self,repeats):
        self.repeats=repeats
    def setLine(self, line):
        if line>=0 and line<int(self.sheet.get_height()/self.size[1]): self.y_sheet=line
    def getNextImage(self):
        global frame_atual
        if self.wait and frame_atual%(self.pause_time+self.step)==0:
            self.wait=False
            if self.x_sheet==int(self.sheet.get_width()/self.size[0])-1: self.x_sheet-=1
            if self.rewind: self.x_sheet+=1
        if frame_atual%self.step==0 and self.stop==False and self.wait==False:
            if int(((self.x_sheet+1)*self.size[0])/self.sheet.get_width())>=1 or (self.x_sheet+1)<=(-self.next+1)/2:
                if self.rewind:
                    self.next=(-1)
                    self.x_sheet=int(self.sheet.get_width()/self.size[0])-2
                    self.rewind=False
                else:
                    self.x_sheet=(-self.next+1)/2
                    if self.next==(-1):
                        self.next=1
                        self.rewind=True
                        
                if self.repeats>0:
                    self.repeats-=(-self.next+1)/2
                    if self.repeats==0:
                        self.stop=True
                        self.x_sheet=int(self.sheet.get_width()/self.size[0])-1
                if self.pause_time>0:
                    self.wait=True
                    if self.next==-1:self.x_sheet=int(self.sheet.get_width()/self.size[0])-1
                    if self.rewind:self.x_sheet=(-self.next+1)/2
            else:
                self.x_sheet+=self.next
        return pygame.transform.flip(self.sheet.subsurface((self.x_sheet*self.size[0],self.y_sheet*self.size[1]),self.size),self.invert[0],self.invert[1])
    def blitOn(self,screen):
        screen.blit(self.getNextImage(),(self.x,self.y))


class inimigoAlvo(object):#inimigoAlvo(pygame.image.load("inimigo01sheet2.png"),(20,20),10,False,1,1,1,
    def __init__(self,sprite,size,nextsprite,rewind,atk,vel,hp, voador, tipo, x,y , movimento, sentidox,sentidoy,mana):
        self.mana=mana
        self.sprite=animacaoSprite(sprite,size,nextsprite,rewind)
        self.pos=[x,y]
        self.pixelpos=[0,0]
        self.atk=atk
        self.vel=vel
        self.hp=hp
        self.fly=voador
        self.type=tipo
        self.hpmax=0;self.hpmax+=hp
        self.sentido=[sentidox,sentidoy]#(1,0)horizontal,vertical
        self.parede=[0,0]
        self.colidiu=False
        self.movimento=movimento
        self.vectorpos=0
        self.vectorstep=1
        self.rewind=False
        self.repeat=False
    def setZero(self,mapa):
        mapa[0][self.pos[1]][self.pos[0]].addPiece(None)
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
                    try:
                        if self.movimento[self.vectorpos+1][0]==1:
                            self.sprite.invert[0]=False
                        if self.movimento[self.vectorpos+1][0]==-1:
                            self.sprite.invert[0]=True
                    except:
                        pass
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
        
    
class animacaoPerene(object):
    def __init__(self,animacao):
        self.sprite=animacao
    def setZero(self,mapa):pass
    def getNextImage(self):self.sprite.getNextImage()
    def fightControls(self,mapa):pass

class bloqueioPerene(object):
    def setZero(self,mapa):pass
    def getNextImage(self):pass
    def fightControls(self,mapa):pass


class torreGuerreiro(object):
    def __init__(self,sprite,size,nextsprite,rewind,atk,vel,rng,alto,dmgtipos, x,y,custo,personagem):
        self.mana=custo
        self.player=personagem
        self.sprite=animacaoSprite(sprite,size,nextsprite,rewind)
        self.atk=atk
        self.vel=vel
        self.rng=rng
        self.fly=alto
        self.dmg_types=dmgtipos
        self.aim=None
        self.x=x
        self.y=y
    def setZero(self,mapa):
        mapa[1][self.y][self.x].addPiece(None)
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
                            if mapa[0][self.y+e][self.x+i].piece.fly==self.fly or self.fly:
                                if self.sprite.y!=1: self.sprite.setLine(1)
                                self.aim=mapa[0][self.y+e][self.x+i]
                    except:
                        pass
        else:            
            if frame_atual%self.vel==0:
                try:
                    self.aim.piece.hp-=self.atk*self.dmg_types[self.aim.piece.type]
                    if self.aim.piece.hp<=0:
                        self.player.mana+=self.aim.piece.mana
                        self.aim.addPiece(None)
                        self.aim=None
                        if self.sprite.y_sheet!=0: self.sprite.setLine(0)
                        self.player.score+=1
                except:
                    self.aim=None
                    self.sprite.setLine(0)

class accelGame(object):
    def __init__(self, fps):
        self.fps=fps
    def linkReply(self,prevscr):
        prevscr.fps=self.fps
        return prevscr

class charSelected(object):
    def __init__(self,mouse,sprite,size,nextsprite,rewind,atk,vel,rng,voador,tipo,mana):
        self.mouse=mouse
        self.sprite=sprite
        self.size=size
        self.nextsprite=nextsprite
        self.rewind=rewind
        self.atk=atk
        self.vel=vel
        self.rng=rng
        self.fly=voador
        self.dmg_type=tipo
        self.mana=mana
    def linkReply(self,prevscr):
        self.mouse.setSelection(self.sprite,self.size,self.nextsprite,self.rewind,self.atk,self.vel,self.rng,self.fly,self.dmg_type,self.mana)
        return prevscr

class quadradoControlavel(object):
    def __init__(self,player):
        self.player=player
        self.x=1
        self.y=1
        self.sprite=animacaoSprite(pygame.image.load("selecao4.png"),(40,40),9,True)
        self.buttonup=False
        self.dentro=True
        self.botaodireito=False
        self.botaoesquerdo=False
        self.nullSelection()
        self.size=1
    def setSize(self,size):
        self.size=size
    def setSelection(self,sprite,size,nextsprite,rewind,atk,vel,rng,fly,dmg,mana):
        self.char_sprite=sprite
        self.char_size=size
        self.nextsprite=nextsprite
        self.rewind=rewind
        self.atk=atk
        self.vel=vel
        self.rng=rng
        self.fly=fly
        self.dmg_type=dmg
        self.mana=mana
    def nullSelection(self):
        self.setSelection(None,None,None,None,None,None,None,None,None,None)
    def blitOn(self,screen):
        if self.dentro:
            if self.char_sprite!=None:
                screen.blit(self.char_sprite.subsurface(((0,0),self.char_size)),((self.x*self.size)-(self.char_size[0]/2)+(self.size/2),(self.y*self.size)-(self.char_size[1]*3/4)+(self.size/2)-5) )
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
                        if mapa[1][self.y][self.x].numID<=8 and mapa[1][self.y][self.x].numID>=0:
                            if self.player.mana>=self.mana:
                                mapa[1][self.y][self.x].addPiece(torreGuerreiro(self.char_sprite,self.char_size,self.nextsprite,self.rewind,self.atk,self.vel,self.rng,self.fly,self.dmg_type, self.x,self.y,self.mana,self.player))
                                self.player.mana-=self.mana
                            self.nullSelection()
            else:
                self.nullSelection()
        if self.botaodireito:
            if mapa[0][self.y][self.x].numID==0:
                if self.dentro:
                    pass #acontecimentos para botao direito
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
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
        return False
            
class lifeTarget(object):
    def __init__(self,player,pos, sentido=None):
        self.pos=pos
        self.sentido=sentido
        self.player=player
    def setZero(self,mapa):
        pass
    def fightControls(self,mapa):
        if self.sentido==None:
            for x in range(-1,2):
                for y in range(-1,2):
                    around=mapa[0][self.pos[1]+y][self.pos[0]+x]
                    if around.piece!=None:
                        self.player.life-=around.piece.atk
                        around.piece=None
                        
        else:
            point=mapa[0][self.pos[1]+self.sentido[1]][self.pos[0]+self.sentido[0]]
            if point.piece!=None:
                
                self.player.life-=point.piece.atk
                point.piece=None
                

class spawnInimigo(object):
    def __init__(self,pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,mana,quantidades):
        self.spawntime=time
        self.spawn=where
        self.pos=pos
        self.mana=mana
        self.movimento=movimento

        self.sprite=sprites
        self.size=tamanhos
        self.next=nextsprites
        self.rewind=rewinds
        self.atk=forcas
        self.vel=velocidades
        self.hp=vidas
        self.fly=voador
        self.type=tipos
        self.sentido=sentidos
        self.quantidade=[0,quantidades]
        self.contador=0
        self.pause=True
        self.pause_time=pause_time
    def setZero(self,mapa):
        self.quantidade[0]=0
        self.contador=0
        self.pause=False
    def fightControls(self,mapa):
        global frame_atual
        if self.pause and frame_atual%self.pause_time[self.contador]==0:
            self.pause=False
        if self.contador<len(self.sprite):
            if frame_atual%self.spawntime[self.contador]==0 and self.pause==False:
                if self.quantidade[0]<self.quantidade[1][self.contador]:
                    sc=self.contador
                    inimigo=inimigoAlvo(self.sprite[sc],self.size[sc],self.next[sc], self.rewind[sc], self.atk[sc],self.vel[sc],self.hp[sc],self.fly[sc],self.type[sc], (self.pos[0]+self.spawn[0]), (self.pos[1]+self.spawn[1]), self.movimento[sc], self.sentido[sc][0], self.sentido[sc][1],self.mana[sc])
                    mapa[0][self.pos[1]+self.spawn[1]][self.pos[0]+self.spawn[0]].piece=inimigo
                    self.quantidade[0]+=1
                else:
                    self.contador+=1
                    self.quantidade[0]=0
                    self.pause=True
                
class mapaLimitavel(object):
    def __init__(self,mouse,player,mapa,imagens,size,*fases_liberadas):
        self.alingment=(0,0)
        self.stage_key=list(fases_liberadas)
        self.player=player
        self.mapa=mapa
        self.imagens=imagens
        self.desenhaMapa()
        self.size=size
        self.selecao=mouse
        self.qnt_inimigos=0
    def desenhaMapa(self):
        for z in range(len(self.mapa)):
            for y in range(len(self.mapa[z])):
                for x in range(len(self.mapa[z][y])):
                    try:
                        if self.mapa[z][y][x]<len(self.imagens) and self.mapa[z][y][x]>=0:
                            self.mapa[z][y][x]=blocoTabuleiro(self.mapa[z][y][x],self.imagens[self.mapa[z][y][x]])
                        else:
                            self.mapa[z][y][x]=blocoTabuleiro(self.mapa[z][y][x],None)
                    except:
                        pass
    def setZero(self,tela):
        global frame_atual
        frame_atual=0
        tela.fps=60
        for camada in self.mapa:
            for fileira in camada:
                for bloco in fileira:
                    if bloco.piece!=None:
                        bloco.piece.setZero(self.mapa)
        self.player.setZero()
        self.selecao.nullSelection()
    def addSpawn(self,pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,manas,quantidades):
        for qnt in quantidades:
            self.qnt_inimigos+=qnt
        self.mapa[1][pos[1]][pos[0]].piece=spawnInimigo(pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,manas,quantidades)
    def addTarget(self,plr,pos, sentido=None):
        self.mapa[1][pos[1]][pos[0]].piece=lifeTarget(plr,pos,sentido)
    def blitOn(self,screen):
        if self.selecao.size!=self.size:
            self.selecao.size=self.size
        for z in range(len(self.mapa)):                                
            for y in range(len(self.mapa[z])):
                for x in range(len(self.mapa[z][y])):
                    if self.mapa[z][y][x].piece!=None:
                        try:
                            self.mapa[z][y][x].piece.movimentoPadrao(self.mapa,self.size)
                        except:
                            try:
                                self.mapa[z][y][x].piece.fightControls(self.mapa)
                            except:
                                pass
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

                        #screen.fill((0,0,0),pygame.Rect(posx+2,posy,self.size-4,8))
                        screen.fill((255,0,0),pygame.Rect(posx+4,posy+2,self.size-8,4))
                        
                        life=self.size-((self.mapa[0][y][x].piece.hpmax-self.mapa[0][y][x].piece.hp)*self.size/self.mapa[0][y][x].piece.hpmax)

                        screen.fill((0,255,50),pygame.Rect(posx+4,posy+2,life-8,4))
                except:
                    pass #print "erro desenhar inimigo"
                try:
                    if self.mapa[1][y][x].piece!=None:
                        alinhaspriteX=(self.size/2)-(self.mapa[1][y][x].piece.sprite.size[0]/2)
                        alinhaspriteY=(self.size/2)-(self.mapa[1][y][x].piece.sprite.size[1]*3/4)
                        torre_peca=self.mapa[1][y][x].piece.sprite
                        if torre_peca.x==0 and torre_peca.y==0:
                            screen.blit(torre_peca.getNextImage(), (self.alingment[0]+(x*self.size)+alinhaspriteX,self.alingment[1]+(y*self.size)+alinhaspriteY))
                        else:
                            screen.blit(torre_peca.getNextImage(), (torre_peca.x,torre_peca.y))
                        #screen.blit(pygame.transform.scale(self.mapa[y][x].getNextImage(),(40,33)), (self.alingment[0]+(x*self.size),self.alingment[1]+(y*self.size)))
                except:
                    pass #print "erro desenhar torre"

        if self.player.life>(self.player.maxlife*2)/3:
            cor_vida=(25,255,0)
        else:
            if self.player.life>self.player.maxlife/3:
                cor_vida=(255,200,10)
            else:
                cor_vida=(255,10,10)
        screen.blit(din_12.render("VIDAS:",True,(255,255,255)),(740,0))
        screen.blit(dinB_22.render(str(self.player.life),True,cor_vida),(740,10))
        screen.blit(din_12.render("SCORE:",True,(255,255,255)),(32,0))
        screen.blit(dinB_22.render(str(self.player.score),True,(255,255,255)),(32,10))
        screen.blit(din_12.render("MANA:",True,(255,255,255)),(680,0))
        screen.blit(dinB_22.render(str(self.player.mana),True,(10,125,255)),(680,10))
        self.selecao.blitOn(screen)
        
    def keyControls(self,event):
        self.selecao.keyControls(event,self.mapa, self.alingment)
        return False

class winnerScreen(object):
    def __init__(self,tela,link,mapa,music=None):
        self.tela=tela
        self.link=link
        self.mapa=mapa
        self.music=music
    def blitOn(self,scr):
        global voltar_retry
        if self.mapa.player.maxlife-self.mapa.player.life+self.mapa.player.score==self.mapa.qnt_inimigos:
            if self.music:
                pygame.mixer.music.load(self.music[0])
                pygame.mixer.music.play(self.music[1], self.music[2])
            pygame.mouse.set_visible(True)
            for fase in self.mapa.stage_key:
                fase.unlockButton()
            saveAll()
            voltar_retry.link=linkedMusic(self.tela,self.tela.stored_music,-1,0.0)
            time.sleep(2)
            self.mapa.setZero(self.tela)
            self.tela.linkcalled=self.link
    def keyControls(self,event):pass

class gameOver(object):
    def __init__(self,tela,link,mapa,music=None):
        self.tela=tela
        self.link=link
        self.mapa=mapa
        self.music=music
    def blitOn(self,scr):
        global voltar_retry
        if self.mapa.player.life<=0:
            if self.music:
                pygame.mixer.music.load(self.music[0])
                pygame.mixer.music.play(self.music[1], self.music[2])
            pygame.mouse.set_visible(True)
            voltar_retry.link=linkedMusic(self.tela,self.tela.stored_music,-1,0.0)
            time.sleep(2)
            self.mapa.setZero(self.tela)
            self.tela.linkcalled=self.link
    def keyControls(self,event):pass

class statusPlayer(object):
    def __init__(self,vida, mana):
        self.life=vida
        self.maxlife=vida
        self.mana=mana
        self.initialmana=mana
        self.score=0
        self.counter=0
    def setZero(self):
        self.life=self.maxlife
        self.mana=self.initialmana
        self.score=0
        self.counter=0
        
class volumeControl(object):
    def __init__(self, how_much):
        self.amount=how_much
    def linkReply(self, prevscr):
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + self.amount)
        return prevscr

class renderVolume(object):
    def __init__(self, fonte,cor,pos,diferenciador=1):
        self.font=fonte
        self.color=cor
        self.pos=pos
        self.unit=diferenciador
    def blitOn(self,scr):
        scr.blit(self.font.render(str(int(pygame.mixer.music.get_volume()*self.unit)),True,self.color),self.pos)
    def keyControls(self,event):pass

class escritorDireto(object):
    def __init__(self, render, pos):
        self.render=render
        self.pos=pos
    def blitOn(self,scr):
        scr.blit(self.render,self.pos)
    def keyControls(self,event):pass

class estruturaPause(object):
    def __init__(self):
        self.link=False
    def blitOn(self,scr):
        pygame.mouse.set_visible(True)
        scr.blit(dinB_22.render("PAUSE",True,(255,255,255)),(370,278))
    def keyControls(self,event):
        retorno=False
        if event.type==KEYUP:
            if event.key==K_SPACE:
                retorno=self.link
                pygame.mixer.music.unpause()
        return retorno

config_pause=estruturaPause()
tela_pause=pyTreeBee.dynamicScreen((800,600),30,(0,0,0),config_pause)
                
class controlesExtras(object):
    def __init__(self,tela, pausavel=True):
        self.tela=tela
        self.frame_skip=1
        self.pausavel=pausavel
        self.primeira_vez=True
    def blitOn(self,screen):
        global frame_atual
        if self.primeira_vez:
            frame_atual=0
            self.primeira_vez=False
        frame_atual+=self.frame_skip
    def keyControls(self,event):
        global tela_pause, config_pause
        retorno=False
        if event.type==KEYUP:
            if event.key==K_ESCAPE:
                self.tela.storedlink=None
                self.tela.running=False
            if self.pausavel and event.key==K_SPACE:
                config_pause.link=self.tela
                retorno=tela_pause
                pygame.mixer.music.pause()
        return retorno

###matriz seletora de tiles
matriz_fase_A=[
    [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, -1],
    [-1, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, -1],
    [-1, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, -1],
    [-1, 9, 9, 9, -1, -1, 9, 9, 9, -1, -1, 9, 9, 9, -1, -1, 9, 9, 9, -1],
    [-1, 9, 9, 9, -1, -1, 9, 9, 9, -1, -1, 9, 9, 9, -1, -1, 9, 9, 9, -1],
    [-1, 9, 9, 9, -1, -1, 9, 9, 9, -1, -1, 9, 9, 9, -1, -1, 9, 9, 9, -1],
    [-1, 9, 9, 9, -1, -1, 9, 9, 9, -1, -1, 9, 9, 9, -1, -1, 9, 9, 9, -1],
    [10, 9, 9, 9, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, 9, 9, 9, 16],
    [10, 9, 9, 9, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, 9, 9, 9, 16],
    [10, 9, 9, 9, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, 9, 9, 9, 16],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    ],
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [4, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7, 4],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1, -1, -1, -1, 3],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1, -1, -1, -1, 3],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1, -1, -1, -1, 3],
        [5, -1, -1, -1, 0, 2, -1, -1, -1, 3, 5, -1, -1, -1, 0, 2, -1, -1, -1, 3],
        [5, -1, -1, -1, 3, 5, -1, -1, -1, 3, 5, -1, -1, -1, 3, 5, -1, -1, -1, 3],
        [5, -1, -1, -1, 3, 5, -1, -1, -1, 3, 5, -1, -1, -1, 3, 5, -1, -1, -1, 3],
        [8, -1, -1, -1, 3, 5, -1, -1, -1, 6, 8, -1, -1, -1, 3, 5, -1, -1, -1, 6],
        [-1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1],
        [-1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1],
        [-1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1],
        [1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1]
        ],
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]
    ]

matriz_fase_5=[
    [
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
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ],
    [
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
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ],
    [
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
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ]
    ]

matriz_fase_4=[
   [
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,15,15,15,15,15,15,15,15,15,15,15,15,15,15,-1,-1,-1],
      [-1,-1,-1, 9, 9, 9, 9, 9, 9,-1,-1, 9, 9, 9, 9, 9, 9,-1,-1,-1],
      [-1,-1,-1, 9, 9,-1,-1,-1, 9,-1,-1, 9,-1,-1,-1, 9, 9,-1,-1,-1],
      [-1,-1, 9, 9, 9,-1,-1,-1, 9, 9, 9, 9,-1,-1,-1, 9, 9, 9,-1,-1],
      [-1,-1, 9, 9, 9,-1,-1,-1, 9,-1,-1, 9,-1,-1,-1, 9, 9, 9,-1,-1], 
      [-1,-1, 9, 9, 9,-1,-1,-1, 9,-1,-1, 9,-1,-1,-1, 9, 9, 9,-1,-1],
      [-1,-1, 9, 9, 9,-1,-1,-1, 9, 9, 9, 9,-1,-1,-1, 9, 9, 9,-1,-1],
      [-1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,-1],
      [-1, 9,-1,-1, 9, 9,-1,-1, 9, 9, 9, 9,-1,-1, 9, 9,-1,-1, 9,-1],
      [-1, 9,-1,-1, 9, 9,-1,-1, 9, 9, 9, 9,-1,-1, 9, 9,-1,-1, 9,-1],
      [-1, 9,-1,-1, 9, 9,-1,-1, 9, 9, 9, 9,-1,-1, 9, 9,-1,-1, 9,-1],
      [-1,13,-1,-1,13,13,-1,-1,13,13,13,13,-1,-1,13,13,-1,-1,13,-1]
   ],
   [
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [ 4, 4, 5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 3, 4, 4],
      [ 4, 4, 5,-1,-1,-1,-1,-1,-1, 0, 2,-1,-1,-1,-1,-1,-1, 3, 4, 4],
      [ 4, 4, 5,-1,-1, 0, 1, 2,-1, 6, 8,-1, 0, 1, 2,-1,-1, 3, 4, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1,-1,-1,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1, 0, 2,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1, 6, 8,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 5,-1,-1,-1, 6, 7, 8,-1,-1,-1,-1, 6, 7, 8,-1,-1,-1, 3, 4],
      [ 5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 3],
      [ 5,-1, 0, 2,-1,-1, 0, 2,-1,-1,-1,-1, 0, 2,-1,-1, 0, 2,-1, 3],
      [ 5,-1, 3, 5,-1,-1, 3, 5,-1,-1,-1,-1, 3, 5,-1,-1, 3, 5,-1, 3],
      [ 5,-1, 3, 5,-1,-1, 3, 5,-1,-1,-1,-1, 3, 5,-1,-1, 3, 5,-1, 3],
      [ 5,-1, 6, 8,-1,-1, 6, 8,-1,-1,-1,-1, 6, 8,-1,-1, 6, 8,-1, 3]
   ],
   [
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
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
   ]
]   
matriz_fase_3=[ 
 [  
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],   
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  
  [-1, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, -1],  
  [-1, 9, -1, -1, -1, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, -1, -1, -1, 9, -1],  
  [-1, 9, -1, -1, -1, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, -1, -1, -1, 9, -1], 
  [-1, 9, -1, -1, -1, 9, 9, 9, 9, -1, -1, 9, 9, 9, 9, -1, -1, -1, 9, -1],
  [-1, 9, -1, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1, 9, -1], 
  [-1, 9, -1, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1, 9, -1], 
  [-1, 9, -1, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1, 9, -1], 
  [-1, 9, -1, -1, -1, 9, 9, -1, -1, 15, 15, -1, -1, 9, 9, -1, -1, -1, 9, -1], 
  [-1, 9, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, -1, -1, 9, -1],  
  [10, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 12],  
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
  ],
 [   
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  
  [4, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7, 4],  
  [5, -1, -1, -1, -1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1, -1, -1, -1, 3],  
  [5, -1, 0, 1, 1, 1, 1, 2, -1, 3, 5, -1, 0, 1, 1, 1, 1, 2, -1, 3],   
  [5, -1, 3, 4, 4, 7, 7, 8, -1, 3, 5, -1, 6, 7, 7, 4, 4, 5, -1, 3],  
  [5, -1, 3, 4, 5, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1, 3, 4, 5, -1, 3],  
  [5, -1, 3, 4, 5, -1, 0, 1, 1, 4, 4, 1, 1, 2, -1, 3, 4, 5, -1, 3], 
  [5, -1, 3, 4, 5, -1, 3, 4, 4, 4, 4, 4, 4, 5, -1, 3, 4, 5, -1, 3],  
  [5, -1, 3, 4, 5, -1, 6, 4, 4, 4, 4, 4, 4, 8, -1, 3, 4, 5, -1, 3], 
  [5, -1, 3, 4, 5, -1, -1, 6, 8, -1, -1, 6, 8, -1, -1, 3, 4, 5, -1, 3], 
  [8, -1, 3, 4, 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, 0, 4, 4, 5, -1, 6], 
  [-1, -1, 3, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 5, -1, -1],   
  [1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1]
  ],  
 [   
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  
  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
  ]
 ]   


matriz_fase_2=[
   [   
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [10, 9, 9, 9, 9, 9, 9, 9, 9,-1,-1, 9, 9, 9, 9, 9, 9, 9, 9,16],
      [10, 9, 9, 9, 9, 9, 9, 9, 9,-1,-1, 9, 9, 9, 9, 9, 9, 9, 9,16],
      [-1,-1,-1,-1,-1,-1,-1, 9, 9,-1,-1, 9, 9,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1, 9, 9,-1,-1, 9, 9,-1,-1,-1,-1,-1,-1,-1],
      [-1, 9, 9, 9, 9, 9, 9, 9, 9,-1,-1, 9, 9, 9, 9, 9, 9, 9, 9,-1],
      [-1, 9, 9, 9, 9, 9, 9, 9, 9,-1,-1, 9, 9, 9, 9, 9, 9, 9, 9,-1],
      [-1, 9, 9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 9, 9,-1],
      [-1, 9, 9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 9, 9,-1],
      [-1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,-1],
      [-1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
   ],
   [  
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [ 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1, 3, 5,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1, 3, 5,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [ 1, 1, 1, 1, 1, 1, 2,-1,-1, 3, 5,-1,-1, 0, 1, 1, 1, 1, 1, 1],
      [ 4, 7, 7, 7, 7, 7, 8,-1,-1, 3, 5,-1,-1, 6, 7, 7, 7, 7, 7, 4],
      [ 5,-1,-1,-1,-1,-1,-1,-1,-1, 3, 5,-1,-1,-1,-1,-1,-1,-1,-1, 3],
      [ 5,-1,-1,-1,-1,-1,-1,-1,-1, 3, 5,-1,-1,-1,-1,-1,-1,-1,-1, 3],
      [ 5,-1,-1, 0, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 2,-1,-1, 3],
      [ 5,-1,-1, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8,-1,-1, 3],
      [ 5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 3],
      [ 5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 3],
      [ 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4]   
   ],
   [
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
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
   ]
]

matriz_fase_1=[
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
        [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
        [12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14],
        [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
        [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
        [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
        [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
        [17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
        [17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17]
        ],
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ],
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]
    ]

#tela gameover e player
player=statusPlayer(30,70)
mouse=quadradoControlavel(player)
game_over=pyTreeBee.dynamicScreen((800,600), 30,(100,0,0))
game_over.setImage(pygame.image.load('gameover.png'),(0,0))
#game_over.setMusic()
winner_scr=pyTreeBee.dynamicScreen((800,600), 30,(100,100,255))
winner_scr.setImage(pygame.image.load('vitoria.png'),(0,0))
#loading dos tiles
def tileList(tile_set,size):
    tile_list=[]
    for h in range(tile_set.get_height()//40):
        for w in range(tile_set.get_width()//40):
            tile_list.append(tile_set.subsurface((w*40,h*40),(40,40)))
    return tile_list
tile_list_0=tileList(pygame.image.load("tileset0.png").convert(),40)
tile_list_1=tileList(pygame.image.load("tileset1.png").convert(),40)
tile_list_2=tileList(pygame.image.load("tileset2.png").convert(),40)
tile_list_3=tileList(pygame.image.load("tileset3.png").convert(),40)
#Botões e Seqüênciamentos das Fases
#A
mapa_fase_A = mapaLimitavel(mouse,player,matriz_fase_A, tile_list_1,40)
fase_A = pyTreeBee.dynamicScreen((800,600), 60,(78,133,154),mapa_fase_A)
botao_A=pyTreeBee.linkedButton(linkedMusic(fase_A,"Future Gladiator.mp3",-1, 0.0),din_12,[""],40,500,pygame.Rect(0,0,36,40),0,44,tile_list_1[4])
botao_A.setEach_Text([""],["PÂNCREAS DELGADO"],[""])
botao_A.setEach_BarSize((-2,-3),(-2,-5),(-2,-7))
botao_A=lockedButton(botao_A,'6')
#5
mapa_fase_5 = mapaLimitavel(mouse,player,matriz_fase_5, tile_list_3,40)
fase_5 = pyTreeBee.dynamicScreen((800,600), 60,(78,133,154),mapa_fase_5)
botao_5=pyTreeBee.linkedButton(None,din_12,[""],428,301,pygame.Rect(0,0,324,260),0,0,pygame.image.load("stage5.png").convert())
botao_5.setAll_BarSize((0,0))
botao_5=lockedButton(botao_5,'5')
#4
mapa_fase_4 = mapaLimitavel(mouse,player,matriz_fase_4, tile_list_3,40,botao_5)
fase_4 = pyTreeBee.dynamicScreen((800,600),60,(78,133,154),mapa_fase_4)
botao_4=pyTreeBee.linkedButton(linkedMusic(fase_4,"Future Gladiator.mp3",-1, 0.0),din_12,[""],158,206,pygame.Rect(0,0,260,166),0,0,pygame.image.load("stage4.png").convert())
botao_4.setAll_BarSize((0,0))
botao_4=lockedButton(botao_4,'4')
#3
mapa_fase_3 = mapaLimitavel(mouse,player,matriz_fase_3, tile_list_2,40,botao_4)
fase_3 = pyTreeBee.dynamicScreen((800,600), 60,(78,133,154),mapa_fase_3)
botao_3=pyTreeBee.linkedButton(linkedMusic(fase_3,"Heroic Age.mp3",-1, 0.0),din_12,[""],533,113,pygame.Rect(0,0,230,144),0,0,pygame.image.load("stage3.png").convert())
botao_3.setAll_BarSize((0,0))
botao_3=lockedButton(botao_3,'3')
#2
mapa_fase_2 = mapaLimitavel(mouse,player,matriz_fase_2, tile_list_1,40,botao_3,botao_A)
fase_2 = pyTreeBee.dynamicScreen((800,600), 60,(78,133,154),mapa_fase_2)
botao_2=pyTreeBee.linkedButton(linkedMusic(fase_2,"Volatile Reaction.mp3",-1, 0.0),din_12,[""],323,50,pygame.Rect(0,0,202,120),0,0,pygame.image.load("stage2.png").convert())
botao_2.setAll_BarSize((0,0))
botao_2=lockedButton(botao_2,'2')
#1
mapa_fase_1 = mapaLimitavel(mouse,player,matriz_fase_1, tile_list_0,40,botao_2)
fase_1 = pyTreeBee.dynamicScreen((800,600), 60,(78,133,154),mapa_fase_1)
botao_1=pyTreeBee.linkedButton(linkedMusic(fase_1,"Heroic Age.mp3",-1, 0.0),din_12,[""],24,43,pygame.Rect(0,0,284,72),0,0,pygame.image.load("stage1.png").convert())
botao_1.setAll_BarSize((0,0))

#spawn gerador de hordaS
enemy1=pygame.image.load("inimigo01sheet2.png")
enemy2=pygame.image.load("inimigo02sheet.png")
enemy3=pygame.image.load("inimigo03sheet.png")
enemy4=pygame.image.load("inimigo04sheet.png")
enemy5=pygame.image.load("inimigo05sheet.png")
enemy6=pygame.image.load("inimigo06sheet.png")
enemy7=pygame.image.load("inimigo07sheet.png")
enemy8=pygame.image.load("inimigo08sheet.png")
enemy9=pygame.image.load("inimigo09sheet.png")
'''
for n in range(8):
    exec 'enemy'+str(n+2)+'=pygame.image.load("inimigo0'+str(n+2)+'sheet.png")'
'''
enemy10=pygame.image.load("inimigo10sheet.png")
mov_A_A=[(1,0),(1,0),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),
           (0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
           (0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),
           (1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0),(1,0),(1,0)]
mov_A_B=[(1,0),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),(1,0),(1,0),
           (0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0),(1,0),(1,0),(1,0),
           (0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),
           (1,0),(1,0),(1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0)]
mov_A_C=[(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
          (0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0),(1,0),
          (0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),
          (1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0)]
mov_4_A_1=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(1, 12)
mov_4_A_2=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(1, 12)
mov_4_B_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1)] #(4, 12)
mov_4_B_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1)] #(4, 12) 
mov_4_C=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(5, 12)
mov_4_D_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1)] #(8, 12)
mov_4_D_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1)] #(8, 12)
mov_4_E=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(9, 12)
mov_4_F=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(10, 12)
mov_4_G_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(11, 12)   
mov_4_G_2=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(11, 12)
mov_4_H=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(14, 12)
mov_4_I_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(15, 12)
mov_4_I_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1)] #(15, 12)
mov_4_J_1=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(18, 12)
mov_4_J_2=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1)] #(18, 12)

mov_3_A=[(1, 0), (0, -1), (0, -1), (0, -1), (0, -1),
         (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0),
         (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1),
         (0, 1), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1),
         (1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1)]#(0,11)
mov_3_B=[(-1, 0), (0, -1), (0, -1), (0, -1), (0, -1),
         (0, -1), (0, -1), (0, -1), (0, -1), (0, -1),
         (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0),
         (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1),
         (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1),
         (0, 1), (-1, 0), (0, 1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1)]#(19,11)

mov_2_A=[(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,1),(0,1),(0,1),(0,1),(0,1),
        (1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
        (0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)]
mov_2_B=[(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(0,1),(0,1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,1),(0,1),(0,1),
        (1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
        (0,-1),(0,-1),(0,-1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)]
mov_1_A=[(1, 0), (0, -1), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0), (0, -1), (1, 0), (1, 0),
         (1, 0), (0, -1), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0), (0, -1), (1, 0), (1, 0)]#(0,6)
mov_1_B=[(1, 0), (0, 1), (1, 0), (1, 0), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0),
         (1, 0), (0, 1), (1, 0), (1, 0), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0)]
#botoes de personagens
viking_image=pygame.image.load("vikingchifre_spritesheet.png")
arqueiro_image=pygame.image.load("archer_spritesheet.png")
berserker_image=pygame.image.load("berserker_spritesheet.png")
valquiria_image=pygame.image.load("valkyrie_spritesheet.png")
#diferenciadores: listas de vantagens e desvantagens
#                         nl, rx,  vm,  az,  vr
viking_diferenciador=    [1,0.5,2,1,0.8] #azul
arqueiro_diferenciador=  [1,2,0.5,0.8,1] #verde
berserker_diferenciador= [1,0.8,1,2,0.5] #vermelho
valquiria_diferenciador= [1,1,0.8,0.5,2] #roxo
#mouse,sprite,size,nextsprite,rewind,atk,vel,rng,fly,types
viking_lvl_1=charSelected(mapa_fase_1.selecao,viking_image,(60,50),6,False,25,22,2,False,viking_diferenciador,35)
arqueiro_lvl_1=charSelected(mapa_fase_1.selecao,arqueiro_image,(50,50),5,False,35,30,3,True,arqueiro_diferenciador,50)
berserker_lvl_1=charSelected(mapa_fase_1.selecao,berserker_image,(70,70),5,False,15,5,1,False,berserker_diferenciador,50)
valquiria_lvl_1=charSelected(mapa_fase_1.selecao,valquiria_image,(80,80),4,False,25,12,2,True,valquiria_diferenciador,75)

cor_mana=(0,0,0)#(50,255,50)
cor_fundo=(78,133,154)
botao_viking = pyTreeBee.linkedButton(viking_lvl_1,dinB_12,["    35"],25,535,pygame.Rect(0,0,60,60),0,-15,pygame.image.load("viking.png"))
#texto_viking = pyTreeBee.linkedButton(None,arial,["   Viking"],30,582,pygame.Rect(0,0,0,0),0,0)
botao_viking.setAll_BarColor(cor_fundo)
botao_viking.setAll_TextColor(cor_mana)
botao_arqueiro = pyTreeBee.linkedButton(arqueiro_lvl_1,dinB_12,["    50"],100,535,pygame.Rect(0,0,60,60),0,-15,pygame.image.load("arqueira.png"))
#texto_arqueiro = pyTreeBee.linkedButton(None,arial,[" Arqueiro"],105,582,pygame.Rect(0,0,0,0),0,0)
botao_arqueiro.setAll_BarColor(cor_fundo)
botao_arqueiro.setAll_TextColor(cor_mana)
botao_berserker = pyTreeBee.linkedButton(berserker_lvl_1,dinB_12,["    50"],175,535,pygame.Rect(0,0,60,60),0,-15,pygame.image.load("berserker.png"))
#texto_berserker = pyTreeBee.linkedButton(None,arial,["Berserker"],180,582,pygame.Rect(0,0,0,0),0,0)
botao_berserker.setAll_BarColor(cor_fundo)
botao_berserker.setAll_TextColor(cor_mana)
botao_valquiria = pyTreeBee.linkedButton(valquiria_lvl_1,dinB_12,["    75"],250,535,pygame.Rect(0,0,60,60),0,-15,pygame.image.load("valkyrie.png"))
#texto_valquiria = pyTreeBee.linkedButton(None,arial,["Valquíria"],255,582,pygame.Rect(0,0,0,0),0,0)
botao_valquiria.setAll_BarColor(cor_fundo)
botao_valquiria.setAll_TextColor(cor_mana)
### botoes aceleradores ###
accelx1=pyTreeBee.linkedButton(accelGame(60),din_12,[""],500+150,550,pygame.Rect(0,0,30,30),0,0,pygame.image.load('botao_x1.png'))
accelx1.setAll_BarSize((-10,-10))

accelx2=pyTreeBee.linkedButton(accelGame(90),din_12,[""],550+150,550,pygame.Rect(0,0,30,30),0,0,pygame.image.load('botao_x2.png'))
accelx2.setAll_BarSize((-10,-10))

accelx3=pyTreeBee.linkedButton(accelGame(120),din_12,[""],600+150,550,pygame.Rect(0,0,30,30),0,0,pygame.image.load('botao_x3.png'))
accelx3.setAll_BarSize((-10,-10))

game_over_music=("Steel and Seething.mp3",1,0.0)
###>>>FASES<<<###
###fase A (extra)###

mapa_fase_A.addSpawn( (0,9) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (1,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,1] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[5,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])
mapa_fase_A.addSpawn( (0,10) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (1,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,1] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[5,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])
mapa_fase_A.addSpawn( (0,11) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (1,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,1] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[5,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])
mapa_fase_A.addTarget(player,(19,9),(-1,0))
mapa_fase_A.addTarget(player,(19,10),(-1,0))
mapa_fase_A.addTarget(player,(19,11),(-1,0))

fase_A.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,accelx1,accelx2,accelx3)
fase_A.addItem(controlesExtras(fase_2))
fase_A.addItem(gameOver(fase_2,game_over,mapa_fase_2,game_over_music))
fase_A.addItem(winnerScreen(fase_2,winner_scr,mapa_fase_2))#332=quantidade de inimigos

###fase 4###
#pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,mana,quantidades):
#mov_4_A_1= andar pela borda,mov_4_A_2=descola da borda
mapa_fase_4.addSpawn((1, 12),[120,120,120,120,120,120,120,120,120,120] , [5000,(8*pow(10,13))-(8*pow(10,3)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_A_1,mov_4_A_2,mov_4_A_1,mov_4_A_2,mov_4_A_1,mov_4_A_2,mov_4_A_1,mov_4_A_2,mov_4_A_1,mov_4_A_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_B_1,mov_4_B_2
mapa_fase_4.addSpawn((4, 12),[120,120,120,120,120,120,120,120,120,120] , [15000,(8*pow(10,14))-(8*pow(10,5)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_B_1,mov_4_B_2,mov_4_B_1,mov_4_B_2,mov_4_B_1,mov_4_B_2,mov_4_B_1,mov_4_B_2,mov_4_B_1,mov_4_B_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_C
mapa_fase_4.addSpawn((5, 12),[120,120,120,120,120,120,120,120,120,120] , [1000,(8*pow(10,15))-(8*pow(10,7)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_D_1,mov_4_D_2
mapa_fase_4.addSpawn((8, 12),[120,120,120,120,120,120,120,120,120,120] , [11000,(8*pow(10,13))-(8*pow(10,9)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_D_1,mov_4_D_2,mov_4_D_1,mov_4_D_2,mov_4_D_1,mov_4_D_2,mov_4_D_1,mov_4_D_2,mov_4_D_1,mov_4_D_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_E
mapa_fase_4.addSpawn((9, 12),[120,120,120,120,120,120,120,120,120,120] , [7000,(8*pow(10,14))-(8*pow(10,2)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_F
mapa_fase_4.addSpawn((10, 12),[120,120,120,120,120,120,120,120,120,120] , [17000,(8*pow(10,15))-(8*pow(10,4)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_G_1,mov_4_G_2
mapa_fase_4.addSpawn((11, 12),[120,120,120,120,120,120,120,120,120,120] , [3000,(8*pow(10,16))-(8*pow(10,6)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_G_1,mov_4_G_2,mov_4_G_1,mov_4_G_2,mov_4_G_1,mov_4_G_2,mov_4_G_1,mov_4_G_2,mov_4_G_1,mov_4_G_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_H
mapa_fase_4.addSpawn((14, 12),[120,120,120,120,120,120,120,120,120,120] , [13000,(8*pow(10,15))-(8*pow(10,8)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_I_1,mov_4_I_2
mapa_fase_4.addSpawn((15, 12),[120,120,120,120,120,120,120,120,120,120] , [9000,(8*pow(10,14))-(8*pow(10,10)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_I_1,mov_4_I_2,mov_4_I_1,mov_4_I_2,mov_4_I_1,mov_4_I_2,mov_4_I_1,mov_4_I_2,mov_4_I_1,mov_4_I_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])
#mov_4_J_1 = andar pela borda,mov_4_J_2=descola da borda
mapa_fase_4.addSpawn((18, 12),[120,120,120,120,120,120,120,120,120,120] , [19000,(8*pow(10,16))-(8*pow(10,12)),800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_4_J_1,mov_4_J_2,mov_4_J_1,mov_4_J_2,mov_4_J_1,mov_4_J_2,mov_4_J_1,mov_4_J_2,mov_4_J_1,mov_4_J_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,20,15,10,20,15,30,15,20,1])

for x in range(3,17,1):
    mapa_fase_4.addTarget(player,(x,1),(0,0))

fase_4.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,accelx1,accelx2,accelx3)
fase_4.addItem(controlesExtras(fase_4))
fase_4.addItem(gameOver(fase_4,game_over,mapa_fase_4,game_over_music))
fase_4.addItem(winnerScreen(fase_4,winner_scr,mapa_fase_4))

###fase 3###
mapa_fase_3.addSpawn( (0,11), [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,1] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])
mapa_fase_3.addSpawn( (19,11), [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,1] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])
mapa_fase_3.addTarget(player,(9,9),(0,0))
mapa_fase_3.addTarget(player,(10,9),(0,0))
mapa_fase_3.mapa[1][7][9].addPiece(animacaoPerene(animacaoSprite(pygame.image.load('fontedavida.png'),(160,160),6,False,(40*8,40*5))))
mapa_fase_3.mapa[1][6][9].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][5][9].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][8][9].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][6][8].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][7][8].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][5][10].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][6][10].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][7][10].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][8][10].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][6][11].addPiece(bloqueioPerene())
mapa_fase_3.mapa[1][7][11].addPiece(bloqueioPerene())

fase_3.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,accelx1,accelx2,accelx3)
fase_3.addItem(controlesExtras(fase_3))
fase_3.addItem(gameOver(fase_3,game_over,mapa_fase_3,game_over_music))
fase_3.addItem(winnerScreen(fase_3,winner_scr,mapa_fase_3))#332=quantidade de inimigos
#fase_3.addItem(animacaoSprite(pygame.image.load('fontedavida.png'),(160,160),6,False,(40*8,40*5)))

###fase 2###
mapa_fase_2.addSpawn( (0,3) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])#[1,1,1,1,1,1,1,1,1,1]
mapa_fase_2.addSpawn( (0,2) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])#[0,0,0,0,0,0,0,0,0,0]
mapa_fase_2.addTarget(player,(19,3),(0,0))
mapa_fase_2.addTarget(player,(19,2),(0,0))
fase_2.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,accelx1,accelx2,accelx3)#,texto_viking,texto_arqueiro,texto_berserker,texto_valquiria
fase_2.addItem(controlesExtras(fase_2))
fase_2.addItem(gameOver(fase_2,game_over,mapa_fase_2,game_over_music))
fase_2.addItem(winnerScreen(fase_2,winner_scr,mapa_fase_2))#332=quantidade de inimigos

###fase 1###
mapa_fase_1.addSpawn( (0,6), [120,120,120,120] , [800,800,800,800], (0,0), [enemy3,enemy4,enemy6,enemy8],[(25,25),(22,22),(25,25),(22,22)],[8,8,8,8,8,8,8,8,8,8],[True,False,True,False],[1,1,1,1],[0.5,0.5,0.5,0.5],[100,100,100,100],[False,True,False,True],[0,0,0,0],[mov_1_A,mov_1_B,mov_1_A,mov_1_B],[(1,0),(1,0),(1,0),(1,0)],[50,50,75,75],[1,1,1,1])
mapa_fase_1.addTarget(player,(19,6),(0,0))
fase_1.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,accelx1,accelx2,accelx3)#,texto_viking,texto_arqueiro,texto_berserker,texto_valquiria

fase_1.addItem(controlesExtras(fase_1))
fase_1.addItem(gameOver(fase_1,game_over,mapa_fase_1,game_over_music))
fase_1.addItem(winnerScreen(fase_1,winner_scr,mapa_fase_1))#332=quantidade de inimigos

###>>>TELAS<<<###

###seleção de fases###

selecao_fase = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_1,botao_2,botao_3,botao_4,botao_5,botao_A)
selecao_fase.setImage(pygame.image.load("stageselect.png").convert(),(0,0))
selecao_fase.setMusic("Teller of the Tales.mp3",-1, 0.0)
###tela options###
texto_confirmacao=pyTreeBee.linkedButton(None,dinB_22,["      TENS CERTEZA DE QUE É SÁBIO", "APAGAR TODO O VOSSO PROGRESSO?"],210,220,pygame.Rect(0,0,0,0),0,0)
texto_confirmacao.setAll_TextColor((255,255,255))
tela_confirma_exclusao=pyTreeBee.dynamicScreen((800,600),60,(0,0,0),texto_confirmacao)
botao_apagar=pyTreeBee.linkedButton(tela_confirma_exclusao,din_12,[""],400-(280/2)+12,350,pygame.Rect(0,0,280-12,60-12),0,0)
botao_apagar.setEach_Image(pygame.image.load('botao_apagar1.png'),pygame.image.load('botao_apagar2.png'),pygame.image.load('botao_apagar3.png'))
botao_apagar.setAll_BarSize((-6,-6))

texto_volume=escritorDireto(dinBd_32.render("VOLUME",True,(255,255,255)),(342,105))
escreve_volume=renderVolume(dinB_22,(255,255,255),(384,115+62),100)
aumenta_volume=pyTreeBee.linkedButton(volumeControl(+0.02),dinB_22,[""],500-26,162,pygame.Rect(0,0,60,60),15,5,pygame.image.load("botao_mais.png"))
diminui_volume=pyTreeBee.linkedButton(volumeControl(-0.02),dinB_22,[""],300-26,162,pygame.Rect(0,0,60,60),15,5,pygame.image.load("botao_menos.png"))

tela_options=pyTreeBee.dynamicScreen((800,600),60,(0,0,0),botao_apagar,texto_volume,escreve_volume,aumenta_volume,diminui_volume)
tela_pause.addItem(texto_volume,escreve_volume,aumenta_volume,diminui_volume)

confirma_sim=pyTreeBee.linkedButton(deleteSave(tela_options),din_12,[""],250,300,pygame.Rect(0,0,130-12,60-12),0,0)
confirma_sim.setEach_Image(pygame.image.load('botao_sim1.png'),pygame.image.load('botao_sim2.png'),pygame.image.load('botao_sim3.png'))
confirma_sim.setAll_BarSize((-6,-6))
confirma_nao=pyTreeBee.linkedButton(tela_options,din_12,[""],420,300,pygame.Rect(0,0,130-12,60-12),0,0)
confirma_nao.setEach_Image(pygame.image.load('botao_nao1.png'),pygame.image.load('botao_nao2.png'),pygame.image.load('botao_nao3.png'))
confirma_nao.setAll_BarSize((-6,-6))
tela_confirma_exclusao.addItem(confirma_sim,confirma_nao)
###tela staff###
tela_staff=pyTreeBee.dynamicScreen((800,600),60,(0,0,0))
tela_staff.setImage(pygame.image.load("credits.png").convert(),(0,0))
###tela tutorial###
tela_tutorial=pyTreeBee.dynamicScreen((800,600),60,(0,0,0))
tela_tutorial.setImage(pygame.image.load("tutorial.png").convert(),(0,0))
###tela inicial###
#> letreiro

#> viking
#pescoco=pyTreeBee.linkedButton(None,din_12,[""],0,438,pygame.Rect(0,0,0,0),0,0, pygame.transform.scale(pygame.image.load("pescoco 2.png"),(437,162)))
#cabeca=pyTreeBee.linkedButton(None,arial,[""],0,63,pygame.Rect(0,0,0,0),0,0,  pygame.transform.scale(pygame.image.load("cabeca 4.png"),(357,523)))
#olho=animacaoSprite(pygame.transform.scale(pygame.image.load("olho_spritesheet 2.png"),(760,75)),(190,75),6,True,(90,290))
#olho.setPause(60)
#espada=animacaoSprite(pygame.transform.scale(pygame.image.load("espada_spritesheet.png"),(4800,600)),(800,600),10,True,(0,0))
#espada.setStop(1)

identa_botoes_x=0
identa_botoes_y=-100

#> start
botao_start=pyTreeBee.linkedButton(selecao_fase,din_12,[""],800+identa_botoes_x,300+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_start.setEach_Image(pygame.image.load("start1.png"),pygame.image.load("start2.png"),pygame.image.load("start3.png"))
botao_start.setAll_BarSize((-10,-10))
#> options
botao_options=pyTreeBee.linkedButton(tela_options,din_12,[""],800+identa_botoes_x,380+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_options.setEach_Image(pygame.image.load("options1.png"),pygame.image.load("options2.png"),pygame.image.load("options3.png"))
botao_options.setAll_BarSize((-10,-10))
#> tutorial
botao_tutorial=pyTreeBee.linkedButton(tela_tutorial,din_12,[''],800+identa_botoes_x,460+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_tutorial.setEach_Image(pygame.image.load("tutorial1.png"),pygame.image.load("tutorial2.png"),pygame.image.load("tutorial3.png"))
botao_tutorial.setAll_BarSize((-10,-10))
#> staff
botao_staff=pyTreeBee.linkedButton(tela_staff,din_12,[""],800+identa_botoes_x,540+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_staff.setEach_Image(pygame.image.load("staff1.png"),pygame.image.load("staff2.png"),pygame.image.load("staff3.png"))
botao_staff.setAll_BarSize((-10,-10))
#> tela
tela_inicial = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_start,botao_options,botao_staff,botao_tutorial)#,pescoco,cabeca,olho,espada
tela_inicial.setImage(pygame.image.load("Abertura Nova.png").convert(),(0,0))
tela_inicial.addItem(controlesExtras(tela_inicial,False))
fadeIn(tela_inicial,tela_inicial,[botao_start,(500+identa_botoes_x,300+identa_botoes_y),10],[botao_options,(500+identa_botoes_x,380+identa_botoes_y),15],[botao_tutorial,(500+identa_botoes_x,460+identa_botoes_y),20],[botao_staff,(500+identa_botoes_x,540+identa_botoes_y),25])#[pescoco,(500,500),40],[cabeca,(0,0),40],[espada,(0,600),100]
#botao_start.link=fadeOut(tela_inicial,selecao_fase,[botao_start,(800+identa_botoes_x,300+identa_botoes_y),10],[botao_options,(800+identa_botoes_x,380+identa_botoes_y),15],[botao_tutorial,(800+identa_botoes_x,460+identa_botoes_y),20],[botao_staff,(800+identa_botoes_x,540+identa_botoes_y),25])
###botões de voltar adicionados às telas anteriores###
img_voltar_1=pygame.image.load("botao_voltar1.png")
img_voltar_2=pygame.image.load("botao_voltar2.png")
img_voltar_3=pygame.image.load("botao_voltar3.png")

cir_voltar_1=pygame.image.load("botao_menu1.png")
cir_voltar_2=pygame.image.load("botao_menu2.png")
cir_voltar_3=pygame.image.load("botao_menu3.png")

cir_fases_1=pygame.image.load("botao_avancar1.png")
cir_fases_2=pygame.image.load("botao_avancar2.png")
cir_fases_3=pygame.image.load("botao_avancar3.png")

cir_retry_1=pygame.image.load("botao_retry1.png")
cir_retry_2=pygame.image.load("botao_retry2.png")
cir_retry_3=pygame.image.load("botao_retry3.png")

voltar_para_inicio=pyTreeBee.linkedButton(tela_inicial,din_12,[""],655,530,pygame.Rect(0,0,130-12,60-12),0,0)
voltar_para_inicio.setEach_Image(img_voltar_1,img_voltar_2,img_voltar_3)
voltar_para_inicio.setAll_BarSize((-6,-6))
tela_options.addItem(voltar_para_inicio)
tela_staff.addItem(voltar_para_inicio)
tela_tutorial.addItem(voltar_para_inicio)
voltar_para_inicio_musica=pyTreeBee.linkedButton(linkedMusic(tela_inicial,"Five Armies.mp3", -1, 0.0),din_12,[""],655,530,pygame.Rect(0,0,130-12,60-12),0,0)
voltar_para_inicio_musica.setEach_Image(img_voltar_1,img_voltar_2,img_voltar_3)
voltar_para_inicio_musica.setAll_BarSize((-6,-6))
selecao_fase.addItem(voltar_para_inicio_musica)

voltar_retry=pyTreeBee.linkedButton(None,din_12,[""],220,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_retry.setEach_Image(cir_retry_1,cir_retry_2,cir_retry_3)
voltar_retry.setAll_BarSize((-12,-12))
voltar_menu=pyTreeBee.linkedButton(linkedMusic(tela_inicial,"Five Armies.mp3", -1, 0.0),din_12,[""],375,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_menu.setEach_Image(cir_voltar_1,cir_voltar_2,cir_voltar_3)
voltar_menu.setAll_BarSize((-12,-12))
voltar_selecao=pyTreeBee.linkedButton(selecao_fase,din_12,[""],530,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_selecao.setEach_Image(cir_fases_1,cir_fases_2,cir_fases_3)
voltar_selecao.setAll_BarSize((-12,-12))
game_over.addItem(voltar_menu,voltar_selecao,voltar_retry)
winner_scr.addItem(voltar_menu,voltar_selecao,voltar_retry)
'''
voltar_selecao.link=fadeOut(tela_inicial,tela_inicial,[botao_start,(500,300),10],[botao_options,(500,380),15],[botao_staff,(500,460),20])
selecao_fase.addItem(voltar_selecao)
'''
#fase_1.addItem(pyTreeBee.linkedButton(selecao_fase,din_12,["Voltar"],600,530,pygame.Rect(0,0,50,20),0,0))
### loading save ###

load_fases_liberadas=[botao_2,botao_3,botao_4,botao_5,botao_A]

def saveAll(save=True):
    global load_fases_liberadas    
    for liberada in load_fases_liberadas:
        if save: liberada.stateDump()
        else: liberada.stateLoad();

try:
    saveAll(False)
    
except:
    pass
###início dos ciclos###
time.sleep(0.25)
pyTreeBee.treeBeeStart(tela_inicial)

loading=dinB_22.render("SAVING...",True,(255,255,255))
temporarydisplay.fill((0,0,0))
temporarydisplay.blit(loading,(370,278))
pygame.display.update()
time.sleep(0.25)
### dumping save ###
saveAll()

pygame.quit()

