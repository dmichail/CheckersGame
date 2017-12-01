import pygame
import sys, time, random
from pygame.locals import *
from collections import deque
from Queue import Queue


#COLORS
#R G B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
HIGHLIGHT = (160, 190, 255)
GREY = (190, 190, 190)
DARK_GREY = (130,130,130)


#DIRECTIONS
NORTHWEST = "northwest" # -1, -1 
NORTHEAST = "northeast" # 1, -1
SOUTHWEST = "southwest" # -1, -1 
SOUTHEAST = "southeast" # 1, 1


#Create stack class 
class MStack:
	def __init__(self):
		self.items = []
		
	#check if empty
	def isEmpty(self):
		return self.items == []
		
	#insert new item in stack
	def push(self, item):
		self.items.append(item)
		
	#remove last item
	def pop(self):
		return self.items.pop()
		
	#Get size of stack
	def size(self):
		return len(self.items)
	
	#checks last item without removing it
	def peek(self): 
		return self.items[-1]
		
	def stack_reverse(self):
		return self.items.reverse()

#Create Queue class
#Not used
class MQueue:
	def __init__(self): #Init the queue 
		self.a = Queue()

	def putIn(self, item): #Add new item in queue
		self.a.put(item)
		
	def getNoRemove(self, listB): #Get items without removing
		while not self.a.empty():
			listB.append(self.a.get())
		for item in listB:
			self.a.put(item)
							
	#Gets all items based on the way they entered the queue
	def getOut_All(self):
		while not self.a.empty():
			self.a.get()
			
	#Get size of queue
	def size(self):
		return self.a.qsize()



#Piece class
#Each Piece has a color and king attribute to check if its promoted to king
class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king
	
#Square class	
#Each square has a color and an occupant. If empty , occupant is None
class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant #Square object

