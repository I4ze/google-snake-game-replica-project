from random import randint
import pygame, sys
import os
import copy

pygame.init()

class Cenario:
    def __init__(self, matriz):
        self.matriz = copy.deepcopy(matriz)
        self.grupoParedes = []
        for i, linha in enumerate(self.matriz):
            for j, valor in enumerate(linha):
                if valor == PAREDE:
                    rect = pygame.Rect( (j*tamanho,i*tamanho) ,(tamanho, tamanho))
                    self.grupoParedes.append(rect)

    def desenharMapa(self):
        anterior = 1
        for i, linha in enumerate(self.matriz):
            for j, valor in enumerate(linha):
                retangulo = [(j * tamanho, i * tamanho), (tamanho, tamanho)]
                if valor == PAREDE:
                    pygame.draw.rect(tela, "#578a34", retangulo)
                elif valor == PLACAR:
                    pygame.draw.rect(tela, "#4A752C", retangulo)
                else:
                    if anterior == 1:
                        pygame.draw.rect(tela, "#aad751", retangulo)
                    else:
                        pygame.draw.rect(tela, "#a2d149", retangulo)
                    anterior *= -1

    def DesenharPlacar(self):
        mostrapont = fonte.render(f"{pontos}", True, (255, 255, 255))
        mostraMaiorPlacar = fonte.render(f"{maiorPlacar}", True, (255, 255, 255))

        posicaoMaca = [tamanho, 5]
        posicaoTrofeu = [tamanho*6, 5]
        tela.blits([[imgMaca, posicaoMaca],
                    [mostrapont, (posicaoMaca[0]+70, 26 )],
                    [imgTrofeu, posicaoTrofeu],
                    [mostraMaiorPlacar, (posicaoTrofeu[0]+70, 26 )],
                     ])

    def lerMapa(self, valorProcurado):
        for i, linha in enumerate(self.matriz):
            for j, valor in enumerate(linha):
                if valor == valorProcurado:
                    return [j, i]
        return False

    def quantElementos(self, valor):
        acumulador = 0
        for linha in self.matriz:
            acumulador += linha.count(valor)
        return acumulador

    def removerValores(self, valor, substituto=0):
        for i, linha in enumerate(self.matriz):
            for j, v in enumerate(linha):
                if v == valor:
                    self.matriz[i][j] = substituto

    def substituirElementoN(self, numElemento, valor, substituto):
        acumulador = 0
        for i, linha in enumerate(self.matriz):
            for j, v in enumerate(linha):
                if valor == v:
                    acumulador += 1
                if acumulador > numElemento:
                    self.matriz[i][j] = substituto
                    return [j, i]

    def SusbstituirElementoPos(self, posElemento, substituto):
        posMat = [posElemento[0] // tamanho, posElemento[1] // tamanho]
        posMat = int(posMat[0]),int(posMat[1])
        self.matriz[posMat[1]][posMat[0]] = substituto

    def TocarMscFundo(self):
        pygame.mixer.music.load("Recursos/Sons/hauntedcastle_fundo jogo.mp3")
        pygame.mixer.music.set_volume(0.24)
        pygame.mixer.music.play(-1)

class Cobra(pygame.sprite.Sprite):
    def __init__(self, velocidade, cenario:Cenario):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = velocidade
        self.cenario = cenario
        posMatriz = cenario.lerMapa(COBRA)
        self.posicaoCabeca = [posMatriz[0] * tamanho, posMatriz[1] * tamanho]
        self.corpoCobra = []
        self.corpoColisoes = []

        self.sprites = {
            "cabeca": spriteSheet.subsurface((80,0), (40,40)),
            "corpo": {"curvado": spriteSheet.subsurface((0,0), (40,40)),
                      "reto": spriteSheet.subsurface((40,0), (40,40))},
            "cauda": spriteSheet.subsurface((120,0), (40,40))
        }
        self.image = self.sprites["cabeca"]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.posicaoCabeca

        self.trajeto = []
        self.ultimoMovimento = (0, 0)
        self.caminhoTotal = [[self.posicaoCabeca, self.ultimoMovimento]]*3

    def movimentacao(self):
        if len(self.trajeto) > 0:
            trajetoAtual = self.trajeto[0]
            
            proxPos = [self.posicaoCabeca[0] + trajetoAtual[0] * self.velocidade,
                       self.posicaoCabeca[1] + trajetoAtual[1] * self.velocidade,]

            matrizAt = [self.posicaoCabeca[0] // tamanho, self.posicaoCabeca[1] // tamanho]
            matrizProx = [proxPos[0] // tamanho, proxPos[1] // tamanho]
            
            if matrizProx[0] - matrizAt[0] != 0 and matrizProx[1] - matrizAt[1] != 0:
                return

            if matrizProx != matrizAt and self.posicaoCabeca != self.caminhoTotal[-1][0]:
                correcao = []
                if trajetoAtual[0] == -1 or trajetoAtual[1] == -1:
                    correcao = matrizAt
                elif trajetoAtual[0] == 1 or trajetoAtual[1] == 1:
                    correcao = matrizProx
                
                if len(self.trajeto) > 1:
                    self.trajeto.pop(0)
                
                self.posicaoCabeca = correcao[0]*tamanho, correcao[1]*tamanho

                self.caminhoTotal.append( [ self.posicaoCabeca, self.trajeto[0] ] )
                self.atualizarCorpo()
            else:
                self.posicaoCabeca = proxPos
            self.rect.x, self.rect.y = self.posicaoCabeca

    def aumentarCobra(self):
        elemento = pygame.sprite.Sprite()
        elemento.image = self.sprites["cauda"]
        elemento.rect = (-100, -100)
        grupoSprites.add(elemento)
        self.corpoCobra.append([elemento, (0,0)])
        self.atualizarCorpo()
    
    def atualizarCorpo(self):
        if len(self.caminhoTotal) < len(self.corpoCobra):
            return
        
        if len(self.caminhoTotal) > len(self.corpoCobra) + 2:
            self.caminhoTotal.pop(0)
        
        self.cenario.removerValores(COBRA)

        self.corpoColisoes.clear()
        trajetosCobra = []
        for i in range(1, len(self.corpoCobra)+1):
            sprite = self.corpoCobra[i-1][0]
            pos = self.caminhoTotal[-i][0]
            trajeto = self.caminhoTotal[-i][1]

            trajetosCobra.append(trajeto)
            sprite.rect = (pos, (tamanho, tamanho))
            self.corpoCobra[i-1][1] = trajeto
            self.cenario.SusbstituirElementoPos(pos, COBRA)

            if i > 2:
                self.corpoColisoes.append(sprite.rect)
        
        self.definirSpritesCorpo(trajetosCobra)
        self.cenario.SusbstituirElementoPos([self.rect.x, self.rect.y], COBRA)
    
    def definirSpritesCorpo(self, trajetosCobra):   
        for p, parte in enumerate(self.corpoCobra):
            sprite = parte[0]
            sprite.image = self.sprites["cauda"]
            trajAt = trajetosCobra[p]
            
            #Cauda
            if p == len(self.corpoCobra)-1:
                sprite.image = self.sprites["cauda"]
                rotacao = 0
                if trajAt[0] == -1:
                    rotacao = 180
                elif trajAt[1] == 1:
                    rotacao = -90
                elif trajAt[1] == -1:
                    rotacao = 90
                sprite.image = pygame.transform.rotate(sprite.image, rotacao)
            
            #Resto do Corpo
            else:
                trajPos = trajetosCobra[p+1]

                if trajAt != trajPos:
                    sprite.image = self.sprites["corpo"]["curvado"]
                    rotacao = 0
                    if (trajAt[0] == 1 and trajPos[1] == 1) or (trajAt[1] == -1 and trajPos[0] == -1):
                        rotacao = 90
                    elif (trajAt[1] == 1 and trajPos[0] == 1) or (trajAt[0] == -1 and trajPos[1] == -1):
                        rotacao = -90
                    elif (trajAt[1] == -1 and trajPos[0] == 1) or (trajAt[0] == -1 and trajPos[1] == 1):
                        rotacao = 180
                    sprite.image = pygame.transform.rotate(sprite.image, rotacao)

                else:
                    sprite.image = self.sprites["corpo"]["reto"]
                    if trajAt[0] != 0:
                        sprite.image = pygame.transform.rotate(sprite.image, 90)

    def desenharCobra(self):
        rotacao = 0
        if len(self.trajeto):
            trajAtual = self.trajeto[0]
            if trajAtual[0] == -1:
                rotacao = 180
            elif trajAtual[1] == 1:
                rotacao = -90
            elif trajAtual[1] == -1:
                rotacao = 90

        self.image = pygame.transform.rotate(self.image, rotacao)
        tela.blit(self.image, self.rect)
        self.image = pygame.transform.rotate(self.image, -rotacao)

    def processarEventos(self, e):
        moveAnterior = self.ultimoMovimento

        if ((e.key == pygame.K_LEFT or e.key == pygame.K_a)
            and (self.ultimoMovimento != [1, 0])):
                self.ultimoMovimento = [-1, 0]
        elif ((e.key == pygame.K_RIGHT or e.key == pygame.K_d)
            and (self.ultimoMovimento != [-1, 0])):
                self.ultimoMovimento = [1, 0]
        elif ((e.key == pygame.K_UP or e.key == pygame.K_w)
            and (self.ultimoMovimento != [0, 1])):
                self.ultimoMovimento = [0, -1]
        elif ((e.key == pygame.K_DOWN or e.key == pygame.K_s)
            and (self.ultimoMovimento != [0, -1])):
               self.ultimoMovimento = [0, 1]

        if moveAnterior != self.ultimoMovimento and len(self.trajeto) <= 3:
            self.trajeto.append(self.ultimoMovimento)


class Fruta(pygame.sprite.Sprite):
    def __init__(self, cenario: Cenario):
        self.cenario = cenario
        posMatriz = self.cenario.lerMapa(2)
        self.posicao = [posMatriz[0] * tamanho, posMatriz[1] * tamanho]

        super().__init__()
        self.sprites = []
        for i in range(8):
            spr = spriteSheet.subsurface((i*40,40), (40,40))
            self.sprites.append(spr)

        self.spriteAtual = 0
        self.image = self.sprites[self.spriteAtual]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.posicao[0], self.posicao[1]]

    def AtualizarSpriteFruta(self):
        self.spriteAtual += 0.25
        if self.spriteAtual >= len(self.sprites):
            self.spriteAtual = 0.25
        self.image = self.sprites[int(self.spriteAtual)]

    def gerarFruta(self):
        quant = self.cenario.quantElementos(0)
        espacoEscolhido = randint(0, quant)
        self.cenario.SusbstituirElementoPos(self.posicao, LIVRE)
        pos = self.cenario.substituirElementoN(espacoEscolhido, LIVRE, FRUTA)
        self.posicao = [pos[0] * tamanho, pos[1] * tamanho]
        self.rect = (self.posicao,(tamanho, tamanho))

    def TocarSomPonto(self):
        somPonto = pygame.mixer.Sound("Recursos/Sons/coin_+1ponto.wav")
        somPonto.play()

class TelaInicio(pygame.sprite.Sprite):
    def __init__(self):
        self.tamanho = [300, 352]
        self.posicao = [(largura/2)-(self.tamanho[0]/2), (altura/2)-(self.tamanho[1]/2)]
        self.fundo = pygame.image.load("Recursos/Imagens/fundo.png")
        self.fotoCobra = pygame.image.load("Recursos/Imagens/telaInicio.png")

    def DesenharTela(self):
        cenario.desenharMapa()
        cobra.desenharCobra()
        grupoSprites.draw(tela)
        
        mostrapont = fonte.render(f"{pontos}", True, (255, 255, 255))
        mostraMaiorPlacar = fonte.render(f"{maiorPlacar}", True, (255, 255, 255))
        
        instrucoes = fonte.render(f"Pressione qualquer tecla para iniciar", True, (255,255,255))
        tela.blit(self.fundo, (0,0))
        pygame.draw.rect(tela, (77, 193, 249), (self.posicao[0], self.posicao[1], 300, 352))
        tela.blits([[self.fotoCobra, self.posicao],
                   [imgMaca, (self.posicao[0]+35, self.posicao[1]+35)], 
                   [mostrapont, (self.posicao[0]+58, self.posicao[1]+110)],
                   [imgTrofeu, (self.posicao[0]+195, self.posicao[1]+35)], 
                   [mostraMaiorPlacar, (self.posicao[0]+217, self.posicao[1]+110)],
                   [instrucoes, (self.posicao[0]-70, self.posicao[1]+370)]])
        pygame.display.update()

    def ProcessarComandoSair(self):
      if e.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()

    def TocarMsc(self):
        pygame.mixer.music.load("Recursos/Sons/movingrightalong_menu.wav")
        pygame.mixer.music.set_volume(0.30)
        pygame.mixer.music.play(-1)

matrizMapa = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

tamanho = 40
largura = len(matrizMapa[0]) * tamanho
altura = len(matrizMapa) * tamanho
tela = pygame.display.set_mode((largura, altura))

LIVRE, PAREDE, FRUTA, COBRA, PLACAR = 0, 1, 2, 3, 4

fonte = pygame.font.SysFont("comic sans", 28, False, False)

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, "Recursos","Imagens")

spriteSheet = pygame.image.load(os.path.join(diretorio_imagens, "SpritesJogo.png")).convert_alpha()
spriteIcones = pygame.image.load(os.path.join(diretorio_imagens, "Icones.png")).convert_alpha()
imgMaca = spriteIcones.subsurface((70,0),(70,70))
imgTrofeu = spriteIcones.subsurface((0,0),(70,70))

telaDeInicio = TelaInicio()
telaDeInicio.TocarMsc()
tocarMscMenu = True
pontos = 0
maiorPlacar = pontos

INICIANDO, EXECUTANDO, EMMENU = 1,2,3
estado_jogo = INICIANDO
max_pontos = 0

while True:
  if estado_jogo == INICIANDO:
    grupoSprites = pygame.sprite.Group()
    
    cenario = Cenario(matrizMapa)
    fruta = Fruta(cenario)
    cobra = Cobra(4.6, cenario)

    grupoSprites.add(fruta)
    
    max_pontos = cenario.quantElementos(LIVRE)+2
    estado_jogo = EMMENU
    
  elif estado_jogo == EXECUTANDO:
    pontos = 0
    cenario.TocarMscFundo()
    while True:
        pygame.time.Clock().tick(60)
    
        grupoSprites.update()
        cobra.movimentacao()
    
        fruta.AtualizarSpriteFruta()
        cenario.desenharMapa()
        cenario.DesenharPlacar()
        grupoSprites.draw(tela)
        cobra.desenharCobra()
    
        pygame.display.update()
    
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                cobra.processarEventos(e)
    
        if (cobra.rect.collidelist(cenario.grupoParedes) != -1 or 
            cobra.rect.collidelist(cobra.corpoColisoes) != -1):
          tocarMscMenu = True
          estado_jogo = INICIANDO
          break
    
        if cobra.rect.colliderect(fruta.rect):
            cobra.aumentarCobra()
            fruta.TocarSomPonto()
            pontos += 1
            if pontos > maiorPlacar:
                maiorPlacar = pontos
            if pontos == max_pontos:
                grupoSprites.remove(fruta)
                tocarMscMenu = True
                estado_jogo = INICIANDO
                break
            
            fruta.gerarFruta()
          
  elif estado_jogo == EMMENU:
    if tocarMscMenu == True:
        telaDeInicio.TocarMsc()
        tocarMscMenu = False
        telaDeInicio.DesenharTela()

    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif e.type == pygame.KEYDOWN:
        if e.key == pygame.K_ESCAPE:
          telaDeInicio.ProcessarComandoSair()
        else:
          estado_jogo = EXECUTANDO