# -*- coding: cp1252 -*-
import pyTreeBee,pygame,sys,os,time, pygame.mixer, copy
import cPickle as pickle
from pygame.locals import*

dir_music='Sound\\'
dir_image='Image\\'
dir_fonts='Font\\'

infoObject = pygame.display.Info()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((infoObject.current_w//2)-400, (infoObject.current_h//2)-300)
temporarydisplay=pygame.display.set_mode((800,600))
dinB_22=pygame.font.Font(dir_fonts+"DIN-Black.otf",22)
dinB_72=pygame.font.Font(dir_fonts+"DIN-Black.otf",72)
dinBd_32=pygame.font.Font(dir_fonts+"DIN-Bold.otf",32)

loading=dinB_22.render("LOADING...",True,(255,255,255))
temporarydisplay.blit(loading,(370,278))
pygame.display.update()


high_score=[
    ("ASG",50000),
    ("ARD",45000),
    ("IAN",40000),
    ("GAM",35000),
    ("EWO",30000),
    ("RKS",25000),
    ("ENT",20000),
    ("ERT",15000),
    ("AIN",10000),
    ("MEN",9000),
    ("T  ",8000),
    ("STU",7000),
    ("DIO",6000)
    ]
frame_atual=1
din_12=pygame.font.Font(dir_fonts+"DIN-Medium.otf",12)
dinB_12=pygame.font.Font(dir_fonts+"DIN-Black.otf",12)
pygame.mixer.init()

#musica inicial, precisa dela pros botões de voltar cuidarem disso.
pygame.mixer.music.load(dir_music+"Five Armies.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(5)


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

class deleteSave(object):
    def __init__(self,tela):
        self.tela=tela
    def linkReply(self,prevscr):
        for liberada in load_fases_liberadas:
            liberada.stateClear()
        return self.tela

class unlockerLink(object):
    def __init__(self,link,lock):
        self.link=link
        self.lock=lock
    def linkReply(self,prevscr):
        self.lock.unlocked=True
        self.lock.stateDump()
        return self.link

class congratulouGame(object):
    def __init__(self,vitoria_comum, vitoria_congratulada):
        self.victory=vitoria_comum
        self.congratulations=vitoria_congratulada
        self.unlocked=False
    def blitOn(self,scr):pass
    def keyControls(self,event):
        retorno=False
        if self.unlocked:
            retorno=self.victory
        else:
            retorno=self.congratulations
        return retorno
    def stateLoad(self):
        arq=open('Data\\game data.ages','rb')
        self.unlocked=pickle.load(arq)
        arq.close
    def stateClear(self):
        self.unlocked=False
        self.stateDump()
    def stateDump(self):
        arq=open('Data\\game data.ages','wb')
        pickle.dump(self.unlocked,arq)
        arq.close 
        

class lockedButton(object):
    def __init__(self,linkedButton,id_str):
        self.linkedButton=linkedButton
        self.unlocked=False
        self.id_str=str(id_str)
        self.linkedButton.setAlphaBar([0,0,0])
        self.linkedButton.setAlpha([155,155,155])
    def blitOn(self,scr):
        #if self.unlocked: self.linkedButton.blitOn(scr)
        self.linkedButton.blitOn(scr)
    def keyControls(self,event):
        retorno=False
        if self.unlocked: retorno=self.linkedButton.keyControls(event)
        return retorno
    def unlockButton(self):#na vitoria
        self.unlocked=True
        self.linkedButton.setAlpha([255,255,255])
    def stateLoad(self):#no inicio        
        arq=open('Data\game'+self.id_str+'.ages','rb')
        self.unlocked=pickle.load(arq)
        if self.unlocked: self.linkedButton.setAlpha([255,255,255])
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


class inimigoAlvo(object):#inimigoAlvo(pygame.image.load(dir_image+"inimigo01sheet2.png"),(20,20),10,False,1,1,1,
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
                    if self.y+e>=0 and self.y+e<len(mapa[0]) and self.x+i>=0 and self.x+i<len(mapa[0][0]):
                        try:
                            if mapa[0][self.y+e][self.x+i].piece!=None:
                                if mapa[0][self.y+e][self.x+i].piece.fly==self.fly or self.fly:
                                    if self.sprite.y!=1: self.sprite.setLine(1)
                                    self.aim=mapa[0][self.y+e][self.x+i]
                                    if self.aim.piece.pos[0]>=self.x: self.sprite.invert[0]=True
                                    else: self.sprite.invert[0]=False
                        except:
                            pass
        else:            
            if frame_atual%self.vel==0:
                try:
                    if self.aim.piece.pos[0]>=self.x: self.sprite.invert[0]=True
                    else: self.sprite.invert[0]=False
                    self.aim.piece.hp-=self.atk*self.dmg_types[self.aim.piece.type]
                    if self.aim.piece.hp<=0:
                        self.player.score+=self.aim.piece.hpmax/100
                        self.player.kill_counter+=1
                        self.player.mana+=self.aim.piece.mana
                        self.aim.addPiece(None)
                        self.aim=None
                        if self.sprite.y_sheet!=0: self.sprite.setLine(0)
                        
                except:
                    self.aim=None
                    self.sprite.setLine(0)

class accelGame(object):
    def __init__(self, fps):
        self.fps=fps
    def linkReply(self,prevscr):
        prevscr.fps=self.fps
        return prevscr

class accelKey(object):
    def __init__(self,fps,key):
        self.link=accelGame(fps)
        self.key=key
    def keyControls(self,event):
        retorno=False
        if event.type==KEYUP:
            if event.key==self.key:
                retorno=self.link
        return retorno
    def blitOn(self,scr):pass

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

class charTyped(object):
    def __init__(self,mouse,event_key,sprite,size,nextsprite,rewind,atk,vel,rng,voador,tipo,mana):
        self.mouse=mouse
        self.event_key=event_key
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
    def keyControls(self,event):
        if event.type==KEYUP:
            if event.key==self.event_key:
                self.mouse.setSelection(self.sprite,self.size,self.nextsprite,self.rewind,self.atk,self.vel,self.rng,self.fly,self.dmg_type,self.mana)
        return False
    def blitOn(self,scr): pass

class quadradoControlavel(object):
    def __init__(self):
        self.x=1
        self.y=1
        self.sprite=animacaoSprite(pygame.image.load(dir_image+"selecao4.png").convert_alpha(),(40,40),9,True)
        self.buttonup=False
        self.dentro=True
        self.cor=(0,0,0)
        self.botaodireito=False
        self.botaoesquerdo=False
        self.nullSelection()
        self.size=1
        self.error_sound=pygame.mixer.Sound(dir_music+"error.wav")
        self.drop_sound=pygame.mixer.Sound(dir_music+"heavy-footstep-wood-3.wav")
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
                char_image=self.char_sprite.subsurface(((0,0),self.char_size))
                char_pos=((self.x*self.size)-(self.char_size[0]/2)+(self.size/2),(self.y*self.size)-(self.char_size[1]*3/4)+(self.size/2)-5)
                circle_pos=((self.x*self.size)+(self.size//2)-(self.rng*self.size),(self.y*self.size)+(self.size//2)-(self.rng*self.size))
                
                chromakey=(9,99,9)
                rng_circle=pygame.Surface((self.rng*self.size*2,self.rng*self.size*2))
                rng_circle.fill(chromakey)
                rng_circle.set_colorkey(chromakey)
                pygame.draw.circle(rng_circle, self.cor, (self.rng*self.size, self.rng*self.size), self.rng*40, 2)
                screen.blit(rng_circle,circle_pos)
                pygame.draw.circle(rng_circle, self.cor, (self.rng*self.size, self.rng*self.size), self.rng*40, 0)
                rng_circle.set_alpha(100)
                
                
                screen.blit(rng_circle,circle_pos)
                blit_alpha(screen,char_image, char_pos,200)
            screen.blit(self.sprite.getNextImage(),(self.x*self.size,self.y*self.size))
    def keyControls(self,event,mapa,alingment,player):
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

        if mapa[1][self.y][self.x].numID<=8 and mapa[1][self.y][self.x].numID>=0:
            self.cor=(0,255,0)
        else: self.cor=(255,0,0)
        if self.botaoesquerdo:
            if self.dentro:
                if self.char_sprite!=None:
                    if mapa[1][self.y][self.x].piece==None:
                        if mapa[1][self.y][self.x].numID<=8 and mapa[1][self.y][self.x].numID>=0:
                            if player.mana>=self.mana:
                                self.drop_sound.play()
                                mapa[1][self.y][self.x].addPiece(torreGuerreiro(self.char_sprite,self.char_size,self.nextsprite,self.rewind,self.atk,self.vel,self.rng,self.fly,self.dmg_type, self.x,self.y,self.mana,player))
                                player.mana-=self.mana
                            else:
                                self.error_sound.play()
                            self.nullSelection()
                        else:
                            self.error_sound.play()
                    else:
                        self.error_sound.play()
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
                        self.player.damage_counter+=1
                        around.piece=None
                        
        else:
            point=mapa[0][self.pos[1]+self.sentido[1]][self.pos[0]+self.sentido[0]]
            if point.piece!=None:
                
                self.player.life-=point.piece.atk
                self.player.damage_counter+=1
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
        self.pause=True
    def fightControls(self,mapa):
        global frame_atual
        if self.pause and frame_atual%self.pause_time[self.contador]==0:
            self.pause=False
        if self.contador<len(self.sprite) and self.pause==False:
            if frame_atual%self.spawntime[self.contador]==0:
                if self.quantidade[0]<self.quantidade[1][self.contador]:
                    sc=self.contador
                    inimigo=inimigoAlvo(self.sprite[sc],self.size[sc],self.next[sc], self.rewind[sc], self.atk[sc],self.vel[sc],self.hp[sc],self.fly[sc],self.type[sc], (self.pos[0]+self.spawn[0]), (self.pos[1]+self.spawn[1]), self.movimento[sc], self.sentido[sc][0], self.sentido[sc][1],self.mana[sc])
                    mapa[0][self.pos[1]+self.spawn[1]][self.pos[0]+self.spawn[0]].piece=inimigo
                    self.quantidade[0]+=1
                else:
                    self.contador+=1
                    self.quantidade[0]=0
                    self.pause=True
        else:
            self.pause=True

class tutorialGame(object):
    def __init__(self,mapa,font,text_vector,button_vector):
        self.arrow_img=pygame.image.load(dir_image+'arrow_tuto.png').convert_alpha()
        self.font=font
        self.mapa=mapa
        self.pause=True
        self.text=text_vector
        self.button=button_vector
        self.step=0
    def blitOn(self,display):
        if self.mapa.tutorial_flag:
            self.mapa.tutorial_flag=False
            self.step=0
            self.pause=True
        if self.step<len(self.button):
            if self.mapa.player.mana>0:
                for i in range(len(self.text[self.step])):
                    if self.font.size(self.text[self.step][i])[0]+self.button[self.step].x+self.arrow_img.get_width()>800:
                        pos_x=self.button[self.step].x - self.font.size(self.text[self.step][i])[0]
                    else:
                        pos_x=self.button[self.step].x+self.button[self.step].w#self.arrow_img.get_width()
                    rendertext=self.font.render(self.text[self.step][i],True,(0,0,0))
                    display.blit(rendertext,(pos_x,((self.font.get_height()+1)*i)+self.button[self.step].y-self.arrow_img.get_height()))
                arrow_scaled=pygame.transform.scale(self.arrow_img,(self.button[self.step].w,self.arrow_img.get_height()))
                display.blit(arrow_scaled,(self.button[self.step].x,self.button[self.step].y-self.arrow_img.get_height()))
            if self.pause and self.mapa.player.mana>0: self.mapa.pauseGame(); self.pause=not self.pause
        if not self.pause and self.mapa.player.mana==0: self.mapa.pauseGame(); self.pause=not self.pause
    def keyControls(self,event):
        if self.mapa.player.mana>0 and self.step<len(self.button):
            if event.type==MOUSEBUTTONDOWN:
                if self.button[self.step].collidepoint(event.pos):
                    self.step+=1

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
        self.menu=pygame.image.load(dir_image+"menubot_fundo.png").convert()
        self.pause=False
        self.tutorial_flag=False
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
        frame_atual=1
        for camada in self.mapa:
            for fileira in camada:
                for bloco in fileira:
                    if bloco.piece!=None:
                        bloco.piece.setZero(self.mapa)
        self.pause=False
        self.tutorial_flag=True
        self.player.setZero()
        self.selecao.nullSelection()
    def addSpawn(self,pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,manas,quantidades):
        for qnt in quantidades:
            self.qnt_inimigos+=qnt
        self.mapa[1][pos[1]][pos[0]].piece=spawnInimigo(pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,manas,quantidades)
    def addTarget(self,pos, sentido=None):
        self.mapa[1][pos[1]][pos[0]].piece=lifeTarget(self.player,pos,sentido)
    def blitOn(self,screen):
        if self.selecao.size!=self.size:
            self.selecao.size=self.size
        for z in range(len(self.mapa)):                                
            for y in range(len(self.mapa[z])):
                for x in range(len(self.mapa[z][y])):
                    if self.mapa[z][y][x].piece!=None and self.pause==False:
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
        screen.blit(dinB_22.render(str(int(self.player.score)),True,(255,255,255)),(32,10))
        screen.blit(din_12.render("MANA:",True,(255,255,255)),(680,0))
        screen.blit(dinB_22.render(str(self.player.mana),True,(10,125,255)),(680,10))
        screen.blit(self.menu,(0,520))
        self.selecao.blitOn(screen)
        
    def pauseGame(self):
        self.pause = not self.pause
        pygame.mixer.music.pause() if self.pause else pygame.mixer.music.unpause()
        pygame.mouse.set_visible(self.pause)        
    def keyControls(self,event):
        if event.type==KEYUP:
            if event.key==K_p:
                self.pauseGame()
        self.selecao.keyControls(event,self.mapa, self.alingment,self.player)
        return False

class blitScore(object):
    def __init__(self):
        self.score=0
        self.zero=0
        self.pos=(310,350)
        self.font=pygame.font.Font(dir_fonts+"DIN-Light.otf",32)
        self.cor=(255,255,255)
    def blitOn(self,scr):
        center=400-(self.font.size("SCORE: "+str(int(self.zero)))[0]//2)
        scr.blit(self.font.render("SCORE: "+str(int(self.zero)),True,self.cor),(center,self.pos[1]))
        if self.score!=self.zero:
            if self.zero+1<self.score:
                self.zero+=self.score*0.006
            else:
                self.zero=self.score
    def keyControls(self,event):pass

class winnerScreen(object):
    def __init__(self,tela,link,mapa,score,music=None):
        self.tela=tela
        self.link=link
        self.mapa=mapa
        self.music=music
        self.score=score
    def blitOn(self,scr):
        global voltar_retry,frame_atual
        if self.mapa.player.damage_counter+self.mapa.player.kill_counter>=self.mapa.qnt_inimigos and self.mapa.player.life>0:
            self.tela.fps=60
            if frame_atual%120==0:
                if self.music:
                    pygame.mixer.music.load(self.music[0])
                    pygame.mixer.music.play(self.music[1], self.music[2])
                pygame.mouse.set_visible(True)
                for fase in self.mapa.stage_key:
                    fase.unlockButton()
                saveAll()
                self.score.zero=0
                self.score.score=(((self.mapa.player.score*1.3)+(self.mapa.player.mana*1.159))*0.82)*self.mapa.player.life*0.921
                voltar_retry.link=linkedMusic(self.tela,self.tela.stored_music,-1,0.0)
                self.mapa.setZero(self.tela)
                self.tela.linkcalled=self.link
    def keyControls(self,event):pass

class linkedZero(object):
    def __init__(self, link, music=None):
        self.link=link
        self.music=music
        self.tela=None
        self.mapa=None
    def linkReply(self,scr):
        global voltar_retry_pause, voltar_menu_pause, voltar_selecao_pause
        if self.music:
            pygame.mixer.music.load(self.music[0])
            pygame.mixer.music.play(self.music[1], self.music[2])
        self.mapa.setZero(self.tela)
        return self.link

class gameOver(object):
    def __init__(self,tela,link,mapa,music=None):
        self.tela=tela
        self.link=link
        self.mapa=mapa
        self.music=music
        self.actived=False
    def blitOn(self,scr):
        global voltar_retry, frame_atual
        if self.mapa.player.life<=0 or self.actived:
            self.tela.fps=60
            if self.actived==False:
                frame_atual=0
                self.actived=True
            if frame_atual%90==0:
                if self.music:
                    pygame.mixer.music.load(self.music[0])
                    pygame.mixer.music.play(self.music[1], self.music[2])
                pygame.mouse.set_visible(True)
                voltar_retry.link=linkedMusic(self.tela,self.tela.stored_music,-1,0.0)
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
        self.kill_counter=0
        self.damage_counter=0
    def setZero(self):
        self.life=self.maxlife
        self.mana=self.initialmana
        self.score=0
        self.kill_counter=0
        self.damage_counter=0
        
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
    def blitOn(self,scr):pass
    def keyControls(self,event):
        retorno=False
        if event.type==KEYUP:
            if event.key==K_SPACE:
                retorno=self.link
                pygame.mixer.music.unpause()
        return retorno



config_pause=estruturaPause()
tela_pause=pyTreeBee.dynamicScreen((800,600),30,(0,0,0),config_pause)
tela_pause.setTitle("Asgard Defense")

class controlesExtras(object):
    def __init__(self,tela, pausavel, mapa=None):
        self.tela=tela
        self.mapa=mapa
        self.frame_skip=1
        self.pausavel=pausavel
        self.primeira_vez=True
    def blitOn(self,screen):
        global frame_atual
        if self.primeira_vez:
            frame_atual=1
            self.primeira_vez=False
        if self.mapa==None:
            frame_atual+=self.frame_skip
        elif self.mapa.pause==False: frame_atual+=self.frame_skip
    def keyControls(self,event):
        global tela_pause, config_pause,voltar_retry_pause, voltar_menu_pause, voltar_selecao_pause
        retorno=False
        if event.type==KEYUP:
            if self.pausavel and event.key==K_SPACE:
                pygame.mouse.set_visible(True)
                voltar_retry_pause.link.mapa=self.mapa
                voltar_menu_pause.link.mapa=self.mapa
                voltar_selecao_pause.link.mapa=self.mapa
                
                voltar_retry_pause.link.tela=self.tela
                voltar_menu_pause.link.tela=self.tela
                voltar_selecao_pause.link.tela=self.tela
                
                voltar_retry_pause.link.link=self.tela
                voltar_retry_pause.link.music=(self.tela.stored_music,-1,0.0)
                config_pause.link=self.tela
                retorno=tela_pause
                pygame.mixer.music.pause()
        return retorno

###matrizes seletoras de tiles
matriz_fase_F=[
   [
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,19,19,19,-1,-1,19,19,19,19,19,-1,-1,19,19,-1,-1,-1,-1],
      [19,-1,-1,-1,-1,-1,-1,19,19,19,19,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1, 0, 1, 1, 1, 1, 1, 2,-1,-1,-1,-1,-1,-1, 0, 1, 1, 1, 2,-1],
      [10,20,20, 7, 7, 7,20,20, 1, 2,-1,-1,-1,-1, 3,20,20,20,20,16],
      [10, 7, 8,-1,-1,-1, 6, 7,20,20, 1, 1, 1, 1,20,20, 7, 7, 7,16],
      [-1,-1,-1,-1,-1,-1,-1,-1, 6, 7, 7, 7,20,20,20, 5,-1,-1,-1,-1],
      [10, 1, 1, 1, 1, 1, 2,-1,-1,-1,-1,-1, 3,20,20,20, 1, 1, 1,16],
      [10, 7, 7, 7, 7,20, 5,-1,-1,-1,-1,-1, 3,20, 7, 7, 7, 7, 7,16],
      [-1,-1,-1,-1,-1, 3,20, 1, 1, 2,-1,-1, 3, 5,-1,-1,-1,-1,-1, 6],
      [-1,19,-1,-1,-1, 6, 7, 7,20,20, 1, 1,20, 5,-1,-1,-1,-1,-1,-1],
      [-1,19,19,-1,-1,18,18,18, 6, 7, 7, 7, 7, 8,-1,19,19,19,19,19],
      [-1,19,19,19,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,19,19,19,19,19,19]
   ],
   [
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [18,18,-1,-1,-1,18,18,-1,-1,-1,-1,-1,18,18,-1,-1,18,18,18,18],
      [-1,18,18,18,18,18,18,-1,-1,-1,-1,18,18,18,18,18,18,18,18,18],
      [18,-1,-1,-1,-1,-1,-1,-1,18,18,18,18,18,18,-1,-1,-1,-1,-1,18],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,18,18,18,18,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,18,18,18,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [18,18,18,18,18,18,18,18,-1,-1,-1,-1,-1,-1,-1,-1,18,18,18,18],
      [-1,-1,-1,-1,-1,-1,-1,18,18,18,18,18,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,18,18,18,18,18,-1,-1,-1,-1,-1,-1,-1,-1],
      [18,18,18,18,18,-1,-1,-1,-1,-1,18,18,-1,-1,18,18,18,18,18,18],
      [18,-1,18,18,18,-1,-1,-1,-1,-1,-1,-1,-1,-1,18,18,18,18,18,18],
      [18,-1,-1,18,18,18,18,18,-1,-1,-1,-1,-1,-1,18,-1,-1,-1,-1,-1],
      [18,-1,-1,-1,18,18,18,18,18,18,18,18,18,18,-1,-1,-1,-1,-1,-1]
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
matriz_fase_E=[
   [
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 3,15,15, 3,-1,-1,-1,-1,-1],
      [ 1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 6, 9, 9, 6, 1,-1,-1,-1, 1],
      [-1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,16],
      [10, 9,-1,-1,-1, 9, 9, 9, 9, 9, 9,-1,-1, 9,-1,-1,-1,-1, 9,16],
      [10, 9,-1,-1,-1, 9,-1,-1,-1,-1,-1,-1,-1, 9,-1,-1,-1,-1, 9, 1],
      [-1, 9, 9, 9, 9, 9,-1,-1,-1, 0, 9, 9, 9, 9,-1,-1,-1,-1, 9,-1],
      [-1, 9, 9, 9, 9, 9,-1,-1,-1, 0,-1,-1, 9, 9,-1,-1,-1,-1, 9,-1],
      [10, 9,-1,-1,-1, 9,-1,-1,-1, 0,-1,-1, 9, 9, 9, 9, 9, 9, 9,-1],
      [10, 9,-1,-1,-1, 9, 9, 9, 9, 9,-1,-1, 9, 9, 9, 9, 9, 9, 9,-1],
      [-1, 9, 9, 9, 9, 9,-1,-1,-1, 9, 9, 9, 9, 9, 9,-1,-1,-1,-1,-1],
      [ 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1],
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
   ],
   [
      [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [ 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,-1,-1,-1,-1, 2, 2, 2, 2, 2],
      [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0, 0,-1],
      [ 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
      [-1,-1, 0, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0, 0, 0,-1,-1],
      [-1,-1, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0,-1, 0, 4, 5, 0,-1, 1],
      [ 0,-1,-1,-1,-1,-1, 0, 4, 5,-1,-1,-1,-1,-1, 0, 7, 8, 0,-1, 0],
      [ 0,-1,-1,-1,-1,-1, 0, 7, 8,-1, 9, 0, 0,-1, 0, 0, 0, 0,-1, 0],
      [-1,-1, 0, 0, 0,-1, 0, 0, 0,-1, 9, 0, 0,-1,-1,-1,-1,-1,-1, 4],
      [-1,-1, 0, 0, 0,-1,-1,-1,-1,-1, 9, 0, 0,-1,-1,-1,-1,-1,-1, 7],
      [ 0,-1,-1,-1,-1,-1, 0, 0, 0,-1,-1,-1,-1,-1, 0, 0, 0, 0, 0, 0],
      [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1],
      [ 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
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
matriz_fase_D=[
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 11, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, -1, -1, 9, 16],
        [10, 9, 9, 9, 9, 9, -1, -1, -1, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 16],
        [-1, -1, -1, -1, 9, 9, -1, -1, -1, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 16],
        [-1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 16],
        [10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, -1, -1, 9, -1, -1, -1, -1],
        [10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, -1, -1, 9, -1, -1, -1, -1],
        [-1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 16],
        [-1, -1, -1, -1, 9, 9, -1, -1, -1, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 16],
        [10, 9, 9, 9, 9, 9, -1, -1, -1, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 16],
        [10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, -1, -1, 9, 16],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 13, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ],
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [7, 7, 7, 7, 7, 7, 7, 7, 8, -1, -1, 6, 7, 7, 4, 4, 4, 4, 7, 7],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 7, 7, 8, -1, -1],
        [-1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 2, -1, -1, -1, -1, -1, -1, -1],
        [1, 1, 1, 1, 2, -1, 6, 7, 7, 7, 7, 7, 8, -1, -1, -1, -1, -1, -1, -1],
        [7, 7, 7, 7, 8, -1, -1, -1, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 2, -1, 0, 1, 1, 1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 7, 7, 8, -1, 6, 7, 7, 7],
        [1, 1, 1, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [7, 7, 7, 7, 8, -1, 0, 1, 1, 1, 1, 1, 2, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, 6, 7, 7, 7, 7, 7, 8, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 2, -1, -1],
        [1, 1, 1, 1, 1, 1, 1, 1, 2, -1, -1, 0, 1, 1, 4, 4, 4, 4, 1, 1]
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
matriz_fase_C=[
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, 15, 15, 15, 15, -1, -1, -1, -1, -1, -1, -1, -1],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [9, -1, -1, -1, 9, 9, -1, -1, -1, 9, 9, -1, -1, -1, 9, 9, -1, -1, -1, 9],
        [9, -1, -1, -1, 9, 9, -1, -1, -1, 9, 9, -1, -1, -1, 9, 9, -1, -1, -1, 9],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [-1, 9, -1, -1, -1, -1, 9, 9, -1, -1, -1, -1, 9, 9, -1, -1, -1, -1, 9, -1],
        [-1, 9, -1, -1, -1, -1, 9, 9, -1, -1, -1, -1, 9, 9, -1, -1, -1, -1, 9, -1],
        [-1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, -1],
        [-1, 9, 9, -1, -1, -1, -1, -1, 9, 9, 9, 9, -1, -1, -1, -1, -1, 9, 9, -1],
        [-1, 9, 9, -1, -1, -1, -1, -1, 9, 9, 9, 9, -1, -1, -1, -1, -1, 9, 9, -1],
        [-1, 9, 9, -1, -1, -1, -1, -1, 9, 9, 9, 9, -1, -1, -1, -1, -1, 9, 9, -1],
        [-1, 13, 13, -1, 12, -1, -1, -1, 13, 13, 13, 13, -1, -1, -1, -1, -1, 13, 13, -1]
        ],
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [6, 7, 7, 7, 7, 7, 7, 8, -1, -1, -1, -1, 6, 7, 7, 7, 7, 7, 7, 8],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 1, 2, -1, -1, 0, 1, 2, -1, -1, 0, 1, 2, -1, -1, 0, 1, 2, -1],
        [-1, 6, 7, 8, -1, -1, 6, 7, 8, -1, -1, 6, 7, 8, -1, -1, 6, 7, 8, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [2, -1, 0, 1, 1, 2, -1, -1, 0, 1, 1, 2, -1, -1, 0, 1, 1, 2, -1, 0],
        [5, -1, 6, 7, 7, 8, -1, -1, 6, 7, 7, 8, -1, -1, 6, 7, 7, 8, -1, 3],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3],
        [5, -1, -1, 0, 1, 1, 1, 2, -1, -1, -1, -1, 0, 1, 1, 1, 2, -1, -1, 3],
        [5, -1, -1, 3, 4, 4, 4, 5, -1, -1, -1, -1, 3, 4, 4, 4, 5, -1, -1, 3],
        [5, -1, -1, 3, 4, 4, 4, 5, -1, -1, -1, -1, 3, 4, 4, 4, 5, -1, -1, 3],
        [8, -1, -1, 6, 7, 7, 7, 8, -1, -1, -1, -1, 6, 7, 7, 7, 8, -1, -1, 6]
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

matriz_fase_B=[
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 6, 7, 7, 7, 7, 7, 7, 7, 8],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 16],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 16],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 16],
        [10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 9, 9, -1, -1, 9, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 9, 9, -1, -1, 9, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 9, 9, -1, -1, 9, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 16],
        [10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 16],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 13, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    ],
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 1, 1, 1, 1, 1, 1, 1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [3, 4, 4, 4, 4, 4, 4, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [6, 7, 7, 7, 7, 7, 7, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 1, 1, 2],
        [0, 1, 1, 1, 2, -1, -1, 0, 2, -1, -1, 3, 4, 4, 4, 4, 4, 4, 4, 5],
        [3, 4, 4, 4, 5, -1, -1, 3, 5, -1, -1, 3, 4, 4, 4, 4, 4, 4, 4, 5],
        [3, 4, 4, 4, 5, -1, -1, 6, 8, -1, -1, 6, 7, 7, 7, 7, 7, 7, 7, 8],
        [6, 7, 7, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 1, 1, 1, 1, 1, 1, 1, 2, -1, -1, 0, 1, 1, 1, 1, 1, 1, 1, 2],
        [6, 7, 7, 7, 7, 7, 7, 7, 8, -1, -1, 6, 7, 7, 7, 7, 7, 7, 7, 8]
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
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [11, -1, -1, -1, 11, -1, -1, 9, 9, 9, 9, 9, 9, -1, -1, 11, 9, 9, 9, 11],
        [9, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, 9],
        [9, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, 9],
        [10, 9, 9, 9, 9, -1, -1, 9, -1, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, 9],
        [9, -1, -1, -1, 9, -1, -1, 9, 16, -1, -1, -1, 9, 9, 9, 9, -1, -1, -1, 9],
        [9, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, -1, 9, 9, 9, 9, -1, -1, -1, 9],
        [9, -1, -1, -1, 9, 9, 9, 9, -1, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, 9],
        [9, -1, -1, -1, 9, 9, 9, 9, -1, -1, -1, 14, 9, -1, -1, 9, -1, -1, -1, 9],
        [9, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, -1, 9, -1, -1, 9, 9, 9, 9, 12],
        [9, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, 9],
        [9, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, -1, 9, -1, -1, 9, -1, -1, -1, 9],
        [13, 9, 9, 9, 13, -1, -1, 9, 9, 9, 9, 9, 9, -1, -1, 13, -1, -1, -1, 13]
        ],
    [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 1, 2, -1, 3, 5, -1, -1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1],
        [-1, 3, 4, 5, -1, 3, 5, -1, 0, 1, 1, 2, -1, 3, 5, -1, 0, 1, 2, -1],
        [-1, 6, 7, 8, -1, 3, 5, -1, 3, 4, 4, 5, -1, 3, 5, -1, 3, 4, 5, -1],
        [-1, -1, -1, -1, -1, 3, 5, -1, 6, 4, 4, 8, -1, 6, 8, -1, 3, 4, 5, -1],
        [-1, 0, 1, 2, -1, 3, 5, -1, -1, 4, 4, 14, -1, -1, -1, -1, 3, 4, 5, -1],
        [-1, 3, 4, 5, -1, 6, 8, -1, 0, 4, 4, 2, -1, -1, -1, -1, 3, 4, 5, -1],
        [-1, 3, 4, 5, -1, -1, -1, -1, 6, 4, 4, 8, -1, 0, 2, -1, 3, 4, 5, -1],
        [-1, 3, 4, 5, -1, -1, -1, -1, 16, 4, 4, -1, -1, 3, 5, -1, 6, 7, 8, -1],
        [-1, 3, 4, 5, -1, 0, 2, -1, 0, 4, 4, 2, -1, 3, 5, -1, -1, -1, -1, -1],
        [-1, 3, 4, 5, -1, 3, 5, -1, 3, 4, 4, 5, -1, 3, 5, -1, 0, 1, 2, -1],
        [-1, 6, 7, 8, -1, 3, 5, -1, 6, 7, 7, 8, -1, 3, 5, -1, 3, 4, 5, -1],
        [-1, -1, -1, -1, -1, 3, 5, -1, -1, -1, -1, -1, -1, 3, 5, -1, 6, 7, 8, -1]
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

matriz_fase_G=[
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
      [ 4, 4, 8,-1,-1, 0, 1, 2,-1, 6, 8,-1, 0, 1, 2,-1,-1, 6, 4, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1,-1,-1,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1, 0, 2,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1, 6, 8,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 8,-1,-1,-1, 6, 7, 8,-1,-1,-1,-1, 6, 7, 8,-1,-1,-1, 6, 4],
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
      [ 4, 4, 8,-1,-1, 0, 1, 2,-1, 6, 8,-1, 0, 1, 2,-1,-1, 6, 4, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1,-1,-1,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1, 0, 2,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 5,-1,-1,-1, 3, 4, 5,-1, 6, 8,-1, 3, 4, 5,-1,-1,-1, 3, 4],
      [ 4, 8,-1,-1,-1, 6, 7, 8,-1,-1,-1,-1, 6, 7, 8,-1,-1,-1, 6, 4],
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
        [-1, -1,  0, -1, -1, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1],
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

#tela gameover e vitória
mouse=quadradoControlavel()
blit_score=blitScore()
game_over=pyTreeBee.dynamicScreen((800,600), 30,(100,0,0))
game_over.setTitle("Asgard Defense")
game_over.setImage(pygame.image.load(dir_image+'gameover.png').convert_alpha(),(0,0))
winner_scr=pyTreeBee.dynamicScreen((800,600), 30,(100,100,255),blit_score)
winner_scr.setTitle("Asgard Defense")
winner_scr.setImage(pygame.image.load(dir_image+'vitoria.png').convert_alpha(),(0,0))
very_winner_scr=pyTreeBee.dynamicScreen((800,600), 30,(100,100,255),blit_score)
very_winner_scr.setTitle("Asgard Defense")
very_winner_scr.setImage(pygame.image.load(dir_image+'vitoria.png').convert_alpha(),(0,0))
congratulations_scr=pyTreeBee.dynamicScreen((800,600), 30,(100,100,255))
congratulations_scr.setTitle("Asgard Defense")
congratulations_scr.setImage(pygame.image.load(dir_image+'congratulations.png').convert(),(0,0))
congratulado=congratulouGame(winner_scr, very_winner_scr)
scr_intermediaria=pyTreeBee.dynamicScreen((800,600), 30,(100,100,255),congratulado)
scr_intermediaria.setTitle("Asgard Defense")
#loading dos tiles
def tileList(tile_set,size):
    tile_list=[]
    for h in range(tile_set.get_height()//40):
        for w in range(tile_set.get_width()//40):
            tile_list.append(tile_set.subsurface((w*40,h*40),(40,40)))
    return tile_list
tile_list_0=tileList(pygame.image.load(dir_image+"tileset0.png").convert(),40)
tile_list_1=tileList(pygame.image.load(dir_image+"tileset1.png").convert(),40)
tile_list_2=tileList(pygame.image.load(dir_image+"tileset2.png").convert(),40)
tile_list_3=tileList(pygame.image.load(dir_image+"tileset3.png").convert(),40)
tile_list_4=tileList(pygame.image.load(dir_image+"tileset4.png").convert(),40)
tile_list_A=tileList(pygame.image.load(dir_image+"tilesetA.png").convert(),40)#[1]
tile_list_B=tileList(pygame.image.load(dir_image+"tilesetB.png").convert(),40)#[18]
tile_list_C=tileList(pygame.image.load(dir_image+"tileset3_old.png").convert(),40)
#Botões e Seqüênciamentos das Fases
botoes_extras_x=26
botoes_extras_y=450
cor_fundo=(0,0,0)#(60,80,110)#(34,57,65)
'''
#G
mapa_fase_G = mapaLimitavel(mouse,statusPlayer(50,70),matriz_fase_G, tile_list_C,40)
fase_G = pyTreeBee.dynamicScreen((800,600),60,cor_fundo,mapa_fase_G)
fase_G.setTitle("Asgard Defense")
botao_G=pyTreeBee.linkedButton(linkedMusic(fase_G,dir_music+"El Magicia.mp3",-1, 0.0),din_12,[""],botoes_extras_x,botoes_extras_y+56,pygame.Rect(0,0,28,32),0,36,pygame.transform.scale(tile_list_C[7],(32,32)))
botao_G.setEach_Text([""],["RETOMADA DE VALGRIND"],[""])
botao_G.setEach_BarSize((-2,-3),(-2,-5),(-2,-7))
botao_G=lockedButton(botao_G,'save_state_G')
#F
mapa_fase_F = mapaLimitavel(mouse,statusPlayer(30,70),matriz_fase_F, tile_list_B,40)
fase_F = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_F)
fase_F.setTitle("Asgard Defense")
botao_F=pyTreeBee.linkedButton(linkedMusic(fase_F,dir_music+"Future Gladiator.mp3",-1, 0.0),din_12,[""],botoes_extras_x+40,botoes_extras_y+56,pygame.Rect(0,0,28,32),0,36,pygame.transform.scale(tile_list_B[19],(32,32)))
botao_F.setEach_Text([""],["SALA DO TESOURO"],[""])
botao_F.setEach_BarSize((-2,-3),(-2,-5),(-2,-7))
botao_F=lockedButton(botao_F,'save_state_F')
#E
mapa_fase_E = mapaLimitavel(mouse,statusPlayer(30,70),matriz_fase_E, tile_list_A,40)
fase_E = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_E)
fase_E.setTitle("Asgard Defense")
botao_E=pyTreeBee.linkedButton(linkedMusic(fase_E,dir_music+"Future Gladiator.mp3",-1, 0.0),din_12,[""],botoes_extras_x+80,botoes_extras_y+56,pygame.Rect(0,0,28,32),0,36,pygame.transform.scale(tile_list_A[1],(32,32)))
botao_E.setEach_Text([""],["SANTUÁRIO DA FREYA"],[""])
botao_E.setEach_BarSize((-2,-3),(-2,-5),(-2,-7))
botao_E=lockedButton(botao_E,'save_state_E')
#D
mapa_fase_D = mapaLimitavel(mouse,statusPlayer(30,70),matriz_fase_D, tile_list_1,40)
fase_D = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_D)
fase_D.setTitle("Asgard Defense")
botao_D=pyTreeBee.linkedButton(linkedMusic(fase_D,dir_music+"Future Gladiator.mp3",-1, 0.0),din_12,[""],botoes_extras_x+80,botoes_extras_y,pygame.Rect(0,0,28,32),0,36,pygame.transform.scale(tile_list_1[7],(32,32)))
botao_D.setEach_Text([""],["VALE DOS VIKINGS"],[""])
botao_D.setEach_BarSize((-2,-3),(-2,-5),(-2,-7))
botao_D=lockedButton(botao_D,'save_state_D')
#C
mapa_fase_C = mapaLimitavel(mouse,statusPlayer(30,70),matriz_fase_C, tile_list_2,40)
fase_C = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_C)
fase_C.setTitle("Asgard Defense")
botao_C=pyTreeBee.linkedButton(linkedMusic(fase_C,dir_music+"Future Gladiator.mp3",-1, 0.0),din_12,[""],botoes_extras_x+120,botoes_extras_y,pygame.Rect(0,0,28,32),0,36,pygame.transform.scale(tile_list_2[7],(32,32)))
botao_C.setEach_Text([""],["HALL DOS BERSERKERS"],[""])
botao_C.setEach_BarSize((-2,-3),(-2,-5),(-2,-7))
botao_C=lockedButton(botao_C,'save_state_C')
#B
mapa_fase_B = mapaLimitavel(mouse,statusPlayer(30,70),matriz_fase_B, tile_list_1,40)
fase_B = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_B)
fase_B.setTitle("Asgard Defense")
botao_B=pyTreeBee.linkedButton(linkedMusic(fase_B,dir_music+"The Complex.mp3",-1, 0.0),din_12,[""],botoes_extras_x+40,botoes_extras_y,pygame.Rect(0,0,28,32),0,36,pygame.transform.scale(tile_list_1[7],(32,32)))
botao_B.setEach_Text([""],["FLORESTA DAS VALQUÍRIAS"],[""])
botao_B.setEach_BarSize((-2,-3),(-2,-5),(-2,-7))
botao_B=lockedButton(botao_B,'save_state_B')
#A
mapa_fase_A = mapaLimitavel(mouse,statusPlayer(30,70),matriz_fase_A, tile_list_1,40)
fase_A = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_A)
fase_A.setTitle("Asgard Defense")
botao_A=pyTreeBee.linkedButton(linkedMusic(fase_A,dir_music+"Movement Proposition.mp3",-1, 0.0),din_12,[""],botoes_extras_x,botoes_extras_y,pygame.Rect(0,0,28,32),0,36,pygame.transform.scale(tile_list_1[7],(32,32)))
botao_A.setEach_Text([""],["PLANÍCIE DAS ARQUEIRAS"],[""])
botao_A.setEach_BarSize((-2,-3),(-2,-5),(-2,-7))
botao_A=lockedButton(botao_A,'save_state_A')

#FASE EXTRAS TEXTO
area_fases_extras=pyTreeBee.linkedButton(None,din_12,[""],0,396,pygame.Rect(0,0,421,204),0,0)
area_fases_extras.setEach_Image(pygame.image.load(dir_image+"stage61.png").convert(),pygame.image.load(dir_image+"stage62.png").convert(),pygame.image.load(dir_image+"stage62.png").convert())
area_fases_extras.setAll_BarSize((0,0))
area_fases_extras=lockedButton(area_fases_extras,'save_state_1')
'''
#5
mapa_fase_5 = mapaLimitavel(mouse,statusPlayer(100,70),matriz_fase_5, tile_list_4,40)#,botao_E,botao_F)
fase_5 = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_5)
fase_5.setTitle("Asgard Defense")
botao_5=pyTreeBee.linkedButton(linkedMusic(fase_5,dir_music+"Epic.mp3",-1,0.0),din_12,[""],426,238,pygame.Rect(0,0,324,260),0,0)
botao_5.setEach_Image(pygame.image.load(dir_image+"stage51.png").convert(),pygame.image.load(dir_image+"stage52.png").convert(),pygame.image.load(dir_image+"stage52.png").convert())
botao_5.setAll_BarSize((0,0))
botao_5=lockedButton(botao_5,'save_state_5')
#4
mapa_fase_4 = mapaLimitavel(mouse,statusPlayer(50,70),matriz_fase_4, tile_list_3,40,botao_5)#,botao_G)
fase_4 = pyTreeBee.dynamicScreen((800,600),60,cor_fundo,mapa_fase_4)
fase_4.setTitle("Asgard Defense")
botao_4=pyTreeBee.linkedButton(linkedMusic(fase_4,dir_music+"Future Gladiator.mp3",-1, 0.0),din_12,[""],158,206,pygame.Rect(0,0,260,166),0,0)
botao_4.setEach_Image(pygame.image.load(dir_image+"stage41.png").convert(),pygame.image.load(dir_image+"stage42.png").convert(),pygame.image.load(dir_image+"stage42.png").convert())
botao_4.setAll_BarSize((0,0))
botao_4=lockedButton(botao_4,'save_state_4')
#3
mapa_fase_3 = mapaLimitavel(mouse,statusPlayer(30,70),matriz_fase_3, tile_list_2,40,botao_4)#,botao_C)
fase_3 = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_3)
fase_3.setTitle("Asgard Defense")
botao_3=pyTreeBee.linkedButton(linkedMusic(fase_3,dir_music+"Volatile Reaction.mp3",-1, 0.0),din_12,[""],539,93,pygame.Rect(0,0,230,144),0,0)
botao_3.setEach_Image(pygame.image.load(dir_image+"stage31.png").convert(),pygame.image.load(dir_image+"stage32.png").convert(),pygame.image.load(dir_image+"stage32.png").convert())
botao_3.setAll_BarSize((0,0))
botao_3=lockedButton(botao_3,'save_state_3')
#2
mapa_fase_2 = mapaLimitavel(mouse,statusPlayer(30,70),matriz_fase_2, tile_list_1,40,botao_3)#,area_fases_extras,botao_A,botao_B,botao_D)
fase_2 = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_2)
fase_2.setTitle("Asgard Defense")
botao_2=pyTreeBee.linkedButton(linkedMusic(fase_2,dir_music+"Heroic Age.mp3",-1, 0.0),din_12,[""],323,50,pygame.Rect(0,0,202,120),0,0)
botao_2.setEach_Image(pygame.image.load(dir_image+"stage21.png").convert(),pygame.image.load(dir_image+"stage22.png").convert(),pygame.image.load(dir_image+"stage22.png").convert())
botao_2.setAll_BarSize((0,0))
botao_2=lockedButton(botao_2,'save_state_2')
#1
mapa_fase_1 = mapaLimitavel(mouse,statusPlayer(1,35),matriz_fase_1, tile_list_0,40,botao_2)
fase_1 = pyTreeBee.dynamicScreen((800,600), 60,cor_fundo,mapa_fase_1)
#fase_1.setTitle("Asgard Defense")
botao_1=pyTreeBee.linkedButton(linkedMusic(fase_1,dir_music+"Lord of the Land.mp3",-1, 0.0),din_12,[""],24,43,pygame.Rect(0,0,284,72),0,0)
botao_1.setEach_Image(pygame.image.load(dir_image+"stage11.png").convert(),pygame.image.load(dir_image+"stage12.png").convert(),pygame.image.load(dir_image+"stage12.png").convert())
botao_1.setAll_BarSize((0,0))

#spawn gerador de hordaS
enemy1=pygame.image.load(dir_image+"inimigo01sheet2.png").convert_alpha()
enemy2=pygame.image.load(dir_image+"inimigo02sheet.png").convert_alpha()
enemy3=pygame.image.load(dir_image+"inimigo03sheet.png").convert_alpha()
enemy4=pygame.image.load(dir_image+"inimigo04sheet.png").convert_alpha()
enemy5=pygame.image.load(dir_image+"inimigo05sheet.png").convert_alpha()
enemy6=pygame.image.load(dir_image+"inimigo06sheet.png").convert_alpha()
enemy7=pygame.image.load(dir_image+"inimigo07sheet.png").convert_alpha()
enemy8=pygame.image.load(dir_image+"inimigo08sheet.png").convert_alpha()
enemy9=pygame.image.load(dir_image+"inimigo09sheet.png").convert_alpha()
'''
for n in range(8):
    exec 'enemy'+str(n+2)+'=pygame.image.load(dir_image+"inimigo0'+str(n+2)+'sheet.png")'
'''
enemy10=pygame.image.load(dir_image+"inimigo10sheet.png")

mov_G_A_1=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(1, 12)
mov_G_A_2=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(1, 12)
mov_G_B_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1)] #(4, 12)
mov_G_B_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1)] #(4, 12) 
mov_G_C=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(5, 12)
mov_G_D_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1)] #(8, 12)
mov_G_D_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1)] #(8, 12)
mov_G_E=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(9, 12)
mov_G_F=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(10, 12)
mov_G_G_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(11, 12)   
mov_G_G_2=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(11, 12)
mov_G_H=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(14, 12)
mov_G_I_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(15, 12)
mov_G_I_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1)] #(15, 12)
mov_G_J_1=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1)] #(18, 12)
mov_G_J_2=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1)] #(18, 12)



