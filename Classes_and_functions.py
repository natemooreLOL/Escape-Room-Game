import pygame
pygame.init()
screen = pygame.display.set_mode((500, 650))
font = pygame.font.SysFont("Arial", 48)
#Classes and functions will be made here and imported into the pygame file to reduce clutter

#function to check if something is within a box (Like a mouse click)
#takes in tuples for every input (coordinate pairs)
def mouse_between(top_left, bottom_right, mouse_pos):
    return (top_left[0] <= mouse_pos[0] <= bottom_right[0]) and (top_left[1] <= mouse_pos[1] <= bottom_right[1])

class RoomContainer:
    def __init__(self):
        self.rooms = []
    def add_room(self, room):
        self.rooms.append(room)
    def change_room(self, input_room):
        for room in self.rooms:
            if room.name == input_room.name:
                room.activate()
            else:
                room.deactivate()
    def render(self):
        for room in self.rooms:
            room.render()
    def click(self, mouse_pos):
        for room in self.rooms:
            if room.active:
                room.click(mouse_pos)
                return
    def cursor_render(self, mouse_pos):
        for room in self.rooms:
            if room.active:
                room.cursor_render(mouse_pos)
                return

class Room:
    def __init__(self, name, image):
        self.name = name
        self.objects = []
        self.doors = []
        self.locks = []
        self.non_renders = []
        self.image = pygame.image.load(image).convert_alpha()
        self.active = False
    def add_object(self, obj):
        self.objects.append(obj)
    def add_door(self, door):
        self.doors.append(door)
    def add_lock(self, lock):
        self.locks.append(lock)
    def add_nonrender(self, item):
        self.non_renders.append(item)
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
    def render(self):
        if self.active:
            screen.blit(self.image, (0,0))
            for obj in self.objects:
                obj.render()
            for door in self.doors:
                door.render()
            for lock in self.locks:
                lock.render()
    def click(self, mouse_pos):
        lock_active = False
        for lock in self.locks:
            if lock.show_lock:
                lock_active = True
        if lock_active:
            for lock in self.locks:
                if mouse_between(lock.top_left, lock.bottom_right, mouse_pos):
                    lock.click()
                    return
                if lock.show_lock:
                    lock.num_click(mouse_pos)
                    return
        else:
            for object in self.objects:
                if mouse_between(object.top_left, object.bottom_right, mouse_pos):
                    object.click()
                    return
            for obj in self.non_renders:
                if mouse_between(obj.top_left, obj.bottom_right, mouse_pos):
                    obj.click()
                    return
            for lock in self.locks:
                if mouse_between(lock.top_left, lock.bottom_right, mouse_pos):
                    lock.click()
                    return
            for door in self.doors:
                if mouse_between(door.top_left, door.bottom_right, mouse_pos):
                    door.click()
                    return
    def cursor_render(self, mouse_pos):
        lock_active = False
        for lock in self.locks:
            if lock.show_lock:
                lock_active = True
        if lock_active:
            for lock in self.locks:
                if mouse_between(lock.top_left, lock.bottom_right, mouse_pos):
                    pygame.mouse.set_cursor(pygame.cursors.diamond)
                    return
                if lock.show_lock:
                    lock.cursor_render(mouse_pos)
                    return
        else:
            for object in self.objects:
                if mouse_between(object.top_left, object.bottom_right, mouse_pos) and object.visible:
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
                    return
            for obj in self.non_renders:
                if mouse_between(obj.top_left, obj.bottom_right, mouse_pos):
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
                    return
            for lock in self.locks:
                if mouse_between(lock.top_left, lock.bottom_right, mouse_pos):
                    pygame.mouse.set_cursor(pygame.cursors.diamond)
                    return
            for door in self.doors:
                if mouse_between(door.top_left, door.bottom_right, mouse_pos):
                    pygame.mouse.set_cursor(pygame.cursors.tri_left)
                    return
        pygame.mouse.set_cursor(pygame.cursors.arrow)
            

class Door:
    def __init__(self, top_left, locked_image, unlocked_image, connected_room, open = False):
        self.open = open
        self.top_left = top_left

        
        #self.bottom_right = bottom_right
        self.locked_image = pygame.image.load(locked_image).convert_alpha()
        self.unlocked_image = pygame.image.load(unlocked_image).convert_alpha()
        self.bottom_right = tuple(x + y for x, y in zip(self.top_left, self.unlocked_image.get_size()))
        self.connected_room = connected_room
    def open_door(self):
        self.open = True
    def render(self):
        if self.open:
            screen.blit(self.unlocked_image, self.top_left)
        else:
            screen.blit(self.locked_image, self.top_left)
    def click(self):
        if self.open:
            room_list.change_room(self.connected_room)


