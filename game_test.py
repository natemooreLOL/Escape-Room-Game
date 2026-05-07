import pygame
pygame.init()
from Classes_and_functions import mouse_between
from Classes_and_functions import RoomContainer
from Classes_and_functions import Room
from Classes_and_functions import Item
from Classes_and_functions import Inventory
from Classes_and_functions import ItemLock
from Classes_and_functions import Door
from Classes_and_functions import inventory
from Classes_and_functions import LockDigit
from Classes_and_functions import NumberLock

#Human Written Tests

def test_mouse_between():
    assert mouse_between((0,0),(10,10),(5,5))

def test_room_switching():
    room_container = RoomContainer()
    test_room1 = Room('testroom1','images/intro.png')
    test_room2 = Room('testroom2','images/intro.png')
    room_container.add_room(test_room1)
    room_container.add_room(test_room2)
    room_container.change_room(test_room1)
    assert test_room1.active

def test_adding_items():
    test_item = Item(None,'Item')
    test_inventory = Inventory()
    test_inventory.add_item(test_item)
    assert test_item in test_inventory.items

def test_item_lock():
    test_door = Door((0,0),'images/intro.png','images/intro.png',None)
    test_item = Item(None,'Item')
    test_item_lock = ItemLock(test_item,(0,0),(0,0),test_door)
    inventory.add_item(test_item)
    test_item_lock.click()
    assert test_door.open

def test_adding_digits():
    test_numlock = NumberLock('images/intro.png',(0,0),(0,0),None)
    test_numlock.add_digit(5, (0,0),(0,0),(0,0))
    assert len(test_numlock.digits) == 1

#pytest is weird with pygame so i just did this
#i think that the pygame this is using is obsolete or something
test_mouse_between()
test_item_lock()
test_adding_items()
test_room_switching()
test_adding_digits()

#AI written tests
#
#AI CODE BEGINS HERE
#

from unittest.mock import MagicMock, patch, PropertyMock
import sys
 
# ---------------------------------------------------------------------------
# Mock pygame entirely before importing the module under test
# ---------------------------------------------------------------------------
 
pygame_mock = MagicMock()
 
# Fake image that reports a fixed size so bottom_right calculations work
fake_surface = MagicMock()
fake_surface.get_size.return_value = (100, 50)
pygame_mock.image.load.return_value = fake_surface
pygame_mock.font.SysFont.return_value = MagicMock()
pygame_mock.display.set_mode.return_value = MagicMock()
 
# Provide cursor constants used in cursor_render methods
pygame_mock.cursors.diamond = "diamond"
pygame_mock.cursors.broken_x = "broken_x"
pygame_mock.cursors.tri_left = "tri_left"
pygame_mock.cursors.arrow = "arrow"
 
sys.modules["pygame"] = pygame_mock
 
# Now import the module (globals like inventory/room_list/bottom_text are created)
import Classes_and_functions as cf
 
 
# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------
 
def make_item(name="key"):
    item = cf.Item(image="fake.png", name=name)
    return item
 
 
def make_door(open=False):
    door = cf.Door(
        top_left=(10, 10),
        locked_image="images/key.png",
        unlocked_image="images/key.png",
        connected_room=MagicMock(),
        open=open,
        click_message="It's locked.",
    )
    return door
 
 
# ===========================================================================
# Test 1 – mouse_between
# ===========================================================================
 
class TestMouseBetween:
    def test_inside_returns_true(self):
        assert cf.mouse_between((0, 0), (100, 100), (50, 50)) is True
 
    def test_outside_returns_false(self):
        assert cf.mouse_between((0, 0), (100, 100), (150, 50)) is False
 
    def test_on_boundary_returns_true(self):
        assert cf.mouse_between((0, 0), (100, 100), (0, 0)) is True
        assert cf.mouse_between((0, 0), (100, 100), (100, 100)) is True
 
    def test_just_outside_boundary_returns_false(self):
        assert cf.mouse_between((0, 0), (100, 100), (101, 50)) is False
 
 
# ===========================================================================
# Test 2 – Inventory add / remove
# ===========================================================================
 
class TestInventory:
    def setup_method(self):
        self.inv = cf.Inventory()
 
    def test_add_item_increases_count(self):
        self.inv.add_item(make_item("key"))
        assert len(self.inv.items) == 1
 
    def test_remove_item_decreases_count(self):
        item = make_item("key")
        self.inv.add_item(item)
        self.inv.remove_item(item)
        assert len(self.inv.items) == 0
 
    def test_remove_nonexistent_item_does_not_raise(self):
        ghost = make_item("ghost")
        self.inv.remove_item(ghost)  # should not raise
 
    def test_item_present_check(self):
        item = make_item("key")
        self.inv.add_item(item)
        assert item in self.inv.items
 
 
