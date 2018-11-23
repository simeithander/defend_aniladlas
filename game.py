import pygame, sys
from pygame.locals import *

## Game Defend aniladlas, desenvolvido por Simei Thander e Rafael Crisostomos
## IFRN - CNAT - TADS 2018.2

pygame.init()

size = width, height = 640, 480
display = pygame.display.set_mode(size)
pygame.display.set_caption("Search and kill aniladlas")
background_img = pygame.image.load("arquivos/middleground.png")
heroi_x = 10
heroi_y = 430
vel_x = 1
vel_y = 1
altura_pulo = 100

#blocos
lista_chao = [33,97,161,225,289,353,417,481,545,609,673]

#personagem
class player:
  def __init__(self, x, y, size):
    self.jumping = False
    self.jump_offset = 0

def events():
  eventos = pygame.event.get()
  for e in eventos:
    if e.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def lodo(lodo_x,lodo_y):
    lodo = pygame.image.load("arquivos/lodo.png")
    lodorect = lodo.get_rect()
    lodorect.center = (lodo_x,lodo_y)
    lodo.set_colorkey((255,0,255))
    display.blit(lodo, lodorect)

def heroi(heroi_x,heroi_y):
  heroi = pygame.image.load("arquivos/player/player-idle/player-idle-1.png")
  heroirect = heroi.get_rect()
  heroirect.center = (heroi_x,heroi_y)
  heroi.set_colorkey((255, 0, 255))
  display.blit(heroi, heroirect)

def bloco(bloco_x, bloco_y):
  bloco = pygame.image.load("arquivos/spt_bloco.png")
  blocorect = bloco.get_rect()
  blocorect.center = (bloco_x,bloco_y)
  bloco.set_colorkey((255,0,255))
  display.blit(bloco, blocorect)

def controles(heroi):
  global heroi_x, vel_x, heroi_y
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
       heroi_x -= vel_x
       heroi(heroi_x,heroi_y)
  if keys[pygame.K_RIGHT]:
       heroi_x += vel_x
       heroi(heroi_x,heroi_y)
  if keys[K_UP] and player.jumping == False and player.jump_offset == 0:
       player.jumping = True

def pulando(player):
  global altura_pulo
  if player.jumping:
    player.jump_offset += 5
  if player.jump_offset >= altura_pulo:
    player.jumping = False
  elif player.jump_offset > 0 and player.jumping == False:
    player.jump_offset -= 5

def cenario():
    display.blit(background_img, (0, 0))
    #constroi os blocos do chão
    for posicao in lista_chao:
        bloco(posicao,460)
    #constroi as pedras e o lodo
    for posicao in lista_chao:
        lodo(posicao,448)

#inicio
while True:
  eventos = pygame.event.get()
  for e in eventos:
    if e.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    #print(e)
  cenario()
  heroi(heroi_x, heroi_y)
  controles(heroi)

  pygame.display.flip()