mov_C_A_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1),
          (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1),
          (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)]#(1,12)
mov_C_A_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0),
           (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)]#(1,12)
mov_C_B_1=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1),
           (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1)]#(2,12)
mov_C_B_2=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0),
           (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1),
           (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1)]#(2,12)
mov_C_C=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)]#(8,12)
mov_C_D=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1),
         (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1)]#(9,12)
mov_C_E= [(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1),
          (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1)]#(10,12)
mov_C_F=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1),
         (1, 0), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1)]#(11,12)
mov_C_G=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0),
         (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1)]#(17,12)
mov_C_H_1=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1),
          (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1)]#(18,12)
mov_C_H_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0),
           (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1)]#(18,12)
mov_C_H_3=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0),
           (-1, 0), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1)]#(18,12)

mov_B_A=[(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
         (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]#(0,1)
mov_B_B=[(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1),
         (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]#(0,5)
mov_B_C_1=[(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (1, 0),
         (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]#(0,10)
mov_B_C_2=[(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
           (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)]#(0,10)
mov_B_D= [(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0),
          (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0),
          (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]#(9,12)
mov_B_E=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1),
         (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]#(10,12)


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

mov_5_A=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0)]#(19, 12)
mov_5_B=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0)] #(0, 12)
mov_5_C=[(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0)]#(15, 1)
mov_5_D=[(1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0)] #(0, 4)
mov_5_E=[(0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0)] #(15, 12)
mov_5_F=[(0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (1, 0), (1, 0)]#(4, 1)
mov_5_G=[(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0)]#(19, 1)
mov_5_H=[(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0)]#(0, 1)
mov_5_I=[(-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0)]#(19, 9)
mov_5_J=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0)]#(4, 12)


mov_4_A_1=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1)]#(1, 12)
mov_4_A_2=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1)]#(1, 12)
mov_4_B_1=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1)]#(4, 12)
mov_4_B_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1)]#(4, 12)
mov_4_C=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1)]   #(5, 12)
mov_4_D=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1)] #(8, 12)
mov_4_E=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1)] #(9, 12)
mov_4_F=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1)]#(10, 12)
mov_4_G=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1)]#(11, 12)
mov_4_H=[(0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1)]#(14, 12)
mov_4_I_1=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1)]#(15, 12)
mov_4_I_2=[(0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1)]#(15, 12) 
mov_4_J_1=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1)]#(18, 12)
mov_4_J_2=[(0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (0, -1)]#(18, 12)

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
viking_image=pygame.image.load(dir_image+"vikingchifre_spritesheet.png").convert_alpha()
arqueiro_image=pygame.image.load(dir_image+"archer_spritesheet.png").convert_alpha()
berserker_image=pygame.image.load(dir_image+"berserker_spritesheet.png").convert_alpha()
valquiria_image=pygame.image.load(dir_image+"valkyrie_spritesheet.png").convert_alpha()
#diferenciadores: listas de vantagens e desvantagens
#                         nl, rx,  vm,  az,  vr
viking_diferenciador=    [1,0.5,2,1,0.8] #azul
arqueiro_diferenciador=  [1,2,0.5,0.8,1] #verde
berserker_diferenciador= [1,0.8,1,2,0.5] #vermelho
valquiria_diferenciador= [1,1,0.8,0.5,2] #roxo
#mouse,sprite,size,nextsprite,rewind,atk,vel,rng,fly,types
viking_click=charSelected(mouse,viking_image,(60,50),6,False,25,22,2,False,viking_diferenciador,35)
arqueiro_click=charSelected(mouse,arqueiro_image,(50,50),5,False,35,30,3,True,arqueiro_diferenciador,50)
berserker_click=charSelected(mouse,berserker_image,(70,70),5,False,15,5,1,False,berserker_diferenciador,50)
valquiria_click=charSelected(mouse,valquiria_image,(80,80),4,False,25,12,2,True,valquiria_diferenciador,75)

tecla_viking=charTyped(mouse,K_q,viking_image,(60,50),6,False,25,22,2,False,viking_diferenciador,35)
tecla_arqueiro=charTyped(mouse,K_w,arqueiro_image,(50,50),5,False,35,30,3,True,arqueiro_diferenciador,50)
tecla_berserker=charTyped(mouse,K_e,berserker_image,(70,70),5,False,15,5,1,False,berserker_diferenciador,50)
tecla_valquiria=charTyped(mouse,K_r,valquiria_image,(80,80),4,False,25,12,2,True,valquiria_diferenciador,75)


pick_som=pygame.mixer.Sound(dir_music+"bow.wav")
botao_viking = pyTreeBee.linkedButton(viking_click,dinB_12,[""],0,520,pygame.Rect(0,0,80,80),0,-15,pygame.image.load(dir_image+"menubot_1.png").convert())
botao_viking.setAll_BarSize((0,0))
botao_viking.setSelect_Sound(pick_som)
botao_arqueiro = pyTreeBee.linkedButton(arqueiro_click,dinB_12,[""],80,520,pygame.Rect(0,0,80,80),0,-15,pygame.image.load(dir_image+"menubot_2.png").convert())
botao_arqueiro.setAll_BarSize((0,0))
botao_arqueiro.setSelect_Sound(pick_som)
botao_berserker = pyTreeBee.linkedButton(berserker_click,dinB_12,[""],160,520,pygame.Rect(0,0,80,80),0,-15,pygame.image.load(dir_image+"menubot_3.png").convert())
botao_berserker.setAll_BarSize((0,0))
botao_berserker.setSelect_Sound(pick_som)
botao_valquiria = pyTreeBee.linkedButton(valquiria_click,dinB_12,[""],240,520,pygame.Rect(0,0,80,80),0,-15,pygame.image.load(dir_image+"menubot_4.png").convert())
botao_valquiria.setAll_BarSize((0,0))
botao_valquiria.setSelect_Sound(pick_som)
### botoes aceleradores ###
accel_som=pygame.mixer.Sound(dir_music+"blip-1.wav")
accel_som.set_volume(0.25)
accelx1=pyTreeBee.linkedButton(accelGame(60),din_12,[""],800-180,520,pygame.Rect(0,0,60,60),0,0,pygame.image.load(dir_image+'menubot_x1.png').convert_alpha())
accelx1.setAll_BarSize((0,0))
accelx1.setSelect_Sound(accel_som)

accelx2=pyTreeBee.linkedButton(accelGame(90),din_12,[""],800-120,520,pygame.Rect(0,0,60,60),0,0,pygame.image.load(dir_image+'menubot_x2.png').convert_alpha())
accelx2.setAll_BarSize((0,0))
accelx2.setSelect_Sound(accel_som)

accelx3=pyTreeBee.linkedButton(accelGame(120),din_12,[""],800-60,520,pygame.Rect(0,0,60,60),0,0,pygame.image.load(dir_image+'menubot_x3.png').convert_alpha())
accelx3.setAll_BarSize((0,0))
accelx3.setSelect_Sound(accel_som)

tecla_x1=accelKey(60,K_1)
tecla_x2=accelKey(90,K_2)
tecla_x3=accelKey(120,K_3)

winner_music=(dir_music+"medieval-fanfare.wav",1,0.0)
game_over_music=(dir_music+"Funeral March for Brass.mp3",1,0.0)
###>>>FASES<<<###
casa=pygame.image.load(dir_image+'casa.png').convert_alpha()
tree_1=pygame.image.load(dir_image+'tree1.png').convert_alpha()
tree_2=pygame.image.load(dir_image+'tree2.png').convert_alpha()
'''
###fase G### !!!!!!!!!!!!!!!!!!!!!!PRECISA BALANCEAMENTO!!!!!!!!!!!

#mov_G_A_1= andar pela borda,mov_G_A_2=descola da borda
fator_G=2000
mapa_fase_G.addSpawn((1, 12),[120,120,120,120,120,120,120,120,120,120] , [fator_G*3, fator_G*10, fator_G*15,fator_G*31,fator_G*40,fator_G*45,fator_G*49,fator_G*54,fator_G*64,fator_G*69] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_A_1,mov_G_A_2,mov_G_A_1,mov_G_A_2,mov_G_A_1,mov_G_A_2,mov_G_A_1,mov_G_A_2,mov_G_A_1,mov_G_A_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,1,1,2,3,2,3,4,25], [10,10,10,10,10,10,10,10,10,1])#[10,5,10,10,15,10,20,10,20,1]
#mov_G_B_1,mov_G_B_2
mapa_fase_G.addSpawn((4, 12),[120,120,120,120,120,120,120,120,120,120] , [fator_G*8, fator_G*12, fator_G*16,fator_G*29,fator_G*38,fator_G*44,fator_G*50,fator_G*55,fator_G*65,fator_G*71] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_B_1,mov_G_B_2,mov_G_B_1,mov_G_B_2,mov_G_B_1,mov_G_B_2,mov_G_B_1,mov_G_B_2,mov_G_B_1,mov_G_B_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])
#mov_G_C
mapa_fase_G.addSpawn((5, 12),[120,120,120,120,120,120,120,120,120,120] , [800      , fator_G*13, fator_G*17,fator_G*27,fator_G*36,fator_G*43,fator_G*52,fator_G*56,fator_G*67,fator_G*72] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_C,mov_G_C,mov_G_C,mov_G_C,mov_G_C,mov_G_C,mov_G_C,mov_G_C,mov_G_C,mov_G_C] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])
#mov_G_D_1,mov_G_D_2
mapa_fase_G.addSpawn((8, 12),[120,120,120,120,120,120,120,120,120,120] , [fator_G*6, fator_G*11, fator_G*20,fator_G*25,fator_G*34,fator_G*42,fator_G*53,fator_G*57,fator_G*64,fator_G*70] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_D_1,mov_G_D_2,mov_G_D_1,mov_G_D_2,mov_G_D_1,mov_G_D_2,mov_G_D_1,mov_G_D_2,mov_G_D_1,mov_G_D_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])
#mov_G_E
mapa_fase_G.addSpawn((9, 12),[120,120,120,120,120,120,120,120,120,120] , [fator_G*4, fator_G*12, fator_G*18,fator_G*23,fator_G*32,fator_G*41,fator_G*51,fator_G*58,fator_G*65,fator_G*71] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_E,mov_G_E,mov_G_E,mov_G_E,mov_G_E,mov_G_E,mov_G_E,mov_G_E,mov_G_E,mov_G_E] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])
#mov_G_F
mapa_fase_G.addSpawn((10, 12),[120,120,120,120,120,120,120,120,120,120] ,[fator_G+400, fator_G*14, fator_G*21,fator_G*30,fator_G*33,fator_G*47,fator_G*49,fator_G*59,fator_G*68,fator_G*72] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_F,mov_G_F,mov_G_F,mov_G_F,mov_G_F,mov_G_F,mov_G_F,mov_G_F,mov_G_F,mov_G_F] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])
#mov_G_G_1,mov_G_G_2
mapa_fase_G.addSpawn((11, 12),[120,120,120,120,120,120,120,120,120,120] ,[fator_G*2, fator_G*13, fator_G*19,fator_G*28,fator_G*35,fator_G*44,fator_G*50,fator_G*60,fator_G*66,fator_G*69] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_G_1,mov_G_G_2,mov_G_G_1,mov_G_G_2,mov_G_G_1,mov_G_G_2,mov_G_G_1,mov_G_G_2,mov_G_G_1,mov_G_G_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])
#mov_G_H
mapa_fase_G.addSpawn((14, 12),[120,120,120,120,120,120,120,120,120,120] ,[fator_G*7, fator_G*10, fator_G*17,fator_G*26,fator_G*37,fator_G*48,fator_G*52,fator_G*61,fator_G*65,fator_G*71] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_H,mov_G_H,mov_G_H,mov_G_H,mov_G_H,mov_G_H,mov_G_H,mov_G_H,mov_G_H,mov_G_H] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])
#mov_G_I_1,mov_G_I_2
mapa_fase_G.addSpawn((15, 12),[120,120,120,120,120,120,120,120,120,120] ,[fator_G*5, fator_G*12, fator_G*16,fator_G*24,fator_G*39,fator_G*47,fator_G*53,fator_G*62,fator_G*67,fator_G*73] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_I_1,mov_G_I_2,mov_G_I_1,mov_G_I_2,mov_G_I_1,mov_G_I_2,mov_G_I_1,mov_G_I_2,mov_G_I_1,mov_G_I_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])
#mov_G_J_1 = andar pela borda,mov_G_J_2=descola da borda
mapa_fase_G.addSpawn((18, 12),[120,120,120,120,120,120,120,120,120,120] ,[fator_G*9,fator_G*14, fator_G*15,fator_G*22,fator_G*40,fator_G*46,fator_G*51,fator_G*63,fator_G*64,fator_G*70] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,5] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,180,300,180,450,700,1080,600,1350,12000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,2,4,3,0,4,0], [mov_G_J_1,mov_G_J_2,mov_G_J_1,mov_G_J_2,mov_G_J_1,mov_G_J_2,mov_G_J_1,mov_G_J_2,mov_G_J_1,mov_G_J_2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [10,10,10,10,10,10,10,10,10,1])

for x in range(3,17,1):
    mapa_fase_G.addTarget((x,1),(0,0))

fase_G.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)
fase_G.addItem(controlesExtras(fase_G,True,mapa_fase_G))
fase_G.addItem(gameOver(fase_G,game_over,mapa_fase_G,game_over_music))
fase_G.addItem(winnerScreen(fase_G,winner_scr,mapa_fase_G,blit_score,winner_music))



###fase F ###
###fase E ###
###fase D ###

###fase C (extra)### !!!!!!!!!!!!!!!!!!!!!!PRECISA BALANCEAMENTO!!!!!!!!!!!
#parei aqui: testar as tragetórias dos spawns(mapa 2 da maria)
#mapa_fase_C.addSpawn( (0,1) , [120] , [800] , (0,0) , [enemy1] , [(20,20)] , [8] , [True] , [1] , [0.5] , [120] ,[False],[0], [mov_B_A] , [(1,0)] ,[5], [20])
#mapa_fase_C.addSpawn( (0,10) , [120,120] , [800,800] , (0,0) , [enemy1,enemy1] , [(20,20),(20,20)] , [8,8] , [True,True] , [1,1] , [0.5,0.5] , [120,120] ,[False,False],[0,0], [mov_B_C_1,mov_B_C_2] , [(1,0),(1,0)] ,[5,5], [5,5])
#mapa_fase_C.addTarget((8,1),(0,0))
#mapa_fase_C.addTarget((9,1),(0,0))
#mapa_fase_C.addTarget((10,1),(0,0))
#mapa_fase_C.addTarget((11,1),(0,0))


#fase_C.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)
#fase_C.addItem(controlesExtras(fase_C, True, mapa_fase_C))
#fase_C.addItem(gameOver(fase_C,game_over,mapa_fase_C,game_over_music))
#fase_C.addItem(winnerScreen(fase_C,winner_scr,mapa_fase_C))

###fase B (extra)### !!!!!!!!!!!!!!!!!!!!!!PRECISA BALANCEAMENTO!!!!!!!!!!!

mapa_fase_B.addSpawn( (0,1) , [120] , [800] , (0,0) , [enemy1] , [(20,20)] , [8] , [True] , [1] , [0.5] , [120] ,[False],[0], [mov_B_A] , [(1,0)] ,[5], [20])
mapa_fase_B.addSpawn( (0,5) , [120] , [800] , (0,0) , [enemy1] , [(20,20)] , [8] , [True] , [1] , [0.5] , [120] ,[False],[0], [mov_B_B] , [(1,0)] ,[5], [20])
mapa_fase_B.addSpawn( (0,10) , [120,120] , [800,800] , (0,0) , [enemy1,enemy1] , [(20,20),(20,20)] , [8,8] , [True,True] , [1,1] , [0.5,0.5] , [120,120] ,[False,False],[0,0], [mov_B_C_1,mov_B_C_2] , [(1,0),(1,0)] ,[5,5], [5,5])
mapa_fase_B.addSpawn( (9,12) , [120] , [1] , (0,0) , [enemy1] , [(20,20)] , [8] , [True] , [1] , [0.5] , [120] ,[False],[0], [mov_B_D] , [(1,0)] ,[5], [5])
mapa_fase_B.addSpawn( (10,12) , [120] , [800] , (0,0) , [enemy1] , [(20,20)] , [8] , [True] , [1] , [0.5] , [120] ,[False],[0], [mov_B_E] , [(1,0)] ,[5], [20])
mapa_fase_B.addTarget((19,2),(0,0))
mapa_fase_B.addTarget((19,3),(0,0))
mapa_fase_B.addTarget((19,4),(0,0))
mapa_fase_B.addTarget((19,9),(0,0))
mapa_fase_B.addTarget((19,10),(0,0))
for a in range(0,6,2):
    mapa_fase_B.mapa[1][1][12+a].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*(12+a),40*0))))
    
    mapa_fase_B.mapa[1][2][2+a].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*(2+a),40*1))))
    mapa_fase_B.mapa[1][2][3+a].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*(3+a),40*1))))
    
    mapa_fase_B.mapa[1][12][2+a].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*(2+a),40*11))))
    mapa_fase_B.mapa[1][12][1+a].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*(1+a),40*11))))
    
    mapa_fase_B.mapa[1][12][13+a].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*(13+a),40*11))))
    mapa_fase_B.mapa[1][12][14+a].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*(14+a),40*11))))
for a in range(3):
    mapa_fase_B.mapa[1][6][1+a].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*(1+a),40*6))))
    mapa_fase_B.mapa[1][7][1+a].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*(1+a),40*7))))
for b in range(0,3,2):
    for a in range(0,7,2):
        mapa_fase_B.mapa[1][5+b][11+a].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*(11+a),40*(4+b)))))
        mapa_fase_B.mapa[1][6+b][12+a].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*(12+a),40*(5+b)))))

mapa_fase_B.mapa[1][7][8].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*(8),40*(6)))))


fase_B.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)
fase_B.addItem(controlesExtras(fase_B, True, mapa_fase_B))
fase_B.addItem(gameOver(fase_B,game_over,mapa_fase_B,game_over_music))
fase_B.addItem(winnerScreen(fase_B,winner_scr,mapa_fase_B,blit_score,winner_music))

##fase A (extra)### !!!!!!!!!!!!!!!!!!!!!!PRECISA BALANCEAMENTO!!!!!!!!!!!

mapa_fase_A.addSpawn( (0,9) , [120,120,120,120,120,120,120,120,120,120] , [20,800,800,800,800,800,800,800,800,800] , (1,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C,mov_A_C] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[5,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])
mapa_fase_A.addSpawn( (0,10) , [120,120,120,120,120,120,120,120,120,120] , [20,800,800,800,800,800,800,800,800,800] , (1,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B,mov_A_B] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[5,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])
mapa_fase_A.addSpawn( (0,11) , [120,120,120,120,120,120,120,120,120,120] , [20,800,800,800,800,800,800,800,800,800] , (1,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A,mov_A_A] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[5,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])
mapa_fase_A.addTarget((19,9),(-1,0))
mapa_fase_A.addTarget((19,10),(-1,0))
mapa_fase_A.addTarget((19,11),(-1,0))

fase_A.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)
fase_A.addItem(controlesExtras(fase_A, True, mapa_fase_A))
fase_A.addItem(gameOver(fase_A,game_over,mapa_fase_A,game_over_music))
fase_A.addItem(winnerScreen(fase_A,winner_scr,mapa_fase_A,blit_score,winner_music))
'''
###fase 5###

#pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,mana,quantidades):
fator_5=8100
mapa_fase_5.addSpawn( (19,12), [120,120] , [800,38800] , (0,0) , [enemy1,enemy6] , [(20,20),(25,25)] , [8,8] , [False]*2 , [1,1] , [0.5,0.5] , [100,700] ,[False,False],[0,4], [mov_5_A] *2, [(1,0),(1,0)] ,[2,6], [50,50])#1,6
mapa_fase_5.addSpawn( (0,12), [120,120] , [800,38800] , (0,0) , [enemy1,enemy6] , [(20,20),(25,25)] , [8,8] , [False]*2 , [1,1] , [0.5,0.5] , [100,700] ,[False,False],[0,4], [mov_5_B] *2, [(1,0),(1,0)] ,[2,6], [50,50])
mapa_fase_5.addSpawn( (15,1), [120,120] , [8700,54200] , (0,0) , [enemy2,enemy8] , [(25,25),(22,22)] , [8,8] , [False]*2 , [1,1] , [0.5,0.5] , [180,600] ,[False,True],[2,0], [mov_5_C] *2, [(1,0),(1,0)] ,[2,7], [50,50])#2,8
mapa_fase_5.addSpawn( (0,4), [120,120] , [8700,54200] , (0,0) , [enemy2,enemy8] , [(25,25),(22,22)] , [8,8] , [False]*2 , [1,1] , [0.5,0.5] , [180,600] ,[False,True],[2,0], [mov_5_D] *2, [(1,0),(1,0)] ,[2,7], [50,50])
mapa_fase_5.addSpawn( (15,12), [120,120,240] , [31200,69700,72500] , (0,0,0) , [enemy5,enemy10,enemy10] , [(22,22),(20,20),(20,20)] , [8,8,8] , [False, False, False] , [1,10,20] , [0.5,0.5,0.25] , [450,12000,10000] ,[False,False,False],[0,0,0], [mov_5_E] *3, [(1,0),(1,0),(1,0)] ,[4,200,200], [50,1,2])#5,10,10
mapa_fase_5.addSpawn( (4,1), [120,120,240] , [31200,69700,72500] , (0,0,0) , [enemy5,enemy10,enemy10] , [(22,22),(20,20),(20,20)] , [8,8,8] , [False, False, False] , [1,10,20] , [0.5,0.5,0.25] , [450,12000,10000] ,[False,False,False],[0,0,0], [mov_5_F] *3, [(1,0),(1,0),(1,0)] ,[4,200,200], [50,1,2])#5,10,10
mapa_fase_5.addSpawn( (19,1), [120,120] , [16000,61300] , (0,0) , [enemy3,enemy9] , [(25,25),(25,25)] , [8,8] , [False]*2 , [1,1] , [0.5,0.5] , [300,1350] ,[False,False],[3,4], [mov_5_G] *2, [(1,0),(1,0)] ,[3,9], [50,50])#3,9
mapa_fase_5.addSpawn( (0,1), [120,120] , [16000,61300] , (0,0) , [enemy3,enemy9] , [(25,25),(25,25)] , [8,8] , [False]*2 , [1,1] , [0.5,0.5] , [300,1350] ,[False,False],[3,4], [mov_5_H] *2, [(1,0),(1,0)] ,[3,9], [50,50])
mapa_fase_5.addSpawn( (19,9), [120,120] , [23900,46900] , (0,0) , [enemy4,enemy7] , [(22,22),(20,20)] , [8,8] , [False]*2 , [1,1] , [0.5,0.5] , [180,1080] ,[True,False],[1,3], [mov_5_I] *2, [(1,0),(1,0)] ,[4,5], [50,50])#4,7
mapa_fase_5.addSpawn( (4,12), [120,120] , [23900,46900] , (0,0) , [enemy4,enemy7] , [(22,22),(20,20)] , [8,8] , [False]*2 , [1,1] , [0.5,0.5] , [180,1080] ,[True,False],[1,3], [mov_5_J] *2, [(1,0),(1,0)] ,[4,5], [50,50])

mapa_fase_5.addTarget((8,5),(0,0))
mapa_fase_5.addTarget((11,5),(0,0))
mapa_fase_5.addTarget((8,8),(0,0))
mapa_fase_5.addTarget((11,8),(0,0))

mapa_fase_5.mapa[1][0][0].addPiece(animacaoPerene(animacaoSprite(pygame.image.load(dir_image+'trono.png').convert_alpha(),(80,320),6,False,(40*9,40*3))))
#mapa_fase_5.mapa[1][4][10].addPiece(bloqueioPerene())

for y in range(6):
    mapa_fase_5.mapa[1][4+y][9].addPiece(bloqueioPerene())
    mapa_fase_5.mapa[1][4+y][10].addPiece(bloqueioPerene())

fase_5.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)
fase_5.addItem(controlesExtras(fase_5,True, mapa_fase_5))
fase_5.addItem(gameOver(fase_5,game_over,mapa_fase_5,game_over_music))
fase_5.addItem(winnerScreen(fase_5,scr_intermediaria,mapa_fase_5,blit_score,winner_music))

