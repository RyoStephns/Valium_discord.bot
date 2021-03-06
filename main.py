from asyncio.tasks import sleep
import random
from typing import Optional
import discord
from discord import embeds
from discord.ext import commands
from discord import client
from discord.member import Member
from discord.user import User
from discord_components import *
from random import randint
import asyncio
from discord.ext import commands
from database import *
import os
from dotenv import load_dotenv


#======================================================================================


prefix = '*'
load_dotenv()
token = os.getenv('TOKEN_ID')
client = commands.Bot(command_prefix= prefix, help_command=None)


#======================================================================================


@client.event
async def on_ready():
    await client.change_presence(status= discord.Status.idle, activity= discord.Game(name='Prefix is *'))
    print('Bot is Online')
    DiscordComponents(client)

@client.command()
async def info(ctx):
    async with ctx.channel.typing():
        await asyncio.sleep(5)
        myEmbed = discord.Embed(title= 'About', description= 'Bot is created at 6th September 2021', color= ctx.author.color )
        myEmbed.add_field(name= 'Current Version',value='`(v.2.7)`\n',inline=False)
        # myEmbed.add_field(name= 'New Updates..',value= '`(v.2.7)`\nReleased date : `(17/09/21)`\n`✓Added new commands`\n`✓New features`',inline=False)
        myEmbed.add_field(name= 'Incoming Update released soon..',value='Status : `Beta test`',inline= False)
        myEmbed.set_image(url='https://cdna.artstation.com/p/assets/images/images/012/916/652/large/daniel-riise-rocksoverview.jpg?1537181807')
    await ctx.message.channel.send('Here is the latest information about me <3',embed=myEmbed)

@client.command(name='create')
async def create(ctx):
    if CheckID(ctx.message.author.id) == True:
        await ctx.send('You already have `Valium` Account')

    else:
        async with ctx.channel.typing():
            await asyncio.sleep(5)
        Create_Account(ctx.message.author.id,ctx.author.display_name)
        await ctx.send('Succesfuly create `Valium` Account')

@client.command(name= 'players')
async def ReadAll(ctx):
    if ctx.message.author.id == 500762971165818910:
        players=Read()
        await ctx.send(players)
    else:
        await ctx.send('This command is only valid for GM')

@client.command(name='credit',aliases=['cr'])
async def credit(ctx,target:Optional[Member]):
        target= target or ctx.author
        if  CheckID(ctx.message.author.id) != True:
            await ctx.send('You dont have`Valium` account')
            await ctx.send('Type `create` to make one')
        elif  CheckID(target.id) != True:
            await ctx.send('The user you mentioned dont have `Valium` account')
        elif CheckID(target.id) == True:
            data= Check(target.id,'credit')
            credit = "{:,}".format(data)
            embeds=discord.Embed(color= ctx.author.color )
            embeds.add_field(name='** **',value= f'```python\n{credit} Cr\n```')
            embeds.set_thumbnail(url='https://image.freepik.com/free-vector/video-game-coin-pixelated-icon_24908-33120.jpg')
            embeds.set_author(name=target.display_name+"'s Credits",icon_url=target.avatar_url)
            await ctx.send(ctx.author.mention,embed=embeds)

@client.command()
async def ping(ctx):
	await ctx.send(f'Whut? {ctx.message.author.mention}')

@client.command(name='help',aliases=['com','co'])
async def help(ctx):
    prefix_embed= discord.Embed(title='Commands', color= ctx.author.color )
    prefix_embed.add_field(name = 'General',value = '`info` | `help` | `ping`',inline= False)
    prefix_embed.add_field(name = 'Gamble',value = '`dice`',inline= False)
    prefix_embed.add_field(name = 'Battle',value = '`Hunt`',inline= False)
    prefix_embed.add_field(name = 'Account',value = '`create` | `profile` | `bag` | `use`',inline= False)
    prefix_embed.add_field(name = 'Economy',value = '`credit` | `shop` | `buy` | `sell` | `give(amount)(mention)`',inline= False)
    prefix_embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.channel.purge(limit= 1)
    await ctx.message.channel.send(embed=prefix_embed)

