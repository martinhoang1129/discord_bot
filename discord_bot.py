import discord
import requests                                     # json is a module that helps make data readable 
import json 
import urllib3 
import random 
import os
from discord.ext import commands, tasks 
from itertools import cycle
import asyncio 
import time
import math 


# represents the bot 
# client = discord.Client() 
client = commands.Bot(command_prefix='$')


board = {7: ' ', 8: ' ', 9: ' ',
         4: ' ', 5: ' ', 6: ' ',
         1: ' ', 2: ' ', 3: ' '}

player = "X"
bot = "O" 

def printBoard(board): 
    print(board[7] + " | " + board[8] + " | " + board[9])
    print("--+---+--")
    print(board[4] + " | " + board[5] + " | " + board[6])
    print("--+---+--")
    print(board[1] + " | " + board[2] + " | " + board[3])
    print("\n")

# Checks if space is free
# If space is not free then it'll ask user to input another position 
def spaceIsFree(position): 
    return board[position] == ' '                           # need return to tell us True/False boolean 
         
# inserting letter in open space 
def insertLetter(letter, position): 
    board[position] = letter                                # Syntax error earlier. I am not returning a value and equating it to letter. I am assigning. return board[pos] == letter isn't correct 

# Player move checks if spaceIsFree then insertLetter into board 
def playerMove():  
    while True: 
        try:                                                # Try/except allows us to handle input error 
            move = int(input('Where would you like to move? [1-9]: '))
            if spaceIsFree(move):                           # condition should be if int(input) is successful. If not it'll print the reason why and then reloop 
                insertLetter(player, move)
                break
            else: 
                print("Space is taken. Pick another position")
        except: 
            print('Please enter a number from [1-9]: ')
    if isWinner(board): 
        print('X has won!')
    if isTie(): 
        print('Tie game!')
    

# uses minMax function 
# computer will be minimizing as "O". X is maximizing 
def pcMove(): 
    bestScore = math.inf
    bestMove = 0 
    alpha = -math.inf 
    beta = math.inf
    start = time.time() 
    # loop through Keys in dictionary. Look for empty Value. Place letter and compute score using minimax F(x). Then remove the letter. 
    # if score is highest, replace current bestScore
    # bestMove for that score is the key, the number in the dictionary 
    # this f(x) pcMove and the loop relates the Key, value to the score and minimax function 
    for key in board.keys(): 
        if board[key] == ' ': 
            board[key] = bot 
            score = minimax(board, 0, alpha, beta, True)# depth of 0 but it'll increase as keys loop through the dictionary 
            board[key] = ' '               # place temp move, compute score of that move, and then remove it. Do this to compute scores of all possible moves 
            if score < bestScore: 
                bestScore = score 
                bestMove = key 
    end = time.time() 
    print("Evaluation time: {}s".format(round(end - start, 7)))

    insertLetter(bot, bestMove)  
    if isWinner(board): 
        print('O has won!')
    if isTie(): 
        print('Tie game!')
          
    return 
          

# minimax function utlized within pcMove()
def minimax(position, depth, alpha, beta, isMaximizing):
    # with any recrusive function, we need a basecase 
    # Tells us how each move is scored 
    # This is the base case right here. At the basecase, it gives a score of who won 
    # depth 0 means current node. (depth - 1) means we want to keep checking the next node down everyturn until we reach the basecase/the leaf node 
    if whichLetterWon(player): 
        return 1 
    elif whichLetterWon(bot): 
        return -1
    elif isTie(): 
        return 0 

    # maximizing 
    if isMaximizing: 
        bestScore = -math.inf
        for key in board.keys(): 
            if board[key] == ' ': 
                board[key] = player 
                score = minimax(board, depth - 1, alpha, beta, False) 
                board[key] = ' ' 
                if score > bestScore: 
                    bestScore = score
                alpha = max(alpha, score) 
                if beta <= alpha:
                    break            
        return bestScore             

    # minimizing
    else: 
        bestScore = math.inf 
        for key in board.keys(): 
            if board[key] == ' ': 
                board[key] = bot 
                score = minimax(board, depth - 1,alpha, beta, True) 
                board[key] = ' ' 
                if score < bestScore: 
                    bestScore = score
                beta = min(beta, score)
                if beta <= alpha: 
                    break            
        return bestScore
    
# Need whichLetterWon function for minimax to score winner. 
def whichLetterWon(mark): 
    if board[7] == board[8] == board[9] == mark: 
        return True 
    elif board[4] == board[5] == board[6] == mark: 
        return True
    elif board[1] == board[2] == board[3] == mark: 
        return True
    elif board[1] == board[4] == board[7] == mark: 
        return True
    elif board[2] == board[5] == board[8] == mark: 
        return True
    elif board[3] == board[6] == board[9] == mark: 
        return True
    elif board[1] == board[5] == board[9] == mark: 
        return True
    elif board[7] == board[5] == board[3] == mark: 
        return True
    else:                                  
        return False 

# winning condition
def isWinner(board): 
    if board[7] == board[8] == board[9] != ' ': 
        return True 
    elif board[4] == board[5] == board[6] != ' ': 
        return True
    elif board[1] == board[2] == board[3] != ' ': 
        return True
    elif board[1] == board[4] == board[7] != ' ': 
        return True
    elif board[2] == board[5] == board[8] != ' ': 
        return True
    elif board[3] == board[6] == board[9] != ' ': 
        return True
    elif board[1] == board[5] == board[9] != ' ': 
        return True
    elif board[7] == board[5] == board[3] != ' ': 
        return True
    else:                                  
        return False        

