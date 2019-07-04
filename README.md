## Heritage of Alkya
This project is a FF-like RPG game created with python (pygame). As other games of the same type this game gives you a quest. In a medieval-fantastic world in danger because of darkness forces your quest is to exterminate these forces to bring back peace and freedom in the world. -

## Build status

![Build status](https://img.shields.io/badge/build-not%20created-red.svg?style=popout-square)

## Code style
[![Code style](https://img.shields.io/badge/code%20style-python%20pep8-brightgreen.svg?style=popout-square)](https://www.python.org/dev/peps/pep-0008/)
 
## Screenshots
![screen mapgenerator](https://github.com/Lightpearl26/Heritage-of-Alkya/blob/master/screen_mapgenerator.png)

## Tech/framework used
using SDL with pygame module. -

## Code Example
```python
class TitleScreen(BaseScene):
	"""
	"""
	def __init__(self):
		BaseScene.__init__(self)
		self.options = widget.ChoiceBox(["New Game", "Continue", "Options", "Quit Game"], (cts.WINDOW_SIZE_X//4, 2*cts.WINDOW_SIZE_Y//6, cts.WINDOW_SIZE_X//2, cts.WINDOW_SIZE_Y//2))
	
	def action(self):
		self.running = False
		option = self.options.get()
		if option == "Quit Game":
			pygame.quit()
			exit()

		elif option == "New Game":
			pass

		elif option == "Continue":
			pass

		else:
			pass

	def up(self):
		self.options.up()
	
	def down(self):
		self.options.down()

	def render(self):
		BaseScene.render(self)
		font = pygame.font.SysFont("Arial", 32, bold=True, italic=True)
		title = font.render(cts.GAME_TITLE, True, (255, 255, 255))
		title_rect = title.get_rect(center=(cts.WINDOW_SIZE_X//2, cts.WINDOW_SIZE_Y//6))
		self.surface.blit(title, title_rect)
		self.options.blit(self.surface)
```

## Installation
No installation created now but you can help by contributing on the project. -

## Contribute

[How to contribute](https://github.com/Lightpearl26/Heritage-of-Alkya/blob/master/CONTRIBUTING.md). -

## License
[![License type](https://img.shields.io/badge/license-GNU%20GPL-brightgreen.svg?style=popout-square)](https://github.com/Lightpearl26/Heritage-of-Alkya/blob/master/LICENSE)

GNU GPL © [Lightpearl26](https://github.com/Lightpearl26)