###fase 4###
#quantidades de cada horda
#vida de cada horda
#mana de cada horda
fator_4=2000
mapa_fase_4.addSpawn((1, 12),[120]*10 , [fator_4*7  ,fator_4*8,fator_4*13,fator_4*20,fator_4*27,fator_4*33,fator_4*34,fator_4*36,fator_4*37,fator_4*45] , (0,0) , [enemy1,enemy2,enemy2,enemy4,enemy5,enemy6,enemy7,enemy7,enemy8,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(20,20),(22,22),(20,20)] , [8]*10 , [False]*10 , [1,1,1,1,1,1,1,1,1,25] , [0.5]*10 , [100,180,180,180,600,850,1200,1200,600,15000] ,[False,False,False,True,False,False,False,False,True,False],[0,2,2,1,2,4,3,3,0,0], [mov_4_A_1,mov_4_A_1,mov_4_A_2,mov_4_A_1,mov_4_A_1,mov_4_A_1,mov_4_A_1,mov_4_A_1,mov_4_A_1,mov_4_A_2] , [(1,0)]*10 ,[1,2,2,4,5,6,7,7,8,150], [10,10,10,10,10,10,10,10,10,1])#10

mapa_fase_4.addSpawn((4, 12),[120]*13 , [fator_4*2  ,fator_4*8,fator_4*11,fator_4*14,fator_4*21,fator_4*25,fator_4*26,fator_4*29,fator_4*31,fator_4*38,fator_4*39,fator_4*41,fator_4*42] , (0,0) , [enemy1,enemy2,enemy2,enemy3,enemy4,enemy5,enemy5,enemy6,enemy6,enemy8,enemy8,enemy9,enemy9] , [(20,20),(25,25),(25,25),(25,25),(22,22),(22,22),(22,22),(25,25),(25,25),(22,22),(22,22),(25,25),(25,25)] , [8]*13 , [False]*13 , [1,1,1,1,1,1,1,1,1,1,1,1,1] , [0.5]*13 , [100,180,180,380,180,600,600,850,850,600,600,1600,1600] ,[False,False,False,False,True,False,False,False,False,True,True,False,False],[0,2,2,3,1,2,2,4,4,0,0,0,0], [mov_4_B_1,mov_4_B_1,mov_4_B_2,mov_4_B_1,mov_4_B_2,mov_4_B_2,mov_4_B_1,mov_4_B_2,mov_4_B_1,mov_4_B_2,mov_4_B_1,mov_4_B_2,mov_4_B_1] , [(1,0)]*13 ,[1,2,2,3,4,5,5,6,6,8,8,9,9], [10,10,10,10,10,10,10,10,10,10,10,10,10])#13 hordas
mapa_fase_4.addSpawn((5, 12),[120]*8  , [fator_4*5  ,fator_4*9,fator_4*16,fator_4*23,fator_4*28,fator_4*32,fator_4*35,fator_4*40] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy9] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(25,25)] , [8]*8 , [False]*8 , [1,1,1,1,1,1,1,1] , [0.5]*8 , [100,180,380,180,600,850,1200,1600] ,[False,False,False,True,False,False,False,False],[0,2,3,1,2,4,3,4], [mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C,mov_4_C] , [(1,0)]*8 ,[1,2,3,4,5,6,7,9], [10,10,10,10,10,10,10,10])#8

