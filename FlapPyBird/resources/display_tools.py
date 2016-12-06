from FlapPyBird.resources.config import *


def displayStat(SCREEN, stat, text=None):
      """displays score in center of screen"""
      try:
          scoreDigits = [int(x) for x in list(str(stat))]
          totalWidth = 0 # total width of all numbers to be printed

          for digit in scoreDigits:
              totalWidth += IMAGES['numbers'][digit].get_width()

          Xoffset = (SCREENWIDTH - totalWidth) / 2

      except:
          pass

      if text == "energy":
          for digit in scoreDigits:
              SCREEN.blit(IMAGES['numbers'][digit], (Xoffset - 70, 473))
              Xoffset += IMAGES['numbers'][digit].get_width()
          SCREEN.blit(IMAGES[text], (35, 440))

      elif text == "distance":
          for digit in scoreDigits:
              SCREEN.blit(IMAGES['numbers'][digit], (Xoffset + 100, 473))
              Xoffset += IMAGES['numbers'][digit].get_width()
          SCREEN.blit(IMAGES[text], (205, 440))

      elif text == "scores":
          """displays score in center of screen"""

          for digit in scoreDigits:
              SCREEN.blit(IMAGES['numbers'][digit], (130, 45))

          SCREEN.blit(IMAGES[text], (105, 15))

      elif text == "topology":
          text_font = pygame.font.Font(None, 30)
          topology = stat
          # Input
          text = text_font.render("I:" + str(topology[0]), 1, (0, 0, 0))
          SCREEN.blit(text, (140, 430))

          # Output
          text = text_font.render("O:" + str(topology[1]), 1, (0, 0, 0))
          SCREEN.blit(text, (140, 450))

          # -h
          text = text_font.render("H:" + str(topology[2]), 1, (0, 0, 0))
          SCREEN.blit(text, (140, 470))

          # -l
          text = text_font.render("L:" + str(topology[3]), 1, (0, 0, 0))
          SCREEN.blit(text, (140, 490))

          SCREEN.blit(IMAGES['topology'], (100, 395))

      elif text == "species":
          """displays score in center of screen"""
          for digit in scoreDigits:
              SCREEN.blit(IMAGES['numbers'][digit], (235, 30))

          SCREEN.blit(IMAGES[text], (205, 0))

      elif text == "generation":
          for digit in scoreDigits:
              SCREEN.blit(IMAGES['numbers'][digit], (Xoffset+130, 368))
              Xoffset += IMAGES['numbers'][digit].get_width()
          SCREEN.blit(IMAGES[text], (190, 395))
