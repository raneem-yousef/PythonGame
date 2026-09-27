import os
import sys
import cfg
import random
import pygame
from modules import *


def loadSounds():
    shoot_sound = pygame.mixer.Sound(cfg.SHOOT_SOUND)
    win_sound = pygame.mixer.Sound(cfg.WIN_SOUND)
    lose_sound = pygame.mixer.Sound(cfg.LOSE_SOUND)
    dead_sound = pygame.mixer.Sound(cfg.DEAD_SOUND)
    return shoot_sound, win_sound, lose_sound, dead_sound


def game_intro(screen):
    clock = pygame.time.Clock()
    intro = True
    font = pygame.font.SysFont('arial', 22)
    title_font = pygame.font.SysFont('arial', 45)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    intro = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(cfg.SPACE_BLUE)

        title = title_font.render(
            "RANEEM'S SPACE GAME", True, cfg.WHITE
        )
        title_rect = title.get_rect(center=(400, 120))
        screen.blit(title, title_rect)

        instructions = [
            "A / Left Arrow  : Move Left",
            "D / Right Arrow : Move Right",
            "P / p           : Pause",
            "Left Click      : Shoot",
            "Right Click     : Shoot",
            "Space / Enter   : Shoot",
            "Reach 1000 points to win!"
        ]

        y = 190
        for instruction in instructions:
            text = font.render(instruction, True, cfg.WHITE)
            text_rect = text.get_rect(center=(400, y))
            screen.blit(text, text_rect)
            y += 35

        pygame.draw.rect(screen, cfg.GREEN, (330, 470, 140, 55))

        start_text = font.render("START", True, cfg.BLACK)
        start_rect = start_text.get_rect(center=(400, 497))
        screen.blit(start_text, start_rect)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 330 < mouse[0] < 470 and 470 < mouse[1] < 525:
            pygame.draw.rect(screen, cfg.WHITE, (330, 470, 140, 55))
            screen.blit(start_text, start_rect)

            if click[0] or click[2]:
                intro = False

        pygame.display.update()
        clock.tick(60)


def paused(screen):
    clock = pygame.time.Clock()
    pause_game = True
    font = pygame.font.SysFont('arial', 45)
    small_font = pygame.font.SysFont('arial', 22)

    while pause_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_game = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(cfg.SPACE_BLUE)

        text = font.render("PAUSED", True, cfg.WHITE)
        text_rect = text.get_rect(center=(400, 250))
        screen.blit(text, text_rect)

        continue_text = small_font.render(
            "Press P to Continue", True, cfg.WHITE
        )
        continue_rect = continue_text.get_rect(center=(400, 330))
        screen.blit(continue_text, continue_rect)

        pygame.display.update()
        clock.tick(60)


def endInterface(screen, color, is_win):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 45)
    small_font = pygame.font.SysFont('arial', 25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    mouse = pygame.mouse.get_pos()

                    if 300 < mouse[0] < 500 and 400 < mouse[1] < 460:
                        return True

                    if 300 < mouse[0] < 500 and 480 < mouse[1] < 540:
                        pygame.quit()
                        sys.exit()

        screen.fill(color)

        if is_win:
            text = font.render(
                "CONGRATS, YOU WIN!", True, cfg.WHITE
            )
        else:
            text = font.render(
                "YOU LOSE!", True, cfg.WHITE
            )

        text_rect = text.get_rect(center=(400, 270))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, cfg.GREEN, (300, 400, 200, 60))

        restart_text = small_font.render(
            "RESTART", True, cfg.BLACK
        )
        restart_rect = restart_text.get_rect(center=(400, 430))
        screen.blit(restart_text, restart_rect)

        pygame.draw.rect(screen, cfg.RED, (300, 480, 200, 60))

        exit_text = small_font.render(
            "EXIT", True, cfg.WHITE
        )
        exit_rect = exit_text.get_rect(center=(400, 510))
        screen.blit(exit_text, exit_rect)

        pygame.display.update()
        clock.tick(60)