@client.command(name= 'dice', aliases=['dc'])
async def dice(ctx,answer=0,bet=0):
    num=(random.randint(1,6))
    if CheckID(ctx.message.author.id) != True:
        await ctx.send('You dont have `Valium` account')
        await ctx.send('Type `create` to make one')
    elif CheckID(ctx.message.author.id) == True:
        dat=Check(ctx.message.author.id,'credit')
        if answer == 0 and bet == 0:
            await ctx.send('`*dice (number)(bet)`')
            await ctx.send('`Rule:\nChoose a number between 1-6\nPrize amount is 10 times from your bet`')
        elif bet == 0:
            await ctx.send('Input bet amount')
        elif answer > 6:
            await ctx.send('Number is out of range')
            await ctx.send('Choose a number between `1-6`')
        elif dat < bet:
            await ctx.send('Not enough `credit`\nset lower bet')
        else: 
            prize = 10*bet
            pr = "{:,}".format(prize)
            cost = bet
            cst = "{:,}".format(cost) 
            await ctx.send(f'{ctx.author.display_name} pick `{answer}`',
            components=ActionRow(
                    [
                        Button(
                        style= ButtonStyle.green,
                        label='Generate'
                        )
                    ]
                )
            )
            inter= await client.wait_for('button_click')
            if inter.component.label == 'Generate':
                if answer == num:
                    Edit(ctx.message.author.id,'credit',True,prize)
                    await inter.respond(content= num)
                    await ctx.send(content=f'Damnn lucky!! {ctx.author.display_name} got `{pr}`Cr')
                else:
                    Edit(ctx.message.author.id,'credit',False,cost)
                    await inter.respond(content= num)
                    await ctx.send(content=f'Too bad! you lost `{cst}`Cr')

@client.command(name='profile', aliases=['p'])
async def profile(ctx,target:Optional[Member]):
    target= target or ctx.author
    if CheckID(target.id) == True:
        Health= Check(target.id,'hp')
        hplimit= Check(target.id,'hplim')
        mplimit= Check(target.id,'mplim')
        Attack= Check(target.id,'str')
        Defence= Check(target.id,'def')
        Vit= Check(target.id,'vit')
        Mp= Check(target.id,'mp')
        Int= Check(target.id,'intel')
        Level= Check(target.id,'lvl')
        Exp= Check(target.id,'exp')
        Expup= Check(target.id,'expup')
        
        prof= discord.Embed(title=f'*Level*  `{Level}`\n*EXP*   `{Exp}/{Expup}`',description=f'*Class* : `None`',color=ctx.author.color)
        Hp =f'```python\n({Health}/{hplimit})\n```'
        mp =f'```python\n({Mp}/{mplimit})\n```'
        prof.add_field(name=f':small_blue_diamond: **HP**', value=Hp)
        prof.add_field(name=f':small_blue_diamond: **MP**', value=f'{mp}\n-----------',inline=False)
        prof.add_field(name='`STR`',value=f'```{Attack}```',inline=True)
        prof.add_field(name='`DEF`',value=f'```{Defence}```',inline=True)
        prof.add_field(name='`VIT`',value=f'```{Vit}```',inline= True)
        prof.add_field(name='`INT`',value=f'```{Int}```',inline= False)
        prof.set_author(name=f'{target.display_name}`s Profile',icon_url=target.avatar_url)
        await ctx.send(embed=prof)
    elif CheckID(ctx.message.author.id) != True:
        await ctx.send('You dont have `Valium` account')
        await ctx.send('use `create` to register')
    elif CheckID(target.id) != True:
        await ctx.send('The user you mentioned dont have `Valium` account')