class LockDigit:
#class that contains everything a numberlock needs for a individual digit to be displayed on it
    def __init__(self, location, top_left, bottom_right, max_num):
    #max_num is how high the number can go before looping back to zero, default 9
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.cur_code = 0
        self.location = location
        self.max_num = max_num
    def increment_code(self):
        self.cur_code = (self.cur_code + 1) % (self.max_num+1)

class NumberLock:
    def __init__(self, image, top_left, bottom_right, connected_door):
        self.answer = []
        self.digits = []
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.connected_door = connected_door
        self.image = image
        self.show_lock = False
    def add_digit(self, answer, location, top_left, bottom_right, max_num=9):
        self.answer.append(answer)
        self.digits.append(LockDigit(location, top_left, bottom_right, max_num))
    def render(self):
        if self.show_lock:
            screen.blit(pygame.image.load(self.image).convert_alpha(), (0,0))
            for digit in self.digits:
                screen.blit(font.render(str(digit.cur_code), True, (0,0,0)), digit.location)
    def check_code(self):
        code_right = True
        for index, answer in enumerate(self.answer):
            if answer != self.digits[index].cur_code:
                code_right = False
        if code_right:
            self.connected_door.open_door()
            self.show_lock = False
    def click(self):
        if self.connected_door.open:
            self.connected_door.click()
        else:
            if self.show_lock:
                self.show_lock = False
            else:
                self.show_lock = True
    def num_click(self, mouse_pos):
        for digit in self.digits:
            if mouse_between(digit.top_left, digit.bottom_right, mouse_pos):
                digit.increment_code()
                self.check_code()
                return
    def cursor_render(self, mouse_pos):
        if mouse_between(self.top_left,self.bottom_right,mouse_pos):
            pygame.mouse.set_cursor(pygame.cursors.diamond)
            return
        else:
            for digit in self.digits:
                if mouse_between(digit.top_left, digit.bottom_right, mouse_pos):
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
                    return
                else:
                    pygame.mouse.set_cursor(pygame.cursors.arrow)
                
        

class ItemLock:
    def __init__(self, item, top_left, bottom_right, door):
        self.item = item
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.door = door
    def click(self):
        if self.item in inventory.items:
            self.door.open_door()
            inventory.remove_item(self.item)

class Item:
    def __init__(self, image, name):
        self.image = image
        self.name = name

class Inventory:
    def __init__(self):
        self.items = []
    def add_item(self, item):
        self.items.append(item)
    def remove_item(self, remitem):
        for item in self.items:
            if item.name == remitem.name:
                self.items.remove(item)
    def render_items(self):
        for index, item in enumerate(self.items):
            screen.blit(pygame.image.load(item.image).convert_alpha(), (25+index*75,525))

class ClickableItem:
    def __init__(self, item, top_left,image, visible=True):
        self.item = item
        self.image = pygame.image.load(image).convert_alpha()
        self.visible = visible
        self.top_left = top_left
        self.bottom_right = tuple(x + y for x, y in zip(self.top_left, self.image.get_size()))
    def render(self):
        if self.visible:
            screen.blit(self.image, self.top_left)
    def click(self):
        if self.visible == True:
            self.visible = False
            inventory.add_item(self.item)


class ClickableObject:
    def __init__(self, name, description, top_left, bottom_right):
        self.name = name
        self.description = description
        self.top_left = top_left
        self.bottom_right = bottom_right

    def click(self):
        bottom_text.update_text(f'You clicked on {self.name}. {self.description}')

class BottomText():
    def __init__(self):
        self.timer = 0
        self.text = ''
        self.font_size = 48
        self.text_font = pygame.font.SysFont("Arial", self.font_size)
    def render(self):
        
        if self.timer < 250:
            self.timer += 1
            if self.timer < 30:
                screen.blit(self.text_font.render(str(self.text),True,(self.timer*8.5,self.timer*8.5,self.timer*8.5)), (0,600))
            elif self.timer < 220:
                screen.blit(self.text_font.render(str(self.text),True,(255,255,255)), (0,600))
            else:
                screen.blit(self.text_font.render(str(self.text),True,((250-self.timer)*8.5,(250-self.timer)*8.5,(250-self.timer)*8.5)), (0,600))
    def update_text(self,text):
        self.text = text
        if len(text) < 20:
            self.font_size = 48
        elif len(text) < 30:
            self.font_size = 36
        elif len(text) < 40:
            self.font_size = 30
        else:
            self.font_size = 26
        self.text_font = pygame.font.SysFont("Arial", self.font_size)
        self.timer = 0

inventory = Inventory()
room_list = RoomContainer()
bottom_text = BottomText()