mapa_fase_4.addSpawn((8, 12),[120]*6  , [800        ,fator_4*9 ,fator_4*19,fator_4*21,fator_4*25,fator_4*41] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy9] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25)] , [8]*6 , [False]*6 , [1,1,1,1,1,1] , [0.5]*6 , [100,180,380,180,600,1600] ,[False,False,False,True,False,False],[0,2,3,1,2,4],  [mov_4_D,mov_4_D,mov_4_D,mov_4_D,mov_4_D,mov_4_D] , [(1,0)]*6 ,[1,2,3,4,5,9], [10,10,10,10,10,10])#6
mapa_fase_4.addSpawn((9, 12),[120]*9  , [fator_4*4  ,fator_4*10,fator_4*17,fator_4*22,fator_4*30,fator_4*34,fator_4*36,fator_4*37,fator_4*43] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy6,enemy7,enemy7,enemy8,enemy9] , [(20,20),(25,25),(25,25),(22,22),(25,25),(20,20),(20,20),(22,22),(25,25)] , [8]*9 , [False]*9 , [1,1,1,1,1,1,1,1,1] , [0.5]*9 , [100,180,380,180,850,1200,1200,600,1600] ,[False,False,False,True,False,False,False,True,False],[0,2,3,1,4,3,3,0,4], [mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E,mov_4_E] , [(1,0)]*9 ,[1,2,3,4,6,7,7,8,9], [10,10,10,10,10,10,10,10,10])#9
mapa_fase_4.addSpawn((10, 12),[120]*9 , [fator_4*4  ,fator_4*13,fator_4*18,fator_4*22,fator_4*30,fator_4*34,fator_4*35,fator_4*38,fator_4*43] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy6,enemy7,enemy7,enemy8,enemy9] , [(20,20),(25,25),(25,25),(22,22),(25,25),(20,20),(20,20),(22,22),(25,25)] , [8]*9 , [False]*9 , [1,1,1,1,1,1,1,1,1] , [0.5]*9 , [100,180,380,180,850,1200,1200,600,1600] ,[False,False,False,True,False,False,False,True,False],[0,2,3,1,4,3,3,0,4], [mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F,mov_4_F] , [(1,0)]*9 ,[1,2,3,4,6,7,7,8,9], [10,10,10,10,10,10,10,10,10])#9
mapa_fase_4.addSpawn((11, 12),[120]*6 , [fator_4+400,fator_4*12,fator_4*16,fator_4*24,fator_4*27,fator_4*44] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy9] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25)] , [8]*6 , [False]*6 , [1,1,1,1,1,1] , [0.5]*6 , [100,180,380,180,600,1600] ,[False,False,False,True,False,False],[0,2,3,1,2,4], [mov_4_G,mov_4_G,mov_4_G,mov_4_G,mov_4_G,mov_4_G] , [(1,0)]*6 ,[1,2,3,4,5,9], [10,10,10,10,10,10])#6

