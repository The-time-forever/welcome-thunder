import cv2
import pygame
import random


WIDTH = 512
HEIGHT = 768
CAM_WIDTH = 640
CAM_HEIGHT = 480


pygame.init()
pygame.display.set_caption("Face Controlled Thunder")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    exit()


cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
if face_cascade.empty():

    cap.release()
    exit()

# -------- Page 1--------
pygame.display.set_caption("Welcome Thunder")
bg = pygame.image.load("start_bg0.jpg")
screen.blit(bg, (0, 0))

myfont = pygame.font.SysFont("simhei", 60)
color_black = (0, 0, 0)
color_red = (255, 0, 0)
textimage = myfont.render("Welcome Thunder", True, color_black)
screen.blit(textimage, (45, 185))
textimage = myfont.render("Welcome Thunder", True, color_red)
screen.blit(textimage, (40, 180))

plane_img_start = pygame.image.load("plane.png").convert_alpha()
screen.blit(plane_img_start, ((WIDTH - 100) / 2, 300))

startimage = pygame.image.load("start.png").convert_alpha()
screen.blit(startimage, ((WIDTH - 138) / 2, 600))

instruction = pygame.image.load("instruction3.png").convert_alpha()
screen.blit(instruction, (20, 350))

myfont1 = pygame.font.SysFont("simhei", 20)
textimage1 = myfont1.render("space means shoot", True, color_black)
screen.blit(textimage1, (170, 580))

ctn_start = True
while ctn_start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ctn_start = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            exit()
    pygame.display.update()

# -------- Page 2--------
by = pygame.image.load("map1.jpg")
W, H = 100, 148


plane = pygame.image.load("jet.png").convert_alpha()
attack = pygame.image.load("bullet.png").convert_alpha()
missile = pygame.image.load("daodan.png").convert_alpha()
bullet = pygame.image.load("alien_bullet.png").convert_alpha()
shield_image = pygame.image.load("superglow05.png").convert_alpha()

x, y = (WIDTH - W) / 2, HEIGHT - H
attack_W, attack_H = 16, 16
attack_list, missiles_list, enemies_list, enemy_bullets_list = [], [], [], []

missile_cooldown = 5000
last_missile_time = 0
player_health = 100
invincibility_duration = 1000
last_hit_time = 0
player_invincible = False
score = 0
ui_font = pygame.font.SysFont("simhei", 28)

shield_active = False
shield_skill_used = False
shield_duration = 3000
shield_start_time = 0

HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT = 150, 25
health_images = {
    100: pygame.transform.scale(pygame.image.load("health_100.png").convert_alpha(),
                                (HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)),
    80: pygame.transform.scale(pygame.image.load("health_80.png").convert_alpha(),
                               (HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)),
    60: pygame.transform.scale(pygame.image.load("health_60.png").convert_alpha(),
                               (HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)),
    40: pygame.transform.scale(pygame.image.load("health_40.png").convert_alpha(),
                               (HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)),
    20: pygame.transform.scale(pygame.image.load("health_20.png").convert_alpha(),
                               (HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)),
    0: pygame.transform.scale(pygame.image.load("health_0.png").convert_alpha(), (HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
}
health_steps = [100, 80, 60, 40, 20, 0]


enemy_move_event = pygame.USEREVENT
enemy_spawn_event = pygame.USEREVENT + 1
enemy_shoot_event = pygame.USEREVENT + 2
attack_event = pygame.USEREVENT + 3
missile_event = pygame.USEREVENT + 4
pygame.time.set_timer(enemy_move_event, 50)
pygame.time.set_timer(enemy_spawn_event, 1500)
pygame.time.set_timer(enemy_shoot_event, 2000)
pygame.time.set_timer(attack_event, 20)
pygame.time.set_timer(missile_event, 20)


SCORE_TO_TRIGGER_BOSS = 200
boss_fight_triggered = False
boss_active = False
be = False
boss_image = pygame.image.load("boss_1.png").convert_alpha()
boss_rect = boss_image.get_rect()
boss_max_health = 1000
boss_health = boss_max_health
boss_speed_x = 3
BOSS_HEALTH_BAR_WIDTH = 400
BOSS_HEALTH_BAR_HEIGHT = 25
BOSS_HEALTH_BAR_COLOR_BG = (50, 50, 50)
BOSS_HEALTH_BAR_COLOR_FG = (255, 0, 0)

clock = pygame.time.Clock()
frame_counter = 0
face_pos = None
PROCESS_EVERY_N_FRAMES = 3
ctn_game = True
while ctn_game:
    clock.tick(60)
    frame_counter += 1


    ret, frame = cap.read()
    if not ret:
        break


    frame = cv2.flip(frame, 1)
    if frame_counter % PROCESS_EVERY_N_FRAMES == 0:
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))
        if len(faces) > 0:
            face_pos = faces[0]
            fx, fy, fw, fh = face_pos
            cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)

    if face_pos is not None:
        fx, fy, fw, fh = face_pos
        face_center_x = fx + fw // 2
        face_center_y = fy + fh // 2
        target_x = (face_center_x / CAM_WIDTH) * WIDTH
        target_y = (face_center_y / CAM_HEIGHT) * HEIGHT
        x = target_x - W / 2
        y = target_y - H / 2
        x = max(0, min(x, WIDTH - W))
        y = max(0, min(y, HEIGHT - H))

    cv2.imshow("Camera Feed", frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctn_game = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ctn_game = False
            elif event.key == pygame.K_SPACE:
                attack_x = x + W / 2 - attack_W / 2
                new_attack = pygame.Rect(attack_x, y, attack_W, attack_H)
                attack_list.append(new_attack)
            elif event.key == pygame.K_e:
                current_time = pygame.time.get_ticks()
                if current_time - last_missile_time > missile_cooldown:
                    last_missile_time = current_time
                    missile_x = x + W / 2 - missile.get_width() / 2
                    new_missile = pygame.Rect(missile_x, y, missile.get_width(), missile.get_height())
                    missiles_list.append(new_missile)


        elif event.type == enemy_spawn_event and not boss_fight_triggered:
            random_enemy_image = pygame.image.load(f"alien_{random.randint(1, 5)}.png").convert_alpha()
            enemy_W, enemy_H = random_enemy_image.get_size()
            new_enemy_rect = pygame.Rect(random.randint(0, WIDTH - enemy_W), -enemy_H, enemy_W, enemy_H)
            enemies_list.append((new_enemy_rect, random_enemy_image))

        elif event.type == enemy_move_event:
            for enemy_tuple in enemies_list: enemy_tuple[0].y += 2
            for bullet_rect in enemy_bullets_list: bullet_rect.y += 5

        elif event.type == enemy_shoot_event:
            if boss_active:
                bullet_W, bullet_H = bullet.get_size()
                enemy_bullets_list.append(
                    pygame.Rect(boss_rect.centerx - bullet_W / 2, boss_rect.bottom, bullet_W, bullet_H))
            else:
                for enemy_tuple in enemies_list:
                    enemy_rect = enemy_tuple[0]
                    bullet_W, bullet_H = bullet.get_size()
                    enemy_bullets_list.append(
                        pygame.Rect(enemy_rect.centerx - bullet_W / 2, enemy_rect.bottom, bullet_W, bullet_H))

        elif event.type == attack_event:
            for attack_rect in attack_list: attack_rect.y -= 10

        elif event.type == missile_event:
            for missile_rect in missiles_list: missile_rect.y -= 5


    player_rect = pygame.Rect(x, y, W, H)
    if player_health < 50 and not shield_skill_used:
        shield_active = True
        shield_skill_used = True
        shield_start_time = pygame.time.get_ticks()
    if shield_active:
        current_time = pygame.time.get_ticks()
        if current_time - shield_start_time > shield_duration:
            shield_active = False




    if score >= SCORE_TO_TRIGGER_BOSS and not boss_fight_triggered:
        boss_fight_triggered = True
        boss_active = True
        boss_rect.centerx = WIDTH / 2
        boss_rect.bottom = 0
        enemies_list.clear()
        enemy_bullets_list.clear()

    if boss_active:
        boss_rect.x += boss_speed_x
        if boss_rect.left < 0 or boss_rect.right > WIDTH: boss_speed_x *= -1
        if boss_rect.top < 20: boss_rect.y += 1


    for bullet_rect in attack_list[:]:
        for enemy_tuple in enemies_list[:]:
            if bullet_rect.colliderect(enemy_tuple[0]):
                attack_list.remove(bullet_rect)
                enemies_list.remove(enemy_tuple)
                score += 10
                break
        if boss_active and bullet_rect.colliderect(boss_rect):
            attack_list.remove(bullet_rect)
            boss_health -= 10

    for missile_rect in missiles_list[:]:
        for enemy_tuple in enemies_list[:]:
            if missile_rect.colliderect(enemy_tuple[0]):
                enemies_list.remove(enemy_tuple)
                score += 50
        if boss_active and missile_rect.colliderect(boss_rect):
            missiles_list.remove(missile_rect)
            boss_health -= 50


    current_time = pygame.time.get_ticks()
    if player_invincible and current_time - last_hit_time > invincibility_duration:
        player_invincible = False

    if not player_invincible and not shield_active:
        for bullet_rect in enemy_bullets_list[:]:
            if player_rect.colliderect(bullet_rect):
                enemy_bullets_list.remove(bullet_rect)
                player_health -= 20
                last_hit_time = current_time
                player_invincible = True
                break
        for enemy_tuple in enemies_list[:]:
            if player_rect.colliderect(enemy_tuple[0]):
                player_health = 0
                break


    if player_health <= 0: ctn_game = False
    if boss_health <= 0 and boss_active:
        ctn_game = False
        be = True


    enemies_list = [e for e in enemies_list if e[0].top < HEIGHT]
    enemy_bullets_list = [b for b in enemy_bullets_list if b.top < HEIGHT]
    attack_list = [a for a in attack_list if a.bottom > 0]
    missiles_list = [m for m in missiles_list if m.bottom > 0]


    screen.blit(by, (0, 0))
    screen.blit(plane, player_rect)
    if shield_active:
        shield_rect = shield_image.get_rect(center=player_rect.center)
        screen.blit(shield_image, shield_rect)
    for enemy_rect, enemy_image in enemies_list: screen.blit(enemy_image, enemy_rect)
    for bullet_rect in enemy_bullets_list: screen.blit(bullet, bullet_rect)
    for attack_rect in attack_list: screen.blit(attack, attack_rect)
    for missile_rect in missiles_list: screen.blit(missile, missile_rect)


    health_bar_to_show = None
    for step in health_steps:
        if player_health >= step:
            health_bar_to_show = health_images[step]
            break
    if health_bar_to_show:
        screen.blit(health_bar_to_show, (10, 10))
        health_text = ui_font.render(str(player_health), True, (255, 255, 255))
        screen.blit(health_text, (health_bar_to_show.get_width() + 20, 12))

    score_text = ui_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 15, 10))

    if boss_active:
        screen.blit(boss_image, boss_rect)
        current_health_width = (boss_health / boss_max_health) * BOSS_HEALTH_BAR_WIDTH
        health_bar_bg_rect = pygame.Rect((WIDTH - BOSS_HEALTH_BAR_WIDTH) / 2, 10, BOSS_HEALTH_BAR_WIDTH,
                                         BOSS_HEALTH_BAR_HEIGHT)
        health_bar_fg_rect = pygame.Rect((WIDTH - BOSS_HEALTH_BAR_WIDTH) / 2, 10, current_health_width,
                                         BOSS_HEALTH_BAR_HEIGHT)
        pygame.draw.rect(screen, BOSS_HEALTH_BAR_COLOR_BG, health_bar_bg_rect)
        pygame.draw.rect(screen, BOSS_HEALTH_BAR_COLOR_FG, health_bar_fg_rect)
    cv2.waitKey(1)
    pygame.display.update()

# -------- Page 3--------
gameover_img = pygame.image.load("map3.png")
success_img = pygame.image.load("success.png").convert_alpha()
ctn_end = True
while ctn_end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            ctn_end = False

    screen.blit(gameover_img, (0, 0))
    if be:
        screen.blit(success_img, (0, 0))

    pygame.display.update()


cap.release()
cv2.destroyAllWindows()
pygame.quit()
exit()