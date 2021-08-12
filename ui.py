import pygame, sys, random
from pygame import Vector2, Color
from pygame.font import Font

pygame.init()

class Button:
	def __init__(self, screen, pos, command=None, size=[100, 40] , padding=[0, 0], text='', bg=(244, 244, 244), 
					fg=(99, 99, 99), font=(None, 32), border=0, border_color=(70, 70, 70), radius=20, 
					shadow_color=(0, 0, 0, 100), offset=(-10, 10)):
		
		self.screen = screen
		self.size = size
		self.pos = Vector2(pos)
		self.text = text
		self.command = command
		self.bg = Color(bg)
		self.fg = Color(fg)
		self.font = Font(font[0], font[1])
		self.padding = padding
		self.border = border
		self.border_color = Color(border_color)
		self.radius = radius
		self.shadow_color = Color(shadow_color[:3])
		self.offset = offset
		self.alpha = 100 if len(shadow_color) == 3 else shadow_color[3]

		self.hovered = False
		self.clicked = False
		self.hover_color = Color(25, 25, 25)
		self.font_surface = self.font.render(self.text, True, self.fg)
		self.text_size = self.font.size(self.text)
		self._corectButtonSize()
		self._corectPadding()
		self.rect = pygame.Rect(self.pos, self.size)

	def _corectPadding(self):
		if isinstance(self.padding, int):
			self.padding = [self.padding, self.padding]
		self.size = [self.size[0] + self.padding[0] * 2, self.size[1] + self.padding[1] * 2]

	def _corectButtonSize(self):
			if self.size[0] < self.text_size[0]:
				self.size[0] += self.text_size[0] - self.size[0]
			if self.size[1] < self.text_size[1]:
				self.size[1] += self.text_size[1] - self.size[1]

	def _renderShadow(self):
		surf = pygame.Surface(self.size)
		surf.fill((123, 222, 213))
		surf.set_colorkey((123, 222, 213))
		surf.set_alpha(self.alpha)
		pygame.draw.rect(surf, self.shadow_color, (0, 0, self.rect.width, self.rect.height), 0, self.radius)
		self.screen.blit(surf, (self.pos + Vector2(self.offset)))

	def _backgroundColor(self):
		if self.hovered:
			return self.bg - self.hover_color
		else:
			return self.bg

	def _borderColor(self):
		if self.hovered:
			return self.border_color - self.hover_color
		else:
			return self.border_color

	def _textColor(self):
		if self.hovered:
			return self.fg - self.hover_color
		else:
			return self.fg

	def _renderBackground(self):
		color = self._backgroundColor()
		pygame.draw.rect(self.screen, color, self.rect, 0, self.radius)

	def _renderBorder(self):
		color = self._borderColor()
		if self.border:
			if self.border > min(self.rect.height, self.rect.width):
				self.border = int(min(self.rect.height, self.rect.width) / 2)
			pygame.draw.rect(self.screen, color, self.rect, self.border, self.radius)

	def _renderText(self):
		color = self._textColor()
		self.font_surface = self.font.render(self.text, True, color)
		self.screen.blit(self.font_surface, 
			(self.rect.center[0] - self.text_size[0] / 2, self.rect.center[1] - self.text_size[1] / 2))

	def is_pressed(self, func):
		if self.rect.collidepoint(pygame.mouse.get_pos()) and self.command != None:
			func()

	def update(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.hovered = True
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				self.is_pressed(self.command)
				self.clicked = True
		else:
			self.hovered = False
		if not pygame.mouse.get_pressed()[0]:
			self.clicked = False

	def render(self):
		self._renderShadow()
		self._renderBackground()
		self._renderBorder()
		self._renderText()


class Label:
	def __init__(self, surface, text, color=(0, 0, 0), font=(None, 96), antialias=True, shadow_color=(0, 0, 0, 100), 
				offset=(0, 0), bold=False, italic=False, underline=False):

		self.surface = surface 
		self.text = text
		self.color = Color(color) 
		self.font = Font(font[0], font[1])
		self.font.bold = bold
		self.font.italic = italic
		self.font.underline = underline
		self.antialias = antialias
		self.shadow_color = shadow_color[:3]
		self.offset = Vector2(offset)
		self.alpha = 100 if len(shadow_color) == 3 else shadow_color[3]

		self.text_size = self.font.size(self.text)
		self.label = self.font.render(self.text, self.antialias, self.color)
		self.shadow = self.font.render(self.text, self.antialias, self.shadow_color)

	def _renderShadow(self, pos):
		if self.offset:
			shadow_surface = pygame.Surface(self.text_size)
			shadow_surface.fill((123, 222, 213))
			shadow_surface.set_colorkey((123, 222, 213))
			shadow_surface.set_alpha(self.alpha)
			shadow_surface.blit(self.shadow, (0, 0))
			self.surface.blit(shadow_surface, pos + self.offset)

	def _renderText(self, pos):
			self.surface.blit(self.label, pos)



	def render(self, pos):
		self._renderShadow(pos)
		self._renderText(pos)
