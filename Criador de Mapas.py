# -*- coding: cp1252 -*-
import pyTreeBee, pygame,os,pickle
from pygame.locals import*
infoObject = pygame.display.Info()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((infoObject.current_w//2)-250, (infoObject.current_h//2)-50)
temporarydisplay=pygame.display.set_mode((500,100))
tile_set=None
tamanho=40
caminhos=[]
 
mapa=[
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
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]],

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
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]],
             
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
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
             ]
din_12=pygame.font.Font('DIN-Medium.otf',14)
dinB_12=pygame.font.Font("DIN-Black.otf",14)

class persistenciaDados(object):
    def __init__ (self, save_notload):
        self.switch=save_notload
    def linkReply(self, scr):
        global mapa
        if self.switch:
            print 'saving'
            try:
                arq = open('map.ages','wb')
                pickle.dump(mapa,arq)
                arq.close
            except:
                print 'erro save'
        else:
            print 'loading'
            try:
                arq = open('map.ages','rb')
                mapa=pickle.load(arq)
                arq.close
            except:
                print 'erro load'
        return scr

class exportarCaminho(object):
    def linkReply(self, prevscr):
        global caminhos
        arq = open('exported_caminhos.txt','wb')
        texto=''
        for caminho in caminhos:
            texto+=str(caminho)+'   '
        arq.write(str(texto))
        arq.close
        return prevscr
class exportarMapa(object):
    def linkReply(self, prevscr):
        global mapa
        arq = open('exported_mapa.txt','wb')
        texto='[   '
        for camada in mapa:
            texto+='[   '
            for linha in camada:
                texto+=str(linha)+'   '
            texto+=']   '
        texto+=']   '
        arq.write(str(texto))
        arq.close
        return prevscr

