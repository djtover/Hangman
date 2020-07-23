import pygame
import math

#Display
pygame.init()
WIDTH,HEIGHT = 800,500
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hangman")


#adding the images
images = []
for i in range(7):
  image = pygame.image.load("hangman"+ str(i)+".png")
  images.append(image)


#button letters location
RADIUS = 20
GAP = 15
startx = round((WIDTH -(RADIUS*2 +GAP)*13)/2)
starty = 400  
letters = []
ascii_letter = 65
for i in range(26):
  x = startx + GAP*2 + ((RADIUS*2 + GAP)*(i%13))
  y = starty +((i//13)*(GAP+RADIUS*2))
  letters.append([x,y,chr(ascii_letter+i),True])
letters.append([WIDTH*4//5,HEIGHT*3//5,"ENTER",True])


#font
LETTER_FONT = pygame.font.SysFont("comicsans",40)
WORD_FONT = pygame.font.SysFont("comicsans",60)
TITLE_FONT = pygame.font.SysFont("comicsans",80)

#variables
hangman_status = 0
word = ""
word = word.upper()
guessed = []
FPS = 60
clock = pygame.time.Clock()


#colors
WHITE= (255,255,255)
BLACK = (0,0,0)


#draw when guessing 
def drawGame():
  win.fill(WHITE)


  # draw title
  text = TITLE_FONT.render("HANGMAN",1,BLACK)
  win.blit(text,((WIDTH//2 - text.get_width()//2),20))
  # draw word
  display_word = ""
  for letter in word:
    if letter in guessed:
      display_word += letter + " "
    else:
      display_word += "_ " 
  text = WORD_FONT.render(display_word,1,BLACK)
  win.blit(text, (400,200))

  #draw letters
  for letter in letters:
    x,y,ltr,visible = letter
    if visible:
      pygame.draw.circle(win,BLACK,(x,y),RADIUS,3)
      text = LETTER_FONT.render(ltr, 1 ,BLACK)
      win.blit(text,(x-(text.get_width()//2),y - (text.get_height()//2)))

  win.blit(images[hangman_status],(100,100))
  pygame.display.update()


#Function to display final message on screen
def display_message(msg):
  pygame.time.delay(500)
  win.fill(WHITE)
  text = WORD_FONT.render(msg,1,BLACK)
  win.blit(text, (WIDTH//2-(text.get_width()//2),HEIGHT//2 - (text.get_height()//2)))
  pygame.display.update()
  pygame.time.delay(3000)


#drawing home page
def drawHome():
  win.fill(WHITE)
   # draw title
  text = TITLE_FONT.render("HANGMAN",1,BLACK)
  win.blit(text,((WIDTH//2 - text.get_width()//2),20))

  # draw word
  text = WORD_FONT.render(word,1,BLACK)
  win.blit(text, (400,200))

   #draw letters
  for letter in letters:
    x,y,ltr,visible = letter
    if ltr == "ENTER":
      pygame.draw.rect(win,BLACK,(x-10,y-10,120,50))
      text = LETTER_FONT.render(ltr,1,WHITE)
      win.blit(text,(x,y))
    else:
      pygame.draw.circle(win,BLACK,(x,y),RADIUS,3)
      text = LETTER_FONT.render(ltr, 1 ,BLACK)
      win.blit(text,(x-(text.get_width()//2),y - (text.get_height()//2)))
  win.blit(images[hangman_status],(100,100))    
  pygame.display.update()



def resetGame():
  global hasWord,word,hangman_status
  hasWord = False  
  word = "" 
  for letter in letters:
    letter[3] = True
  hangman_status = 0
  guessed.clear()


#Game Loop
hasWord = False
run = True
while(run):
  clock.tick(FPS)
  if hasWord: 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        m_x, m_y = pygame.mouse.get_pos()
        # checkButtonClicked(m_x,m_y,hangman_status)
        for letter in letters:
          x,y,ltr,visible = letter
          if visible:
            dis = math.sqrt((m_x - x)**2 + (m_y - y)**2)
            if dis<RADIUS:
              letter[3] = False
              guessed.append(ltr)
              if ltr not in word:
                hangman_status+=1 
      
    drawGame()  
    won = True
    for letter in word:
      if letter not in guessed:
        won = False
        break

    if won:
      display_message("You won!")
      resetGame()


    if hangman_status == 6:
      display_message("You lost! The word was "+ word) 
      resetGame()     



# checking if button clicked for homepage
  else:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        m_x, m_y = pygame.mouse.get_pos()
        for letter in letters:
          x,y,ltr,visible = letter
          if visible:
            if ltr=="ENTER" and ((x-10)<=m_x<= (x+110) and (y-10<=m_y<=y+40)):
                hasWord = True
                letter[3] = False
            else:
              dis = math.sqrt((m_x - x)**2 + (m_y - y)**2)
              if dis<RADIUS:
                  word += ltr           
    drawHome()

pygame.quit() 