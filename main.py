import nextcord, json, re, httpx, certifi, datetime
from nextcord.ext import commands
import os
import json
import datetime
import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tontakoonz"
    )
except:
    print("Can't Connect To A Database.")
    exit()

with open('config.json', 'r', encoding='utf-8') as f:
    config_data = json.load(f)
USE_URL = config_data["USE_URL"]
bot = commands.Bot(command_prefix='mst!',help_command=None,intents=nextcord.Intents.all())
config = json.load(open('./config.json', 'r', encoding='utf-8'))

class shopView(nextcord.ui.View):

    def __init__(self, discord_id: dict, product_id: dict):
        super().__init__(timeout=None)
        self.discord_id = discord_id
        self.product_id = product_id

    @nextcord.ui.button(
        label='✅ Confirm',
        custom_id='already',
        style=nextcord.ButtonStyle.green,
        row=1
    )
    async def already(self, button: nextcord.Button, interaction: nextcord.Interaction):
        connection.connect()
        discord_id = self.discord_id
        product_id = self.product_id
        db_cursor = connection.cursor()
        db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (discord_id,))
        result = db_cursor.fetchall()
        if result:
            for data in result:
                db_cursorx = connection.cursor()
                db_cursorx.execute("SELECT * FROM product WHERE id = %s", (int(product_id),))
                resultx = db_cursorx.fetchall()
                for datax in resultx:
                    if data[2] >= datax[3]:
                        db_cursor.execute("SELECT * FROM stock WHERE product = %s AND sell_to IS NULL LIMIT 1", (datax[1],))
                        result = db_cursor.fetchall()
                        if result:
                            for dataz in result:
                                db_cursorc = connection.cursor()
                                db_cursorc.execute("UPDATE stock SET sell_to = %s, sell_date = CURRENT_TIMESTAMP() WHERE id = %s", (discord_id, dataz[0],))
                                db_cursorc.execute("UPDATE user SET point = point - %s WHERE discord_id = %s", (datax[3], discord_id,))
                                if data[4] == "Member":
                                    db_cursorc.execute("UPDATE user SET rank = 'Customer' WHERE discord_id = %s", (discord_id,))
                                connection.commit()
                                channelDM = await interaction.user.create_dm()
                                if (channelDM):
                                    embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'`🙏`  `|`   `Thanks You {interaction.user} For Buy Us Product :)`\n```\nProduct: {dataz[1]}\nID:{dataz[0]}\nPrice: {datax[3]}\nDescription: {datax[2]}\n```\n`👇` `|` `Your Product`\n```\n{dataz[2]}\n```', color=nextcord.Color.green())
                                    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                                    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                                    await channelDM.send(embed=embed)
                                embed = nextcord.Embed(title=f'Notify Product Buyed 🔔', description=f'`🕵️` `|` `Discord` : <@{discord_id}>\n```\nProduct: {dataz[1]}\nPrice: {datax[3]}\nCurrent Point: {int(data[2]) - int(datax[3])}\n```\n`👇` `|` `Product`\n```\n{dataz[2]}\n```', color=nextcord.Color.green())
                                embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                                embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                                await bot.get_channel(config['buysuccess']).send(embed=embed)
                                embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'`🙏`  `|`   `Thanks You {interaction.user} For Buy Us Product :)`\n```\nProduct: {dataz[1]}\nPrice: {datax[3]}\nDescription: {datax[2]}\n```\n`👇` `|` `Your Product`\n```\n{dataz[2]}\n```\n\n**[Click To View Bot Direct Message.](https://discord.com/channels/@me/1234516328660996096)**', color=nextcord.Color.green())
                                embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                                embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                                await interaction.response.edit_message(embed=embed, view=None)
                        else:
                            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nProduct Is Out Of Stock. Please Wait Administrator Restock.\n```', color=nextcord.Color.red())
                            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                            await interaction.response.edit_message(embed=embed, view=None)
                    else:
                        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nYour Point Is Not Enough To Buy Product.\nYour Need More {int(datax[3]) - int(data[2])} Point To Buy A {datax[1]}```', color=nextcord.Color.red())
                        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                        await interaction.response.edit_message(embed=embed, view=None)
        else:               
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nPlease Register An Account First!```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.response.edit_message(embed=embed, view=None)

    #     userJSON = json.load(open('./database/users.json', 'r', encoding='utf-8'))

    #     if (len(open(f'./{self.product_id}.txt', 'r', encoding='utf-8').readlines()) == 0):
    #         return await interaction.response.edit_message(embed=nextcord.Embed(description='สินค้าหมดโปรดรอเเอดมินเติม stock', color=nextcord.Color.red()), view=None)
    #     else:
    #         if (userJSON[str(interaction.user.id)]['point'] >= self.discord_id['price']):
    #             userJSON[str(interaction.user.id)]['point'] -= self.discord_id['price']
    #             userJSON[str(interaction.user.id)]['transaction'].append({
    #                 "payment": {
    #                     "product": self.discord_id['name'],
    #                     "time": str(datetime.datetime.now())
    #                 }
    #             })
    #             json.dump(userJSON, open('./database/users.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
            
    #             role = nextcord.utils.get(interaction.user.guild.roles, id = self.discord_id['roleId'])
    #             try:
    #                 await interaction.user.add_roles(role)
    #             except Exception as error:
    #                 print(f'FAIL TO ADD ROLE TO {interaction.user} - {str(error)}')
    #             topupLogEmbed = nextcord.Embed(
    #                 title='`ซื้อสินค้าสำเร็จโปรดเช็คกล่องข้อความ`',
    #                 description=f'''
    # `⌚` ผู้ใช้ `:` <@{interaction.user.id}>
    # `💸` ราคา `:` {self.discord_id['price']}
    # `📦` ทำการซื้อสินค้า `:` {self.discord_id['name']}
    # ''',
    #                 color=nextcord.Color.light_grey()
    #             )
    #             if (interaction.user.avatar):
    #                 topupLogEmbed.set_thumbnail(url=interaction.user.avatar.url)
    #             try:
    #                 await bot.get_channel(config['buysuccess']).send(embed=topupLogEmbed)
    #             except:
    #                 print('FAIL TO SEND MESSAGE TOPUP LOG')
    #             key = open(f"./{self.product_id}.txt", "r").read().split('\n', 1)[0]
    #             x = open(f"./{self.product_id}.txt", "r").readlines()
    #             f = open(f"./{self.product_id}.txt", "w")
    #             for line in x:
    #                 if line.strip("\n") != key:
    #                     f.write(line)
    #             channelDM = await interaction.user.create_dm()
    #             if (channelDM):
    #                 await channelDM.send(embed=nextcord.Embed(title=f"```🙏 : ขอบคุณสำหรับการสั่งซื้อสินค้าจาก VinxyShop ```", description=f"\n\n\n\u200b\n<@{interaction.user.id}>\n\nสินค้า : \n```{self.discord_id['name']}```\nราคา : \n```{self.discord_id['price']}```\nรายละเอียดสินค้า : \n```{key}```\n- [วิธีการเลือกซื้อสินค้า]({USE_URL})", color=nextcord.Color.light_grey()))
    #             success_embed = nextcord.Embed(description=f'```✅ : คุณสั่งซื้อสินค้าสำเร็จ ```\n```{key}```', color=nextcord.Color.light_grey())
    #             await interaction.response.edit_message(embed=success_embed, view=None)
    #             await bot.get_channel(int(config['logbuydm'])).send(embed=nextcord.Embed(
    #                         description=f'''`✅`  :  ซื้อสินค้าสำเร็จ\n\nผู้ใช้  :  <@{interaction.user.id}>\n\nสินค้าที่ซื้อ  :  {key}''',
    #                         color=nextcord.Color.from_rgb(255,0,0)))
    #         else:
    #             embed = nextcord.Embed(description=f'เงินของท่านไม่เพียงพอ ขาดอีก ({self.discord_id["price"] - userJSON[str(interaction.user.id)]["point"]}) บาท', color=nextcord.Color.red())
    #             await interaction.response.edit_message(embed=embed, view=None)

    @nextcord.ui.button(
        label='❌ Cancel',
        custom_id='cancel',
        style=nextcord.ButtonStyle.red,
        row=1
    )
    async def cancel(self, button: nextcord.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nSuccessfully Cancel To Buy A Product.\n```', color=nextcord.Color.red())
        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        await interaction.response.edit_message(embed=embed, ephemeral=True)
    
