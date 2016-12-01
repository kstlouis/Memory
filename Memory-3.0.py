# Memory version 3.0
# This version should include all game features


import pygame, sys, time, random,uaio
from pygame.locals import *


def main():
   pygame.init()
   surface=create_window()
   game=Game(surface)
   game.play()
   pygame.display.quit()
   
def create_window():
   surface=pygame.display.set_mode((500,400),0,0)
   pygame.display.set_caption('Memory')
   return surface

class Tile:
   surface=None
   board_size=4
   fg_color=pygame.Color('black')
   
   def set_surface(cls,surface):
      cls.surface=surface
       
   def __init__(self,x,y,width,height,image):
      self.x=x
      self.y=y
      self.width=width
      self.height=height
      self.clicked=False
      self.image=image
      self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
      
   def draw(self):
      if self.clicked:
         pygame.draw.rect(Tile.surface,Tile.fg_color,self.rect,Tile.board_size)
         Tile.surface.blit(self.image,self.rect)
      else:
         pygame.draw.rect(Tile.surface,Tile.fg_color,self.rect,Tile.board_size)
         image=pygame.image.load('image0.bmp')
         Tile.surface.blit(image,self.rect)      
         
class Game:
   board_size=4
   
   def __init__(self,surface):
      self.surface=surface
      self.create_board()
      self.close_clicked=False
      self.continue_game=True
      Tile.set_surface(Tile,self.surface)
      self.count=0
      self.image_to_compare=None
      
   def create_board(self):
      self.board=[]
      self.load_image()
      count=0
      for row_index in range(0,Game.board_size):
         row=[]
         for column_index in range(0,Game.board_size):
               window_width=self.surface.get_width()
               window_height=self.surface.get_height()
               width=window_width//5
               height=window_height//4
               x=width*row_index
               y=height*column_index
               image=self.images[count]
               tile=Tile(x,y,width,height,image)
               count=count+1
               row.append(tile)
         self.board.append(row)
          
   def load_image(self):
      self.images=[]
      for index in range(1,9):
         image='image'+str(index)+'.bmp'
         image=pygame.image.load(image)
         self.images.append(image)
      self.images=self.images+self.images
      random.shuffle(self.images)

   def play(self):
      self.draw()
      while not self.close_clicked:
         self.handle_event()
         if self.continue_game:
               self.draw_score()
               self.decide_continue()
         self.draw()
         
   def draw(self):
      for row in self.board:
         for tile in row:
               tile.draw()
      pygame.display.update()
      
   def handle_event(self):
      event=pygame.event.poll()
      if event.type==QUIT:
         self.close_clicked=True
      if event.type== MOUSEBUTTONUP and self.continue_game:
         position=event.pos
         for row in self.board:
               for tile in row:    
                  if tile.rect.collidepoint(position):
                     if tile.clicked==False:
                           tile.clicked=True
                           self.compare_image(tile)


   def compare_image(self,tile):
      if self.image_to_compare==None:
         self.image_to_compare=tile
      elif tile.image==self.image_to_compare.image:
         self.count=self.count+2
         self.image_to_compare=None
      else:
         pygame.display.update()
         self.draw()
         time.sleep(0.5)
         self.image_to_compare.clicked=False
         tile.clicked=False
         self.image_to_compare=None
   
   def decide_continue(self):
      if self.count==16:
         self.continue_game=False
         
   def draw_score(self):
      score=pygame.time.get_ticks()//1000
      score_width=uaio.get_width(str(score),70)
      window_width=self.surface.get_width()
      x=window_width-score_width
      uaio.draw_string(str(score),self.surface,(x,0),70)
      

main()