@client.command(name= 'shop')
async def shop(ctx, menu= 1):
    if CheckID(ctx.message.author.id) != True:
        await ctx.send('You dont have `Valium` account')
        await ctx.send('Type `create` to make one')
    else:
        if menu == 1:
            emb=discord.Embed(title=f'Shop page - {menu}/2', description='*Consumable*\n`Potion(S)` `+90HP` | `70 Cr`\n`Potion(M)` `+150HP` | `100 Cr`\n`Potion(L)` `+500HP` | `300 Cr`\n')
            await ctx.send(embed=emb)
        elif menu == 2:
            emb=discord.Embed(title=f'Shop page - {menu}/2', description='*Dungeon Key*\n`D Gate Key` | `400 Cr`\n`C Gate Key` | `600 Cr`\n`B Gate Key` | `1000 Cr`\n`A Gate Key` | `2000 Cr`\n')
            await ctx.send(embed=emb)

@client.command(name='buy',aliases=['b'])
async def buy(ctx, name=None, amt= 1):
    user=ctx.message.author.id
    if CheckID(user) != True:
        await ctx.send('You dont have `Valium` account')
        await ctx.send('type `create` to make one')
    else:
        credit=Check(user,'credit')
        if name == None:
            emb=discord.Embed(name='Shop Rule',description='** **',color= ctx.author.color)
            emb.add_field(name='Potions',value='potion-[size]\nExample: *buy potion-s',inline=False)
            emb.add_field(name='Gate key',value='[type]-key\nExample: *buy d-key',inline=False)
            await ctx.send('`*buy (item)(value)`',embed=emb)
        elif name == 'potion-s':
            price=50*amt
            if credit > price or credit == price:
                EditUsable(user,'pots',True,amt)
                Edit(user,'credit',False,price)
                await ctx.send(f'Player bought `{amt}` Potion(S)')
            else:
                await ctx.send('Not enough `Credits`')
        elif name == 'potion-m':
            price=100*amt
            if credit > price or credit == price:
                EditUsable(user,'potm',True,amt)
                Edit(user,'credit',False,price)
                await ctx.send(f'Player bought `{amt}` Potion(M)')
            else:
                await ctx.send('Not enough `Credits`')
        elif name == 'potion-l':
            price=300*amt
            if credit > price or credit == price:
                EditUsable(user,'potl',True,amt)
                Edit(user,'credit',False,price)
                await ctx.send(f'Player bought `{amt}` Potion(L)')
            else:
                await ctx.send('Not enough `Credits`')
        elif name == 'd-key':
            price=400*amt
            if credit > price or credit == price:
                EditUsable(user,'dgate',True,amt)
                Edit(user,'credit',False,price)
                await ctx.send(f'Player bought `{amt}` D-Gate Key')
            else:
                await ctx.send('Dont have enough `Credits`')
        elif name == 'c-key':
            price=600*amt
            if credit > price or credit == price:
                EditUsable(user,'cgate',True,amt)
                Edit(user,'credit',False,price)
                await ctx.send(f'Player bought `{amt}` C-Gate Key')
            else:
                await ctx.send('Dont have enough `Credits`')
        elif name == 'b-key':
            price=1000*amt
            if credit > price or credit == price:
                EditUsable(user,'bgate',True,amt)
                Edit(user,'credit',False,price)
                await ctx.send(f'Player bought `{amt}` B-Gate Key')
            else:
                await ctx.send('Dont have enough `Credits`')
        elif name == 'a-key':
            price=2000*amt
            if credit > price or credit == price:
                EditUsable(user,'agate',True,amt)
                Edit(user,'credit',False,price)
                await ctx.send(f'Player bought `{amt}` A-Gate Key')
            else:
                await ctx.send('Dont have enough `Credits`')