mapa_fase_4.addSpawn((14, 12),[120]*8 , [fator_4*6  ,fator_4*12,fator_4*19,fator_4*20,fator_4*28,fator_4*32,fator_4*36,fator_4*40] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy9] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(25,25)] , [8]*8 , [False]*8 , [1,1,1,1,1,1,1,1] , [0.5]*8 , [100,180,380,180,600,850,1200,1600] ,[False,False,False,True,False,False,False,False],[0,2,3,1,2,4,3,4], [mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H,mov_4_H] , [(1,0)]*8 ,[1,2,3,4,5,6,7,9], [10,10,10,10,10,10,10,10])#8
mapa_fase_4.addSpawn((15, 12),[120]*13, [fator_4*3  ,fator_4*8,fator_4*11,fator_4*15,fator_4*24,fator_4*26,fator_4*27,fator_4*29,fator_4*31,fator_4*37,fator_4*39,fator_4*42,fator_4*44] , (0,0) , [enemy1,enemy2,enemy2,enemy3,enemy4,enemy5,enemy5,enemy6,enemy6,enemy8,enemy8,enemy9,enemy9] , [(20,20),(25,25),(25,25),(25,25),(22,22),(22,22),(22,22),(25,25),(25,25),(22,22),(22,22),(25,25),(25,25)] , [8]*13 , [False]*13 , [1,1,1,1,1,1,1,1,1,1,1,1,1] , [0.5]*13 , [100,180,180,380,180,600,600,850,850,600,600,1600,1600] ,[False,False,False,False,True,False,False,False,False,True,True,False,False],[0,2,2,3,1,2,2,4,4,0,0,0,0], [mov_4_I_1,mov_4_I_2,mov_4_I_1,mov_4_I_1,mov_4_I_2,mov_4_I_1,mov_4_I_2,mov_4_I_2,mov_4_I_1,mov_4_I_2,mov_4_I_1,mov_4_I_1,mov_4_I_2] , [(1,0)]*13 ,[1,2,2,3,4,5,5,6,6,8,8,9,9], [10,10,10,10,10,10,10,10,10,10,10,10,10])#13