class registerView(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label='✅ Confirm',
        custom_id='confirm',
        style=nextcord.ButtonStyle.green,
        row=1
    )
    async def confirm(self, button: nextcord.Button, interaction: nextcord.Interaction):
        connection.connect()
        db_cursor = connection.cursor()
        db_cursor.execute("INSERT INTO user (discord_id, date) VALUES (%s, CURRENT_TIMESTAMP())", (interaction.user.id,))
        connection.commit()
        db_cursor.close()
        connection.close()
        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```Successfully Register An Account!```', color=nextcord.Color.green())
        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        await interaction.response.edit_message(embed=embed, view=None)

    @nextcord.ui.button(
        label='❌ Cancel',
        custom_id='cancel',
        style=nextcord.ButtonStyle.red,
        row=1
    )
    async def cancel(self, button: nextcord.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```Register Was Cancel```', color=nextcord.Color.red())
        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        await interaction.response.edit_message(embed=embed, view=None)

class shopSelect(nextcord.ui.Select):

    def __init__(self):
        options = []
        i = 0
        connection.connect()
        db_cursor = connection.cursor()
        db_cursor.execute("SELECT * FROM product")
        result = db_cursor.fetchall()
        if result:
            for data in result:
                db_cursorx = connection.cursor()
                db_cursorx.execute("SELECT COUNT(*) FROM stock WHERE product = %s AND sell_to IS NULL", (data[1],))
                resultx = db_cursorx.fetchall()
                for datax in resultx:
                    options.append(nextcord.SelectOption(
                        value=data[0],
                        label=data[1],
                        description=f'{data[2]} | Stocks: {datax[0]} | Price: {data[3]}',
                        emoji=data[4]
                    ))
                i += 1
        else:
            options.append(nextcord.SelectOption(
                value='999',
                label='Not Have Any Product :(',
                description='Please Wait Administrator. Add A Product',
                emoji='🙏'
            ))
        db_cursor.close()
        db_cursorx.close()
        connection.close()
        
        super().__init__(custom_id='shopSelect', placeholder='Select A Product Do Your Like To Buy 🎈', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        connection.connect()
        db_cursor = connection.cursor()
        db_cursor.execute("SELECT * FROM product WHERE id = %s", (self.values[0],))
        result = db_cursor.fetchall()
        if result:
            for data in result:
                db_cursorx = connection.cursor()
                db_cursorx.execute("SELECT * FROM stock WHERE product = %s AND sell_to IS NULL", (data[1],))
                resultx = db_cursorx.fetchall()
                if resultx:
                    if str(data[0]) == str(self.values[0]):
                        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nDo You Want To Buy {data[1]} For {data[3]} Point?```', color=nextcord.Color.green())
                        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                        await interaction.send(embed=embed, view=shopView(discord_id=interaction.user.id,product_id=self.values[0]), ephemeral=True)
                else:
                    embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nProduct Is Out Of Stock. Please Wait Administrator Restock A Product.```', color=nextcord.Color.red())
                    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                    await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nProduct Is Not Found.```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.send(embed=embed, ephemeral=True)
        db_cursorx.close()
        db_cursor.close()
        connection.close()

class topupModal(nextcord.ui.Modal):

    def __init__(self):
        super().__init__(title='Topup With Truewallet Gift', timeout=None, custom_id='topup-modal')
        self.link = nextcord.ui.TextInput(
            label = 'Truewallet Gift',
            placeholder = 'https://gift.truemoney.com/campaign/?v=xxxxxxxxxxxxxxx',
            style = nextcord.TextInputStyle.short,
            required = True
        )
        self.add_item(self.link)

    async def callback(self, interaction: nextcord.Interaction):
        link = str(self.link.value).replace(' ', '')
        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nChecking...```', color=nextcord.Color.yellow())
        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        message = await interaction.response.send_message(embed=embed, ephemeral=True)
        if re.match(r'https:\/\/gift\.truemoney\.com\/campaign\/\?v=+[a-zA-Z0-9]{18}', link):
            voucher_hash = link.split('?v=')[1]
            response = httpx.post(
                url = f'https://gift.truemoney.com/campaign/vouchers/{voucher_hash}/redeem',
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/8a0.0.3987.149 Safari/537.36'
                },
                json = {
                    'mobile': config['phoneNumber'],
                    'voucher_hash': f'{voucher_hash}'
                },
                verify=certifi.where(),
            )
            if (response.status_code == 200 and response.json()['status']['code'] == 'SUCCESS'):
                data = response.json()
                amount = int(float(data['data']['my_ticket']['amount_baht']))
                connection.connect()
                db_cursor = connection.cursor()
                db_cursor.execute("UPDATE user SET point = point + %s WHERE discord_id = %s", (amount,interaction.user.id,))
                db_cursor.execute("UPDATE user SET rank = 'Customer' WHERE discord_id = %s", (interaction.user.id,))
                db_cursor.execute("INSERT INTO topup_history (discord_id, ref, method, amount, date) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP())", (interaction.user.id, link, "TrueWallet", amount,))
                connection.commit()
                embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nTopup Successfully\nUser: {interaction.user}\nDiscord ID: {interaction.user.id}\nGateway: TrueWallet\nRef.: {link}\nAmount: {amount}```', color=nextcord.Color.green())
                embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                db_cursor.execute("SELECT point FROM user WHERE discord_id = %s", (interaction.user.id,))
                result = db_cursor.fetchall()
                for data in result:
                    current = data[0]
                embedx = nextcord.Embed(title=f'Notify Point Has Been Topup 🔔', description=f'`🕵️` `|` `Discord User` : <@{interaction.user.id}>\n```\nTopup Point: {amount}\nRemaining Point: {current}\n```', color=nextcord.Color.green())
                embedx.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                embedx.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                await bot.get_channel(config['logtopups']).send(embed=embedx)
            else:
                embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nTopup Not Successfully. Please Try Again.\n```', color=nextcord.Color.red())
                embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        else:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nLink Pattern Is Not Correct. Please Try Again.\n```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        await message.edit(embed=embed)

class shopsView(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(shopSelect())

class menuView(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        # self.add_item(shopSelect())
    
    @nextcord.ui.button(
        label='🕵️ Account',
        custom_id='account',
        # emoji="", # ผมไม่ได้เพิ่ม emoji ตามที่ต้องการไปให้ ถ้าจะเพิ่มสามารถเพิ่มได้ตรงนี้
        style=nextcord.ButtonStyle.primary,
        row=1
    )

    async def account(self, button: nextcord.Button, interaction: nextcord.Interaction):
        connection.connect()
        db_cursor = connection.cursor()
        db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (interaction.user.id,))
        result = db_cursor.fetchall()
        if result:
            for data in result:
                if (data[6] == None):
                    update_date = 'Not Found.'
                else:
                    update_date = data[6]
                embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nUsername: {interaction.user}\nDiscord ID: {interaction.user.id}\nRank: {data[4]}\nPoint: {data[2]}\nTotal Topup: {data[3]}\nLast Update Data: {update_date}```', color=nextcord.Color.green())
                embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nPlease Register An Account First!```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.send(embed=embed, ephemeral=True)
        db_cursor.close()
        connection.close()

    @nextcord.ui.button(
        label='🏦 Topup',
        custom_id='topup',
        #emoji="", # ผมไม่ได้เพิ่ม emoji ตามที่ต้องการไปให้ ถ้าจะเพิ่มสามารถเพิ่มได้ตรงนี้
        style=nextcord.ButtonStyle.green,
        row=1
    )

    async def topup(self, button: nextcord.Button, interaction: nextcord.Interaction):
        connection.connect()
        db_cursor = connection.cursor()
        db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (interaction.user.id,))
        result = db_cursor.fetchall()
        if result:
            await interaction.response.send_modal(topupModal())
        else:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nPlease Register An Account First!```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.send(embed=embed, ephemeral=True)
        db_cursor.close()
        connection.close()


    @nextcord.ui.button(
        label='🧺 Product',
        custom_id='product',
        # emoji="", # ผมไม่ได้เพิ่ม emoji ตามที่ต้องการไปให้ ถ้าจะเพิ่มสามารถเพิ่มได้ตรงนี้
        style=nextcord.ButtonStyle.gray,
        row=1
    )

    async def product(self, button: nextcord.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed()
        embed.set_author(name=f"{config['header']}",)
        embed.description = f'''\n`🛒`  `|`   `Shop System By Tontakooon`
\n`🚨`  `|`  `In Alpha And Testing`\n
\n```diff
+ If Your Have Any Problem Open A Ticket For Support
+ Select A Product Below And Topup To Buy A Product :)
```'''
        embed.set_image(url='https://storage.ko-fi.com/cdn/useruploads/post/330f80a5-28d4-4807-8d08-e54e2bdcb7b9_bluecityrevisitedclean.gif')
        embed.color = nextcord.Color.dark_gold()
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        await interaction.send(embed=embed, ephemeral=True, view=shopsView())


    @nextcord.ui.button(
        label='📖 History',
        custom_id='history',
        #emoji="", # ผมไม่ได้เพิ่ม emoji ตามที่ต้องการไปให้ ถ้าจะเพิ่มสามารถเพิ่มได้ตรงนี้
        style=nextcord.ButtonStyle.gray,
        row=1
    )

    async def history(self, button: nextcord.Button, interaction: nextcord.Interaction):
        connection.connect()
        db_cursor = connection.cursor()
        db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (interaction.user.id,))
        result = db_cursor.fetchall()
        if result:
            db_cursor.execute("SELECT * FROM topup_history WHERE discord_id = %s ORDER BY id DESC LIMIT 1", (interaction.user.id,))
            result = db_cursor.fetchall()
            if result:
                for data in result:
                    history = f"\nAmount: {data[4]}\nRef: {data[2]}\nTopup By: {data[3]}\nDate: {data[5]}\n----------"
                embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nLast Topup History\n----------{history}\n```', color=nextcord.Color.green())
                embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                await interaction.send(embed=embed, ephemeral=True)
            else:
                embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nYour Not Have Any Topup History.```', color=nextcord.Color.red())
                embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
                embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
                await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nPlease Register An Account First!```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.send(embed=embed, ephemeral=True)

    @nextcord.ui.button(
        label='📃 Register',
        custom_id='register',
        #emoji="", # ผมไม่ได้เพิ่ม emoji ตามที่ต้องการไปให้ ถ้าจะเพิ่มสามารถเพิ่มได้ตรงนี้
        style=nextcord.ButtonStyle.grey,
        row=1
    )

    async def register(self, button: nextcord.Button, interaction: nextcord.Interaction):
        connection.connect()
        db_cursor = connection.cursor()
        db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (interaction.user.id,))
        result = db_cursor.fetchall()
        if not result:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nWant To Register Account With Us?\nPlease Read Agreement First Before Register👇\n```', color=nextcord.Color.green())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.send(embed=embed, view=registerView(), ephemeral=True)
        else:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nYour Have Already Register An Account!\n```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.send(embed=embed, ephemeral=True)
        db_cursor.close()
        connection.close()

@bot.event
async def on_ready():
    bot.add_view(menuView())
    bot.add_view(registerView())
    os.system('cls')
    stream_name = config['STREAM_NAME']
    print(f"Logged in as: {bot.user}")
    await bot.change_presence(
        activity=nextcord.Streaming(name=stream_name, url="https://www.twitch.tv/sxnax545"))

class AddStock(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("เพิ่มสินค้า")
        self.product_id = nextcord.ui.TextInput(
            label="สินค้า",
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.key = nextcord.ui.TextInput(
            label="ข้อมูลสินค้า",
            required=True,
            style=nextcord.TextInputStyle.paragraph
        )
        self.add_item(self.product_id)
        self.add_item(self.key)
    async def callback(self, interaction: nextcord.Interaction):
        f = open(f'./{self.product_id.value}.txt','a')
        key = self.key.value
        if key in open(f'./{self.product_id.value}.txt','r').read():
            await interaction.response.send_message(embed=nextcord.Embed(description=f"มีสินค้า ```{key}``` อยู่ใน database แล้ว!",color=0xff0000),ephemeral=True)
        else:
            if len(open(f'./{self.product_id.value}.txt','r').readlines()) == 0:
                f.write(key)
                await interaction.response.send_message(embed=nextcord.Embed(description=f"เขียนสินค้า ```{key}``` ลง database แล้ว!",color=0x00ff00),ephemeral=True)
            else:
                f.write('\n')
                f.write(key)
                await interaction.response.send_message(embed=nextcord.Embed(description=f"เขียนสินค้า ```{key}``` ลง database แล้ว!",color=0x00ff00),ephemeral=True)

class RemoveStock(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Delete Stock Menu")
        self.product_name = nextcord.ui.TextInput(
            label="Product",
            required=True,
            style=nextcord.TextInputStyle.short
        )
        self.stock_id = nextcord.ui.TextInput(
            label="Stock ID",
            required=True,
            style=nextcord.TextInputStyle.paragraph
        )
        self.add_item(self.product_name)
        self.add_item(self.stock_id)
    async def callback(self, interaction: nextcord.Interaction):
        product_name = self.product_name.value
        stock_id = self.stock_id.value
        connection.connect()
        db_cursor = connection.cursor()
        db_cursor.execute("SELECT * FROM product WHERE product = %s", (product_name,))
        result = db_cursor.fetchall()
        if result:
            print()
        else:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nProduct Not Found!\n```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.send(embed=embed, ephemeral=True)

@bot.slash_command(
        name='addstock',
        description='📍︱Add Stock︱ Only Administrator',
        guild_ids=[config['serverId']]
)

async def addStock(interaction: nextcord.Interaction):
    if (interaction.user.id not in config['ownerIds'] or not interaction.permissions.administrator):
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nNot Allow.```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            return await interaction.send(embed=embed, ephemeral=True)
    await interaction.response.send_modal(AddStock())

@bot.slash_command(
        name='removestock',
        description='📍︱Delete Stock︱Only Administrator',
        guild_ids=[config['serverId']]
)

async def removeStock(interaction: nextcord.Interaction):
    if (interaction.user.id not in config['ownerIds'] or not interaction.permissions.administrator):
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nNot Allow.```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            return await interaction.send(embed=embed, ephemeral=True)
    await interaction.response.send_modal(RemoveStock())

@bot.slash_command(
        name='addpoint',
        description='📍︱Add Point For Member︱Only Administrator',
        guild_ids=[config['serverId']]
)

async def addpoint(interaction: nextcord.Interaction, member: nextcord.Member, amount: int):
    if (interaction.user.id not in config['ownerIds'] or not interaction.permissions.administrator):
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nNot Allow.```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            return await interaction.send(embed=embed, ephemeral=True)
    discord_id = str(member.id)
    interaction_name = str(interaction.user)
    connection.connect()
    db_cursor = connection.cursor()
    db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (discord_id,))
    result = db_cursor.fetchall()
    if result:
        db_cursor.execute("UPDATE user SET point = point + %s, total = total + %s WHERE discord_id = %s", (amount, amount, discord_id,))
        db_cursor.execute("INSERT INTO topup_history (discord_id, ref, method, amount, date) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP())", (discord_id, interaction_name, "Administrator", amount,))
        connection.commit()
    else:
        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nUser Is Not Register An Account.```', color=nextcord.Color.red())
        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        return await interaction.send(embed=embed, ephemeral=True)
    db_cursor.execute("SELECT point FROM user WHERE discord_id = %s", (discord_id,))
    result = db_cursor.fetchall()
    for data in result:
        current = data[0]
    embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nSuccessfully Added A Point\nUsername: {member.name}\nDiscord ID: {discord_id}\nAdded Point: {amount}\nRemaining Point: {current}\n```', color=nextcord.Color.green())
    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
    await interaction.send(embed=embed, ephemeral=True)
    embed = nextcord.Embed(title=f'Notify Point Has Been Added By Admin 🔔', description=f'`🕵️` `|` `Discord Admin` : <@{interaction.user.id}> | `Discord User` : <@{discord_id}>\n```\nAdded Point: {amount}\nRemaining Point: {current}\n```', color=nextcord.Color.green())
    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
    await bot.get_channel(config['buysuccess']).send(embed=embed)
    db_cursor.close()
    connection.close()

@bot.slash_command(
        name='removepoint',
        description='📍︱Remove Point From Member︱ Only Administrator',
        guild_ids=[config['serverId']]
)

async def removepoint(interaction: nextcord.Interaction, member: nextcord.Member, amount: int):
    if (interaction.user.id not in config['ownerIds'] or not interaction.permissions.administrator):
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nNot Allow.```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            return await interaction.send(embed=embed, ephemeral=True)
    discord_id = str(member.id)
    connection.connect()
    db_cursor = connection.cursor()
    db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (discord_id,))
    result = db_cursor.fetchall()
    if result:
        if result[2] >= amount:
            db_cursor.execute("UPDATE user SET point = point - %s WHERE discord_id = %s", (amount, discord_id,))
            connection.commit()
        else:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nInvaild Amount. Please Input A Correct Amount\n```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            return await interaction.send(embed=embed, ephemeral=True)
    else:
        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nUser Is Not Register An Account.\n```', color=nextcord.Color.red())
        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        db_cursor.close()
        connection.close()
        return await interaction.send(embed=embed, ephemeral=True)
    db_cursor.execute("SELECT point FROM user WHERE discord_id = %s", (discord_id,))
    result = db_cursor.fetchall()
    for data in result:
        current = data[0]
    embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nSuccessfully Remove A Point\nUsername: {member.name}\nDiscord ID: {discord_id}\nRemoved Point: {amount}\nRemaining Point: {current}\n```', color=nextcord.Color.green())
    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
    await interaction.send(embed=embed, ephemeral=True)
    embed = nextcord.Embed(title=f'Notify Point Has Been Removed By Admin 🔔', description=f'`🕵️` `|` `Discord Admin` : <@{interaction.user.id}> | `Discord User` : <@{discord_id}>\n```\nRemoved Point: {amount}\nRemaining Point: {current}\n```', color=nextcord.Color.green())
    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
    await bot.get_channel(config['buysuccess']).send(embed=embed)
    db_cursor.close()
    connection.close()

@bot.slash_command(
        name='deleteuser',
        description='📍︱Remove Point From Member︱ Only Administrator',
        guild_ids=[config['serverId']]
)

async def deleteuser(interaction: nextcord.Interaction, member: nextcord.Member):
    if (interaction.user.id not in config['ownerIds'] or not interaction.permissions.administrator):
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nNot Allow.\n```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            return await interaction.send(embed=embed, ephemeral=True)
    connection.connect()
    db_cursor = connection.cursor()
    db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (str(member.id),))
    result = db_cursor.fetchall()
    if result:
        db_cursor.execute("DELETE FROM user WHERE discord_id = %s", (str(member.id),))
        connection.commit()
    else:
        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nUser Is Not Register.\n```', color=nextcord.Color.red())
        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        return await interaction.send(embed=embed, ephemeral=True)
    embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nSuccessfully Deleted User\nUsername: {member.name}\nDiscord ID: {member.id}\n```', color=nextcord.Color.green())
    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
    await interaction.send(embed=embed, ephemeral=True)
    embed = nextcord.Embed(title=f'Notify User Has Been Deleted By Admin 🔔', description=f'`🕵️` `|` `Discord Admin` : <@{interaction.user.id}> | `Discord User` : <@{member.id}>\n```\nDiscord ID: {member.id}\n```', color=nextcord.Color.green())
    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
    await bot.get_channel(config['buysuccess']).send(embed=embed)