class carregaImagem(object):
    def __init__(self,link,imagem,tamanho,caixa_aviso):
        self.link=link
        self.imagem=imagem
        self.tamanho=tamanho
        self.caixa_aviso=caixa_aviso
    def linkReply(self,scr):
        global mapa, caminhos
        verifica_1=False
        verifica_2=False
        retorno=scr
        try:
            tile_set=pygame.image.load(self.imagem.text)
            verifica_1=True
        except:
            self.caixa_aviso.setAll_Text(["IMAGEM INVÁLIDA"])
        try:
            tamanho=int(self.tamanho.text)
            verifica_2=True
        except:
            self.caixa_aviso.setAll_Text(["TAMANHO INVÁLIDO"])
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((infoObject.current_w//2)-400, (infoObject.current_h//2)-300)
        if verifica_1 and verifica_2:
            retorno=self.link
            self.link.addItem(mouseTile(mapa, caminhos, tile_set,tamanho))
        if not verifica_1 and not verifica_2:
            self.caixa_aviso.setAll_Text(["DADOS INVÁLIDOS"])
        return retorno

class mouseTile(object):
    def __init__(self, mapa,caminhos,tile_set,tamanho):
        self.tile_set=[]
        for h in range(tile_set.get_height()//tamanho):
            for w in range(tile_set.get_width()//tamanho):
                self.tile_set.append(tile_set.subsurface((w*tamanho,h*tamanho),(tamanho,tamanho)))
        self.tamanho=tamanho
        self.select=0
        self.layer=0
        self.x=1
        self.y=1
        self.clicou_dir=False
        self.clicou_esq=False
        self.mapa=mapa
        self.dentro=True
        self.caminhos=caminhos
        self.spawn_pos=(0,0)
        self.spawn_way=[]
        self.desenha_caminho=False
        self.mostrar_caminhos=False
        self.caminho_pointer=-1
    def keyControls(self,event):
        if self.clicou_esq:
            if self.desenha_caminho:
                self.caminhos.append([self.spawn_pos,self.spawn_way])
                self.spawn_way=[]
                self.desenha_caminho=False
            else:
                self.spawn_pos=(self.x,self.y)
                self.desenha_caminho=True
        if self.clicou_dir:            
            try:
                if self.y>=0 and self.x>=0 and self.y<len(self.mapa[self.layer]) and self.x<len(self.mapa[self.layer][self.y]):
                    self.mapa[self.layer][self.y][self.x]=self.select
            except:
                pass
        if event.type==MOUSEMOTION:
            self.x,self.y = event.pos[0]//self.tamanho,event.pos[1]//self.tamanho
        if event.type==MOUSEBUTTONDOWN:
            if event.button==1:
                if self.dentro:self.clicou_dir=True
            if event.button==3:
                if self.dentro: self.clicou_esq=True
        if event.type==MOUSEBUTTONUP:
            if event.button==1:
                if self.dentro:self.clicou_dir=False
            if event.button==3:
                if self.dentro: self.clicou_esq=False
            if event.button==4:
                if self.select< len(self.tile_set)-1: self.select+=1
            if event.button==5:
                if self.select>=0: self.select-=1
        if event.type==KEYUP:
            if event.key== K_m:
                if self.mostrar_caminhos:
                    self.caminho_pointer=-1
                    self.mostrar_caminhos=False
                else:
                    self.mostrar_caminhos=True
            if self.desenha_caminho==False:
                if event.key== K_UP:
                    if self.select< len(self.tile_set)-1: self.select+=1
                if event.key== K_DOWN:
                    if self.select>=0: self.select-=1
                if event.key== K_RIGHT:
                    if self.layer< 2: self.layer+=1
                if  event.key==K_LEFT:
                    if self.layer> 0: self.layer-=1
            else:
                if event.key==K_UP:
                    self.spawn_way.append( (0,-1) )
                if event.key==K_DOWN:
                    self.spawn_way.append( (0,1) )
                if event.key==K_RIGHT:
                    self.spawn_way.append( (1,0) )
                if event.key==K_LEFT:
                    self.spawn_way.append( (-1,0) )
            if event.key==K_SPACE:
                if self.mostrar_caminhos:
                    if self.caminho_pointer< len(self.caminhos): self.caminho_pointer+=1
                    else: self.caminho_pointer=(-1)
    def blitOn(self,scr):
        if self.layer==0:cor=(0,0,0)
        if self.layer==1:cor=(255,0,0)
        if self.layer==2:cor=(250,200,200)
        for z in range(len(self.mapa)):
            for y in range(len(self.mapa[z])):
                for x in range(len(self.mapa[z][y])):
                    if self.mapa[z][y][x]>=0: scr.blit(self.tile_set[self.mapa[z][y][x]],(x*self.tamanho,y*self.tamanho))
        scr.blit(din_12.render('('+str(self.x)+','+str(self.y)+') '+str(self.select)+' -> Layer:'+str(self.layer),True,cor),(0,550))
        if self.y<13:
            if self.dentro!=True:
                pygame.mouse.set_visible(False)
                self.dentro=True
        else:
            if self.dentro:
                pygame.mouse.set_visible(True)
                self.dentro=False
        if self.mostrar_caminhos:
            for caminho in self.caminhos:
                for pos in range(0, len(caminho[1]), 1):
                    result=[caminho[0][0],caminho[0][1]]
                    for retro in range(pos, -1, -1):
                        result[0]+=caminho[1][retro][0]
                        result[1]+=caminho[1][retro][1]
                    scr.fill((255,255,255),pygame.Rect((result[0]*self.tamanho)-4+self.tamanho//4,(result[1]*self.tamanho)-4+self.tamanho//4,2+self.tamanho//2,2+self.tamanho//2))
                    scr.fill((100,100,100),pygame.Rect((result[0]*self.tamanho)+self.tamanho//4,(result[1]*self.tamanho)+self.tamanho//4,self.tamanho//2,self.tamanho//2))
            if self.caminho_pointer>=0 and self.caminho_pointer<len(self.caminhos):
                for pos in range(0, len(self.caminhos[self.caminho_pointer][1]), 1):
                        result=[self.caminhos[self.caminho_pointer][0][0],self.caminhos[self.caminho_pointer][0][1]]
                        for retro in range(pos, -1, -1):
                            result[0]+=self.caminhos[self.caminho_pointer][1][retro][0]
                            result[1]+=self.caminhos[self.caminho_pointer][1][retro][1]
                        scr.fill((0,0,0),pygame.Rect((result[0]*self.tamanho)-4+self.tamanho//4,(result[1]*self.tamanho)-4+self.tamanho//4,2+self.tamanho//2,2+self.tamanho//2))
                        scr.fill((255,255,255),pygame.Rect((result[0]*self.tamanho)+self.tamanho//4,(result[1]*self.tamanho)+self.tamanho//4,self.tamanho//2,self.tamanho//2))
        if self.desenha_caminho:
            for pos in range(0, len(self.spawn_way), 1):
                result=[self.spawn_pos[0],self.spawn_pos[1]]
                for retro in range(pos, -1, -1):
                    result[0]+=self.spawn_way[retro][0]
                    result[1]+=self.spawn_way[retro][1]
                scr.fill((255,255,255),pygame.Rect((result[0]*self.tamanho)-4+self.tamanho//4,(result[1]*self.tamanho)-4+self.tamanho//4,2+self.tamanho//2,2+self.tamanho//2))
                scr.fill((0,0,0),pygame.Rect((result[0]*self.tamanho)+self.tamanho//4,(result[1]*self.tamanho)+self.tamanho//4,self.tamanho//2,self.tamanho//2))
        else:
            if self.dentro:
                if self.select>=0:
                    scr.blit(self.tile_set[self.select],(self.x*self.tamanho,self.y*self.tamanho))
                else:
                    scr.fill((0,0,0),pygame.Rect(self.x*self.tamanho,self.y*self.tamanho,self.tamanho,self.tamanho))
        

tela_B = pyTreeBee.dynamicScreen((800,600),60,(100,200,200),pyTreeBee.linkedButton(exportarMapa(),din_12,["EXPORTAR","MAPA"],500,525,pygame.Rect(0,0,100,50),0,0),pyTreeBee.linkedButton(exportarCaminho(),din_12,["EXPORTAR","CAMINHOS"],300,525,pygame.Rect(0,0,100,50),0,0))
#pyTreeBee.linkedButton(persistenciaDados(True),din_12,["SALVAR","(MAPA APENAS)"],300,525,pygame.Rect(0,0,100,50),0,0),pyTreeBee.linkedButton(persistenciaDados(False),din_12,["CARREGAR","MAPA ANTERIOR"],400,525,pygame.Rect(0,0,100,50),0,0)
arquivo_imagem=pyTreeBee.entryBox(din_12,".png",300,50,25)
tamanho_imagem=pyTreeBee.entryBox(din_12,"",75,375,25)
caixa_aviso=pyTreeBee.linkedButton(None,dinB_12,[""],50,75,pygame.Rect(0,0,0,0),0,0)
caixa_aviso.setAll_TextColor((255,0,0))
botao_ok=pyTreeBee.linkedButton(carregaImagem(tela_B,arquivo_imagem,tamanho_imagem,caixa_aviso),dinB_12,["CARREGAR"],210,70,pygame.Rect(0,0,80,30),2,5)
tela_A = pyTreeBee.dynamicScreen((500,100),60,(200,200,100),caixa_aviso,arquivo_imagem,tamanho_imagem,botao_ok,pyTreeBee.linkedButton(None,dinB_12,["Tile Set"],50,0,pygame.Rect(0,0,0,0),0,0),pyTreeBee.linkedButton(None,dinB_12,["Tamanho"],375,0,pygame.Rect(0,0,0,0),0,0))
tela_A.setTitle('Criador de Mapas - Asgard Defense')
pyTreeBee.treeBeeStart(tela_A)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((infoObject.current_w//2)-250, (infoObject.current_h//2)-50)
pygame.display.set_mode((500,100))
temporarydisplay.fill((0,0,0))
temporarydisplay.blit(dinB_12.render("Até mais! ^^",True,(255,255,255)),(50,50))
pygame.display.update()
pygame.mouse.set_visible(True)
pygame.quit()
