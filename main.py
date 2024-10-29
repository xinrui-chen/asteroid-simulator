import turtle as trtl
import random as rand
import math

text = trtl.Turtle()
score_writer = trtl.Turtle()
counter = trtl.Turtle()
spaceship = trtl.Turtle()

def player():
  global spaceship
  spaceship = trtl.Turtle()
  spaceship.turtlesize(3)
  spaceship.penup()
  spaceship.color("white")
  spaceship.showturtle()

asteroid_icon = "asteroid.gif"

wn = trtl.Screen()
wn.setup(width = 1.0, height = 1.0)
wn.addshape(asteroid_icon)
wn.bgpic("bgpic.gif")

asteroid_list = [] #stores the asteroids printed
vis = [] #marks which asteroids has been popped 

word = ""
words_spelled = 0
score = 0
stop_timer = False

alphabet = [
  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
  "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]
words_list = [
  "Nebula", "Planet", "Star", "Galaxy", "Asteroid", "Comet", "Supernova",
  "Blackhole", "Sun", "Mercury", "Venus", "Earth", "Mars", "Saturn", "Jupiter",
  "Neptune", "Uranus", "Pluto", "Eclipse"
]

n = 20 #total asteroids = n + len(word)

#generates the asteroids
def coords():
  global n
  for i in range(n - len(word)):
    x = rand.randint(-250, 250)
    y = rand.randint(-250, 175)
    while (asteroids(x, y, ".") == False):
      x = rand.randint(-250, 250)
      y = rand.randint(-250, 175)

  #i is the number of times the program prints out the extra letters (guarantees the chosen word is able to be spelled out)
  for i in range(2):
    for letter in word:
      x = rand.randint(-250, 250)
      y = rand.randint(-250, 175)
      while (asteroids(x, y, letter) == False): #ensures the letters of the chosen word are generated on asteroids so the game is possible
        x = rand.randint(-250, 250)
        y = rand.randint(-250, 175)

#appends asteroids to asteroid list  
def asteroids(x, y, cL):
  global asteroid_list, vis
  if (math.sqrt(x * x + y * y) <= 25):
	  return False
  for asteroid in asteroid_list:
    xdist = x - asteroid[1]
    ydist = y - asteroid[2]
    #change 42 to control minimum distance between asteroids
    if math.sqrt(xdist * xdist + ydist * ydist) <= 42:
      return False

  current_letter = cL
  if cL == ".":
    current_letter = rand.choice(alphabet)
  
  asteroid_list.append((trtl.Turtle(shape=asteroid_icon), x, y, current_letter))
  vis.append(False)
	
  #DEBUG: print(len(asteroid_list))
  asteroid_list[-1][0].hideturtle()
  asteroid_list[-1][0].penup()

  #writes the letter
  asteroid_list[-1][0].goto(x - 12, y - 18)

  if current_letter == "J":
    asteroid_list[-1][0].goto(x - 4, y - 15)
    asteroid_list[-1][0].write(current_letter, font=("Arial", 20, "bold"))
  else:
    asteroid_list[-1][0].write(current_letter, font=("Arial", 20, "bold"))

  #shows the asteroid
  asteroid_list[-1][0].goto(x, y)
  asteroid_list[-1][0].showturtle()
  asteroid_list[-1][0].penup()

  return True

#writes the word the player has to spell out
def draw_word():
  global word, text
  text.hideturtle()
  text.clear()
  text.color("white")
  text.penup()
  text.goto(-275, 250)
  text.pendown()
  word = (rand.choice(words_list)).upper()
  text.write(word, font = ("Arial", 25, "bold"))
  
#_timer_
TIME = 70
timer = TIME #seconds on timer 
pTime = TIME 
counter_interval = 200  #interval for 1/5 second/1 tick, 1000 represents 1 second

#draws the score
def draw_score():
  global score, score_writer
  score_writer.hideturtle()
  score_writer.clear()
  score_writer.color("white")
  score_writer.penup()
  score_writer.goto(75, 200)
  score_writer.pendown()
  score_writer.write("Score: " + str(score), font = ("Arial", 25, "bold"))

#draws the timer/counter
def draw_timer():
  global counter, timer
  counter.hideturtle()
  counter.clear()
  counter.color("white")
  counter.penup()
  counter.goto(75, 250)
  counter.write("Timer: " + str(int(timer)), font = ("Arial", 25, "bold"))

#timer
def countdown():
  global timer, prev_time, score, words_spelled, stop_timer, asteroid_list
  if (stop_timer == True):
    return

  if timer <= 0:
    wn.clearscreen()
    wn.bgpic("bgpic.gif")
    player()
    global n
    letter_counter = trtl.Turtle()
    letter_counter.hideturtle()
    word_counter = trtl.Turtle()
    word_counter.hideturtle()
    reset = trtl.Turtle()
    reset.hideturtle()
    spaceship.hideturtle()

    letter_counter.color("white")
    letter_counter.penup()
    letter_counter.goto(-150, 50)
    letter_counter.write("Letters popped: " + str(score), font = ("Arial", 25, "bold"))

    word_counter.color("white")
    word_counter.penup()
    word_counter.goto(-150, -50)
    word_counter.write("Words spelled: " + str(words_spelled), font = ("Arial", 25, "bold"))

    reset.color("white")
    reset.penup()
    reset.goto(-250, -150)
    reset.write("Press R to restart the game", font = ("Arial", 25, "bold"))
    
    #clear list
    global asteroid_list, vis
    asteroid_list.clear()
    vis.clear()
    spaceship.hideturtle()
    
    wn.onkeypress(restart, "r")
    wn.listen()
    
  else:
    timer -= 0.2
    if (abs(int(timer * 10) - int(timer) * 10) <= 1):
      draw_timer()
    trtl.ontimer(countdown, counter_interval)  # repeat every 0.2 second
  
def changeword(letter):
  global word, text
  word = word.replace(letter, " ", 1)
  text.hideturtle()
  text.clear()
  text.color("white")
  text.penup()
  text.goto(-275, 250)
  text.pendown()
  text.write(word, font = ("Arial", 25, "bold"))

def checkletter(letter):
  global word, score, words_spelled
  for ltr in word:
    if ltr == letter:
      #DEBUG: print("i: " + str(i) + "   word[i]: " + word[i])
      changeword(ltr)
      score += 1
      draw_score()
      #DEBUG: print("Before: Letter list: " + str(letter_list))
      #DEBUG: print("Pop letter at " + str(i) + " from the list: " + letter_list[i])

      #DEBUG: print("After: Letter list: " + str(letter_list))
      break

def remove_asteroid(index):
  global asteroid_list, timer, pTime
  #checks if index is out of range and if asteroid is already visited
  if vis[index] == True or index < 0 or index >= len(asteroid_list):
	  return
  #set timer to float and change 1 to maybe 0.1 or 0.25 
  if (pTime - timer <= 0.2):
    return
  #timer to prevent repl from randomly popping indexes twice
  pTime = timer
  #will only "delete" asteroid at index at first call

  checkletter(asteroid_list[index][3])
  #DEBUG: print("-", asteroid_list[index][3], index)
  
  asteroid_list[index][0].clear()
  asteroid_list[index][0].hideturtle()
  vis[index] = True

def left():
  spaceship.left(90)

def right():
  spaceship.right(90)

def forward():
  global words_spelled, asteroid_list, stop_timer
  spaceship.forward(5)

  #checks if word is all spaces, then clear screen and prints out new asteroids and word
  if word.isspace() == True:
    stop_timer = True
    words_spelled += 1
    wn.clearscreen()
    wn.bgpic("bgpic.gif")
    global n, asteroid_list, vis
    player()
    draw_word()
    #DEBUG: print("-----------------------------------------------------------") 
    asteroid_list.clear()
    vis.clear()
    
    coords()
    draw_score()

    stop_timer = False
    countdown()

    spaceship.showturtle()
    wn.onkeypress(left, 'Left')
    wn.onkeypress(right, 'Right')
    wn.onkeypress(forward, 'Up')

    wn.listen()
  #checks if spaceship is interacting with another asteroid, remove asteroid if hits
  else:
    for i in range(len(asteroid_list)):
      if (vis[i] == True):
        continue
      xdist = spaceship.xcor() - asteroid_list[i][1]
      ydist = spaceship.ycor() - asteroid_list[i][2]
      if math.sqrt(xdist * xdist + ydist * ydist) <= 22:
        remove_asteroid(i)
        break

#restarts the game on key press "R"
def restart():
  wn.clearscreen()
  global word, words_spelled, score, stop_timer, timer, pTime
  word = ""
  words_spelled = 0
  score = 0
  stop_timer = False
  timer = TIME
  pTime = TIME

  wn.bgpic("bgpic.gif")
  player()
  draw_word()
  coords()
  draw_score()
  countdown()
  spaceship.showturtle()
  wn.onkeypress(left, 'Left')
  wn.onkeypress(right, 'Right')
  wn.onkeypress(forward, 'Up')
  wn.onkeypress(restart, "r")
  
  wn.listen()
  
#Beginning of game
player()
draw_word()
coords()
draw_score()
countdown()

spaceship.showturtle()
wn.onkeypress(left, 'Left')
wn.onkeypress(right, 'Right')
wn.onkeypress(forward, 'Up')

wn.listen()