# check for tie 
def isTie(): 
    for key in board.keys():                # iterate through keys. Check if empty value at KV. If so then False (no tie). This method is better than hardcoding 
        if board[key] == ' ': 
            return False
    return True 

@client.command(aliases=['TTT', 'tictactoe']) 
async def tic_tac_toe(ctx): 
    await ctx.send(printBoard(board))           #anything that's print may need to be changed to await.ctx.send 
    # while not isWinner(board): 
    #     playerMove()
    #     printBoard(board)
    #     pcMove() 
    #     printBoard(board)
    #     if isTie(): 
    #         break    














# function telling us when users leave and join server 
@client.event
async def on_member_join(member): 
    print(member + 'has joined the server')

@client.event
async def on_member_remove(member): 
    print(member + 'has left the server')

# event: bot is ready, it logs in 
@client.event
async def on_ready(): 
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Blessing People"))

# utilizing Cogs & classes 
# allows cleaner code. Write functions within classes/cogs organizes function
# we can also write code in a seperate .py file and load it in for cleaner code
@client.command()
async def load(ctx, extension): 
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension): 
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension): 
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('H:\Programming\Projects\cogs'):                                   # ./ tells us to look for all files within current directory 
     if filename.endswith('.py'): 
         client.load_extension(f'cogs.{filename[:-3]}')


# loop updating status isn't working 
status = cycle(['Blessing People', 'Saving Lives', 'Turning up', 'Praising da Lord', 'Making Miracles'])
# loop updating playing status of bot every 10s
@tasks.loop(seconds=30) 
async def change_status(): 
    await client.change_presence(activity=discord.Game(next(status))) 


# using converters to parse data 
# banning and unbanning for X amount time 
# need to add permission requirement. Do not want everyone to use ban/kick/unbann/delete message options 
class DurationConverter(commands.Converter): 
    async def convert(self, ctx, argument): 
        amount = argument[:-1]                      # everything before the 2nd to last character is the amount 
        unit = argument[-1]                         # the last character is the unit 

        if amount.isdigit() and unit in ['s', 'm']: 
            return (int(amount), unit) 

        raise commands.BadArgument(message='Not a valid duration')    # error handling. Similar to command error but this is a user input error 


# # # converter searches up the member using other information rather than specific names 
@client.command() 
async def ban(ctx, member: commands.MemberConverter, duration: DurationConverter): 
    multiplier = {'s': 1, 'm': 60}      # tuple used to multiply s for ban
    amount, unit = duration 

    await ctx.guild.ban(member) 
    await ctx.send(f'{member} has been banned for {amount}{unit}!')
    await asyncio.sleep(amount * multiplier[unit])
    await ctx.guild.unban(member) 



TOKEN = 'OTQxNjk3NjUwNzQ5NzQ3MjAw.YgZuRw.exizPEQ9qSDkJW0B8bW794K1B5g'
client.run(TOKEN) 



# sad_words = ['sad', 'help', 'depressed', 'sucks', 'miserable', 'depressing', 'why',' bleak', 'daunting', 'disheartening', 'stress', 'stressed', 'stressful']
# encouragement = ['You can do this!', 'You got this bro', 'I will guide you', 'God has never failed', 'God cannot fail', 'Everything happens for a reason', 'God is with you wherever you go']

# # function gets a quote 
# # quote is in form of a dictionary 
# def get_quote(): 
#     response = requests.get("https://zenquotes.io/api/random")
#     json_data = json.loads(response.text) 
#     quote = json_data[0]['q'] + " -" + json_data[0]['a']                                # creates the quote + author 
#     return quote 

# def get_verse(): 
#     verse = requests.get("https://quotes.rest/bible/verse.json")
#     json_data = json.loads(verse.text) 
#     bible_verse = json_data['contents']['book'] + ' ' + json_data['contents']['chapter'] + ': ' + json_data['contents']['number'] + ' - ' + json_data['contents']['verse']
#     return bible_verse


# # event: receiving message
# # event is something the bot listens for  
# @client.event
# async def on_message(message): 
#     # nothing happens if message is from ourself
#     if message.author == client.user: 
#         return 

#     # is message a cmd? 
#     # whenever someone says $hello, the bot will respond back 
#     if message.content.startswith('$hello'): 
#         await message.channel.send('Hello!')

#     if message.content.startswith('$inspire'): 
#         quote = get_quote()
#         await message.channel.send(quote)  

#     if message.content.startswith('$verse'): 
#         bible_verse = get_verse()
#         await message.channel.send(bible_verse) 
    
#     # check for sad words within the user message
#     # nested double loop. Loop through each word within the sentence. Then checks for word within list looking for a match 
#     if any(word in message.content for word in sad_words) and '$help' not in message.content: 
#         await message.channel.send(random.choice(encouragement))
    
#     # On message overrides any commands from running, so we need this line 
#     # https://discordpy.readthedocs.io/en/rewrite/faq.html#why-does-on-message-make-my-commands-stop-working
#     await client.process_commands(message)                              # line is critical. If this line doesn't exist, the program doesn't run any commands. 

