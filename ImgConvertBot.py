from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup as Markup
from ImgConvertBotUtils import messages, keyboards, convert_file
import pyromod
import asyncio
import os

async def get_reply(message, ask_message, reply_markup=False, return_raw=False, photo=False):
    if reply_markup != False:
        answer = await message.chat.ask(f"{ask_message}", reply_markup=reply_markup)
    else:
        answer = await message.chat.ask(f"{ask_message}")
           
    if photo:
        while answer.photo == None:
           answer = await message.chat.ask(f"this is not a vaild photo!, send a vaild photo")
           if answer.text != None:
               if answer.text == "/start" or answer.from_user.is_self:
                   return False
        else:
            return answer
            
            
    if return_raw:
        return answer
           
    return answer.text



API_ID = 0
API_HASH = ""
TOKEN = ""

bot = Client("ImgConvertBot", API_ID,API_HASH, bot_token=TOKEN)

@bot.on_message(filters.private)
async def main(bot, message):
    chat_id = message.chat.id
    text = message.text
    
    if text == "/start":
        await bot.send_message(chat_id, messages["startup_message"].format(message.from_user.first_name), reply_markup=Markup(keyboards["main"]))

    elif text == "/kill":
        exit()
        
        
@bot.on_callback_query()
async def handy(bot, CallBack):
    data = CallBack.data
    message = CallBack.message
    chat_id = message.chat.id


    if data == "conv":
        sent_photo = await get_reply(message, "Send your Photo!", photo=True)
        if sent_photo:
            print(sent_photo)
            await bot.send_message(chat_id, "Converting...")
            photo_path = await sent_photo.download()
            extension = photo_path[-3:]
            if extension == "jpg":
                new_file = convert_file(photo_path, "png")
                try:
                    os.remove(photo_path)                  
                    await bot.send_photo(chat_id, photo=new_file)
                    await bot.send_document(chat_id, document=new_file)
                    await bot.send_message(chat_id, "Done!", reply_markup=Markup(keyboards["back"]))                    
                    os.remove(new_file)
                except Exception as e:
                    print(e)
                    await bot.send_message(chat_id, "An Unknown Error has occurred!")
                
            elif extension == "png":
                new_file = convert_file(photo_path, "jpg")
                try:
                    os.remove(photo_path)
                    await bot.send_photo(chat_id, photo=new_file)
                    await bot.send_document(chat_id, document=new_file)
                    await bot.send_message(chat_id, "Done!", reply_markup=Markup(keyboards["back"]))
                    os.remove(new_file)
                except Exception as e:
                    print(e)
                    await bot.send_message(chat_id, "An Unknown Error has occurred!")     
                              
            else:
               await bot.send_message(chat_id, "unsported format!", reply_markup=Markup(keyboards["back"]))


    elif data == "back":
        await bot.send_message(chat_id, messages["startup_message"].format(message.from_user.first_name), reply_markup=Markup(keyboards["main"]))

            
            
            
            
            
            
asyncio.run(bot.run())            