@bot.slash_command(
        name='info',
        description='📍︱Get User Info︱ Only Administrator',
        guild_ids=[config['serverId']]
)

async def info(interaction: nextcord.Interaction, member: nextcord.Member):
    if (interaction.user.id not in config['ownerIds'] or not interaction.permissions.administrator):
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nNot Allow.```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            return await interaction.send(embed=embed, ephemeral=True)
    connection.connect()
    db_cursor = connection.cursor()
    db_cursor.execute("SELECT * FROM user WHERE discord_id = %s", (interaction.user.id,))
    result = db_cursor.fetchall()
    if result:
        for data in result:
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'`🕵️`  `|`   `User` `:` <@{member.id}>\n```\nDiscord ID: {member.id}\nPoint: {data[2]}\nTotal Topup: {data[3]}\nRanks: {data[4]}\nLast Update Data: {data[5]}\n```', color=nextcord.Color.green())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            await interaction.send(embed=embed, ephemeral=True)
    else:
        embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nUser Is Not Register An Account.\n```', color=nextcord.Color.red())
        embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
        embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
        await interaction.send(embed=embed, ephemeral=True)
    db_cursor.close()
    connection.close()

@bot.slash_command(   # ระบบบอทขายสินค้าในดิสคอร์ด
        name='setup',
        description='📍︱Setup System︱ Only Administrator',
        guild_ids=[config['serverId']]
)