# ===========================================================================
# Test 3 – Door open / click behaviour
# ===========================================================================
 
class TestDoor:
    def test_open_door_sets_flag(self):
        door = make_door(open=False)
        door.open_door()
        assert door.open is True
 
    def test_click_locked_door_updates_bottom_text(self):
        door = make_door(open=False)
        cf.bottom_text.update_text = MagicMock()
        door.click()
        cf.bottom_text.update_text.assert_called_once_with("It's locked.")
 
    def test_click_open_door_changes_room(self):
        door = make_door(open=True)
        cf.room_list.change_room = MagicMock()
        door.click()
        cf.room_list.change_room.assert_called_once_with(door.connected_room)
 
 
# ===========================================================================
# Test 4 – NumberLock check_code
# ===========================================================================
 
class TestNumberLock:
    def _make_lock(self):
        door = make_door()
        lock = cf.NumberLock(
            image="lock.png",
            top_left=(50, 30),
            bottom_right=(450, 470),
            connected_door=door,
        )
        # Two-digit code: answer is [3, 7]
        lock.add_digit(answer=3, location=(100, 200), top_left=(90, 190), bottom_right=(140, 230))
        lock.add_digit(answer=7, location=(200, 200), top_left=(190, 190), bottom_right=(240, 230))
        return lock, door
 
    def test_wrong_code_does_not_open_door(self):
        lock, door = self._make_lock()
        # digits start at 0,0 — wrong
        lock.check_code()
        assert door.open is False
 
    def test_correct_code_opens_door(self):
        lock, door = self._make_lock()
        lock.digits[0].cur_code = 3
        lock.digits[1].cur_code = 7
        lock.check_code()
        assert door.open is True
 
    def test_correct_code_hides_lock(self):
        lock, door = self._make_lock()
        lock.show_lock = True
        lock.digits[0].cur_code = 3
        lock.digits[1].cur_code = 7
        lock.check_code()
        assert lock.show_lock is False
 
 
# ===========================================================================
# Test 5 – ClickableItem pickup behaviour
# ===========================================================================
 
class TestClickableItem:
    def setup_method(self):
        # Reset the shared inventory for a clean slate
        cf.inventory.items.clear()
 
    def test_click_adds_item_to_inventory(self):
        item = make_item("torch")
        ci = cf.ClickableItem(item=item, top_left=(10, 10), image="images/key.png", visible=True)
        ci.click()
        assert item in cf.inventory.items
 
    def test_click_makes_object_invisible(self):
        item = make_item("torch")
        ci = cf.ClickableItem(item=item, top_left=(10, 10), image="images/key.png", visible=True)
        ci.click()
        assert ci.visible is False
 
    def test_click_when_invisible_does_not_add_to_inventory(self):
        item = make_item("torch")
        ci = cf.ClickableItem(item=item, top_left=(10, 10), image="images/key.png", visible=False)
        ci.click()
        assert item not in cf.inventory.items
 


#
#BACK TO HUMAN CODE TO TEST
#

testmousestuff = TestMouseBetween()
testmousestuff.test_inside_returns_true()
testmousestuff.test_just_outside_boundary_returns_false()
testmousestuff.test_on_boundary_returns_true()
testmousestuff.test_outside_returns_false()

testinventory = TestInventory()
testinventory.setup_method()
testinventory.test_remove_item_decreases_count()
testinventory.test_add_item_increases_count()
testinventory.test_item_present_check()
testinventory.test_remove_nonexistent_item_does_not_raise()

testdoor = TestDoor()
testdoor.test_click_locked_door_updates_bottom_text()
testdoor.test_click_open_door_changes_room()
testdoor.test_open_door_sets_flag()

testnumlock = TestNumberLock()
testnumlock.test_correct_code_hides_lock()
testnumlock.test_correct_code_opens_door()
testnumlock.test_wrong_code_does_not_open_door()

testclickableitem = TestClickableItem()
testclickableitem.setup_method
testclickableitem.test_click_adds_item_to_inventory()
testclickableitem.test_click_makes_object_invisible()
testclickableitem.test_click_when_invisible_does_not_add_to_inventory()