# -*- coding: cp1252 -*-
import pyTreeBee,pygame,sys,os,time, pygame.mixer
from pygame.locals import*
infoObject = pygame.display.Info()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((infoObject.current_w//2)-400, (infoObject.current_h//2)-300)
temporarydisplay=pygame.display.set_mode((800,600))
arialBlack=pygame.font.SysFont("Arial Black",22)

loading=arialBlack.render("LOADING...",True,(255,255,255))
temporarydisplay.blit(loading,(0,0))
pygame.display.update()

frame_atual=0
arial=pygame.font.SysFont("Arial",12)
arial12b=pygame.font.SysFont("Arial Black",12)
pygame.mixer.init()

#musica inicial, precisa dela pros botões de voltar cuidarem disso.
pygame.mixer.music.load("Five Armies.mp3")
pygame.mixer.music.play(-1, 0.0)

class linkedMusic(object):
    def __init__(self, link, music, repeat, start_time):
        self.link=link
        self.music=music
        self.repeat=repeat
        self.start_time=start_time
    def linkReply(self,prevscr):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(self.repeat,self.start_time)
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
    def __init__(self,size,player):
        self.player=player
        self.x=1
        self.y=1
        self.sprite=animacaoSprite(pygame.image.load("selecao4.png"),(40,40),9,True)
        self.size=size
        self.buttonup=False
        self.dentro=True
        self.botaodireito=False
        self.botaoesquerdo=False
        self.nullSelection()
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
                        if mapa[1][self.y][self.x].numID>=3 and mapa[1][self.y][self.x].numID<=11:
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
    def fightControls(self,mapa):
        global frame_atual
        if self.pause and frame_atual%self.pause_time[self.contador-1]==0:
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
    def __init__(self,player,mapa,imagens,size):
        self.alingment=(0,0)
        self.player=player
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
        self.selecao=quadradoControlavel(self.size,self.player)
    def addSpawn(self,pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,manas,quantidades):
        self.mapa[1][pos[1]][pos[0]].piece=spawnInimigo(pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,manas,quantidades)
    def addTarget(self,plr,pos, sentido=None):
        self.mapa[1][pos[1]][pos[0]].piece=lifeTarget(plr,pos,sentido)
    def blitOn(self,screen):
        for z in range(len(self.mapa)):                                
            for y in range(len(self.mapa[z])):
                for x in range(len(self.mapa[z][y])):
                    if self.mapa[z][y][x].piece!=None:
                        try:
                            self.mapa[z][y][x].piece.movimentoPadrao(self.mapa,self.size)
                        except:
                            self.mapa[z][y][x].piece.fightControls(self.mapa)
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
                        screen.blit(self.mapa[1][y][x].piece.sprite.getNextImage(), (self.alingment[0]+(x*self.size)+alinhaspriteX,self.alingment[1]+(y*self.size)+alinhaspriteY))
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
        screen.blit(arial.render("VIDAS:",True,(255,255,255)),(740,0))
        screen.blit(arialBlack.render(str(self.player.life),True,cor_vida),(740,10))
        screen.blit(arial.render("SCORE:",True,(255,255,255)),(32,0))
        screen.blit(arialBlack.render(str(self.player.score),True,(255,255,255)),(32,10))
        screen.blit(arial.render("MANA:",True,(255,255,255)),(680,0))
        screen.blit(arialBlack.render(str(self.player.mana),True,(10,125,255)),(680,10))
        self.selecao.blitOn(screen)
        
    def keyControls(self,event):
        self.selecao.keyControls(event,self.mapa, self.alingment)
        return False

class winnerScreen(object):
    def __init__(self,tela,link,player,qnt_inimigos):
        self.tela=tela
        self.link=link
        self.retorno=None
        self.player=player
        self.inimigos=qnt_inimigos
    def blitOn(self,scr):
        if self.player.maxlife-self.player.life+self.player.score==self.inimigos:
            self.tela.linkcalled=self.link
    def keyControls(self,event):
        pass

class gameOver(object):
    def __init__(self,tela,link,player):
        self.tela=tela
        self.link=link
        self.retorno=False
        self.player=player
    def blitOn(self,scr):
        global frame_atual
        if self.retorno!=False: frame_atual=0
        if self.player.life<=0:
            self.tela.linkcalled=self.link
    def keyControls(self,event):
        return self.retorno

class statusPlayer(object):
    def __init__(self,vida, mana):
        self.life=vida
        self.maxlife=vida
        self.mana=mana
        self.score=0
        self.counter=0

class controlesExtras(object):
    def __init__(self,tela):
        self.tela=tela
        self.frame_skip=1
    def blitOn(self,screen):
        global frame_atual
        frame_atual+=self.frame_skip
    def keyControls(self,event):
        if event.type==KEYUP:
            if event.key==K_ESCAPE:
                self.tela.storedlink=None
                self.tela.running=False
        return False

        
#matriz seletora de tiles
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
#tela gameover e player
player=statusPlayer(30,70)
game_over=pyTreeBee.dynamicScreen((800,600), 30,(100,0,0))
game_over.setImage(pygame.image.load('gameover.png'),(0,0))
winner_scr=pyTreeBee.dynamicScreen((800,600), 30,(100,100,255))
winner_scr.setImage(pygame.image.load('vitoria.png'),(0,0))
#loading dos tiles
tile_grama=pygame.image.load("tileset_grama.png").convert()
tiles_fase_1=[pygame.image.load("mapacaminho6.png").convert(),pygame.image.load("mapaentrada3.png").convert(),pygame.image.load("mapasaida3.png").convert()]#,tile_grama.subsurface((40,40),(40,40)),tile_grama.subsurface((40,80),(40,40)),tile_grama.subsurface((0,80),(40,40)),tile_grama.subsurface((80,80),(40,40)),tile_grama.subsurface((80,0),(40,40)),tile_grama.subsurface((0,0),(40,40)),tile_grama.subsurface((40,40),(0,40)),tile_grama.subsurface((40,0),(40,40)),tile_grama.subsurface(
for w in range(3):
    for h in range(3):
        tiles_fase_1.append(tile_grama.subsurface((w*40,h*40),(40,40)))
tiles_fase_1.append((34,57,65))
mapa_fase_1 = mapaLimitavel(player,matriz_fase_1, tiles_fase_1,40)
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
mov_y3=[(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,1),(0,1),(0,1),(0,1),(0,1),
        (1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
        (0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)]
mov_y2=[(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(0,1),(0,1),(0,1),(0,1),(0,1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,1),(0,1),(0,1),
        (1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
        (0,-1),(0,-1),(0,-1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)]
#pos,time,pause_time,where,sprites,tamanhos,nextsprites,rewinds,forcas,velocidades,vidas,voador,tipos,movimento,sentidos,mana,quantidades):
mapa_fase_1.addSpawn( (0,3) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (1,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,1] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_y3,mov_y3,mov_y3,mov_y3,mov_y3,mov_y3,mov_y3,mov_y3,mov_y3,mov_y3] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])#[1,1,1,1,1,1,1,1,1,1]
mapa_fase_1.addSpawn( (0,2) , [120,120,120,120,120,120,120,120,120,120] , [800,800,800,800,800,800,800,800,800,800] , (1,0) , [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10] , [(20,20),(25,25),(25,25),(22,22),(22,22),(25,25),(20,20),(22,22),(25,25),(20,20)] , [8,8,8,8,8,8,8,8,8,8] , [True,True,True,False,False,True,True,False,True,True] , [1,1,1,1,1,1,1,1,1,1] , [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] , [120,200,400,220,550,800,1280,700,1550,15000] ,[False,False,False,True,False,False,False,True,False,False],[0,2,1,0,3,4,0,4,2,0], [mov_y2,mov_y2,mov_y2,mov_y2,mov_y2,mov_y2,mov_y2,mov_y2,mov_y2,mov_y2] , [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)] ,[2,2,3,4,4,6,5,7,9,150], [20,20,15,10,20,15,30,15,20,1])#[0,0,0,0,0,0,0,0,0,0]
#alvo para o inimigo dar pontos de dano
mapa_fase_1.addTarget(player,(19,3),(-1,0))
mapa_fase_1.addTarget(player,(19,2),(-1,0))
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
botao_viking = pyTreeBee.linkedButton(viking_lvl_1,arial12b,["    35"],25,535,pygame.Rect(0,0,60,60),0,-15,pygame.transform.scale(pygame.image.load("viking.png"),(60,60)))
#texto_viking = pyTreeBee.linkedButton(None,arial,["   Viking"],30,582,pygame.Rect(0,0,0,0),0,0)
botao_viking.setAll_BarColor(cor_fundo)
botao_viking.setAll_TextColor(cor_mana)
botao_arqueiro = pyTreeBee.linkedButton(arqueiro_lvl_1,arial12b,["    50"],100,535,pygame.Rect(0,0,60,60),0,-15,pygame.transform.scale(pygame.image.load("arqueira.png"),(60,60)))
#texto_arqueiro = pyTreeBee.linkedButton(None,arial,[" Arqueiro"],105,582,pygame.Rect(0,0,0,0),0,0)
botao_arqueiro.setAll_BarColor(cor_fundo)
botao_arqueiro.setAll_TextColor(cor_mana)
botao_berserker = pyTreeBee.linkedButton(berserker_lvl_1,arial12b,["    50"],175,535,pygame.Rect(0,0,60,60),0,-15,pygame.transform.scale(pygame.image.load("berserker.png"),(60,60)))
#texto_berserker = pyTreeBee.linkedButton(None,arial,["Berserker"],180,582,pygame.Rect(0,0,0,0),0,0)
botao_berserker.setAll_BarColor(cor_fundo)
botao_berserker.setAll_TextColor(cor_mana)
botao_valquiria = pyTreeBee.linkedButton(valquiria_lvl_1,arial12b,["    75"],250,535,pygame.Rect(0,0,60,60),0,-15,pygame.transform.scale(pygame.image.load("valkyrie.png"),(60,60)))
#texto_valquiria = pyTreeBee.linkedButton(None,arial,["Valquíria"],255,582,pygame.Rect(0,0,0,0),0,0)
botao_valquiria.setAll_BarColor(cor_fundo)
botao_valquiria.setAll_TextColor(cor_mana)
### botoes aceleradores ###
accelx1=pyTreeBee.linkedButton(accelGame(60),arial,[""],500+150,550,pygame.Rect(0,0,30,30),0,0,pygame.image.load('botao_x1.png'))
accelx1.setAll_BarSize((-10,-10))

accelx2=pyTreeBee.linkedButton(accelGame(90),arial,[""],550+150,550,pygame.Rect(0,0,30,30),0,0,pygame.image.load('botao_x2.png'))
accelx2.setAll_BarSize((-10,-10))

accelx3=pyTreeBee.linkedButton(accelGame(120),arial,[""],600+150,550,pygame.Rect(0,0,30,30),0,0,pygame.image.load('botao_x3.png'))
accelx3.setAll_BarSize((-10,-10))


###>>>FASES<<<###

###fase 1###
fase_1 = pyTreeBee.dynamicScreen((800,600), 60,(78,133,154),mapa_fase_1,botao_viking,botao_arqueiro, botao_berserker,botao_valquiria,accelx1,accelx2,accelx3)#,texto_viking,texto_arqueiro,texto_berserker,texto_valquiria

fase_1.addItem(controlesExtras(fase_1))
fase_1.addItem(gameOver(fase_1,game_over,player))
fase_1.addItem(winnerScreen(fase_1,winner_scr,player,332))
#fase_1.setMusic("Volatile Reaction.mp3",-1, 0.0)           #ATIVE-ME PARA MUSICA! 8-)

###>>>TELAS<<<###

###seleção de fases###
botao_1=pyTreeBee.linkedButton(linkedMusic(fase_1,"Volatile Reaction.mp3",-1, 0.0),arial,["Fase 1","Idavoll"],100,100,pygame.Rect(0,0,280,192),-20,200,pygame.image.load("logo_fase1.png").convert())
botao_1.setEach_BarSize((-20,-5),(-20,-10),(-20,-15))
selecao_fase = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_1)
selecao_fase.setMusic("Teller of the Tales.mp3",-1, 0.0)
###tela options###
tela_options=pyTreeBee.dynamicScreen((800,600),60,(200,255,0),pyTreeBee.linkedButton(None,arial,["Você tem a opção de...","VOLTAR!","","HUE","   HUE","      BR","        BR"],300,300,pygame.Rect(0,0,0,0),0,0))
###tela staff###
tela_staff=pyTreeBee.dynamicScreen((800,600),60,(0,0,0))
tela_staff.setImage(pygame.image.load("credits.png").convert(),(0,0))
###tela tutorial###
tela_tutorial=pyTreeBee.dynamicScreen((800,600),60,(0,0,0))
tela_tutorial.setImage(pygame.image.load("tela_tutorial.png").convert(),(0,0))
###tela inicial###
#> letreiro

#> viking
#pescoco=pyTreeBee.linkedButton(None,arial,[""],0,438,pygame.Rect(0,0,0,0),0,0, pygame.transform.scale(pygame.image.load("pescoco 2.png"),(437,162)))
#cabeca=pyTreeBee.linkedButton(None,arial,[""],0,63,pygame.Rect(0,0,0,0),0,0,  pygame.transform.scale(pygame.image.load("cabeca 4.png"),(357,523)))
#olho=animacaoSprite(pygame.transform.scale(pygame.image.load("olho_spritesheet 2.png"),(760,75)),(190,75),6,True,(90,290))
#olho.setPause(60)
#espada=animacaoSprite(pygame.transform.scale(pygame.image.load("espada_spritesheet.png"),(4800,600)),(800,600),10,True,(0,0))
#espada.setStop(1)

identa_botoes_x=0
identa_botoes_y=-100

#> start
botao_start=pyTreeBee.linkedButton(selecao_fase,arial,[""],800+identa_botoes_x,300+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_start.setEach_Image(pygame.image.load("start1.png"),pygame.image.load("start2.png"),pygame.image.load("start3.png"))
botao_start.setAll_BarSize((-10,-10))
#> options
botao_options=pyTreeBee.linkedButton(tela_options,arial,[""],800+identa_botoes_x,380+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_options.setEach_Image(pygame.image.load("options1.png"),pygame.image.load("options2.png"),pygame.image.load("options3.png"))
botao_options.setAll_BarSize((-10,-10))
#> tutorial
botao_tutorial=pyTreeBee.linkedButton(tela_tutorial,arial,[''],800+identa_botoes_x,460+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_tutorial.setEach_Image(pygame.image.load("tutorial1.png"),pygame.image.load("tutorial2.png"),pygame.image.load("tutorial3.png"))
botao_tutorial.setAll_BarSize((-10,-10))
#> staff
botao_staff=pyTreeBee.linkedButton(tela_staff,arial,[""],800+identa_botoes_x,540+identa_botoes_y,pygame.Rect(0,0,180,60),0,0)
botao_staff.setEach_Image(pygame.image.load("staff1.png"),pygame.image.load("staff2.png"),pygame.image.load("staff3.png"))
botao_staff.setAll_BarSize((-10,-10))
#> tela
tela_inicial = pyTreeBee.dynamicScreen((800,600),60,(200,255,200),botao_start,botao_options,botao_staff,botao_tutorial)#,pescoco,cabeca,olho,espada
tela_inicial.setImage(pygame.image.load("Abertura Nova.png").convert(),(0,0))
tela_inicial.addItem(controlesExtras(tela_inicial))
fadeIn(tela_inicial,tela_inicial,[botao_start,(500+identa_botoes_x,300+identa_botoes_y),10],[botao_options,(500+identa_botoes_x,380+identa_botoes_y),15],[botao_tutorial,(500+identa_botoes_x,460+identa_botoes_y),20],[botao_staff,(500+identa_botoes_x,540+identa_botoes_y),25])#[pescoco,(500,500),40],[cabeca,(0,0),40],[espada,(0,600),100]
#botao_start.link=fadeOut(tela_inicial,selecao_fase,[botao_start,(800+identa_botoes_x,300+identa_botoes_y),10],[botao_options,(800+identa_botoes_x,380+identa_botoes_y),15],[botao_tutorial,(800+identa_botoes_x,460+identa_botoes_y),20],[botao_staff,(800+identa_botoes_x,540+identa_botoes_y),25])
###botões de voltar adicionados às telas anteriores###
img_voltar=pygame.image.load("botao_voltar.png")

voltar_para_inicio=pyTreeBee.linkedButton(tela_inicial,arial,[""],680,550,pygame.Rect(0,0,100,30),0,0,img_voltar)
voltar_para_inicio.setAll_BarSize((-10,-10))
tela_options.addItem(voltar_para_inicio)
tela_staff.addItem(voltar_para_inicio)
tela_tutorial.addItem(voltar_para_inicio)
voltar_para_inicio_musica=pyTreeBee.linkedButton(linkedMusic(tela_inicial,"Five Armies.mp3", -1, 0.0),arial,[""],680,550,pygame.Rect(0,0,100,30),0,0,img_voltar)
voltar_para_inicio_musica.setAll_BarSize((-10,-10))
selecao_fase.addItem(voltar_para_inicio_musica)
'''
voltar_selecao.link=fadeOut(tela_inicial,tela_inicial,[botao_start,(500,300),10],[botao_options,(500,380),15],[botao_staff,(500,460),20])
selecao_fase.addItem(voltar_selecao)
'''
#fase_1.addItem(pyTreeBee.linkedButton(selecao_fase,arial,["Voltar"],600,530,pygame.Rect(0,0,50,20),0,0))
###início dos ciclos###
time.sleep(0.1)
pyTreeBee.treeBeeStart(tela_inicial)


