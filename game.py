import pygame
pygame.init()

import Classes_and_functions
from Classes_and_functions import room_list
from Classes_and_functions import inventory
from Classes_and_functions import bottom_text

pygame.mixer.init()
pygame.mixer.music.load('labyrinth_escape.ogg')
pygame.mixer.music.set_volume(0.5) # Ears will no longer bleed when the music starts
pygame.mixer.music.play(-1)  # Loops the music indefinitely



screen = pygame.display.set_mode((500, 650))
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont("Arial", 48)

##Add Rooms##
room1A = Classes_and_functions.Room('room1A','images/Room_1-A/room_1-A.png')
room1B = Classes_and_functions.Room('room1B','images/Room_1-b/background.png')
room2 = Classes_and_functions.Room('room2','images/Room 2/room_2.PNG')
room3 = Classes_and_functions.Room('room3','images/room3/room_3.png')
victory_room = Classes_and_functions.Room('victory','images/victory.png')

##Add Items##
basic_key = Classes_and_functions.Item('images/key.png','key')
screwdriver = Classes_and_functions.Item('images/screwdriver.png', 'screwdriver')

##Components of room1A##
arrow_right_1A = Classes_and_functions.Door((464,15),'images/Room_1-A/arrowright.png','images/Room_1-A/arrowright.png',room1B,True)
door1_1A = Classes_and_functions.Door((63,126),'images/Room_1-A/door1closed.png','images/Room_1-A/door1open.png',room2)
door2_1A = Classes_and_functions.Door((466,168),'images/Room_1-A/door2closed.png','images/Room_1-A/door2open.png',victory_room)
key_1A = Classes_and_functions.ClickableItem(basic_key,(220,303),'images/Room_1-A/key.png')
lock_door1_1A = Classes_and_functions.ItemLock(basic_key,(144,276),(165,294),door1_1A)
##Add Components##
room1A.add_door(arrow_right_1A)
room1A.add_door(door1_1A)
room1A.add_door(door2_1A)
room1A.add_object(key_1A)
room1A.add_nonrender(lock_door1_1A)

##Components of room1B##
arrow_left_1B = Classes_and_functions.Door((0,18),'images/Room_1-B/arrow_away.PNG','images/Room_1-B/arrow_away.PNG',room1A,True)
door_1B = Classes_and_functions.Door((0,161),'images/Room_1-B/door_closed.PNG','images/Room_1-B/door_open.PNG',victory_room)
screwdriver_1B = Classes_and_functions.ClickableItem(screwdriver,(328,438),'images/Room_1-B/screwdriver.PNG')
lock_1B = Classes_and_functions.NumberLock('images/Room_1-B/Escape Room lock.png',(76,285),(104,336),door_1B)
toolbox_1B = Classes_and_functions.ClickableObject('a toolbox', 'Nothing looks useful.', (350, 375), (440, 460))
##Add digits to lock##
lock_1B.add_digit(5,(120,305),(105,265),(170,400))
lock_1B.add_digit(9,(205,305),(180,265),(250,400))
lock_1B.add_digit(6,(285,305),(260,265),(330,400))
lock_1B.add_digit(3,(365,305),(335,265),(410,400))
##Add Components##
room1B.add_door(arrow_left_1B)
room1B.add_door(door_1B)
room1B.add_object(screwdriver_1B)
room1B.add_lock(lock_1B)
room1B.add_nonrender(toolbox_1B)

##Components of room2##
door1_2 = Classes_and_functions.Door((0,119),'images/Room 2/door1closed.PNG','images/Room 2/door1open.PNG',room3)
door2_2 = Classes_and_functions.Door((419,130),'images/Room 2/door2open.PNG','images/Room 2/door2open.PNG',room1A,True)
lock_2 = Classes_and_functions.NumberLock('images/Room 2/lock_enlarged.png',(85,290),(117,346),door1_2)
greendice = Classes_and_functions.ClickableObject('a green die', 'It reads four',(174,311),(193,337))
bluedice = Classes_and_functions.ClickableObject('a blue die', 'It reads six',(260,325),(279,350))
purpledice = Classes_and_functions.ClickableObject('a purple die', 'It reads one',(339,264),(358,289))
orangedice = Classes_and_functions.ClickableObject('a orange die', 'It reads three',(269,421),(288,446))
##Add digits to lock##
lock_2.add_digit(6,(125,310),(105,265),(170,400),6)
lock_2.add_digit(3,(205,310),(180,265),(250,400),6)
lock_2.add_digit(1,(285,310),(260,265),(330,400),6)
lock_2.add_digit(4,(360,310),(335,265),(410,400),6)
##Add Components##
room2.add_door(door1_2)
room2.add_door(door2_2)
room2.add_lock(lock_2)
room2.add_nonrender(greendice)
room2.add_nonrender(bluedice)
room2.add_nonrender(purpledice)
room2.add_nonrender(orangedice)

#Components of room3##
arrow_down_3 = Classes_and_functions.Door((13,455),'images/room3/arrow_down.png','images/room3/arrow_down.png',room2,True)
vent_3 = Classes_and_functions.Door((110,244),'images/room3/vent_cover.PNG','images/room3/empty_vent.png',room3, click_message='You can\'t open the vent right now')
shelf_3 = Classes_and_functions.ClickableObject('a shelf','It\'s empty',(260,0),(500,440))
##code_note_3 = Classes_and_functions.ClickableObject('a note','it reads \"5 9 6 3\"',(130,317),(194,355))
vent_lock_check_3 = Classes_and_functions.ItemLock(screwdriver,(110,244),(238,391),vent_3)
##Add Components##
room3.add_door(arrow_down_3)
room3.add_door(vent_3)
room3.add_nonrender(shelf_3)
room3.add_nonrender(vent_lock_check_3)


##Add rooms to room list##
room_list.add_room(victory_room)
room_list.add_room(room1A)
room_list.add_room(room1B)
room_list.add_room(room2)
room_list.add_room(room3)
##Set starting room##
room_list.change_room(room1A)


while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #detects if mouse is hovering over lock when clicking, then shows lock, if it clicks the lock while displaying it, it hides the lock
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                room_list.click(event.pos)

    mouse_position = pygame.mouse.get_pos()
    
    screen.fill("black") #wipes previous screen

    #render game here
    screen.blit(pygame.image.load("images/inventory.png").convert(), (0,500))
    inventory.render_items()
    bottom_text.render()

    room_list.render()

    room_list.cursor_render(mouse_position)






    #----Displays Mouse Position----
    ##MOUSE_POS_DEBUG = font.render(str(mouse_position), True, (0, 0, 0))
    ##screen.blit(MOUSE_POS_DEBUG, (0,0))
    #---Comment Out When Unneeded---


    pygame.display.flip() #shows screen

    clock.tick(60) #sets FPS to 60

pygame.quit()