from main import bot, dp

from aiogram.types import Message, InputMediaPhoto
from config import admin_id, channel_id

class Item(object):
    def __init__(self, descr, coun, sizeVer, price, chapter):
        self.descr = descr
        self.coun = coun
        self.sizeVer = sizeVer
        self.price = price
        self.chapter = chapter



class NewPost(object):
    def __init__(self, npic):
        self.nCapt1 = ""
        self.nPic = npic
        self.price = 0
        self.glinkT = ""
        self.GroupPic = []
        self.GroupPic.append(self.nPic)
        self.ItGroupMed = False
        self.grMed = list()
        self.endCapt = ""

    def ncap(self, n):
        self.nCapt1 = n

    def npic(self, np):
        self.GroupPic.append(np)
        self.ItGroupMed = True

    def nprice(self, p):
        self.price = p

    def genNLink(self):
        global MaxIndT
        self.glinkT = f"[Купить](http://t.me/MFBT1_bot?start={MaxIndT})"

    def genGrMed(self):
        self.genNLink()
        self.endCapt = self.nCapt1 + "\n" + "Цена: " + self.price + "\n" + self.glinkT
        if self.ItGroupMed:
            self.grMed.append(InputMediaPhoto(self.nPic, self.endCapt, 'MarkdownV2'))
            for i in range(1, len(self.GroupPic)):
                self.grMed.append(InputMediaPhoto(self.GroupPic[i]))


items = []
idchats = [admin_id]
a12341 = False
d21 = False
condNewPost = 0
MaxIndT = 10


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id[0], text="Бот запущен")


def newclientID(a):

    for numb in range(0, len(idchats)):
        if a == idchats[numb]:
            return
    idchats.append(a)


async def sendMFAIDC(textM):
    if len(idchats) == 0:
        return
    for numb in range(0, len(idchats)):
        await bot.send_message(chat_id=idchats[numb], text=textM)
        await bot.send_message(chat_id=admin_id[0], text=idchats[numb])

@dp.message_handler(content_types=['photo'])
async def pho_mess(message: Message):
    global condNewPost
    global Npost
    if condNewPost == 2:
        Npost.npic(message.photo[2].file_id)
    elif condNewPost == 1:
        Npost = NewPost(message.photo[2].file_id)
        condNewPost += 1
        await bot.send_message(chat_id=message.from_user.id, text="Теперь напишите описание нового товара")
    else:
        #await bot.send_media_group(chat_id=admin_id, media=message.photo)
        await bot.send_photo(chat_id=admin_id[0], photo=message.photo[2].file_id, caption=message.caption)


@dp.message_handler()
async def echo(message: Message):
    newclientID(message.from_user.id)
    global a12341
    global condNewPost
    global Npost
    global MaxIndT
    if message.from_user.id in admin_id:
        if message.text == "/help":
            await bot.send_message(chat_id=message.from_user.id,
                                   text="/NewPost - создать новый пост в тг канал"
                                        "\n/EndPost - закончить и опубликовать пост в тг канал"
                                        "\n/StopPost - отменить создание поста в тг канал")
        if message.text == "/StopPost":
            condNewPost = 0
        if condNewPost == 4:
            if message.text == "/EndPost":
                if Npost.ItGroupMed:
                    await bot.send_media_group(chat_id=channel_id,
                                               media=Npost.grMed)
                else:
                    await bot.send_photo(chat_id=channel_id,
                                         photo=Npost.nPic,
                                         caption=Npost.endCapt,
                                         parse_mode='MarkdownV2')
                MaxIndT += 1
                condNewPost = 0
        elif condNewPost == 3:
            Npost.nprice(message.text)
            condNewPost = 4
            Npost.genGrMed()
            if Npost.ItGroupMed:
                await bot.send_media_group(chat_id=message.from_user.id,
                                           media=Npost.grMed)
            else:
                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=Npost.nPic,
                                     caption=Npost.endCapt,
                                     parse_mode='MarkdownV2')
            await bot.send_message(chat_id=message.from_user.id,
                                   text="напишите /EndPost если хотите опубликовать пост и "
                                        "/StopPost если хотите отменить создание поста")
        elif condNewPost == 2:
            Npost.ncap(message.text)
            condNewPost = 3
            await bot.send_message(chat_id=message.from_user.id, text="напишите цену за товар")
        if message.text == "/NewPost":
            condNewPost = 1
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Отправьте изображения, которые будут демонстрировать товар"
                                        "(напишите /StopPost чтобы прервать создание поста или "
                                        "/EndPost чтобы закончить пост)")
        elif message.text == "/op.sendallEnd":
            a12341 = False
        elif a12341:
            for numb in range(0, len(idchats)):
                await bot.send_message(chat_id=idchats[numb], text=message.text)
                await bot.send_message(chat_id=admin_id[0], text=idchats[numb])
        if message.text == "/op.sendallStart":
            a12341 = True

    #await bot.send_message(chat_id=message.from_user.id, text=text)
    #await bot.send_photo(chat_id=admin_id, photo=message.photo[2].get_file(), caption="f")

    await bot.send_message(chat_id=admin_id[0],
                           text=f"Привет, пользователь {message.from_user.username} с id={message.from_user.id} "
                                f"и name={message.from_user.full_name} написал боту: {message.text}")