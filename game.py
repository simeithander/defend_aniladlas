'''
Game Defend Aniladlas
Alunos: Simei Thander e Rafael Crisostomos
IFRN - TADS 2018.2 - www.ifrn.edu.br
'''
import pygame, os, sys
pygame.mixer.init()
pygame.init()
'''
#define o mixer
pygame.mixer.pre_init(44100, 16, 2, 5000)
#define a musica de fundo
bg_music = pygame.mixer.Sound("arquivos/song/game_play.ogg")
#define que a musica irá se repetir
bg_music_play = bg_music .play(-1)
#da play da musica
bg_music_play.queue(bg_music)'''
#Define o tamanho da tela do jogo
display_width = 640
display_height = 480
#seta na variavel win o display com largura e altura
win = pygame.display.set_mode((display_width, display_height))
#Seta o nome do game na barra superior de titulos
pygame.display.set_caption("Defend Aniladlas")
#obtem o clock do Pygame
clock = pygame.time.Clock()
#Define que o loop começará verdadeiro
run = True
home_screen = True
dead = False
slow = False
while run:
    t = pygame.time.get_ticks()
    main = True
    score = 0
    font = pygame.font.SysFont('verdana', 18)
    #Define algumas variáveis para altura, largura, coordenada X e Y, velocidade
    x = 15
    y = 398
    width = 64
    height = 55
    hitbox = (x+11, y, 39, 55)
    cont_idle = 0
    #Velocidade
    vel = 8
    #Define a condição do pulo
    is_jump = False
    max_jump = 9
    #Define a contagem do pulo
    jump_count = 9
    #Define para onde está percorrendo o personagem:
    left = False
    right = False
    #contagem de passos
    walk_count = 0
    #estado do botão left:
    press_left = False
    #Condição de inicialização do Game
    
    #váriaveis globais para o slug
    x_slug = 640
    y_slug = 411
    width_slug = 64
    height_slug = 42
    end_slug = 0
    walk_count_slug = 0
    vel_slug = 1
    patch_slug = [end_slug, x_slug]
    screen_slug = True

    def score_screen():
        global score
        text_point = font.render('Pontos: ' + str(score), 1, (255,255,255))
        win.blit(text_point, (550, 5))
    
    #detecta colisão
    def isPointInsideRect(x, y, rect):
        if x > rect.left and x < rect.right and y > rect.top and y < rect.bottom:
            return True
        else:
            return False
   
    #colisão
    def colision():
        global x, y, x_slug, y_slug, main, home_screen, score, screen_slug, dead

        char = pygame.image.load("arquivos/player/player-idle/p_right_idle.png")
        char_rect = char.get_rect().move(x,y)
        char_rect.width = 64

        if screen_slug:
            slug = pygame.image.load("arquivos/monsters/slug/slug-left-1.png")
            slug_rect = slug.get_rect().move(x_slug,y_slug)
            slug_rect.width = 45
            pygame.draw.rect(win, (255,0,0), slug_rect, 2)
            #pygame.draw.rect(win, (255,0,0), char_rect, 2)
     
            for a, b in [(slug_rect, char_rect), (char_rect, slug_rect)]:
                if isPointInsideRect(a.left, a.top, b):
                    main = False
                    home_screen = True
                    dead = True
                if isPointInsideRect(a.left, a.bottom, b):
                    screen_slug = False
                    score += 1
                '''    
                if isPointInsideRect(a.right, a.top, b):
                    main = False
                    home_screen = True
                '''
                if isPointInsideRect(a.right, a.right, b):
                    main = False
                    home_screen = True
                    dead = True
            
    #Desenha o cenário
    def draw_scenario():
        win.blit(pygame.image.load("arquivos/bg.jpg"),(0,0))
        bloco = pygame.image.load("arquivos/bloco.jpg")
        house = pygame.image.load("arquivos/house.png")
        win.blit(house,(50,211))
        cont = 0
        for i in range(0,31):
            win.blit(bloco,(cont,453))
            cont += 32
    #desenha o personagem
    def draw_char():
        global x, y, width, height, walk_count, left, right, press_left, jump_count, cont_idle, sec
        #obtem as teclas
        keys = pygame.key.get_pressed()
        #carrega os sprites do personagem
        walk_right = [
        pygame.image.load("arquivos/player/player-skip/p_left_1.png"),
        pygame.image.load("arquivos/player/player-skip/p_left_2.png"),
        pygame.image.load("arquivos/player/player-skip/p_left_3.png"),
        pygame.image.load("arquivos/player/player-skip/p_left_4.png"),
        pygame.image.load("arquivos/player/player-skip/p_left_5.png"),
        pygame.image.load("arquivos/player/player-skip/p_left_6.png"),
        pygame.image.load("arquivos/player/player-skip/p_left_7.png"),
        pygame.image.load("arquivos/player/player-skip/p_left_8.png")]
        walk_left = [
        pygame.image.load("arquivos/player/player-skip/p_right_1.png"),
        pygame.image.load("arquivos/player/player-skip/p_right_2.png"),
        pygame.image.load("arquivos/player/player-skip/p_right_3.png"),
        pygame.image.load("arquivos/player/player-skip/p_right_4.png"),
        pygame.image.load("arquivos/player/player-skip/p_right_5.png"),
        pygame.image.load("arquivos/player/player-skip/p_right_6.png"),
        pygame.image.load("arquivos/player/player-skip/p_right_7.png"),
        pygame.image.load("arquivos/player/player-skip/p_right_8.png")]
        #sprites de pulo

        jump_left = [
        pygame.image.load("arquivos/player/player-jump/player-jump-left-1.png"),
        pygame.image.load("arquivos/player/player-jump/player-jump-left-2.png"),
        pygame.image.load("arquivos/player/player-jump/player-jump-left-3.png"),
        pygame.image.load("arquivos/player/player-jump/player-jump-left-4.png")]
        jump_right = [
        pygame.image.load("arquivos/player/player-jump/player-jump-right-1.png"),
        pygame.image.load("arquivos/player/player-jump/player-jump-right-2.png"),
        pygame.image.load("arquivos/player/player-jump/player-jump-right-3.png"),
        pygame.image.load("arquivos/player/player-jump/player-jump-right-4.png")]

        #sprite Idle (parado)
        char_right_idle = [
        pygame.image.load("arquivos/player/player-idle/player-idle-1.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-2.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-3.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-4.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-5.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-6.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-7.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-8.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-9.png"),]

        char_left_idle = [
        pygame.image.load("arquivos/player/player-idle/player-idle-left-1.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-left-2.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-left-3.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-left-4.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-left-5.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-left-6.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-left-7.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-left-8.png"),
        pygame.image.load("arquivos/player/player-idle/player-idle-left-9.png"),]
    
        #define a animação de movimento do personagem
        if walk_count + 1 >= 16:
            walk_count = 0
        if press_left:
            #define a animação parado
            char_position = char_left_idle[cont_idle//3]
            cont_idle += 1

            if cont_idle == 18:
                cont_idle = 0

            if left:
                char_position = walk_left[walk_count//3]
                walk_count +=1
                press = True
        else:
            #define a animação parado
            char_position = char_right_idle[cont_idle//3]
            cont_idle += 1

            if cont_idle == 18:
                cont_idle = 0

            if right:
                char_position = walk_right[walk_count//3]
                walk_count +=1
                press = True

        #define a animação do pulo
        if is_jump:
            if press_left:
                char_position = jump_left[jump_count//3]
                if left:
                    char_position = jump_left[jump_count//3]
            else:
                char_position = jump_right[jump_count//3]
                if right:
                    char_position = jump_right[jump_count//3] 
               
        win.blit(char_position, (x,y))
        
    #Cria o inimigo Slug
    def draw_enemy_slug():
        global x_slug, y_slug, end_slug, walk_count_slug, vel_slug, width_slug, height_slug, patch_slug, screen_slug

        walk_left = [
        pygame.image.load("arquivos/monsters/slug/slug-left-1.png"),
        pygame.image.load("arquivos/monsters/slug/slug-left-2.png"),
        pygame.image.load("arquivos/monsters/slug/slug-left-3.png"),
        pygame.image.load("arquivos/monsters/slug/slug-left-4.png"),]
        walk_right = [
        pygame.image.load("arquivos/monsters/slug/slug-right-1.png"),
        pygame.image.load("arquivos/monsters/slug/slug-right-2.png"),
        pygame.image.load("arquivos/monsters/slug/slug-right-3.png"),
        pygame.image.load("arquivos/monsters/slug/slug-right-4.png"),]

        #move o inimigo
        if vel_slug > 0:
            if x_slug + vel_slug < patch_slug[1]:
                x_slug += vel_slug
            else:
                vel_slug = vel_slug * -1
                walk_count_slug = 0
        else:
            if x_slug - vel_slug > patch_slug[0]:
                x_slug += vel_slug
            else:
                vel_slug = vel_slug * -1
                walk_count_slug = 0

        #desenha o inimigo
        if screen_slug:
            if walk_count_slug + 1 >= 32:
                walk_count_slug = 0
            if vel_slug > 0:
                win.blit(walk_right[walk_count_slug // 8],(x_slug, y_slug))
                walk_count_slug += 1
            else:
                win.blit(walk_left[walk_count_slug // 8],(x_slug, y_slug))
                walk_count_slug += 1

    #Define a movimentação do personagem
    def move_char():
        global x, y, width, height, win, is_jump, jump_count, max_jump, left, right, press_left
       
        #Armazena na variável key a tecla pressionada
        keys = pygame.key.get_pressed()
        #Altera as variáveis de acordo com a tecla pressionada
        #A condição após o AND limita o personagem para nao sair da tela
        if keys[pygame.K_LEFT] and x > vel:
            x -= vel
            right = False
            left = True
            press_left = True
        elif keys[pygame.K_RIGHT] and x < display_width - width - vel:
            x += vel
            right = True
            left = False
            press_left = False
        else:
            right = False
            left = False
            walk_count = 0

        #Se for pressionado a tecla de pulo, será realizado a condição abaixo:
        if not(is_jump):
            if keys[pygame.K_SPACE]:
                is_jump = True
                right = False
                left = False
                walk_count = 0
                pygame.mixer.music.load("arquivos/song/jump.wav")
                pygame.mixer.music.play()
        else:
            #define a velocidade e altura do pulo
            if jump_count >= -max_jump:
                #variavel para não deixar o pulo negativo
                neg = 1
                if jump_count < 0:
                    neg = -1
                y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jump = False
                jump_count = max_jump

    def time_game():
        global sec, x_slug, vel_slug, screen_slug, score, main, home_screen, slow
        sec = (pygame.time.get_ticks() - t) // 1000
        
        if not screen_slug and score == 1:
            x_slug = 640
            vel_slug = 2
            screen_slug = True
        elif not screen_slug and score == 2:
            x_slug = 640
            vel_slug = 6
            screen_slug = True
        if sec == 20:
            main = False
            home_screen = True
            slow = True

        time = font.render("Time: " + str(sec) + "s", True, (255,255,255))
        win.blit(time, (550, 25))

    #desenha as animações na tela
    def draw():
        #placar e tempo
        score_screen()
        time_game()       
        #Desenha dos objetos na tela
        draw_char()
        draw_enemy_slug()
        #chama a colisão
        colision()
        pygame.display.update()

    #Define o loop principal
    while main:
        if not home_screen:
            #define os frames per seconds do jogo
            clock.tick(60)
            #desenha o cenario:
            draw_scenario()
            #chama a função que desenha os objetos animados
            draw()
            #chama a funcao de mover o personagem
            move_char()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main = False
                    run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                main = False
                home_screen = True
                dead = False
        while home_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    home_screen = False
                    main = False
                    run = False
            #Tela de Inicio
            #Chama o background do jogo
            win.blit(pygame.image.load("arquivos/bg.jpg"),(0,0))
            if dead:
                #mostra a mensagem de morte
                win.blit(pygame.image.load("arquivos/dead.png"), (152,130))
            if slow:
                #Mostra a tela de tempo acabado
                win.blit(pygame.image.load("arquivos/lento.png"), (152,130))
            else:            
                #Mostra na tela as informações iniciais
                win.blit(pygame.image.load("arquivos/infos.png"), (152,130))
            #desenha a tecla enter
            win.blit(pygame.image.load("arquivos/enter.png"), (192,360))
            #desenha o logo da tela
            win.blit(pygame.image.load("arquivos/logo.png"), (0,10))
            #atualiza a tela
            pygame.display.update()
            #Verifica se o jogador clicou em Enter para iniciar o jogo
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                home_screen = False
                pygame.mixer.music.load("arquivos/song/star.mp3")
                pygame.mixer.music.play()
        
#encerra o Pygame
pygame.quit()