mapa_fase_4.addSpawn((18, 12),[120]*10 ,[fator_4*7  ,fator_4*10,fator_4*11,fator_4*23,fator_4*25,fator_4*33,fator_4*34,fator_4*35,fator_4*38,fator_4*45] , (0,0) , [enemy1,enemy2,enemy2,enemy4,enemy5,enemy6,enemy7,enemy7,enemy8,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(20,20),(22,22),(20,20)] , [8]*10 , [False]*10 , [1,1,1,1,1,1,1,1,1,25] , [0.5]*10 , [100,180,180,180,600,850,1200,1200,600,15000] ,[False,False,False,True,False,False,False,False,True,False],[0,2,2,1,2,4,3,3,0,0], [mov_4_J_1,mov_4_J_2,mov_4_J_1,mov_4_J_1,mov_4_J_1,mov_4_J_1,mov_4_J_1,mov_4_J_1,mov_4_J_1,mov_4_J_2] , [(1,0)]*10 ,[1,2,2,4,5,6,7,7,8,150], [10,10,10,10,10,10,10,10,10,1])#10

for x in range(3,17,1):
    mapa_fase_4.addTarget((x,1),(0,0))

fase_4.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)
fase_4.addItem(controlesExtras(fase_4,True, mapa_fase_4))
fase_4.addItem(gameOver(fase_4,game_over,mapa_fase_4,game_over_music))
fase_4.addItem(winnerScreen(fase_4,winner_scr,mapa_fase_4,blit_score,winner_music))


