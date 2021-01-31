#!/usr/bin/env python3

# UIDesigner
# Copyright 2020 Johnny Stene <jhonnystene@protonmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
# This is just a small app for designing the UI of arcticOS. It has a 240x320 (the same resolution as the screen) preview,
# and can place/delete text.

import pygame, json

print("UIDesigner version 1.1.0")
print("By Johnny \"jhonnystene\" Stene.")
print("jhonnystene@protonmail.com")
print("This program is free software; you can redistribute it and/or modify")
print("it under the terms of the GNU General Public License as published by")
print("the Free Software Foundation; either version 3 of the License, or")
print("(at your option) any later version.")


pygame.init()
pygame.display.set_caption("UIDesigner")
screen = pygame.display.set_mode((340, 360))

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_LIGHTRED = (255, 102, 102)
COLOR_GRAY = (204, 204, 204)
COLOR_LIGHTGRAY = (230, 230, 230)
COLOR_BLUE = (0, 0, 255)

#
# BUTTONS
#

class UIButton:
	def __init__(self, imagepath, x, y, width, height):
		self.image = pygame.transform.smoothscale(pygame.image.load(imagepath), (width - 4, height - 4))
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
	def draw(self, surface, borderColor=COLOR_BLACK):
		pygame.draw.rect(surface, COLOR_LIGHTGRAY, pygame.Rect(self.x, self.y, self.width, self.height))
		pygame.draw.rect(surface, borderColor, pygame.Rect(self.x, self.y, self.width, self.height), 2)
		surface.blit(self.image, (self.x + 2, self.y + 2))
		
	def isOn(self, x, y):
		if(x > self.x and x < self.x + self.width):
			if(y > self.y and y < self.y + self.height):
				return True
		return False
		
textButton = UIButton("Abc.png", 20, 20, 40, 40)
largeButton = UIButton("Large.png", 20, 60, 40, 26)
mediumButton = UIButton("Medium.png", 20, 86, 40, 26)
smallButton = UIButton("Small.png", 20, 112, 40, 26)

deleteButton = UIButton("Delete.png", 20, 300, 40, 40)
deleting = False

editButton = UIButton("Edit.png", 20, 250, 40, 40)
editing = False

#
# TEXT STUFF
#

FONT_SMALL = pygame.font.SysFont(None, 18)
FONT_REGULAR = pygame.font.SysFont(None, 24)
FONT_LARGE = pygame.font.SysFont(None, 72)

class TextWidget:
	def __init__(self, x, y, text, size):
		self.x = x
		self.y = y
		self.text = text
		self.size = size
		
		self.width = 0
		self.height = 0
		
	def draw(self, surface, outline=None):
		render = None
		
		if(self.size == 1):
			render = FONT_SMALL.render(self.text, True, COLOR_BLACK)
		elif(self.size == 2):
			render = FONT_REGULAR.render(self.text, True, COLOR_BLACK)
		else:
			render = FONT_LARGE.render(self.text, True, COLOR_BLACK)
		
		self.width = render.get_width()
		self.height = render.get_height()
		
		drawX = self.x - (self.width / 2)
		drawY = self.y - (self.height / 2)
		
		if(outline != None):
			pygame.draw.rect(surface, outline, pygame.Rect(drawX, drawY, self.width, self.height), 2)
		
		surface.blit(render, (drawX, drawY))
			
	def drawAt(self, surface, x, y, outline=None):
		render = None
		
		if(self.size == 1):
			render = FONT_SMALL.render(self.text, True, COLOR_BLACK)
		elif(self.size == 2):
			render = FONT_REGULAR.render(self.text, True, COLOR_BLACK)
		else:
			render = FONT_LARGE.render(self.text, True, COLOR_BLACK)
		
		self.width = render.get_width()
		self.height = render.get_height()
		
		drawX = x - (self.width / 2)
		drawY = y - (self.height / 2)
		
		if(outline != None):
			pygame.draw.rect(surface, outline, pygame.Rect(drawX, drawY, self.width, self.height), 2)
		
		surface.blit(render, (drawX, drawY))

	def isOn(self, x, y):
		if(x > self.x and x < self.x + self.width):
			if(y > self.y and y < self.y + self.height):
				return True
		return False
		
#
# MAIN LOOP
#

UIElements = []

HoldingElement = None
MousePosX = 0
MousePosY = 0
MouseDown = False

running = True
while running:
	screen.fill(COLOR_GRAY)
	
	UISurface = pygame.Surface((240, 320))
	pygame.draw.rect(UISurface, COLOR_WHITE, pygame.Rect(0, 0, 240, 320))
	
	for element in UIElements:
		if(deleting and element.isOn(MousePosX - 80, MousePosY - 20)):
			element.draw(UISurface, COLOR_RED)
			if(MouseDown):
				UIElements.remove(element)
		if(editing and element.isOn(MousePosX - 80, MousePosY - 20)):
			element.draw(UISurface, COLOR_BLUE);
			if(MouseDown):
				HoldingElement = element
				UIElements.remove(element)
		else:
			element.draw(UISurface)
			
	screen.blit(UISurface, (80, 20))
	
	if(MousePosX > 80 and MousePosY > 20 
		and MousePosX < 320 and MousePosY < 340
		and HoldingElement != None):
		HoldingElement.drawAt(screen, MousePosX, MousePosY)
	
	textButton.draw(screen)
	largeButton.draw(screen)
	mediumButton.draw(screen)
	smallButton.draw(screen)
	
	if(deleting):
		deleteButton.draw(screen, COLOR_RED)
	else:
		deleteButton.draw(screen)
		
	if(editing):
		editButton.draw(screen, COLOR_BLUE)
		deleting = False
	else:
		editButton.draw(screen)
	
	pygame.display.flip()
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			running = False

		if(event.type == pygame.KEYDOWN):
			if(HoldingElement):
				if(event.key == pygame.K_BACKSPACE):
					HoldingElement.text = HoldingElement.text[:-1]
				else:
					HoldingElement.text += event.unicode

		if(event.type == pygame.MOUSEBUTTONDOWN):
			MouseDown = True
			
			if(MousePosX > 80 and MousePosY > 20 
				and MousePosX < 320 and MousePosY < 340
				and HoldingElement != None):
				HoldingElement.x = MousePosX - 80
				HoldingElement.y = MousePosY - 20
				UIElements.append(HoldingElement)
				HoldingElement = None
				editing = False
			
			if(deleteButton.isOn(event.pos[0], event.pos[1])):
				if(deleting):
					deleting = False
				else:
					deleting = True
			elif(editButton.isOn(event.pos[0], event.pos[1])):
				if(editing):
					editing = False
				else:
					editing = True
					deleting = False
			elif(smallButton.isOn(event.pos[0], event.pos[1])):
				HoldingElement = TextWidget(0, 0, "TEXT!", 1)
				
			elif(mediumButton.isOn(event.pos[0], event.pos[1])):
				HoldingElement = TextWidget(0, 0, "TEXT!", 2)
				
			elif(largeButton.isOn(event.pos[0], event.pos[1])):
				HoldingElement = TextWidget(0, 0, "TEXT!", 3)

		if(event.type == pygame.MOUSEBUTTONUP):
			MouseDown = False

		if(event.type == pygame.MOUSEMOTION):
			MousePosX = event.pos[0]
			MousePosY = event.pos[1]