@client.command(name='use')
async def use(ctx,item=None):
    user= ctx.message.author.id
    if CheckID(user) != True:
        await ctx.send('You dont have `Valium` account')
        await ctx.send('Type `create` to make one')
    else:
        if item == None:
            await ctx.send('`*use (item)`')
            await ctx.send('`Example:\n*use potion-s`')
        
        if CheckID(user) != False:
            userhp=Check(user,'hp')
            hplim=Check(user,'hplim')
            class Potions():
                def __init__(self,Heal):
                    self.Heal = Heal
                def use(self):
                    HP=Check(user,'hp')
                    HPlim=Check(user,'hplim')
                    HealPoint=self.Heal
                    if HealPoint >= HPlim-HP:
                        Edit(user,'hp',True,HPlim-HP)
                        return HealPoint
                    else:
                        val= HP + HealPoint
                        Edit(user,'hp',True,val)
            PotionS=Potions(90)
            PotionM=Potions(150)
            PotionL=Potions(500)
            if item == 'potion-s':
                pots=CheckUsable(user,'pots')
                if pots == 0:
                    await ctx.send('You dont have `Potion(S)`')
                elif userhp == hplim:
                    await ctx.send('Your `HP` is full')
                else:
                    PotionS.use()
                    HP = Check(user,'hp')
                    HPLIM = Check(user,'hplim')
                    After_Potion = discord.Embed(title = 'HP Restored', description = f'{HP}/{HPLIM}',color = ctx.author.color)
                    EditUsable(user,'pots',False,1)
                    await ctx.send(ctx.author.mention,embed = After_Potion)
            elif item == 'potion-m':
                potm=CheckUsable(user,'potm')
                if potm == 0:
                    await ctx.send('You dont have `Potion(M)`')
                elif userhp == hplim:
                    await ctx.send('Your `HP`is full')
                else:
                    PotionM.use()
                    HP = Check(user,'hp')
                    HPLIM = Check(user,'hplim')
                    After_Potion = discord.Embed(title = 'HP Restored', description = f'{HP}/{HPLIM}',color = ctx.author.color)
                    EditUsable(user,'potm',False,1)
                    await ctx.send(ctx.author.mention,embed = After_Potion)

            elif item == 'potion-l':
                potl=CheckUsable(user,'potl')
                if potl == 0:
                    await ctx.send('You dont have `Potion(L)`')
                elif userhp == hplim:
                    await ctx.send('Your `HP` is full')
                else:
                    PotionL.use()
                    HP = Check(user,'hp')
                    HPLIM = Check(user,'hplim')
                    After_Potion = discord.Embed(title = 'HP Restored', description = f'{HP}/{HPLIM}',color = ctx.author.color)
                    EditUsable(user,'potl',False,1)
                    await ctx.send(ctx.author.mention,embed = After_Potion)

@client.command(name='punish')
async def damage(ctx,value,target:Optional[Member]):
    val= int(value)
    user= ctx.message.author.id
    target= target or ctx.author
    Health = Check(target.id,'hp')
    if user != 500762971165818910:
        await ctx.send('This command is only valid for GM')
    else:
        if val > Health:
            Edit(target.id,'hp',False,Health)
            await ctx.send(f'{target.display_name} HP decreased to `0`')
        else:
            Edit(target.id,'hp',False,val)
            await ctx.send('```GM USE Punish```')
            HP = Check(target.id,'hp')
            await ctx.send(f'{target.display_name} HP decreased to `{HP}`')

