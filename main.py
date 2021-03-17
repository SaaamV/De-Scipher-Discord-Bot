import discord
import re
from datetime import datetime
import csv
import time

ctf_category=773227034981826580
main_category=778885302793142293
var_dict={'cr':0,'1':0,'2':0,'3':0,'4':0,'st':0,'11':0,'12':0,'13':0,'21':0,'31':0,'41':0}
no_of_teams=44
start_time=0
start_time_r=0
limit={'11':44,'12':34,'13':24,'21':16,'31':16,'41':8}
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):

        print('Message from {0.author}: {0.content}'.format(message))
        if message.channel.category_id==main_category:

            print('Channel ID - '+str(message.channel.id))
            print('Category ID - '+str(message.channel.category_id))
            print('')
            delay=4                   

            if message.channel.name=='taas-master':
                #PROLOGUE
                if message.content==";prologue":
                    #await message.channel.send(file=discord.File('Round1/round1.csv'))
                    for line in open('prologue.txt',encoding='utf8'):
                        await message.channel.send(line)
                        if line.strip()!='.':
                            time.sleep(delay)

                #EPILOGUE
                if message.content==";epilogue":
                    for line in open('epilogue.txt',encoding='utf8'):
                        await message.channel.send(line)
                        if line.strip()!='.':
                            time.sleep(delay)

                #ROUND START
                if re.findall(';start[1-5]+',message.content) and 'watchers' in str(message.author.roles).casefold():
                    current_round=message.content[6]
                    #DELETE ROLES
 #                   with open('Round'+str(int(current_round)-1)+'/sheet.csv') as fil:
 #                       for roleid in message.guild.roles:
 #                           with open('Round0/sheet.csv') as f:
 #                               if str(roleid) in f.read() and not (str(roleid) in fil.read()):
  #                                  for user in message.guild.get_channel(773227447164207124).members:
  #                                      await user.remove_roles(roleid)

                    var_dict["cr"]=current_round           
                    for line in open('Round'+current_round+'/story.txt',encoding='utf8'):
                        await message.channel.send(line)
                        if current_round==5:
                            time.sleep(delay-2)
                        else:
                            time.sleep(delay)
                    for line in open('Round'+current_round+'/question1.txt',encoding='utf8'):
                        await message.channel.send(line)
                    start_time_r=datetime.now().time()
                    var_dict['st']=time.monotonic()

            answers=[["alexeileonov","retrosuicideparadox",'kepler3b'],['orion'],['p1an3tni9e161114320'],['betelgeuse'],['dreaditrunfromitdestinystillarrives']]
            ans=message.content
            allow=True
            if re.findall("^[1-3]_",ans):
                for line in open('Round'+var_dict['cr']+'/sheet.csv'):
                    s='question-'+str(ans[0])+','+str(message.channel.name).strip()
                    if line.startswith(s):
                        allow=False
                if allow:
                    check=ans[2:]
                    print(re.sub('[^A-Za-z0-9]+', '', check.casefold()))
                    if re.sub('[^A-Za-z0-9]+', '', check.casefold())==answers[int(var_dict['cr'])-1][int(ans[0])-1]:
                        var_dict[str(var_dict['cr'])+str(ans[0])]+=1
                        if var_dict[str(var_dict['cr'])+str(ans[0])]<=limit[str(var_dict['cr'])+str(ans[0])]: #(4-int(ans[0]))*5:
                            ans_time_r=datetime.now().time()
                            ans_time=time.monotonic()
                            print('answer time - '+str(ans_time))
                            with open('Round'+var_dict["cr"]+'/sheet.csv','a',newline='') as file:
                                writer=csv.writer(file)
                                writer.writerow([('question-'+ans[0]),str(message.channel.name).strip(),message.channel.id,ans_time_r,ans_time-var_dict['st']])
                            await message.channel.send("Correct.")
                            if int(var_dict["cr"])==5:
                                await message.channel.send("All tests completed. Samples acquired...")

                            if int(var_dict["cr"])==2:
                                await message.channel.send("Analyzing your results...")
                            if int(var_dict["cr"])==1 and int(ans[0])==3:
                                await message.channel.send("Your training has been completed. Awaiting further orders...")
                            if int(var_dict["cr"])==3 and int(ans[0])==1:
                                await message.channel.send("_Transporting you to the upper chamber. **HOLD**..._")
                            if int(var_dict["cr"])==4 and int(ans[0])==1:
                                await message.channel.send("**_Those who wander far into darkness, realise it too late..._**")

                            for line in open('Round'+var_dict["cr"]+'/question'+f'{int(ans[0])+1}'+'.txt', encoding='utf8'):
                                await message.channel.send(line)                        
                        else:
                            await message.channel.send("The round has been closed!")
                    else:
                        await message.channel.send("**WRONG!**")
                else:
                    await message.channel.send("You have already answered that...")
client = MyClient()
client.run('NzczNDUzMDE5MzY2NDI0NTg2.X6JcQQ.6IzInN48aTiFUGTMCq4N4smwido')