###fase 3### balanceada(OK)

mapa_fase_3.addSpawn( (0,11), [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [False]*10 , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,200,550,800,1280,700,1650,14000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,0,2,1,4,3,0], [mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A,mov_3_A] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [30,20,10,15,10,20,20,30,10,1])
mapa_fase_3.addSpawn( (19,11), [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [False]*10 , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,200,550,800,1280,700,1650,14000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,3,1,0,2,1,4,3,0], [mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B,mov_3_B] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [30,20,10,15,10,20,20,30,10,1])
mapa_fase_3.addTarget((9,9),(0,0))
mapa_fase_3.addTarget((10,9),(0,0))
mapa_fase_3.mapa[1][7][9].addPiece(animacaoPerene(animacaoSprite(pygame.image.load(dir_image+'fontedavida.png').convert_alpha(),(160,160),6,False,(40*8,40*5))))
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

fase_3.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)
fase_3.addItem(controlesExtras(fase_3,True, mapa_fase_3))
fase_3.addItem(gameOver(fase_3,game_over,mapa_fase_3,game_over_music))
fase_3.addItem(winnerScreen(fase_3,winner_scr,mapa_fase_3,blit_score,winner_music))

###fase 2### balanceada (OK)
mapa_fase_2.addSpawn( (0,3) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [False]*10 , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,200,400,200,550,800,1280,600,1550,13000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A,mov_2_A] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])#[1,1,1,1,1,1,1,1,1,1]
mapa_fase_2.addSpawn( (0,2) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (0,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [False]*10 , [1,1,1,1,1,1,1,1,1,15] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [100,200,400,200,550,800,1280,600,1550,13000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B,mov_2_B] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])#[0,0,0,0,0,0,0,0,0,0]
mapa_fase_2.addTarget((19,3),(0,0))
mapa_fase_2.addTarget((19,2),(0,0))


mapa_fase_2.mapa[1][1][4].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*4,40*0))))
mapa_fase_2.mapa[1][1][16].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*16,40*0))))
mapa_fase_2.mapa[1][9][19].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*19,40*8))))
mapa_fase_2.mapa[1][12][15].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*15,40*11))))
mapa_fase_2.mapa[1][12][7].addPiece(animacaoPerene(animacaoSprite(tree_1,(40,80),6,False,(40*7,40*11))))
mapa_fase_2.mapa[1][9][8].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*8,40*8))))
mapa_fase_2.mapa[1][0][7].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*0,40*6))))
mapa_fase_2.mapa[1][1][14].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*14,40*0))))
mapa_fase_2.mapa[1][1][3].addPiece(animacaoPerene(animacaoSprite(tree_2,(40,80),6,False,(40*3,40*0))))

mapa_fase_2.mapa[1][4][1].addPiece(animacaoPerene(animacaoSprite(casa,(80,80),6,False,(40*1,40*4))))
mapa_fase_2.mapa[1][4][2].addPiece(bloqueioPerene())
mapa_fase_2.mapa[1][5][2].addPiece(bloqueioPerene())
mapa_fase_2.mapa[1][5][1].addPiece(bloqueioPerene())

mapa_fase_2.mapa[1][4][18].addPiece(animacaoPerene(animacaoSprite(casa,(80,80),6,False,(40*18,40*4))))
mapa_fase_2.mapa[1][4][19].addPiece(bloqueioPerene())
mapa_fase_2.mapa[1][5][19].addPiece(bloqueioPerene())
mapa_fase_2.mapa[1][5][18].addPiece(bloqueioPerene())

mapa_fase_2.mapa[1][1][9].addPiece(animacaoPerene(animacaoSprite(casa,(80,80),6,False,(40*9,40*1))))
mapa_fase_2.mapa[1][1][10].addPiece(bloqueioPerene())
mapa_fase_2.mapa[1][2][10].addPiece(bloqueioPerene())
mapa_fase_2.mapa[1][2][9].addPiece(bloqueioPerene())

mapa_fase_2.mapa[1][8][10].addPiece(animacaoPerene(animacaoSprite(casa,(80,80),6,False,(40*10,40*8))))
mapa_fase_2.mapa[1][8][11].addPiece(bloqueioPerene())
mapa_fase_2.mapa[1][9][11].addPiece(bloqueioPerene())
mapa_fase_2.mapa[1][9][10].addPiece(bloqueioPerene())

fase_2.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)#,texto_viking,texto_arqueiro,texto_berserker,texto_valquiria
fase_2.addItem(controlesExtras(fase_2,True,mapa_fase_2))
fase_2.addItem(gameOver(fase_2,game_over,mapa_fase_2,game_over_music))
fase_2.addItem(winnerScreen(fase_2,winner_scr,mapa_fase_2,blit_score,winner_music))

###fase 1### balanceada (OK)
mapa_fase_1.addSpawn( (0,6), [120,120,120,120] , [400,1000,2000,3800], (0,0), [enemy3,enemy4,enemy6,enemy8],[(25,25),(22,22),(25,25),(22,22)],[8,8,8,8,8,8,8,8,8,8],[True,False,True,False],[1,1,1,1],[0.5,0.5,0.5,0.5],[400,400,2000,1250],[False,True,False,True],[0,0,0,0],[mov_1_A,mov_1_B,mov_1_A,mov_1_B],[(1,0),(1,0),(1,0),(1,0)],[50,50,75,200],[1,1,1,1])
mapa_fase_1.addTarget((19,6),(0,0))
fase_1.addItem(botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,tecla_viking,tecla_arqueiro,tecla_berserker,tecla_valquiria,tecla_x1,tecla_x2,tecla_x3,accelx1,accelx2,accelx3)#,texto_viking,texto_arqueiro,texto_berserker,texto_valquiria

tutorial_fase_1=tutorialGame(mapa_fase_1,dinB_22,
             [['Clique no botão do Viking',
               'para chamar o Viking.'],
              ['Agora mande-o para uma ',
               'posição válida do campo de batalha.',
               'Tente esta.'],
              ['O próximo inimigo é voador,',
               'com a sua Mana atual de 50 pontos',
               'o ideal é escolher a Arqueira'],
              ['Mande a Arqueira para a posição mais',
               'próxima possível ao foco da invasão.'],
              ['Avistamos um inimigo com uma rígida',
               'carapaça se aproximar, acho que só',
               'o grande Berserker pode nos ajudar.'],
              ['Seu machado terá mais glória ao',
               'enfrentar os inimigos aqui.'],
              ['Outro inimigo voador, mas agora',
               'seus 75 pontos de Mana permitem',
               'chamar a Valquíria ao campo'],
              ['Não temos muitas escolhas, esta',
               'é a sua última posição possível.',
               'Você só tem 1 ponto de Vida, espero que dê tempo.']],
             [pygame.Rect(0,520,80,80),pygame.Rect(80,240,40,40),
              pygame.Rect(80,520,80,80),pygame.Rect(280,240,40,40),
              pygame.Rect(160,520,80,80),pygame.Rect(480,240,40,40),
              pygame.Rect(240,520,80,80),pygame.Rect(680,240,40,40)]
             )
             #6*40 ->2*40, 7*40, 12*40, 17*40

fase_1.addItem(tutorial_fase_1)

fase_1.addItem(controlesExtras(fase_1,True,mapa_fase_1))
fase_1.addItem(gameOver(fase_1,game_over,mapa_fase_1,game_over_music))
fase_1.addItem(winnerScreen(fase_1,winner_scr,mapa_fase_1,blit_score,winner_music))

###>>>TELAS<<<###

###seleção de fases###

selecao_fase = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_1,botao_2,botao_3,botao_4,botao_5)
#selecao_fase.addItem(area_fases_extras,botao_A,botao_B,botao_C,botao_D,botao_E,botao_F,botao_G)
selecao_fase.setTitle("Asgard Defense")
selecao_fase.setImage(pygame.image.load(dir_image+"stageselect.png").convert(),(0,0))
selecao_fase.setMusic(dir_music+"Teller of the Tales.mp3",-1, 0.0)
###tela options###
texto_confirmacao=pyTreeBee.linkedButton(None,dinB_22,["      TENS CERTEZA DE QUE É SÁBIO", "APAGAR TODO O VOSSO PROGRESSO?"],210,220,pygame.Rect(0,0,0,0),0,0)
texto_confirmacao.setAll_TextColor((255,255,255))
tela_confirma_exclusao=pyTreeBee.dynamicScreen((800,600),60,(0,0,0),texto_confirmacao)
tela_confirma_exclusao.setTitle("Asgard Defense")
botao_apagar=pyTreeBee.linkedButton(tela_confirma_exclusao,din_12,[""],400-(280/2)+12,400,pygame.Rect(0,0,280-12,60-12),0,0)
botao_apagar.setEach_Image(pygame.image.load(dir_image+'botao_apagar1.png').convert_alpha(),pygame.image.load(dir_image+'botao_apagar2.png').convert_alpha(),pygame.image.load(dir_image+'botao_apagar3.png').convert_alpha())
botao_apagar.setAll_BarSize((-6,-6))

