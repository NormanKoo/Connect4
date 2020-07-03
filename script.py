import numpy as np
from random import randint

class Game:
  mat = None 
  rows = 0 
  cols = 0 
  turn = 0 
  wins = 0

def display_board (game):
  for row in range (game.rows-1,-1,-1):
    for col in range (game.cols):
      print (int(game.mat[row, col]), end = "  ")
    print ()

def check_victory (game):
  count1 = 0
  count2 = 0
  player1win = 0
  player2win = 0
  #check horizontal win
  for col in range (game.cols-game.wins+1):
    for row in range (game.rows):
      for i in range (game.wins):
        if game.mat[row, col+i] == 1:
          count1 += 1
        elif game.mat[row, col+i] == 2:
          count2 += 1
      if count1 == game.wins:
        player1win += 1
      elif count2 == game.wins:
        player2win += 1
      count1 = 0
      count2 = 0
  #check vertical win
  for row in range (game.rows-game.wins+1):
    for col in range (game.cols):
      for i in range (game.wins):
        if game.mat[row+i, col] == 1:
          count1 += 1
        elif game.mat[row+i, col] == 2:
          count2 += 1
      if count1 == game.wins:
        player1win += 1
      elif count2 == game.wins:
        player2win += 1
      count1 = 0
      count2 = 0
  #check positive gradient diagonal win
  for row in range (game.rows-game.wins+1):
    for col in range (game.cols-game.wins+1):
      for i in range (game.wins):
        if game.mat[row+i, col+i] == 1:
          count1 += 1
        elif game.mat[row+i, col+i] ==2:
          count2 += 1
      if count1 == game.wins:
        player1win += 1
      elif count2 == game.wins:
        player2win += 1
      count1 = 0
      count2 = 0   
  #check negative gradient diagonal win
  for row in range (game.rows-game.wins+1):
    for col in range (game.wins-1, game.cols):
      for i in range (game.wins):
        if game.mat[row+i, col-i] == 1:
          count1 += 1
        elif game.mat[row+i, col-i] == 2:
          count2 += 1
      if count1 == game.wins:
        player1win += 1 
      elif count2 == game.wins:
        player2win += 1
      count1 = 0
      count2 = 0
  if player1win > 0 and player2win > 0:
    #player who made the move wins
    return game.turn % 2 + 1
  elif player1win > 0:
    return 1
  elif player2win > 0:
    return 2
  else:
    #check for unfinished game
    for row in range (game.rows):
      for col in range (game.cols):
        if game.mat[row,col] == 0:
          return 0
    #the board is full, the game draws 
    return 3

def apply_move (game, col, pop):
  if pop == True:
    #shift the whole column down to replace the one at the row 0 
    for row in range (game.rows-1):
      game.mat[row, col] = game.mat[row+1, col]
    game.mat[game.rows-1, col] = 0
    game.turn = game.turn % 2 + 1
    return game
  else:
    #drops the disc
    for row in range (game.rows):
      if game.mat[row, col] == 0:
        game.mat[row, col] = game.turn
        game.turn = game.turn % 2 + 1
        return game

def check_move (game, col, pop):
  if pop == True:
    if game.mat[0, col] == game.turn:
      return True
    else:
      return False
  else:
    for row in range (game.rows):
      if game.mat[row, col] == 0:
        return True
    return False

