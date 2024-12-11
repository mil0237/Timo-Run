import pygame
import sys
import random
import os

# step1 : set screen, fps
# step2 : show timo, jump timo
# step3 : show mushroom, move mushroom

pygame.init()
pygame.display.set_caption('Timo Run')
MAX_WIDTH = 800
MAX_HEIGHT = 400


#소리 로드
pygame.mixer.init()
bgm_sound = pygame.mixer.Sound('sounds/bgm.wav')
jump_sound= pygame.mixer.Sound('sounds/JumpSound.wav')
gameover_sound= pygame.mixer.Sound('sounds/gameover.wav')

def main():
    os.chdir('C:/Users/user/Desktop/TimoRun/Timo-Run')
    # set screen, fps
    screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    fps = pygame.time.Clock()
    
    #bgm play
    bgm_sound.play(-1)

    # background
    backgrounds = [ pygame.image.load('images/background1.png'),
                       pygame.image.load('images/background2.png'),
                       pygame.image.load('images/background3.png')
                       ]
    current_background_index=0
    
    # timo
    imgTimo1 = pygame.image.load('images/timo1.png')
    imgTimo2 = pygame.image.load('images/timo2.png')
    timo_size = 64
    timo_x = 50
    timo_y = MAX_HEIGHT - timo_size
    jump_top = 200  
    double_jump_top = 100
    leg_swap = True
    is_bottom = True
    is_go_up = False
    double_jump = False
    double_jump_used = False

    # Animation control
    animation_speed = 5  # 다리 모양을 변경하는 속도를 설정
    animation_counter = 0

    # mushroom
    imgMushroom = pygame.image.load('images/mushroom.png')
    mushrooms = []
    mushroom_spawn_time = 0
    mushroom_height = imgMushroom.get_size()[1]
   # mushroom_width = imgMushroom.get_size()[0]
   # mushroom_x = MAX_WIDTH
   # mushroom_y = MAX_HEIGHT - mushroom_height
    mushroom_spawn_interval = random.randint(800, 2000)
    mushroom_speed = 12
    mushroom_spawn_rate = 1
    last_spawn_increase_time = pygame.time.get_ticks()
    
    # items
    imgDoubleJumpItem = pygame.image.load('images/double_jump_item.png')
    item_x = random.randint(MAX_WIDTH, MAX_WIDTH*2)
    item_y = random.randint(MAX_HEIGHT - 100, MAX_HEIGHT - 50)

    
    # score
    score = 0
    font = pygame.font.Font(None, 36)
    
    #게임오버 표시
    def show_game_over():
        bgm_sound.stop()
        gameover_sound.play()
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render('Game Over', True, (255,0,0))
        score_text = font.render(f'Score: {score // 30}', True, (255,0,0))
       
        #버튼 추가
        button_font = pygame.font.Font(None, 48)
        quit_button = button_font.render('Exit', True, (255,0,0))
        restart_button = button_font.render('Restart', True, (255,0,0))
        
        quit_button_rect = quit_button.get_rect(center = (MAX_WIDTH//2, MAX_HEIGHT //1.5))
        restart_button_rect = restart_button.get_rect(center = (MAX_WIDTH //2, MAX_HEIGHT//1.2))
        
        screen.fill((255,255,255))
        screen.blit(game_over_text, (MAX_WIDTH // 2 - game_over_text.get_width()//2, MAX_HEIGHT//3))
        screen.blit(score_text, (MAX_WIDTH // 2 - score_text.get_width()//2, MAX_HEIGHT//2))
        screen.blit(quit_button, quit_button_rect)
        screen.blit(restart_button, restart_button_rect)
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif restart_button_rect.collidepoint(event.pos):
                        main()
                   
    while True:
        screen.fill((255, 255, 255))
        screen.blit(backgrounds[current_background_index], (0, 0))

        # event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if is_bottom:
                    is_go_up = True
                    is_bottom = False
                    double_jump_used = False
                    jump_sound.play()
                elif double_jump and not double_jump_used:
                    is_go_up =  True
                    double_jump = False
                    double_jump_used = True
                    jump_sound.play()
                    jump_top -= double_jump_top

        # timo move
        if is_go_up:
            timo_y -= 13.0
        elif not is_go_up and not is_bottom:
            timo_y += 12.0

        # timo top and bottom check
        if is_go_up and timo_y <= jump_top:
            is_go_up = False

        if not is_bottom and timo_y >= MAX_HEIGHT - timo_size:
            is_bottom = True
            timo_y = MAX_HEIGHT - timo_size
            jump_top = 200
        

        # mushroom move
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_increase_time >=10000:
            mushroom_spawn_rate *= 1.8
            mushroom_speed *= 1.2
            current_background_index = (current_background_index +1)%len(backgrounds)
            last_spawn_increase_time = current_time
            
        for mushroom in mushrooms:
            mushroom['x'] -= mushroom_speed
           #        mushroom['x'] -= 12.0
            if mushroom['x']<= 0:
                mushrooms.remove(mushroom)
               # mushroom['x'] = MAX_WIDTH
               # mushroom['y'] = MAX_HEIGHT - mushroom_height
                
     #   if pygame.time.get_ticks() - mushroom_spawn_time > 2000:
     #       mushrooms.append({'x': MAX_WIDTH, 'y': MAX_HEIGHT - mushroom_height})
     #       mushroom_spawn_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - mushroom_spawn_time > mushroom_spawn_interval/mushroom_spawn_rate: 
           # 랜덤 간격마다 새로운 버섯 생성 
           mushrooms.append({'x': MAX_WIDTH, 'y': MAX_HEIGHT - mushroom_height}) 
           mushroom_spawn_time = current_time
           mushroom_spawn_interval = random.randint(1000, 2500)

        # item move
        item_x -= 6.0
        if item_x <= 0:
            item_x = random.randint(MAX_WIDTH, MAX_WIDTH * 2)
            item_y = random.randint(MAX_HEIGHT - 100, MAX_HEIGHT - 50)
            
        # collision detection
        for mushroom in mushrooms:
            if ((timo_x + 10 < mushroom['x'] + imgMushroom.get_width() - 10 and
                 timo_x + timo_size - 10 > mushroom['x'] +10 and
                 timo_y +10< mushroom['y'] + mushroom_height -10 and
                 timo_y + timo_size -10 > mushroom['y']+10)):
                show_game_over()
              
            if (timo_x < item_x+ imgDoubleJumpItem.get_width() and
                timo_x + timo_size > item_x and
                 (timo_y < (item_y + imgDoubleJumpItem.get_height()) and
                  (timo_y + timo_size) > item_y)): 
                double_jump = True 
                item_x = random.randint(MAX_WIDTH, MAX_WIDTH * 2) 
                item_y = random.randint(MAX_HEIGHT - 100, MAX_HEIGHT - 50) # 아이템 위치 조정
        # draw mushroom
        for mushroom in mushrooms:
            screen.blit(imgMushroom, (mushroom['x'], mushroom['y']))

        # draw timo
        if animation_counter == animation_speed:
            leg_swap = not leg_swap
            animation_counter = 0
        else:
            animation_counter += 1

        if leg_swap:
            screen.blit(imgTimo1, (timo_x, timo_y))
        else:
            screen.blit(imgTimo2, (timo_x, timo_y))
            
        #draw double jump item
        screen.blit(imgDoubleJumpItem, (item_x, item_y))

        # score
        score += 1
        text = font.render(f'Score: {score // 30}', True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # update
        pygame.display.update()
        fps.tick(30)


if __name__ == '__main__':
    main()
