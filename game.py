import cv2
import mediapipe as mp
import time
import random
import pygame

pygame.mixer.init()

hit_sound = pygame.mixer.Sound("sound/bounce.wav")
miss_sound = pygame.mixer.Sound("sound/live_lost.wav")
gameover_sound = pygame.mixer.Sound("sound/mario_game_over.mp3")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

#width and height of the window
width, height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Ball properties
ball_x = random.randint(100, 500)
ball_y = 50
ball_radius = 20
ball_dx = 4
ball_dy = 4

# paddle properties
paddle_width = 100
paddle_height = 10
paddle_y = height - 50
paddle_x = width // 2 - paddle_width // 2

score = 0
lives = 3

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            indexFingerTip = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # print(indexFingerTip)
            cv2.circle(img, (int(indexFingerTip.x * width) , int(indexFingerTip.y * height)),7,(255,0,255),cv2.FILLED)
            paddle_x = int(indexFingerTip.x * width) - paddle_width // 2

    # set ball speed 
    ball_x += ball_dx
    ball_y += ball_dy

    # set bounce condition from walls
    if ball_x <= 0 or ball_x >= width:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    # set bounce condition from paddle
    if paddle_y < ball_y + ball_radius < paddle_y + paddle_height:
        if paddle_x < ball_x < paddle_x + paddle_width:
            ball_dy *= -1
            score += 1
            hit_sound.play()
            if ball_dx > 0:
                ball_dx += 0.5
            else:
                ball_dx -= 0.5
            ball_dy -= 0.5 

    # game over conditon
    if ball_y > height:
        lives -= 1
        miss_sound.play()
        ball_x = random.randint(100, 500)
        ball_y = 50
        ball_dx = 4
        ball_dy = 4
        time.sleep(1) 


    cv2.circle(img, (int(ball_x), int(ball_y)), ball_radius, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (paddle_x, paddle_y), (paddle_x + paddle_width, paddle_y + paddle_height), (0, 0, 0), cv2.FILLED)

    cv2.putText(img, f"Score: {score}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
    cv2.putText(img, f"Lives: {lives}", (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Out
    if lives == 0:
        cv2.putText(img, "Game Over!", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        cv2.imshow("Game", img)
        gameover_sound.play()
        cv2.waitKey(3000)
        break

    cv2.imshow("Game", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
