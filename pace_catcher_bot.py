# v0.2.0

import discord
import os
import datetime
import time

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

path_current = f'{os.path.dirname(os.path.realpath(__file__))}'
path_allnames = f'{path_current}\\data\\allnames.txt'
path_temp = f'{path_current}\\data\\temp.txt'
path_dir = f'{path_current}\\data'

# bot started logs
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  ch_name = 'bot-test-1'
  for channel in client.get_all_channels():
    if channel.name == ch_name:
      await channel.send('bot started!')


# Main
@client.event
async def on_message(message):

  # setup guild
  guild = message.guild  

  # return if sended from bot
  if message.author == client.user:
    return
  
  # IDs
  author_1 = 647361970764251156 # admin
  author_2 = 1136700221603192873 # PaceManBot

  # return if sended from not admin and PaceManBot
  if message.author.id != author_1 and message.author.id != author_2:
    return

  # underscore fix
  fix_message = message.content.replace('ˍ', '_')

  # get PB Paces
  channel = discord.utils.get(message.guild.channels, name='pacemanbot-runner-pbpaces')
  pbpaces = await channel.fetch_message(channel.last_message_id) # msg ID
  split = pbpaces.content.replace('\n', '/').replace(' : ', '/')
  pbpace_list = split.split('/')
  print(f'pbpace_list: {pbpace_list}')

  for i in range(0, len(pbpace_list), 7):
    if pbpace_list[i] in fix_message:
      print(f'find Name, PB Paces and PB: {pbpace_list[i]}/{pbpace_list[i+1]}/{pbpace_list[i+2]}/{pbpace_list[i+3]}/{pbpace_list[i+4]}/{pbpace_list[i+5]}/{pbpace_list[i+6]}') # name/fs/ss/b/e/ee/pb
      # add :00
      for m in range(1, 6):
        if pbpace_list[i+m].find(':') == -1:
          pbpace_list[i+m] = f'{pbpace_list[i+m]}:00'
      break

  # priority: -1=NoPlayer, 0= Nothing, 1=FS, 3=SS, 4=B, 5=E, 6=SSPB, 7=EE, 8=BPB, 9=EPB, 10=EEPB
  role = discord.utils.get(guild.roles, name="*FS30:0")
  if fix_message.find(f'{role.id}') != -1: # FS (Bastion)
    priority = 1
    # not exist a FSPB role

  role = discord.utils.get(guild.roles, name="*SS40:0")
  if fix_message.find(f'{role.id}') != -1: # SS (Bastion)
    priority = 3
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(pbpace_list[i+2]): # ss < pb pace
      priority = 6

  role = discord.utils.get(guild.roles, name="*B45:0")
  if fix_message.find(f'{role.id}') != -1: # B
    priority = 4
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(pbpace_list[i+3]): # b < pb pace
      priority = 8

  role = discord.utils.get(guild.roles, name="*E52:0")
  if fix_message.find(f'{role.id}') != -1: # E
    priority = 5
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(pbpace_list[i+4]): # e < pb pace
      priority = 9

  role = discord.utils.get(guild.roles, name="*EE55:0")
  if fix_message.find(f'{role.id}') != -1: # EE
    priority = 7
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(pbpace_list[i+5]): # ee < pb pace
      priority = 10

  role = discord.utils.get(guild.roles, name="FIN")
  if fix_message.find(f'{role.id}') != -1: # FIN
    priority = 0

  role = discord.utils.get(guild.roles, name="NPB")
  if fix_message.find(f'{role.id}') != -1: # NPB
    priority = 11

  # get TwitchID
  channel = discord.utils.get(message.guild.channels, name='pacecatcher-name-to-id')
  ids = await channel.fetch_message(channel.last_message_id) # msg ID
  split = ids.content.replace('\n', '/').replace(' : ', '/')
  id_list = split.split('/')
  print(f'id_list: {id_list}')

  # send Temp
  allname = getallnames(path_allnames, path_dir)
  for l in range(len(allname)):
    if fix_message.find(f'{allname[l]}') != -1:
      with open(path_temp, 'w') as f:
        if allname[l] in id_list:
          f.write(f'{id_list[id_list.index(allname[l])]}')
          print(allname[l])
          print(id_list[id_list.index(allname[l])])
        else:
          f.write(f'{allname[l]}')
        f.write(f'\n{priority}')


  # bot stop command
  if '!stop' in fix_message:
    await message.channel.send('bot closed!')
    await client.close()
    return


# Defs
# https://stackoverflow.com/questions/72630298/adding-any-unix-timestamp-in-discord-py
def convert_to_unix_time(date: datetime.datetime, days: int, hours: int, minutes: int, seconds: int) -> str:
  # Get the end date
  end_date = date + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

  # Get a tuple of the date attributes
  date_tuple = (end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)

  # Convert to unix time
  return f'<t:{int(time.mktime(datetime.datetime(*date_tuple).timetuple()))}:R>'


# https://gist.github.com/himoatm/e6a189d9c3e3c4398daea7b943a9a55d
def string_to_datetime(string):
  return datetime.datetime.strptime(string, '%M:%S')


def getallnames(path, path_dir):
  if os.path.isdir(path_dir) == False:
    os.makedirs(path_dir)
  try:
    with open(path, 'x') as f:
      f.write('')
  except FileExistsError:
    pass
  with open(path) as f:
    name = f.read().splitlines()
  return name


client.run('TOKEN')