@client.command(name='sell')
async def sell(ctx,name=None,value=1):
    user=ctx.message.author.id
    if CheckID(user) != True:
        await ctx.send('You dont have `Valium` account')
        await ctx.send('type `create` to make one')
    else:
        if name == None:
            await ctx.send('`*sell (item)(value)`')
        
        elif name == 'potion-s':
            qty=CheckUsable(user,'pots')
            prc=value*50//2
            nom="{:,}".format(prc)
            if qty > value or qty == value:
                EditUsable(user,'pots',False,value)
                Edit(user,'credit',True,prc)
                await ctx.send(f'Player sold `{value}` Potion(S)')
                await ctx.send(f'Player got `{nom}` Credits')
            elif qty == 0:
                await ctx.send('?')
            else:
                await ctx.send('Insufficient item amount')

        elif name == 'potion-m':
            qty=CheckUsable(user,'potm')
            prc=value*100//2
            nom="{:,}".format(prc)
            if qty > value or qty == value:
                EditUsable(user,'potm',False,value)
                Edit(user,'credit',True,prc)
                await ctx.send(f'Player sold `{value}` Potion(M)')
                await ctx.send(f'Player got `{nom}` Credits')
            elif qty == 0:
                await ctx.send('?')
            else:
                await ctx.send('Insufficient item amount')

        elif name == 'potion-l':
            qty=CheckUsable(user,'potl')
            prc=value*300//2
            nom="{:,}".format(prc)
            if qty > value or qty == value:
                EditUsable(user,'potl',False,value)
                Edit(user,'credit',True,prc)
                await ctx.send(f'Player sold `{value}` Potion(L)')
                await ctx.send(f'Player got `{nom}` Credits')
            elif qty == 0:
                await ctx.send('?')
            else:
                await ctx.send('Insufficient item amount')
        elif name == 'd-key':
            qty=CheckUsable(user,'dgate')
            prc=value*400//2
            nom="{:,}".format(prc)
            if qty > value or qty == value:
                EditUsable(user,'dgate',False,value)
                Edit(user,'credit',True,prc)
                await ctx.send(f'Player sold `{value}` D-key Gate')
                await ctx.send(f'Player got `{nom}` Credits')
            elif qty == 0:
                await ctx.send('?')
            else:
                await ctx.send('Insufficient item amount')
        elif name == 'c-key':
            qty=CheckUsable(user,'cgate')
            prc=value*600//2
            nom="{:,}".format(prc)
            if qty > value or qty == value:
                EditUsable(user,'cgate',False,value)
                Edit(user,'credit',True,prc)
                await ctx.send(f'Player sold `{value}` C-Gate Key')
                await ctx.send(f'Player got `{nom}` Credits')
            elif qty == 0:
                await ctx.send('?')
            else:
                await ctx.send('Insufficient item amount')
        elif name == 'b-key':
            qty=CheckUsable(user,'cgate')
            prc=value*1000//2
            nom="{:,}".format(prc)
            if qty > value or qty == value:
                EditUsable(user,'bgate',False,value)
                Edit(user,'credit',True,prc)
                await ctx.send(f'Player sold `{value}` B-Gate Key')
                await ctx.send(f'Player got `{nom}` Credits')
            elif qty == 0:
                await ctx.send('?')
            else:
                await ctx.send('Insufficient item amount')
        elif name == 'a-key':
            qty=CheckUsable(user,'agate')
            prc=value*2000//2
            nom="{:,}".format(prc)
            if qty > value or qty == value:
                EditUsable(user,'agate',False,value)
                Edit(user,'credit',True,prc)
                await ctx.send(f'Player sold `{value}` A-Gate Key')
                await ctx.send(f'Player got `{nom}` Credits')
            elif qty == 0:
                await ctx.send('?')
            else:
                await ctx.send('Insufficient item amount')