def startGame(
    screen,
    shoot_sound,
    win_sound,
    lose_sound,
    dead_sound
):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 18)

    if not os.path.isfile('score'):
        f = open('score', 'w')
        f.write('0')
        f.close()

    with open('score', 'r') as f:
        highest_score = int(f.read().strip())

    enemies_group = pygame.sprite.Group()

    for i in range(55):
        if i < 11:
            enemy = enemySprite(
                'small',
                i,
                cfg.SMALL_ENEMY_COLOR,
                cfg.ENEMY_BULLET_COLOR
            )
        elif i < 33:
            enemy = enemySprite(
                'medium',
                i,
                cfg.MEDIUM_ENEMY_COLOR,
                cfg.ENEMY_BULLET_COLOR
            )
        else:
            enemy = enemySprite(
                'large',
                i,
                cfg.LARGE_ENEMY_COLOR,
                cfg.ENEMY_BULLET_COLOR
            )

        enemy.rect.x = 85 + (i % 11) * 50
        enemy.rect.y = 120 + (i // 11) * 45
        enemies_group.add(enemy)

    boomed_enemies_group = pygame.sprite.Group()
    en_bullets_group = pygame.sprite.Group()

    ufo = ufoSprite(color=cfg.UFO_COLOR)

    myaircraft = aircraftSprite(
        color=cfg.AIRCRAFT_COLOR,
        bullet_color=cfg.BULLET_COLOR
    )

    my_bullets_group = pygame.sprite.Group()

    enemy_move_count = 24
    enemy_move_interval = 24
    enemy_move_flag = False
    enemy_change_direction_count = 0
    enemy_change_direction_interval = 60
    enemy_need_down = False
    enemy_move_right = True
    enemy_need_move_row = 6
    enemy_max_row = 5
    enemy_shot_interval = 100
    enemy_shot_count = 0
    enemy_shot_flag = False

    running = True
    is_win = False

    move_left = False
    move_right = False

    last_mouse_x = pygame.mouse.get_pos()[0]

    while running:
        screen.fill(cfg.SPACE_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = True

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = True

                if event.key == pygame.K_p:
                    paused(screen)

                if event.key == pygame.K_m:
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.4)

                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    my_bullet = myaircraft.shot()

                    if my_bullet:
                        my_bullets_group.add(my_bullet)
                        shoot_sound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = False

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    my_bullet = myaircraft.shot()

                    if my_bullet:
                        my_bullets_group.add(my_bullet)
                        shoot_sound.play()

        mouse_x = pygame.mouse.get_pos()[0]

        if mouse_x != last_mouse_x:
            myaircraft.rect.x += mouse_x - last_mouse_x
            last_mouse_x = mouse_x

        if move_left:
            myaircraft.rect.x -= 7

        if move_right:
            myaircraft.rect.x += 7

        if myaircraft.rect.x < 0:
            myaircraft.rect.x = 0

        if myaircraft.rect.x > (
            cfg.SCREENSIZE[0] - myaircraft.rect.width
        ):
            myaircraft.rect.x = cfg.SCREENSIZE[0] - myaircraft.rect.width

        if myaircraft.is_cooling:
            myaircraft.cooling_count -= 1

            if myaircraft.cooling_count == 0:
                myaircraft.is_cooling = False

        enemy_shot_count += 1

        if enemy_shot_count > enemy_shot_interval:
            enemy_shot_flag = True

            enemies_survive_list = [
                enemy.number for enemy in enemies_group
            ]

            if enemies_survive_list:
                shot_number = random.choice(enemies_survive_list)

            enemy_shot_count = 0

        enemy_move_count += 1

        if enemy_move_count > enemy_move_interval:
            enemy_move_count = 0
            enemy_move_flag = True
            enemy_need_move_row -= 1

            if enemy_need_move_row == 0:
                enemy_need_move_row = enemy_max_row

            enemy_change_direction_count += 1

            if enemy_change_direction_count > enemy_change_direction_interval:
                enemy_change_direction_count = 1
                enemy_move_right = not enemy_move_right
                enemy_need_down = True

                enemy_move_interval = max(
                    8, enemy_move_interval - 3
                )

                enemy_shot_interval = max(
                    30, enemy_shot_interval - 5
                )

        for enemy in enemies_group:
            if enemy_shot_flag:
                if enemy.number == shot_number:
                    en_bullet = enemy.shot()
                    en_bullets_group.add(en_bullet)

            if enemy_move_flag:
                if enemy.number in range(
                    (enemy_need_move_row - 1) * 11,
                    enemy_need_move_row * 11
                ):
                    if enemy_move_right:
                        enemy.update('right', cfg.SCREENSIZE[1])
                    else:
                        enemy.update('left', cfg.SCREENSIZE[1])
            else:
                enemy.update(None, cfg.SCREENSIZE[1])

            if enemy_need_down:
                if enemy.update('down', cfg.SCREENSIZE[1]):
                    running = False
                    is_win = False

            enemy.draw(screen)

        enemy_move_flag = False
        enemy_need_down = False
        enemy_shot_flag = False

        for boomed_enemy in boomed_enemies_group:
            if boomed_enemy.boom(screen):
                boomed_enemies_group.remove(boomed_enemy)
                del boomed_enemy

        if not myaircraft.one_dead:
            if pygame.sprite.spritecollide(
                myaircraft,
                en_bullets_group,
                True,
                None
            ):
                myaircraft.one_dead = True

        if myaircraft.one_dead:
            if myaircraft.boom(screen):
                myaircraft.resetBoom()
                myaircraft.num_life -= 1
                dead_sound.play()

                if myaircraft.num_life < 1:
                    running = False
                    is_win = False
        else:
            myaircraft.draw(screen)

        if (not ufo.has_boomed) and ufo.is_dead:
            if ufo.boom(screen):
                ufo.has_boomed = True
        else:
            ufo.update(cfg.SCREENSIZE[0])
            ufo.draw(screen)

        for bullet in my_bullets_group:
            if bullet.update():
                my_bullets_group.remove(bullet)
                del bullet
            else:
                bullet.draw(screen)

        for bullet in en_bullets_group:
            if bullet.update(cfg.SCREENSIZE[1]):
                en_bullets_group.remove(bullet)
                del bullet
            else:
                bullet.draw(screen)

        for enemy in enemies_group:
            if pygame.sprite.spritecollide(
                enemy,
                my_bullets_group,
                True,
                None
            ):
                boomed_enemies_group.add(enemy)
                enemies_group.remove(enemy)
                myaircraft.score += enemy.reward

        if pygame.sprite.spritecollide(
            ufo,
            my_bullets_group,
            True,
            None
        ):
            ufo.is_dead = True
            myaircraft.score += ufo.reward

        if myaircraft.score > highest_score:
            highest_score = myaircraft.score

        if (
            myaircraft.score % 2000 == 0
            and myaircraft.score > 0
            and myaircraft.score != myaircraft.old_score
        ):
            myaircraft.old_score = myaircraft.score
            myaircraft.num_life = min(
                myaircraft.num_life + 1,
                myaircraft.max_num_life
            )

        if myaircraft.score >= cfg.WIN_SCORE:
            is_win = True
            running = False

        showText(
            screen, 'SCORE:', cfg.TEXT_COLOR, font, 200, 8
        )
        showText(
            screen, str(myaircraft.score),
            cfg.TEXT_COLOR, font, 200, 24
        )
        showText(
            screen, 'ENEMY:', cfg.TEXT_COLOR, font, 370, 8
        )
        showText(
            screen, str(len(enemies_group)),
            cfg.TEXT_COLOR, font, 370, 24
        )
        showText(
            screen, 'HIGHEST:', cfg.TEXT_COLOR, font, 540, 8
        )
        showText(
            screen, str(highest_score),
            cfg.TEXT_COLOR, font, 540, 24
        )
        showText(
            screen, 'FPS: ' + str(int(clock.get_fps())),
            cfg.GREEN, font, 8, 8
        )

        showLife(
            screen,
            myaircraft.num_life,
            cfg.AIRCRAFT_COLOR
        )

        if pygame.mixer.music.get_volume() == 0:
            showText(
                screen, 'MUSIC: OFF (M)',
                cfg.RED, font, 8, 35
            )
        else:
            showText(
                screen, 'MUSIC: ON (M)',
                cfg.GREEN, font, 8, 35
            )

        pygame.display.update()
        clock.tick(cfg.FPS)

    with open('score', 'w') as f:
        f.write(str(highest_score))

    if is_win:
        win_sound.play()
    else:
        lose_sound.play()

    return is_win


def main():
    pygame.init()

    pygame.display.set_caption(
        "RANEEM'S SPACE GAME "
    )

    screen = pygame.display.set_mode(
        cfg.SCREENSIZE
    )

    pygame.mixer.init()

    pygame.mixer.music.load(
        cfg.BGMPATH
    )

    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(0)

    shoot_sound, win_sound, lose_sound, dead_sound = loadSounds()

    game_intro(screen)

    while True:
        is_win = startGame(
            screen,
            shoot_sound,
            win_sound,
            lose_sound,
            dead_sound
        )

        restart = endInterface(
            screen,
            cfg.SPACE_BLUE,
            is_win
        )

        if restart:
            continue


if __name__ == '__main__':
    main()