#Board class
#These are all the methods that have to interact with the board
class Board:
	def __init__(self):
		self.board = self.new_board()		
		
	def new_board(self):
		#Creates new board
		
		board = [[None ] * 8 for i in range(8)]
		
		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					board[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					board[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					board[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0):
					board[y][x] = Square(BLACK)
					
		#Place pieces
		for x in range(8):
			for y in range(3):
				if board[x][y].color == BLACK:
					board[x][y].occupant = Piece(RED)
			for y in range(5, 8):
				if board[x][y].color == BLACK:
					board[x][y].occupant = Piece(GREEN)
		
		return board
		
	#Check for directions from each square
	def directions(self, dir, (x, y)):
		if dir == NORTHEAST:
			return (x + 1, y - 1)
		elif dir == NORTHWEST:
			return (x - 1, y - 1)
		elif dir == SOUTHEAST:
			return (x + 1, y + 1)
		elif dir == SOUTHWEST:
			return (x - 1, y + 1)
		else:
			return 0
	
	#Get list of locations around a supplied location(x,y)
	def adjacent(self, (x, y)):
		return [self.directions(NORTHEAST, (x, y)), self.directions(NORTHWEST, (x,y)), self.directions(SOUTHEAST, (x,y)), self.directions(SOUTHWEST, (x,y))]
	
	#Faster location search
	def get_location(self, (x,y)):
		return self.board[x][y]
		
	#Check if move is out of bounds
	def on_board(self, (x,y)):
		if x < 0 or x > 7 or y < 0 or y > 7:
			return False
		else:
			return True
			
	#Kinging Piece
	def king(self, (x,y)):
		if self.get_location((x,y)).occupant != None:
			if (self.get_location((x,y)).occupant.color == GREEN and y == 0) or (self.get_location((x,y)).occupant.color == RED and y == 7):
				self.get_location((x,y)).occupant.king = True 
		
	#Generate moves
	def gen_moves(self, (x,y)):
		if self.board[x][y].occupant != None:
			if self.board[x][y].occupant.king == False and self.board[x][y].occupant.color == GREEN:
				gen_moves = [self.directions(NORTHWEST, (x,y)), self.directions(NORTHEAST, (x,y))]
			elif self.board[x][y].occupant.king == False and self.board[x][y].occupant.color == RED:
				gen_moves = [self.directions(SOUTHWEST, (x,y)), self.directions(SOUTHEAST, (x,y))]

			else:
				gen_moves = [self.directions(NORTHWEST, (x,y)), self.directions(NORTHEAST, (x,y)), self.directions(SOUTHWEST, (x,y)), self.directions(SOUTHEAST, (x,y))]

		else:
			gen_moves = []

		return gen_moves

	#Valid moves
	#Return list of valid moves from a give location(x,y)
	#If empty returns none
	def valid_moves(self, (x,y), jump = False):
		gen_moves = self.gen_moves((x,y))
		valid_moves = []
		
		if jump == False:
			for move in gen_moves:
				if jump == False:
					if self.on_board(move):
						if self.get_location(move).occupant == None:
							valid_moves.append(move)
						#Check if space is occupied
						elif self.get_location(move).occupant.color != self.get_location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.get_location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None:
							valid_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
		else:
			for move in gen_moves:
				if self.on_board(move) and self.get_location(move).occupant != None:
					if self.get_location(move).occupant.color != self.get_location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.get_location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None:
						valid_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
		
		return valid_moves
		
	#Remove piece from board
	def remove_piece(self, (x,y)):
		self.board[x][y].occupant = None
		
	#Move piece
	def move_piece(self, (startX, startY), (endX, endY)):
		self.board[endX][endY].occupant = self.board[startX][startY].occupant
		self.remove_piece((startX, startY))
		self.king((endX, endY))
				
	#check if reached end square
	def end_square(self, coords):
		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False
			
	#Get all pieces
	def get_Pieces(self):
		red_pieces = []
		green_pieces = []
		for x in range(8):
			for y in range(8):
				if self.board[x][y].color == BLACK and self.board[x][y].occupant != None:				
					if self.board[x][y].occupant.color == RED:
						red_pieces.append((x,y))
					elif self.board[x][y].occupant.color == GREEN:
						green_pieces.append((x,y))
		return green_pieces,red_pieces

			
#Graphics class 
#This help to design the game window and everything that is placed on it.
class Graphics:
	def __init__(self):
		self.caption = "Checkers"
		
		self.fps = 60
		self.clock = pygame.time.Clock()
		
		self.width = 900
		self.height = 600
		self.screen = pygame.display.set_mode((self.width,self.height), 0, 32)
		self.background = pygame.image.load('board.png').convert()
		
		self.square_size = 600 / 8
		self.piece_size = self.square_size / 2
		
		self.message = False
		
		#Variables used for display moves on screen
		self.number = 0
		self.y_axis = 0
		self.x_axis = 0
		self.history_moves = []
		
	#Call pygame library
	def setup_window(self):
		pygame.init()
		pygame.display.set_caption(self.caption)
		
	#Method thats update everything on screen to the user.
	#Everything exists in the background once created, this method helps show these to the user.
	def update_display(self, board, valid_moves, selected_piece):
		self.screen.blit(self.background,(0,0))
		
		self.highlight_squares(valid_moves, selected_piece)
		self.draw_board_pieces(board)
		#Draw History Board 
		self.draw_history_board()
		
		#Check for final message
		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)
	
	#Extra features(ex history moves, undo/redo)
	def draw_history_board(self):
		pygame.draw.rect(self.screen, WHITE, [601,0,299,self.height/2], 2)
				
	def show_turn(self, turn):		
		self.screen.fill(BLACK, (610,400,200,150))
		if turn == GREEN:
			text = "GREEN"
		else:
			text = "RED"
			
		whos = "Who's Turn: " 
		final = whos + text
		smallText = pygame.font.Font('freesansbold.ttf', 18)
		textSurf, textRect = self.text_objects(final, smallText, WHITE)
		textRect.center = ( (700), (430) )
		self.screen.blit(textSurf, textRect)
		


		
	def show_moves_board(self, msg):
		#self.history_moves.append(msg)
		self.number += 1
		self.y_axis += 10
		#Check if displayed moves are reaching max height
		if self.y_axis > 290:
			self.x_axis = self.x_axis + 80 
			self.y_axis = 10	
		#Start move
		start = msg[0]
		
		#Target move
		target = msg[1]
		#Final message that will display in the screen
		final_line = str(self.number) + ". " + str(start) + "-->" + str(target)
				
		smallText = pygame.font.Font('freesansbold.ttf', 10)
		textSurf, textRect = self.text_objects(final_line, smallText, WHITE)
		textRect.center = ( (650+ self.x_axis), (self.y_axis) )
		self.screen.blit(textSurf, textRect)
					
	#Button
	def button(self,msg,x,y,w,h,ic,ac,action=None):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if x+w > mouse[0] > x and y+h > mouse[1] > y:
			pygame.draw.rect(self.screen, ac, [x,y,w,h])
			
			if click[0] == 1 and action != None:
				action()
		else:
			pygame.draw.rect(self.screen, ic, [x,y,w,h])
		
		smallText = pygame.font.Font('freesansbold.ttf', 20)
		textSurf, textRect = self.text_objects(msg, smallText, WHITE)
		textRect.center = ( (x+(w/2)), (y+(h/2)) )
		self.screen.blit(textSurf, textRect)

		
		
	#Board functions
	def draw_board_squares(self, board):
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size))
	#Draw board pieces and check if piece is king. Then add a smaller circle on top of piece
	def draw_board_pieces(self, board):
		for x in range(8):
			for y in range(8):
				if board.board[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.board[x][y].occupant.color, self.pixel_coords((x,y)), self.piece_size) 

					if board.get_location((x,y)).occupant.king == True:
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x,y)), int (self.piece_size / 1.7), self.piece_size / 4)

	#pixel coords
	def pixel_coords(self, board_coords):
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)
	#Get the boord coords 
	def board_coords(self, (pixel_x, pixel_y)):
		return (pixel_x / self.square_size, pixel_y / self.square_size)	
	#Highlight squares
	def highlight_squares(self, squares, origin):
		for square in squares:
			pygame.draw.rect(self.screen, HIGHLIGHT, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	
		
		if origin != None:
			pygame.draw.rect(self.screen, HIGHLIGHT, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

			
	#Text display
	def text_objects(self, text, font, color):
		textSurface = font.render(text, True, color)
		return textSurface, textSurface.get_rect()
			
				
	#Draws message to the center screen. 	
	def draw_message_center(self, message):
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGHLIGHT, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.width / 2, self.height / 2)

class Game:
	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()
		self.turn = GREEN
		self.selected_piece = None
		self.jump = False
		self.selected_valid_moves = []
		self.undo_stack = MStack()
		self.redo_stack = MStack()
		self.queue = MQueue()
		
	def setup(self):
		self.graphics.setup_window()
			
	def event_loop(self):
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos())
		#print(self.mouse_pos)
		actual_mouse_pos = pygame.mouse.get_pos()
		#print (actual_mouse_pos)
		if self.selected_piece != None:
			self.selected_valid_moves = self.board.valid_moves(self.selected_piece, self.jump)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
	
			if event.type == MOUSEBUTTONDOWN:
				#Check if mouse click is on the board or not.
				if actual_mouse_pos[0] >= 600 or actual_mouse_pos[1] >= 600:
					print (actual_mouse_pos)
					pass
				else:
					
					if self.jump == False:
						if self.board.get_location(self.mouse_pos).occupant != None and self.board.get_location(self.mouse_pos).occupant.color == self.turn:
							self.selected_piece = self.mouse_pos
						elif self.selected_piece != None and self.mouse_pos in self.board.valid_moves(self.selected_piece):
							self.board.move_piece(self.selected_piece, self.mouse_pos)
							#add move in undo stack
							self.undo_stack.push((self.selected_piece, self.mouse_pos))
							#add move to queue
							self.queue.putIn((self.selected_piece, self.mouse_pos))
							#Show move in screen
							self.graphics.show_moves_board((self.selected_piece, self.mouse_pos))

							if self.mouse_pos not in self.board.adjacent(self.selected_piece):
								self.board.remove_piece((self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2))
							
								self.jump = True
								self.selected_piece = self.mouse_pos
				
							else:
								self.end_turn()

					if self.jump == True:					
						if self.selected_piece != None and self.mouse_pos in self.board.valid_moves(self.selected_piece, self.jump):
							self.board.move_piece(self.selected_piece, self.mouse_pos)
							self.board.remove_piece((self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2))

						if self.board.valid_moves(self.mouse_pos, self.jump) == []:
								self.end_turn()

						else:
							self.selected_piece = self.mouse_pos
			#Design buttons
			self.graphics.button("Undo", 610, 600/2+50,80,50, DARK_GREY, GREY, self.undo)
			self.graphics.button("Redo", 710, 600/2+50,80,50, DARK_GREY, GREY, self.redo)
			self.graphics.button("AI Move", 810, 600/2+50,80,50, DARK_GREY, GREY, self.AI_move)
			#Show whos turn
			self.graphics.show_turn(self.turn)

	#Update display
	def update(self):
		self.graphics.update_display(self.board, self.selected_valid_moves, self.selected_piece)
	#Main loop
	def main(self):
		self.setup()
		
		while True:
			self.event_loop()
			self.update()
			
	#End player's turn	
	def end_turn(self):
		if self.turn == GREEN:
			self.turn = RED
		else:
			self.turn = GREEN
		
		self.selected_piece = None
		self.selected_valid_moves = []
		self.jump = False
		
		if self.check_endgame():
			if self.turn == GREEN:
				self.graphics.draw_message_center("RED WINS")
			else:	
				self.graphics.draw_message_center("GREEN WINS")
			time.sleep(3)
			pygame.quit()
			sys.exit
			
	#Check if game is over
	def check_endgame(self):
		for x in range(8):
			for y in range(8):
				if self.board.get_location((x,y)).color == BLACK and self.board.get_location((x,y)).occupant != None and self.board.get_location((x,y)).occupant.color == self.turn:
					if self.board.valid_moves((x,y)) != []:
						return False
		return True
		
	#Undo move
	def undo(self):
		if self.undo_stack.size() > 0:
			last_move = self.undo_stack.pop()
			self.redo_stack.push(last_move)
			#Reverse start - end positions
			(startX,startY) = last_move[1]
			(endX,endY) = last_move[0]
			self.board.move_piece((startX,startY),(endX,endY))
		else:
			print("No moves made yet!")

		if self.turn == GREEN:
			self.turn = GREEN
		else:
			self.turn = RED
			 
			
			
	#Redo
	def redo(self):
		move = ()
		try:
			move = self.redo_stack.pop()
			self.undo_stack.push(move)
			self.board.move_piece((move[0]),(move[1]))
		except RuntimeError:
			print ("Cant deque empty stack")
		except:
			print ("Error")
		if self.turn == GREEN:
			self.turn = GREEN
		else:
			self.turn = RED
	
	#AI
	def AI_move(self):
		green,red = self.board.get_Pieces()
		if self.turn == GREEN:
			green_valid_moves = []
			while green_valid_moves == []:
				green_selected = random.choice(green)
				green_valid_moves = self.board.valid_moves(green_selected, self.jump)			
			end_point = random.choice(green_valid_moves)
			self.board.move_piece((green_selected),(end_point))
			
			#Check for jump
			if end_point not in self.board.adjacent(green_selected):
				self.board.remove_piece((green_selected[0] + (end_point[0] - green_selected[0]) / 2, green_selected[1] + (end_point[1] - green_selected[1]) / 2))		
				self.jump = True
				self.green_selected = end_point
			
			if self.jump == True:
				self.board.remove_piece((green_selected[0] + (end_point[0] - green_selected[0]) / 2, green_selected[1] + (end_point[1] - green_selected[1]) / 2))
			#Add move to undo stack
			self.undo_stack.push((green_selected, end_point))
			#Show move on screen
			self.graphics.show_moves_board((green_selected, end_point))
			
		elif self.turn == RED:
			red_valid_moves = []
			while red_valid_moves == []:
				red_selected = random.choice(red)
				red_valid_moves = self.board.valid_moves(red_selected, self.jump)
			end_point = random.choice(red_valid_moves)
			self.board.move_piece((red_selected),(end_point))
			
			#Check for jump
			if end_point not in self.board.adjacent(red_selected):
				self.board.remove_piece((red_selected[0] + (end_point[0] - red_selected[0]) / 2, red_selected[1] + (end_point[1] - red_selected[1]) / 2))		
				self.jump = True
				self.red_selected = end_point
			
			if self.jump == True:
				self.board.remove_piece((red_selected[0] + (end_point[0] - red_selected[0]) / 2, red_selected[1] + (end_point[1] - red_selected[1]) / 2))
			#Add move to undo stack
			self.undo_stack.push((red_selected, end_point))
			#Show move on screen
			self.graphics.show_moves_board((red_selected, end_point))

				
		self.end_turn()
				
			
			
def main():
	game = Game()
	game.main()
	
if __name__ == '__main__':
	main()