@client.command(name='bag',aliases=['bg'])
async def back(ctx):
    user= ctx.message.author.id
    if CheckID(user) != True:
        await ctx.send('You dont have `Valium` account')
        await ctx.send('type `create` to make one')
    else:
        items=intro(ctx.message.author.id)
        val = len(items)
        if val == 0:
            emb=discord.Embed(title='Inventory', description='Empty',color= ctx.author.color)
            await ctx.send(embed=emb)
        elif val == 1:
            emb=discord.Embed(title='Inventory', description=f'`{items[0][0]} {items[0][1]}`',color= ctx.author.color)
            await ctx.send(embed=emb)
        elif val == 2:
            emb=discord.Embed(title='Inventory', description=f'`{items[0][0]} {items[0][1]}`\n`{items[1][0]} {items[1][1]}`',color= ctx.author.color)
            await ctx.send(embed=emb)
        elif val == 3:
            emb=discord.Embed(title='Inventory', description=f'`{items[0][0]} {items[0][1]}`\n`{items[1][0]} {items[1][1]}`\n`{items[2][0]} {items[2][1]}`',color= ctx.author.color)
            await ctx.send(embed=emb)
        elif val == 4:
            emb=discord.Embed(title='Inventory', description=f'`{items[0][0]} {items[0][1]}`\n`{items[1][0]} {items[1][1]}`\n`{items[2][0]} {items[2][1]}`\n`{items[3][0]} {items[3][1]}`',color= ctx.author.color)
            await ctx.send(embed=emb)
        elif val == 5:
            emb=discord.Embed(title='Inventory', description=f'`{items[0][0]} {items[0][1]}`\n`{items[1][0]} {items[1][1]}`\n`{items[2][0]} {items[2][1]}`\n`{items[3][0]} {items[3][1]}`\n`{items[4][0]} {items[4][1]}`',color= ctx.author.color)
            await ctx.send(embed=emb)
        elif val == 6:
            emb=discord.Embed(title='Inventory', description=f'`{items[0][0]} {items[0][1]}`\n`{items[1][0]} {items[1][1]}`\n`{items[2][0]} {items[2][1]}`\n`{items[3][0]} {items[3][1]}`\n`{items[4][0]} {items[4][1]}`\n`{items[5][0]} {items[5][1]}`',color= ctx.author.color)
            await ctx.send(embed=emb)
        elif val == 7:
            emb=discord.Embed(title='Inventory', description=f'`{items[0][0]} {items[0][1]}`\n`{items[1][0]} {items[1][1]}`\n`{items[2][0]} {items[2][1]}`\n`{items[3][0]} {items[3][1]}`\n`{items[4][0]} {items[4][1]}`\n`{items[5][0]} {items[5][1]}`\n`{items[6][0]} {items[6][1]}`',color= ctx.author.color)
            await ctx.send(embed=emb)
        elif val == 8:
            emb=discord.Embed(title='Inventory', description=f'`{items[0][0]} {items[0][1]}`\n`{items[1][0]} {items[1][1]}`\n`{items[2][0]} {items[2][1]}`\n`{items[3][0]} {items[3][1]}`\n`{items[4][0]} {items[4][1]}`\n`{items[5][0]} {items[5][1]}`\n`{items[6][0]} {items[6][1]}`\n`{items[7][0]} {items[7][1]}`',color= ctx.author.color)
            await ctx.send(embed=emb)

@client.command(name='give')
async def give(ctx,target:Optional[Member],amount):
        if CheckID(ctx.message.author.id) != True:
            await ctx.send('You dont have `Valium` account')
            await ctx.send('type `create` to make one')
        elif CheckID(target.id) != True:
            await ctx.send('The user you mentioned dont have `Valium` account')
        else:
            amo = int(amount)
            user = ctx.message.author.id
            usercredit=Check(user,'credit')

            if user == 500762971165818910:
                Edit(target.id,'credit',True,amo)
                count="{:,}".format(amo)
                await ctx.send(f'GM sent `{count}` Cr.')
            else:
                if usercredit < amo:
                    await ctx.send('You dont have that much')
                elif amo == 0:
                    await ctx.send('`0` Credit?')
                else:
                    Edit(ctx.message.author.id,'credit',False,amo)
                    Edit(target.id,'credit',True,amo)
                    count="{:,}".format(amo)
                    await ctx.send(f'{ctx.author.display_name} sent `{count}` Cr.')

@client.command(name='dummy')
async def dummy(ctx):
    Player=CheckID(ctx.message.author.id)
    Str = Check(ctx.message.author.id,'str')
    Crit = Str * 2 - Str//2
    if Player == True:
        emb= discord.Embed(title='Dummy',description=f'```Record damage taken```')
        await ctx.send(ctx.author.mention,embed= emb,
                components=ActionRow(
                    [
                        Button(
                        style= ButtonStyle.green,
                        label='Hit'
                        ),
                        Button(
                        style= ButtonStyle.red,
                        label='Exit'
                        )
                    ]
                )
            )
        inter= await client.wait_for('button_click')
        if inter.component.label == 'Hit':
            await inter.respond(content= 'Player hit the Dummy')
            Run = True
            Dummy = 0
            while Run:
                Dmg = randint(Str,Crit)
                total=Dummy + Dmg
                Dummy = total
                emb1=discord.Embed(title='Dummy',description=f'```Total Damage : {total}```')
                emb1.add_field(name=ctx.author.display_name,value=f'```Damage Dealt >> {Dmg}```')
                emb1.add_field(name='Dummy',value=f'```Damage Dealt >> 0```')
                await ctx.send(embed=emb1,
                    components=ActionRow(
                        [
                            Button(
                            style= ButtonStyle.green,
                            label='Attack'
                            ),
                            Button(
                            style= ButtonStyle.red,
                            label='Exit'
                            )
                        ]
                    )
                )
                inter= await client.wait_for('button_click')
                if inter.component.label == 'Attack':
                    await inter.respond(content= 'Player use Attack')
                elif inter.component.label == 'Exit':
                    await inter.respond(content= 'Player Exited')
                    Run = False
        elif inter.component.label == 'Exit':
            await inter.respond(content= 'Player Exited')
    else:
        await ctx.send('You dont have `Valium` account')