def computer_move (game, level):
  while level == 1:
    #choosing random moves
    col = randint (0,game.cols-1)
    move = randint (0,1)
    pop = bool (move)
    if check_move (game, col, pop):
      # move is valid
      return (col,pop)
  while level == 2:
    def check_computer_victory(game):
      #check for computer victory
      count = 0
      computerplayerwin = 0
      #check horizontal win
      for col in range (game.cols-game.wins+1):
        for row in range (game.rows):
          for i in range (game.wins):
            if game.mat[row, col+i] == game.turn:
              count += 1
          if count == game.wins:
            computerplayerwin += 1
          count = 0
      #check vertical win
      for row in range (game.rows-game.wins+1):
        for col in range (game.cols):
          for i in range (game.wins):
            if game.mat[row+i, col] == game.turn:
              count += 1
          if count == game.wins:
            computerplayerwin += 1
          count = 0
      #check positive gradient diagonal win
      for row in range (game.rows-game.wins+1):
        for col in range (game.cols-game.wins+1):
          for i in range (game.wins):
            if game.mat[row+i, col+i] == game.turn:
              count += 1
          if count == game.wins:
            computerplayerwin += 1
          count = 0  
      #check negative gradient diagonal win
      for row in range (game.rows-game.wins+1):
        for col in range (game.wins-1, game.cols):
          for i in range (game.wins):
            if game.mat[row+i, col-i] == game.turn:
              count += 1
          if count == game.wins:
            computerplayerwin += 1 
          count = 0
      if computerplayerwin > 0:
        return game.turn
    #temporarily dropping a disc
    for col in range (game.cols):
      for row in range (game.rows):
        if game.mat[row, col] == 0:
          game.mat[row, col] = game.turn
          if check_computer_victory(game) == game.turn:
            #if computer wins, undo the move and return the winning move
            game.mat[row, col] = 0
            if check_move (game, col, False):
              return (col, False)
          else:
            #if computer doesn't win, undo the move and shift to the next column
            game.mat[row, col] = 0
            break
    #temporarily popping a disc
    for col in range (game.cols):
      if game.mat[0, col] == game.turn:
        for row in range (game.rows-1):
          game.mat[row, col] = game.mat[row+1, col]
        game.mat[game.rows-1, col] = 0 
        if check_computer_victory(game) == game.turn:
          #if computer wins, undo the move and return the winning move
          for row in range (game.rows-1, 0, -1):
            game.mat[row, col] = game.mat[row-1, col]
          game.mat[0, col] = game.turn
          if check_move (game, col, True):
            return (col, True)
        else:
          #if computer doesn't win, undo the move 
          for row in range (game.rows-1, 0, -1):
            game.mat[row, col] = game.mat[row-1, col]
          game.mat[0, col] = game.turn
    #if no winning move, computer checks for n-1 consecutive discs of the opponent and tries to block him.
    #if computer cannot block him, computer prevents move that will allow the opponent to win next turn.
    count = 0
    moves_forbidden = []
    #check for potential horizontal win of opponent
    for col in range (game.cols-game.wins+1):
      for row in range (game.rows):
        for i in range (game.wins):
          if game.mat[row, col+i] == game.turn % 2 + 1:
            count += 1
        #if there are n-1 consecutive discs
        if count == game.wins-1:
          for i in range (game.wins):
            #computer tries to drop a disc to prevent the opponent from winning (provided the disc drops in the right place)
            if game.mat[row, col+i] == 0:
              #for bottom row
              if row == 0 and check_move (game, col+i, False):
                return (col+i, False)
              #for rows above row 0
              elif game.mat[row-1, col+i] != 0 and check_move (game, col+i, False):
                return (col+i, False)
              #computer cannot block by dropping a disc (disc drops to the bottom, not in the right place), so it will prevent from building the column to allow the opponent to win
              elif row == 1:
                if game.mat[row-1, col+i] == 0:
                  moves_forbidden.append((col+i, False))
              elif row > 1:
                if game.mat[row-2,col+i] != 0 and game.mat[row-1,col+i] == 0:
                  moves_forbidden.append((col+i, False))
          #computer tries to pop his own disc to drop one of the opponent's n-1 consecutive discs
          for i in range (game.wins):
            if game.mat[row, col+i] == game.turn % 2 + 1:
              if game.mat[0, col+i] == game.turn:
                for row1 in range (game.rows-1):
                  game.mat[row1, col+i] = game.mat[row1+1, col+i]
                game.mat[game.rows-1, col+i] = 0 
                if check_victory (game) == game.turn % 2 + 1:
                  #prevent opponent from winning after popping
                  for row1 in range (game.rows-1, 0, -1):
                    game.mat[row1, col+i] = game.mat[row1-1, col+i]
                  game.mat[0, col+i] = game.turn
                  moves_forbidden.append((col+i, True))
                else:
                  #return the pop move which drops one of the opponent's n-1 consecutive discs
                  for row1 in range (game.rows-1, 0, -1):
                    game.mat[row1, col+i] = game.mat[row1-1, col+i]
                  game.mat[0, col+i] = game.turn
                  if check_move (game, col+i, True):
                    return (col+i, True)
            #if one of the computer's discs is blocking the n-1 consecutive discs of the opponent
            elif game.mat[row, col+i] == game.turn and game.mat[0, col+i] == game.turn:
              #prevent from popping the disc which may allow opponent to win the next turn
              if row < game.rows - 1 and game.mat[row+1, col+i] != game.turn:
                moves_forbidden.append((col+i, True))
              elif row == game.rows - 1:
                moves_forbidden.append((col+i, True))
        count = 0
    #check for potential vertical win of the opponent
    for row in range (game.rows-game.wins+1):
      for col in range (game.cols):
        for i in range (game.wins-1):
          if game.mat[row+i, col] == game.turn % 2 + 1:
            count += 1
        #blocks the opponent n-1 consecutive disc by dropping (popping can't block this)
        if count == game.wins-1:
          if game.mat[row+game.wins-1, col] == 0 and check_move (game, col, False):
            return (col, False)
        count = 0
    #check for potential positive gradient diagonal win of the opponent
    for row in range (game.rows-game.wins+1):
      for col in range (game.cols-game.wins+1):
        for i in range (game.wins):
          if game.mat[row+i, col+i] == game.turn % 2 + 1:
            count += 1
        #if there are n-1 consecutive discs
        if count == game.wins-1:
          for i in range (game.wins):
            #computer tries to drop a disc to prevent the opponent from winning (provided the disc drops in the right place)
            if game.mat[row+i, col+i] == 0:
              #for bottom row
              if row+i == 0 and check_move (game, col+i, False):
                return (col+i, False)
              #for rows above row 0
              elif game.mat[row+i-1, col+i] != 0 and check_move (game, col+i, False):
                return (col+i, False)
              #computer cannot block by dropping a disc(disc drops to the bottom, not in the right place), so it will prevent from building the column to allow the opponent to win
              elif row+i == 1:
                if game.mat[row+i-1, col+i] == 0:
                  moves_forbidden.append((col+i, False))
              elif row+i > 1:
                if game.mat[row+i-2, col+i] != 0 and game.mat[row+i-1, col+i] == 0:
                  moves_forbidden.append((col+i, False))
          #computer tries to pop his own disc to drop one of the opponent's n-1 consecutive discs
          for i in range (game.wins):
            if game.mat[row+i, col+i] == game.turn % 2 + 1:
              if game.mat[0, col+i] == game.turn:
                for row1 in range (game.rows-1):
                  game.mat[row1, col+i] = game.mat[row1+1, col+i]
                game.mat[game.rows-1, col+i] = 0 
                if check_victory (game) == game.turn % 2 + 1:
                  #prevent opponent from winning after popping
                  for row1 in range (game.rows-1, 0, -1):
                    game.mat[row1, col+i] = game.mat[row1-1, col+i]
                  game.mat[0, col+i] = game.turn
                  moves_forbidden.append((col+i, True))
                else:
                  #return the pop move which drops one of the opponent's n-1 consecutive discs 
                  for row1 in range (game.rows-1, 0, -1):
                    game.mat[row1, col+i] = game.mat[row1-1, col+i]
                  game.mat[0, col+i] = game.turn
                  if check_move (game, col+i, True):
                    return (col+i, True)
            #if one of the computer's discs is blocking the n-1 consecutive discs of the opponent
            elif game.mat[row+i, col+i] == game.turn and game.mat[0, col+i] == game.turn:
              #prevent from popping the disc which may allow the opponent to win the next turn
              if row+i < game.rows - 1 and game.mat[row+i+1, col+i] != game.turn:
                moves_forbidden.append((col+i, True))
              elif row+i == game.rows - 1:
                moves_forbidden.append((col+i, True))
        count = 0
    #check for potential negative gradient diagonal win of the opponent
    for row in range (game.rows-game.wins+1):
      for col in range (game.wins-1, game.cols):
        for i in range (game.wins):
          if game.mat[row+i, col-i] == game.turn % 2 + 1:
            count += 1
        #if there are n-1 consecutive discs
        if count == game.wins-1:
          for i in range (game.wins):
            #computer tries to drop a disc to prevent the opponent from winning (provided the disc drops in the right place)
            if game.mat[row+i, col-i] == 0:
              #for bottom row
              if row+i == 0 and check_move (game, col-i, False):
                return (col-i, False)
              #for rows above row 0
              elif game.mat[row+i-1, col-i] != 0 and check_move (game, col-i, False):
                return (col-i, False)
              #computer cannot block by dropping a disc (disc drops to the bottom, not in the right place), so it will prevent from building the column to allow the opponent to win
              elif row+i == 1:
                if game.mat[row+i-1, col-i] == 0:
                  moves_forbidden.append((col-i, False))
              elif row+i > 1:
                if game.mat[row+i-2, col-i] != 0 and game.mat[row+i-1, col-i] == 0:
                  moves_forbidden.append((col-i, False))
          #computer tries to pop his own disc to drop one of the opponent's n-1 consecutive discs
          for i in range (game.wins):
            if game.mat[row+i, col-i] == game.turn % 2 + 1:
              if game.mat [0, col-i] == game.turn:
                for row1 in range (game.rows-1):
                  game.mat[row1, col-i] = game.mat[row1+1, col-i]
                game.mat[game.rows-1, col-i] = 0 
                if check_victory (game) == game.turn % 2 + 1:
                  #prevent opponent from winning after popping
                  for row1 in range (game.rows-1, 0, -1):
                    game.mat[row1, col-i] = game.mat[row1-1, col-i]
                  game.mat[0, col-i] = game.turn
                  moves_forbidden.append((col-i, True))
                else:
                  #return the pop move which drops one of the opponent's n-1 consecutive discs
                  for row1 in range (game.rows-1, 0, -1):
                    game.mat[row1, col-i] = game.mat[row1-1, col-i]
                  game.mat[0, col-i] = game.turn
                  if check_move (game, col-i, True):
                    return (col-i, True)
            #if one of the computer's discs is blocking the n-1 consecutive discs of the opponent
            elif game.mat[row+i, col-i] == game.turn and game.mat[0, col-i] == game.turn:
              #prevent from popping the disc which may allow the opponent to win the next turn
              if row+i < game.rows - 1 and game.mat[row+i+1, col-i] != game.turn:
                moves_forbidden.append((col-i, True))
              elif row+i == game.rows - 1:
                moves_forbidden.append((col-i, True))
        count = 0
    #if the computer can't win directly or the computer can't block the direct win of the opponent
    while True:
      #generate random move
      col = randint (0,game.cols-1)
      move = randint (0,1)
      pop = bool (move)
      #random moves should not be the ones that would allow direct win of the opponent in the next turn
      if (col, pop) in moves_forbidden:
        continue
      else: 
        if check_move (game, col, pop):
          #random move is valid
          return (col, pop)
    