async def setup(interaction: nextcord.Interaction):
    if (interaction.user.id not in config['ownerIds'] or not interaction.permissions.administrator):
            embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nNot Allow.```', color=nextcord.Color.red())
            embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
            embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
            return await interaction.send(embed=embed, ephemeral=True)
    embed = nextcord.Embed()
    embed.set_author(name=f"{config['header']}",)
    embed.description = f'''\n`🛒`  `|`   `Shop System By Tontakooon`
\n`🚨`  `|`  `In Alpha And Testing`\n```css
[ TEST MESSAGE ]

```\n> **[How To Buy?]({USE_URL})**\n\n```diff
+ If Your Have Any Problem Open A Ticket For Support
```'''
    embed.set_image(url=config['image_shop'])
    embed.color = nextcord.Color.light_grey()
    
    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
    
    await interaction.channel.send(embed=embed, view=menuView())
    embed = nextcord.Embed(title=f'`{interaction.user}` 🕵️', description=f'```\nSuccessfully Created A Pannel. Lets Start Making A Money :)```', color=nextcord.Color.green())
    embed.set_image(url='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmY3bW1ua3lodHNhM2dhd2xtdGNveGhyM2hkaW10YnhzYmhhb2FiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xm4uYTatdDtbmCsBCw/giphy.gif')
    embed.set_footer(text=config['footer'], icon_url=config['footer_icon'])
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(config['token'])