@client.command(name= 'delete_user')
async def delete_account(ctx):
    if ctx.message.author.id == 500762971165818910:
        Run = True
        Com = ['cancel','Cancel']
        while Run:
            await ctx.send('Enter user ID\ntype `cancel` to close command')
            Read()
            msg = await client.wait_for('message',check=lambda message : message.author.id == 500762971165818910)
            def check():
                for i in Com:
                    if msg.content == i:
                        return i
            if msg.content == check():
                await ctx.send('Command canceled')
                Run = False
            else:
                try:
                    ID=(int(msg.content))
                    check = CheckID(ID)
                    if check != True:
                        await ctx.send('Player not found')
                        Read()
                    elif check == True:
                        delete(ID)
                        await ctx.send('Player account succesfully deleted')
                        await ctx.send('Command closed')
                        Read()
                        Run = False
                except ValueError:
                    await ctx.send('ID only contains number')
    else:
        await ctx.send('This command is only valid for GM')

@client.command()
async def hunt(ctx):
    Player = CheckID(ctx.message.author.id)
    if Player == True:
        id = ctx.message.author.id
        Health,hplimit,mplimit,Attack,Defence,Mp,Int= Check(id,'hp'),Check(id,'hplim'),Check(id,'mplim'),Check(id,'str'),Check(id,'def'),Check(id,'mp'),Check(id,'intel')
        class Players():
            def __init__(self,types,name,HP,HPLIM,STR,INT,DEF,MP,MPLIM):
                self.types = types
                self.name = name
                self.HP = HP
                self.HPLIM = HPLIM
                self.STR = STR
                self.INT = INT
                self.DEF = DEF
                self.MP = MP
                self.MPLIM = MPLIM
            
            def Attack(self):
                global Pdmg,Mdmg
                pdamage,string = Player.STR,str(Player.STR)
                randomize = [randint(0,2),randint(0,4),randint(0,20)]
                if len(string) == 1:
                    pdamage -= randomize[0]
                    Mob.HP -= pdamage
                    Pdmg = pdamage
                elif len(string) == 2:
                    pdamage -= randomize[1]
                    Mob.HP -= pdamage
                    Pdmg = pdamage
                elif len(string) == 3:
                    pdamage -= randomize[2]
                    Mob.HP -= pdamage
                    Pdmg = pdamage
                '''MOB'''
                mdamage,string = Mob.STR,str(Mob.STR)
                randomize = [randint(0,2),randint(0,4),randint(0,20)]
                if len(string) == 1:
                    mdamage -= randomize[0]
                    Player.HP -= mdamage
                    Mdmg = mdamage
                elif len(string) == 2:
                    mdamage -= randomize[1]
                    Player.HP -= mdamage
                    Mdmg = mdamage
                elif len(string) == 3:
                    mdamage -= randomize[2]
                    Player.HP -= mdamage
                    Mdmg = mdamage
                              
        '''Define'''
        
        Player = Players('Player',ctx.author.display_name,Health,hplimit,Attack,Int,Defence,Mp,mplimit)
        Goblin,Rat,Slime,Boar = Players('Mob','Goblin',30,30,10,0,1,10,10),Players('Mob','Rat',20,20,9,0,0,15,15),Players('Mob','Slime',50,50,5,0,2,15,15),Players('Mob','Boar',30,30,9,0,2,15,15)
        Choices = [Goblin,Rat,Slime,Boar]
        Prize = random.randint(100,300)
        Mob = random.choice(Choices)
        
        '''Start'''
        if Player.HP == 0:
            await ctx.send('Your HP is `0`')
        else:                       
            '''main loop'''
            emb = discord.Embed(title='Enemy Info',description='`type start to proceed or cancel to exit`',color=ctx.author.color)
            emb.add_field(name = 'Enemy',value= '```\nUndefined\n```',inline= False)
            emb.add_field(name = 'Stats',value= '```python\nHP (???/???) | DEF (Unknown) | STR (Unknown)\n```',inline= False)
            info = await ctx.send(ctx.author.mention,embed= emb)
            
            Start = True
            while Start:
                chat = await client.wait_for('message',check= lambda msg : msg.author == ctx.author)
                if chat.content == 'start':
                    await chat.delete()
                    embs = discord.Embed(title='Enemy Info',description='**Command**\n`atk` | `cast`',color=ctx.author.color)
                    embs.add_field(name = 'Enemy',value= f'```python\n{Mob.name}\n```',inline= False)
                    embs.add_field(name = 'Stats',value= f'```python\nHP({Mob.HP}/{Mob.HPLIM}) | DEF({Mob.DEF}) | STR({Mob.STR})```',inline= False)
                    await info.edit(embed=embs)
                    break
                elif chat.content == 'cancel':
                    await chat.delete()
                    await ctx.send('Player has cancelled the command')
                    Start = False
                else:
                    await chat.delete()
            if Start == True:
                Run = True
                while Run:
                    msg = await client.wait_for('message', check= lambda i : i.author == ctx.author)
                    if msg.content == 'atk':
                        Player.Attack()
                        if Mob.HP < 0:
                            Mob.HP = 0
                        elif Player.HP < 0:
                            Player.HP = 0
                        await msg.delete()
                        BattleLog= discord.Embed(title= 'Battle is ongoing',description= '**Command**\n`atk` | `cast`',color=ctx.author.color)
                        BattleLog.add_field(name= f'{Player.name}',value= f'```python\nHP({Player.HP}/{Player.HPLIM}) | MP({Player.MP}/{Player.MPLIM})```\n```Damage >> {Pdmg}```',inline= False)
                        BattleLog.add_field(name= f'{Mob.name}',value= f'```python\nHP({Mob.HP}/{Mob.HPLIM}) | MP({Mob.MP}/{Mob.MPLIM})```\n```Damage >> {Mdmg}```',inline= False)
                        await info.edit(ctx.author.mention,embed=BattleLog)
                        
                        if Mob.HP == 0:
                            embeds = discord.Embed(title= f'{Player.name} win the battle against {Mob.name} :tada:',description= f'{Player.name} got `{Prize}` Cr',color=ctx.author.color)
                            Edit(ctx.message.author.id,'credit',True,Prize)
                            Set(ctx.message.author.id,'hp',Player.HP)
                            await ctx.send(ctx.author.mention,embed=embeds)
                            Run = False
                        elif Player.HP == 0:
                            SetZero(ctx.message.author.id,'hp')
                            embeds = discord.Embed(title= f'{Player.name} killed by {Mob.name}',description= f'{Player.name} got nothing',color=ctx.author.color)
                            await ctx.send(ctx.author.mention,embed=embeds)
                            Run = False
                        else:
                            continue
                    elif msg.content == 'cast':
                        await msg.delete()
                        alert=await ctx.send('This command is not available yet')
                        await sleep(1)
                        await alert.delete()
                    else:
                        await msg.delete()              
    else:
        await ctx.send('You dont have `Valium` account')
        await ctx.send('Type `create` to make one')

@client.command()
async def edit(ctx,name,ToF,value):
    if ToF == 'False':
        Edit(ctx.message.author.id,name,False,int(value))
    elif ToF == 'True':
        Edit(ctx.message.author.id,name,True,int(value))
    await ctx.send('Stats Updated')
client.run(token)