def menu ():
  game = Game ()
  #asking user to input number of rows
  r = int(input("Please enter the number of rows for the game board (min = 5, max = 10, default = 6)."))
  if 5 <= r <= 10:
    game.rows = r
  else:
    print ("Invalid. The number of rows will be 6 by default.")
    game.rows = 6
  #asking user to input number of columns
  c = int(input("Please enter the number of columns for the game board (min = 5, max = 10, default = 7)."))
  if 5 <= c <= 10:
    game.cols = c
  else:
    print ("Invalid. The number of columns will be 7 by default.")
    game.cols = 7
  #asking user to input number of consecutive same-color/number discs required for the player to win
  n = int(input("Please enter the number of consecutive same-color/number discs required for a player to win (min = 3, max = 6, default = 4)."))
  if 3 <= n <= 6:
    #must be smaller than the board
    if n < game.rows and n < game.cols:
      game.wins = n
    else:
      #the number of consecutive same-color/number disc is equal to or greater than the board length
      print ("Your game board is too small for that! Number of consecutive same-color/number discs will be 4 by default.")
      game.wins = 4
  else:
    print ("Invalid. The number of consecutive same-color/number discs will be 4 by default.")
    game.wins = 4
  game.mat = np.zeros((game.rows, game.cols))
  game.turn = 1
  #asking user to play against human or computer
  opponent = input("Who would you like to play against? human (for player 2) or computer:")
  opponent = opponent.lower()
  while opponent != "human" and opponent != "computer":
    print ("Please enter either human or computer.")
    opponent = input("Who would you like to play against? human (for player 2) or computer:")
    opponent = opponent.lower()
  #asking user to choose the difficulty level
  if opponent == "computer":
    level = int(input("Please enter the difficulty level for your computer player. 1 for random computer player, 2 for medium computer player."))
    while level != 1 and level != 2:
      print ("Please enter either 1 or 2.")
      level = int(input("Please enter the difficulty level for your computer player. 1 for random computer player, 2 for medium computer player."))

  display_board (game)
  
  while opponent == "human":
    #player 1's turn
    while game.turn == 1:
      #asking user to input the column to pop/drop or to quit
      print ("key in '#' for your move to quit.")
      col = input("Player "+str(game.turn)+", your move (0-"+str(game.cols-1)+"):")
      if col == "#":
        print ("You quit the game too early, play again next time.")
        return
      else:
        col = int(col)
      while col < 0 or col >= game.cols:
        print ("Please enter integers from 0 -",game.cols-1)
        col = input("Player "+str(game.turn)+", your move (0-"+str(game.cols-1)+"):")
        if col == "#":
          print ("You quit the game too early, play again next time.")
          return
        else:
          col = int(col)
      #asking user to choose either pop or drop
      move = int(input("1 for pop, 0 for drop:"))
      while move != 1 and move != 0:
        print ("Please enter either 0 or 1.")
        move = int(input("1 for pop, 0 for drop:"))
      pop = bool (move)
      if check_move (game, col, pop):
        #valid move is applied to the game
        game = apply_move (game, col, pop)
        display_board (game)
        if check_victory (game) == 0:
          #no winning or draw situation presents
          pass
        elif check_victory (game) == 1:
          print ("Congratulations, Player 1 wins!")
          return
        elif check_victory (game) == 2:
          print ("Congratulations, Player 2 wins!")
          return
        else:
          print ("It is a draw.")
          return
      else:
        #invalid move, continue to the top of the loop
        print ("Your move is invalid.")
    #player 2's turn
    while game.turn == 2:
      #asking user to input the column to pop/drop or to quit
      print ("key in '#' for your move to quit.")
      col = input("Player "+str(game.turn)+", your move (0-"+str(game.cols-1)+"):")
      if col == "#":
        print ("You quit the game too early, play again next time.")
        return
      else:
        col = int(col)
      while col < 0 or col >= game.cols:
        print ("Please enter integers from 0 -",game.cols-1)
        col = input("Player "+str(game.turn)+", your move (0-"+str(game.cols-1)+"):")
        if col == "#":
          print ("You quit the game too early, play again next time.")
          return 
        else:
          col = int(col)
      #asking user to choose either pop or drop
      move = int(input("1 for pop, 0 for drop:"))
      while move != 1 and move != 0:
        print ("Please enter either 0 or 1.")
        move = int(input("1 for pop, 0 for drop:"))
      pop = bool (move)
      if check_move (game, col, pop):
        #valid move is applied to the game
        game = apply_move (game, col, pop)
        display_board (game)
        if check_victory (game) == 0:
          #no winning or draw situation presents
          pass
        elif check_victory (game) == 1:
          print ("Congratulations, Player 1 wins!")
          return
        elif check_victory (game) == 2:
          print ("Congratulations, Player 2 wins!")
          return
        else:
          print ("It is a draw.")
          return
      else:
        #invalid move, continue to the top of the loop
        print ("Your move is invalid.")

  while opponent == "computer":
    #player 1's turn
    while game.turn == 1:
      #asking user to input the column to pop/drop or quit
      print ("key in '#' for your move to quit.")
      col = input("Player "+str(game.turn)+", your move (0-"+str(game.cols-1)+"):")
      if col == "#":
        print ("You quit the game too early, play again next time.")
        return
      else:
        col = int(col)
      while col < 0 or col >= game.cols:
        print ("Please enter integers from 0 -",game.cols-1)
        col = input("Player "+str(game.turn)+", your move (0-"+str(game.cols-1)+"):")
        if col == "#":
          print ("You quit the game too early, play again next time.")
          return
        else:
          col = int(col)
      #asking user to choose either pop or drop
      move = int(input("1 for pop, 0 for drop:"))
      while move != 1 and move != 0:
        print ("Please enter either 0 or 1.")
        move = int(input("1 for pop, 0 for drop:"))
      pop = bool (move)
      if check_move (game, col, pop):
        #valid move is applied to the game
        game = apply_move (game, col, pop)
        display_board (game)
        if check_victory (game) == 0:
          #no winning or draw situation presents
          pass
        elif check_victory (game) == 1:
          print ("Congratulations, Player 1 wins!")
          return
        elif check_victory (game) == 2:
          print ("Too bad, you lose. Computer wins.")
          return
        else:
          print ("It is a draw.")
          return
      else:
        #invalid move, continue to the top of the loop
        print ("Your move is invalid.")
    while game.turn == 2:
      print ("Computer is making his move...")
      computermove = computer_move (game, level)
      #valid computer move is applied
      game = apply_move (game, computermove[0], computermove[1])
      display_board (game)
      if check_victory (game) == 0:
        #no winning or draw situation presents
        pass
      elif check_victory (game) == 1:
        print ("Congratulations, Player 1 wins!")
        return
      elif check_victory (game) == 2:
        print ("Too bad, you lose. Computer wins.")
        return
      else:
        print ("It is a draw.")
        return

menu()