margem_volume_y=100
texto_volume=escritorDireto(dinBd_32.render("VOLUME",True,(255,255,255)),(342,105+margem_volume_y))
escreve_volume=renderVolume(dinB_22,(255,255,255),(384,115+62+margem_volume_y),100)
aumenta_volume=pyTreeBee.linkedButton(volumeControl(+0.02),dinB_22,[""],500-26,162+margem_volume_y,pygame.Rect(0,0,60,60),15,5,pygame.image.load(dir_image+"botao_mais.png").convert_alpha())
diminui_volume=pyTreeBee.linkedButton(volumeControl(-0.02),dinB_22,[""],300-26,162+margem_volume_y,pygame.Rect(0,0,60,60),15,5,pygame.image.load(dir_image+"botao_menos.png").convert_alpha())

tela_options=pyTreeBee.dynamicScreen((800,600),60,(0,0,0),botao_apagar,texto_volume,escreve_volume,aumenta_volume,diminui_volume,escritorDireto(dinB_72.render("OPTIONS",True,(200,200,200)),(260,50)))
tela_options.setTitle("Asgard Defense")
tela_pause.addItem(texto_volume,escreve_volume,aumenta_volume,diminui_volume,escritorDireto(dinB_72.render("PAUSE",True,(200,200,200)),(295,50)))

confirma_sim=pyTreeBee.linkedButton(deleteSave(tela_options),din_12,[""],250,300,pygame.Rect(0,0,130-12,60-12),0,0)
confirma_sim.setEach_Image(pygame.image.load(dir_image+'botao_sim1.png').convert_alpha(),pygame.image.load(dir_image+'botao_sim2.png').convert_alpha(),pygame.image.load(dir_image+'botao_sim3.png').convert_alpha())
confirma_sim.setAll_BarSize((-6,-6))
confirma_nao=pyTreeBee.linkedButton(tela_options,din_12,[""],420,300,pygame.Rect(0,0,130-12,60-12),0,0)
confirma_nao.setEach_Image(pygame.image.load(dir_image+'botao_nao1.png').convert_alpha(),pygame.image.load(dir_image+'botao_nao2.png').convert_alpha(),pygame.image.load(dir_image+'botao_nao3.png').convert_alpha())
confirma_nao.setAll_BarSize((-6,-6))
tela_confirma_exclusao.addItem(confirma_sim,confirma_nao)
###tela staff###
tela_staff=pyTreeBee.dynamicScreen((800,600),60,(0,0,0))
tela_staff.setTitle("Asgard Defense")
tela_staff.setImage(pygame.image.load(dir_image+"credits.png").convert(),(0,0))
###tela tutorial###
tela_tutorial=pyTreeBee.dynamicScreen((800,600),60,(0,0,0))
tela_tutorial.setTitle("Asgard Defense")
tela_tutorial.setImage(pygame.image.load(dir_image+"tutorial.png").convert(),(0,0))
###tela inicial###
#> letreiro

#> viking
#pescoco=pyTreeBee.linkedButton(None,din_12,[""],0,438,pygame.Rect(0,0,0,0),0,0, pygame.transform.scale(pygame.image.load(dir_image+"pescoco 2.png"),(437,162)))
#cabeca=pyTreeBee.linkedButton(None,arial,[""],0,63,pygame.Rect(0,0,0,0),0,0,  pygame.transform.scale(pygame.image.load(dir_image+"cabeca 4.png"),(357,523)))
#olho=animacaoSprite(pygame.transform.scale(pygame.image.load(dir_image+"olho_spritesheet 2.png"),(760,75)),(190,75),6,True,(90,290))
#olho.setPause(60)
#espada=animacaoSprite(pygame.transform.scale(pygame.image.load(dir_image+"espada_spritesheet.png"),(4800,600)),(800,600),10,True,(0,0))
#espada.setStop(1)

identa_botoes_x=0
identa_botoes_y=-100

hover_som=pygame.mixer.Sound(dir_music+"metal-short-tick.aiff")
selected_som=pygame.mixer.Sound(dir_music+"shield-hit-1.wav")
#> start
botao_start=pyTreeBee.linkedButton(selecao_fase,din_12,[""],800+identa_botoes_x,300+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_start.setEach_Image(pygame.image.load(dir_image+"start1.png").convert_alpha(),pygame.image.load(dir_image+"start2.png").convert_alpha(),pygame.image.load(dir_image+"start3.png").convert_alpha())
botao_start.setAll_BarSize((-10,-10))
botao_start.setEach_Sound(hover_som,selected_som)
#> options
botao_options=pyTreeBee.linkedButton(tela_options,din_12,[""],800+identa_botoes_x,380+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_options.setEach_Image(pygame.image.load(dir_image+"options1.png").convert_alpha(),pygame.image.load(dir_image+"options2.png").convert_alpha(),pygame.image.load(dir_image+"options3.png").convert_alpha())
botao_options.setAll_BarSize((-10,-10))
botao_options.setEach_Sound(hover_som,selected_som)
#> tutorial
botao_tutorial=pyTreeBee.linkedButton(tela_tutorial,din_12,[''],800+identa_botoes_x,460+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_tutorial.setEach_Image(pygame.image.load(dir_image+"tutorial1.png").convert_alpha(),pygame.image.load(dir_image+"tutorial2.png").convert_alpha(),pygame.image.load(dir_image+"tutorial3.png").convert_alpha())
botao_tutorial.setAll_BarSize((-10,-10))
botao_tutorial.setEach_Sound(hover_som,selected_som)
#> staff
botao_staff=pyTreeBee.linkedButton(tela_staff,din_12,[""],800+identa_botoes_x,540+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_staff.setEach_Image(pygame.image.load(dir_image+"staff1.png").convert_alpha(),pygame.image.load(dir_image+"staff2.png").convert_alpha(),pygame.image.load(dir_image+"staff3.png").convert_alpha())
botao_staff.setAll_BarSize((-10,-10))
botao_staff.setEach_Sound(hover_som,selected_som)
#> tela
tela_inicial = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_start,botao_options,botao_staff,botao_tutorial)#,pescoco,cabeca,olho,espada
tela_inicial.setTitle("Asgard Defense")
tela_inicial.setImage(pygame.image.load(dir_image+"Abertura Nova.png").convert(),(0,0))
tela_inicial.addItem(controlesExtras(tela_inicial,False))
fadeIn(tela_inicial,tela_inicial,[botao_start,(500+identa_botoes_x,300+identa_botoes_y),10],[botao_options,(500+identa_botoes_x,380+identa_botoes_y),15],[botao_tutorial,(500+identa_botoes_x,460+identa_botoes_y),20],[botao_staff,(500+identa_botoes_x,540+identa_botoes_y),25])#[pescoco,(500,500),40],[cabeca,(0,0),40],[espada,(0,600),100]
#botao_start.link=fadeOut(tela_inicial,selecao_fase,[botao_start,(800+identa_botoes_x,300+identa_botoes_y),10],[botao_options,(800+identa_botoes_x,380+identa_botoes_y),15],[botao_tutorial,(800+identa_botoes_x,460+identa_botoes_y),20],[botao_staff,(800+identa_botoes_x,540+identa_botoes_y),25])
###botões de voltar adicionados às telas anteriores###

voltar_som=pygame.mixer.Sound(dir_music+"sword-sheath.wav")


img_voltar_1=pygame.image.load(dir_image+"botao_voltar1.png").convert_alpha()
img_voltar_2=pygame.image.load(dir_image+"botao_voltar2.png").convert_alpha()
img_voltar_3=pygame.image.load(dir_image+"botao_voltar3.png").convert_alpha()


voltar_para_inicio=pyTreeBee.linkedButton(tela_inicial,din_12,[""],655,530,pygame.Rect(0,0,130-12,60-12),0,0)
voltar_para_inicio.setEach_Image(img_voltar_1,img_voltar_2,img_voltar_3)
voltar_para_inicio.setAll_BarSize((-6,-6))
voltar_para_inicio.setSelect_Sound(voltar_som)
voltar_para_inicio.setSound_Time(0.2)

tela_options.addItem(voltar_para_inicio)
tela_staff.addItem(voltar_para_inicio)
tela_tutorial.addItem(voltar_para_inicio)

voltar_para_inicio_musica=pyTreeBee.linkedButton(linkedMusic(tela_inicial,dir_music+"Five Armies.mp3", -1, 0.0),din_12,[""],800-130+12-27,600-60+12-22,pygame.Rect(0,0,130-12,60-12),0,0)# 27-12,530-12 para ficar no canto inferior direito
voltar_para_inicio_musica.setEach_Image(img_voltar_1,img_voltar_2,img_voltar_3)
voltar_para_inicio_musica.setAll_BarSize((-6,-6))
voltar_para_inicio_musica.setSelect_Sound(voltar_som)
voltar_para_inicio_musica.setSound_Time(0.2)

selecao_fase.addItem(voltar_para_inicio_musica)

cir_voltar_1=pygame.image.load(dir_image+"botao_menu1.png").convert_alpha()
cir_voltar_2=pygame.image.load(dir_image+"botao_menu2.png").convert_alpha()
cir_voltar_3=pygame.image.load(dir_image+"botao_menu3.png").convert_alpha()

cir_fases_1=pygame.image.load(dir_image+"botao_avancar1.png").convert_alpha()
cir_fases_2=pygame.image.load(dir_image+"botao_avancar2.png").convert_alpha()
cir_fases_3=pygame.image.load(dir_image+"botao_avancar3.png").convert_alpha()

cir_retry_1=pygame.image.load(dir_image+"botao_retry1.png").convert_alpha()
cir_retry_2=pygame.image.load(dir_image+"botao_retry2.png").convert_alpha()
cir_retry_3=pygame.image.load(dir_image+"botao_retry3.png").convert_alpha()

voltar_retry_pause=pyTreeBee.linkedButton(linkedZero(None),din_12,[""],220,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_retry_pause.setEach_Image(cir_retry_1,cir_retry_2,cir_retry_3)
voltar_retry_pause.setAll_BarSize((-12,-12))
voltar_menu_pause=pyTreeBee.linkedButton(linkedZero(tela_inicial,(dir_music+"Five Armies.mp3", -1, 0.0)),din_12,[""],375,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_menu_pause.setEach_Image(cir_voltar_1,cir_voltar_2,cir_voltar_3)
voltar_menu_pause.setAll_BarSize((-12,-12))
voltar_selecao_pause=pyTreeBee.linkedButton(linkedZero(selecao_fase),din_12,[""],530,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_selecao_pause.setEach_Image(cir_fases_1,cir_fases_2,cir_fases_3)
voltar_selecao_pause.setAll_BarSize((-12,-12))
tela_pause.addItem(voltar_retry_pause,voltar_menu_pause,voltar_selecao_pause)

voltar_retry=pyTreeBee.linkedButton(None,din_12,[""],220,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_retry.setEach_Image(cir_retry_1,cir_retry_2,cir_retry_3)
voltar_retry.setAll_BarSize((-12,-12))
voltar_menu=pyTreeBee.linkedButton(linkedMusic(tela_inicial,dir_music+"Five Armies.mp3", -1, 0.0),din_12,[""],375,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_menu.setEach_Image(cir_voltar_1,cir_voltar_2,cir_voltar_3)
voltar_menu.setAll_BarSize((-12,-12))
voltar_selecao=pyTreeBee.linkedButton(selecao_fase,din_12,[""],530,450,pygame.Rect(0,0,80-25,80-25),0,0)
voltar_selecao.setEach_Image(cir_fases_1,cir_fases_2,cir_fases_3)
voltar_selecao.setAll_BarSize((-12,-12))
game_over.addItem(voltar_menu,voltar_selecao,voltar_retry)
winner_scr.addItem(voltar_menu,voltar_selecao,voltar_retry)
seguir_congratulation=pyTreeBee.linkedButton(unlockerLink(congratulations_scr,congratulado),din_12,[""],375,450,pygame.Rect(0,0,80-25,80-25),0,0)
seguir_congratulation.setEach_Image(cir_fases_1,cir_fases_2,cir_fases_3)
seguir_congratulation.setAll_BarSize((-12,-12))
very_winner_scr.addItem(seguir_congratulation)
congratulations_scr.addItem(voltar_para_inicio_musica)
'''
voltar_selecao.link=fadeOut(tela_inicial,tela_inicial,[botao_start,(500,300),10],[botao_options,(500,380),15],[botao_staff,(500,460),20])
selecao_fase.addItem(voltar_selecao)
'''
#fase_1.addItem(pyTreeBee.linkedButton(selecao_fase,din_12,["Voltar"],600,530,pygame.Rect(0,0,50,20),0,0))
### loading save ###

load_fases_liberadas=[congratulado,botao_2,botao_3,botao_4,botao_5]#,area_fases_extras,botao_A,botao_B,botao_C,botao_D,botao_E,botao_F,botao_G]

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
time.sleep(0.1)

pyTreeBee.treeBeeStart(tela_inicial)

loading=dinB_22.render("SAVING...",True,(255,255,255))
temporarydisplay.fill((0,0,0))
temporarydisplay.blit(loading,(370,278))
pygame.display.update()
time.sleep(0.1)
### dumping save ###
saveAll()

pygame.quit()

