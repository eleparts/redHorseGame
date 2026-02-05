import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import digitalio
import random
import time

# 전역변수 선언
count = 0
score = 0
groupFlag = False
restartNoJump = False
game_over = False

flowerX = 64
flowerCount = 0
flowerFlag = False
randomFlowerCount = random.randint(0,50)

cloudX = 64
cloudY = random.randint(0,4)
cloudFlag = False

horseX = 0
horseY = 16
horseJump = False
horseCount = 0

delayTimer = 0.01

# 말, 구름, 꽃 이모지 정의
horse1 = [
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1],
 [0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0],
 [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
 [1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
 [1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
 [1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
 [0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
 [1,0,0,0,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0],
 [0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0],
 [0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0],
 [0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0],
 [0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0],
 [0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0],
]

horse2 = [
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0],
 [0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,1,1,0],
 [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
 [0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
 [0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
 [0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
 [1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0],
 [0,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,1,0,0,0],
 [0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0],
 [0,0,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
 [0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1],
 [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
]

horse3 = [
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0],
 [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
 [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
 [0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0],
 [0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
 [1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
 [1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
 [1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0],
 [0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,1,0,0,0],
 [0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0],
 [0,0,0,0,0,0,1,0,1,0,0,1,1,0,0,0,1,0,0,0],
 [0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0],
]

cloud = [
 [0,0,2,2,0],
 [2,2,2,2,0],
 [0,2,2,2,2],
]

flower = [
 [
     [0,3,3,3,0,0,0],
     [0,3,4,3,0,0,0],
     [0,3,3,3,0,0,0],
     [5,0,5,0,5,0,0],
     [0,5,5,5,0,0,0],
 ],
 [
     [0,0,0,0,0,0,0],
     [0,0,0,4,4,4,0],
     [0,0,0,4,4,4,0],
     [0,0,0,5,5,5,0],
     [0,0,0,0,5,0,0],
 ],
 [
     [2,2,2,0,1,1,1],
     [2,2,2,0,1,1,1],
     [0,2,0,0,0,1,0],
     [5,5,5,0,5,5,5],
     [0,5,0,0,0,5,0],
 ]
]

# display 초기화
displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,   										   # 64x32 LED_matrix를 사용하기에, 너비와 높이를 다음과 같이 설정
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7],   # rgb pin 배선 설정
    addr_pins=[board.GP26, board.GP27, board.GP28, board.GP22],					   # addr pin 배선 설정
    clock_pin=board.GP8, latch_pin=board.GP10, output_enable_pin=board.GP9)		   # lat / oe / clk pin 배선 설정

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# 스위치 입력 설정
sw = digitalio.DigitalInOut(board.GP16)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP

# 이모지에 사용할 색상 설정
emoji_bitmap = displayio.Bitmap(64, 32, 7)
emoji_palette = displayio.Palette(7)
emoji_palette[0] = 0x000000 # LED 끄기
emoji_palette[1] = 0xFF0000 # 빨간색
emoji_palette[2] = 0x0DB9F0 # 하늘색
emoji_palette[3] = 0xFFFFFF # 흰색
emoji_palette[4] = 0xFFFF00 # 노란색
emoji_palette[5] = 0x00FF00 # 초록색
emoji_palette[6] = 0x0000FF # 파란색
emoji_tile = displayio.TileGrid(emoji_bitmap, pixel_shader=emoji_palette)

# 제작해둔 이모지 출력하는 함수
def draw_emoji(emoji, start_x, start_y):
    for y in range(len(emoji)):
        for x in range(len(emoji[0])):
            color = emoji[y][x]
            if color != 0:
                screen_x = start_x + x
                screen_y = start_y + y

                if 0 <= screen_x < 64 and 0 <= screen_y < 32:
                    emoji_bitmap[screen_x, screen_y] = color
                    
# 게임오버 기준 (말과 꽃 부딪힐 때 각 좌표값 비교 후 그에 맞는 bool 값 반환하는 함수)
def check_collision(ax, ay, aw, ah, bx, by, bw, bh):
    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )

# 게임오버 후 나타날 ending 문구 제작
endingText1 = f"{score} POINT!"
ending1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=emoji_palette[1],
    text = endingText1)
ending1.x = (64 - len(endingText1) * 6) // 2
ending1.y = 6

endingText2 = "PRESS SW"
ending2 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=emoji_palette[5],
    text = endingText2)
ending2.x = (64 - len(endingText2) * 6) // 2
ending2.y = 16

endingText3 = "TO RESTART"
ending3 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=emoji_palette[6],
    text = endingText3)
ending3.x = (64 - len(endingText3) * 6) // 2
ending3.y = 26

g = displayio.Group()		# 그룹 생성
subg = displayio.Group()
g.append(emoji_tile)
subg.append(ending1)
subg.append(ending2)
subg.append(ending3)
display.root_group = g		# 그룹 내 레이어들을 display에 출력

while True:
    emoji_bitmap.fill(0)	# 전체 화면 지우기
    
    # bool타입 game_over 변수가 true일 때
    # ㄴ> 게임오버되면, 엔딩 문구 출력하고, 스위치 누르면 변수 초기화 후 게임 재시작
    if game_over:
        if groupFlag == False:
           g.append(subg)
           display.refresh()
           time.sleep(1)
           groupFlag = True
        if sw.value == False:
            g.remove(subg)
            groupFlag = False
            score = 0
            game_over = False
            flowerX = 64
            flowerCount = 0
            flowerFlag = False
            randomFlowerCount = random.randint(0,50)
            restartNoJump = True
            delayTimer = 0.01
    
    # 항시 count가 진행되며, 말 이모지가 1~3이 번갈아 출력됩니다.
    count = count + 1
    if count > 30:
        count = 0
    
    if count >= 0 and count <= 10:
        draw_emoji(horse1, horseX, horseY)
    elif count >= 11 and count <= 20:
        draw_emoji(horse2, horseX, horseY)
    elif count >= 21 and count <= 30:
        draw_emoji(horse3, horseX, horseY)
        
    # 엔딩 문장에 점수 갱신 및 가운데 정렬
    ending1.text = f"{score} POINT!"
    ending1.x = (64 - len(ending1.text) * 6) // 2
    
    # flowerX가 64(화면 오른쪽 밖)로 초기화된 상태이고, flowerCount가 랜덤으로 지정된 값만큼 카운트 되었다면,
    # 꽃 모양을 랜덤으로 지정하고, 꽃 이모지 동작을(flowerFlag를 통해) 시작합니다.
    if flowerX == 64 and flowerCount == randomFlowerCount:
        randomFlower = random.randint(0,2)
        flowerFlag = True
    # 꽃 이모지 동작을 시작하면, 이모지를 출력하고 한 칸씩 이동시킵니다.
    flowerCount = flowerCount + 1
    if flowerFlag == True:
        draw_emoji(flower[randomFlower], flowerX, 28)
        flowerX = flowerX - 1
        restartNoJump = False
        # 꽃이 화면 밖으로 넘어가고, 게임오버가 안되었으면, 말이 뛰어넘었음을 판단하여 점수를 증가합니다.
        if flowerX < -6 and game_over == False:
            score = score + 1
            if score < 30 and score % 3 == 0:				# 말 점수에 따라 속도를 높입니다.
                delayTimer = delayTimer - 0.001
            flowerX = 64									# 꽃 관련 변수들을 초기화합니다.
            flowerCount = 0
            flowerFlag = False
            randomFlowerCount = random.randint(0,50)
    
    # cloudX가 64(화면 오른쪽 밖)로 초기화된 상태일 때, 랜덤으로 cloudY 좌표를 지정합니다.
    if cloudX == 64:
        cloudY = random.randint(0,4)
        cloudFlag = True
    # 구름 이모지 동작을 시작하면, 이모지를 출력하고 한 칸씩 이동시킵니다.
    if cloudFlag == True:
        draw_emoji(cloud, cloudX, cloudY)
        cloudX = cloudX - 1
        if cloudX < 0:
            cloudX = 64
            cloudFlag = False
    
    # 버튼을 눌렀을 때, horseJump를 통해 말을 점프하는 것처럼 출력시킵니다.
    # 이때, restartNoJump는 게임오버 후 점프하면서 시작하는 것을 방지합니다.
    if sw.value == False and restartNoJump == False:
        horseJump = True

    # 말을 점프시키면, Y좌표를 5 높게 출력하고, 40 count 동안 유지되다가 내려옵니다.
    if horseJump == True:
        horseY = 11
        horseCount = horseCount + 1
        if horseCount >= 40:
            horseY = 16
            horseJump = False
            horseCount = 0
    print(horseJump)
            
    # 게임오버되지 않은 상태에서 check_collision을 통해 말과 꽃이 부딪혔다면 게임오버시킵니다.
    if game_over == False:
        if check_collision(
            horseX, horseY, 20, 16,
            flowerX, 28, 7, 4
        ):
            game_over = True
            print("GAME OVER")
    elif game_over == True:
        emoji_bitmap.fill(0)
    
    display.refresh() # 앞서 수정했던 led_matrix에 출력하는 코드들을 반영시킵니다.
    
    # 뱀이 움직이는 속도를 조절하는 핵심 부분
    time.sleep(delayTimer)





