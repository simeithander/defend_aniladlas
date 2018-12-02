'''
Game Defend Aniladlas
Alunos: Simei Thander e Rafael Crisostomos
IFRN - TADS 2018.2 - www.ifrn.edu.br
'''
import pygame, os, sys
pygame.mixer.init()
pygame.init()

#Define o tamanho da tela do jogo
display_width = 640
display_height = 480
#seta na variavel win o display com largura e altura
win = pygame.display.set_mode((display_width, display_height))
#Seta o nome do game na barra superior de titulos
pygame.display.set_caption("Defend Aniladlas")
#obtem o clock do Pygame
clock = pygame.time.Clock()

#variaveis para a tela home
run = True
home_screen = True
dead = False
slow = False
you_win = False
#define o mixer
pygame.mixer.pre_init(44100, 16, 2, 5000)
#define a musica de fundo
bg_music = pygame.mixer.Sound("arquivos/song/game_play.ogg")
#define que a musica irá se repetir
bg_music_play = bg_music.play(-1)
#da play da music
bg_music_play.queue(bg_music)

#Define que o loop começará verdadeiro
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
    #contador dos sprites para o char em IDLE
    cont_idle = 0
    #Velocidade
    vel = 10
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
    vel_slug = 2
    patch_slug = [end_slug, x_slug]
    screen_slug = True

    #Contagem de sprites do BOSS
    boss_cont_anim = 0
    boss_cont = 0
    screen_boss = False
    x_boss = 500
    y_boss = 200

    #pontuação
    def score_screen():
        global score
        text_point = font.render('Score: ' + str(score), 1, (255,255,255))
        win.blit(text_point, (550, 5))

    #colisão
    def collision():
        global main, home_screen, screen_slug, dead, you_win, score, x_boss, y_boss

        #Rect do heroi
        char = pygame.image.load("arquivos/player/player-idle/p_right_idle.png")
        char_rect = char.get_rect().move(x,y)
        char_rect.width = 64

        if screen_boss:
            #Rect do BOSS
            boss = pygame.image.load("arquivos/monsters/boss/aniladlas_0.png")
            #matar o boss
            if char_rect.collidepoint(x_boss+30, y_boss) == 1:
                print("morreu o BOSS")
                x_boss = 640
                y_boss = 480
                main = False
                home_screen = True
                you_win = True
            elif char_rect.collidepoint(x_boss, y_boss+90) == 1:
                print("morreu pela esquerda")
                main = False
                home_screen = True
                dead = True
            elif char_rect.collidepoint(x_boss+60, y_boss+55) == 1:
                print("morreu pela direita")
                main = False
                home_screen = True
                dead = True
    
        if screen_slug:
            #Rect do Slug
            slug = pygame.image.load("arquivos/monsters/slug/slug-left-1.png")
            slug_rect = slug.get_rect().move(x_slug,y_slug)
            slug_rect.width = 64
            #matar o slug
            if char_rect.collidepoint(x_slug+34, y_slug) == 1:
                print("morreu o slug")
                screen_slug = False
                score += 1
            elif char_rect.collidepoint(x_slug, y_slug+5) == 1:
                print("morreu pela esquerda")
                main = False
                home_screen = True
                dead = True
            elif char_rect.collidepoint(x_slug+64, y_slug+40) == 1:
                print("morreu pela direita")
                main = False
                home_screen = True
                dead = True
        
    #Desenha o cenário
    def draw_scenario():
        if not screen_slug and score >= 3:
            win.blit(pygame.image.load("arquivos/bg_boss.jpg"),(0,0))
        else:
            win.blit(pygame.image.load("arquivos/bg2.jpg"),(0,0))

        bloco = pygame.image.load("arquivos/bloco.jpg")
        house = pygame.image.load("arquivos/house.png")
        win.blit(house,(50,211))
        cont = 0
        for i in range(0,31):
            win.blit(bloco,(cont,453))
            cont += 32

    #desenha o personagem
    def draw_char():
        global walk_count, cont_idle
        
        walk_right = []
        walk_left = []
        jump_left = []
        jump_right = []
        char_right_idle = []
        char_left_idle = []

        #Carrega os sprites de andar para a lista
        for i in range(0,8):
            walk_right.append(pygame.image.load("arquivos/player/player-skip/p_left_"+str(i)+".png"))
            walk_left.append(pygame.image.load("arquivos/player/player-skip/p_right_"+str(i)+".png"))

        #sprites de pulo
        for i in range(0,4):
            jump_left.append(pygame.image.load("arquivos/player/player-jump/player-jump-left-"+str(i)+".png"))
            jump_right.append(pygame.image.load("arquivos/player/player-jump/player-jump-right-"+str(i)+".png"))

        #sprite Idle (parado)
        for i in range(0,9):
            char_right_idle.append(pygame.image.load("arquivos/player/player-idle/player-idle-"+str(i)+".png"))
            char_left_idle.append(pygame.image.load("arquivos/player/player-idle/player-idle-left-"+str(i)+".png"))
    
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
        global x_slug, walk_count_slug, vel_slug

        walk_left = []
        walk_right = []

        for i in range(0, 4):
            walk_left.append(pygame.image.load("arquivos/monsters/slug/slug-left-"+str(i)+".png"))
            walk_right.append(pygame.image.load("arquivos/monsters/slug/slug-right-"+str(i)+".png"))
        
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

    #desenha o BOSS
    def draw_boss():
        global boss_cont_anim
        sprite = boss_cont_anim//2
        boss = []
        #adiciona os sprites a lista
        for i in range(0, 12):
            boss.append(pygame.image.load("arquivos/monsters/boss/aniladlas_"+str(i)+".png"))
        
        #mostra o boss na tela
        if screen_boss:
            win.blit(boss[sprite], (x_boss,y_boss))

        #tempo dos sprites do boss
        boss_cont_anim += 1
        if boss_cont_anim == 24:
            boss_cont_anim = 0
    
    #move o BOSS aleatoriamente
    def move_boss():
        global screen_boss, boss_cont, x_boss, y_boss, main, home_screen, dead
        #Caso o BOSS entre na tela, será incrimentado um contador e utilizado a divisão por inteiro para 24
        if screen_boss:
            if (boss_cont//24) % 2 == 0:
                screen_boss = True
            elif (boss_cont//24) == 1:
                screen_boss = False
                x_boss = 550
                y_boss = 300
            elif (boss_cont//24) == 3:
                screen_boss = False
                x_boss = 480
                y_boss = 250
            elif (boss_cont//24) == 5:
                screen_boss = False
                x_boss = 350
                y_boss = 150   
            elif (boss_cont//24) == 7:
                screen_boss = False
                x_boss = 500
                y_boss = 355
            elif (boss_cont//24) == 9 and x_boss < 640 and y_boss < 480:
                screen_boss = False
                x_boss = 100
                y_boss = 355
            elif (boss_cont//24) == 11 and x_boss < 640 and y_boss < 480:
                main = False
                home_screen = True
                dead = True  
            #contagem das aparições do BOSS    
            boss_cont +=1   

    #Define a movimentação do personagem
    def move_char():
        global x, y, is_jump, jump_count, left, right, press_left, walk_count
       
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
        global x_slug, vel_slug, screen_slug, main, home_screen, slow, screen_boss
        sec = (pygame.time.get_ticks() - t) // 1000
        if not screen_slug and score == 1:
            x_slug = 640
            vel_slug = 2
            screen_slug = True
        elif not screen_slug and score == 2:
            x_slug = 640
            vel_slug = 6
            screen_slug = True
        elif not screen_slug and score == 3:
            screen_boss = True
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
        draw_boss()
        pygame.display.update()

    #Define o loop principal
    while main:
        if not home_screen:
            #define os frames per seconds do jogo
            clock.tick(60)
            #chama a função mover boss
            move_boss()
            #desenha o cenario:
            draw_scenario()
            #chama a colisão
            collision()
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
            elif slow:
                #Mostra a tela de tempo acabado
                win.blit(pygame.image.load("arquivos/lento.png"), (152,130))
            elif you_win:
                win.blit(pygame.image.load("arquivos/end.png"), (152,130))
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
                pygame.mixer.music.load("arquivos/song/enter.mp3")
                pygame.mixer.music.play()
        
#encerra o Pygame
pygame.quit()
