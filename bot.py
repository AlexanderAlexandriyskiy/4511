from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from rw import read_json , write_json

bot = TeleBot("6433151053:AAHhKogF7nY_9FX4KnIr1bE7wHtmxccrY00")
locations = read_json("locations.json")
players = read_json()

@bot.message_handler(commands = ["start"])
def start(message):
    id = message.from_user.id
    new_player(id)
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*["/help","/play"])
    bot.send_message(id,"Здравствуйте!  Желаете запустить воспоминание #4511?", reply_markup=menu_keyboard)

@bot.message_handler(commands = ["help"])
def help(message):
    id = message.from_user.id
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add("/play")
    bot.send_message(id ,"Воспоминание #4511 посвящено катастрофе 2349 года на космическом корабле 'Asteryx'.  Желаете запустить воспоминание #4511?", reply_markup=menu_keyboard)

@bot.message_handler(commands = ["play"])
def play(message):
    id = message.from_user.id
    new_player(id)
    write_json(players)
    info(id)

@bot.message_handler(func=lambda message: True)
def engine(message):
    id = message.from_user.id
    global players, locations, new_location
    try:
        new_location = locations[players[id]]["actions"][message.text]
        players[id] = new_location
        write_json(players)
        info(id)
    except:
        pass

def new_player(id):
    global players
    players[id] = "Капитанский мостик"
    write_json(players)

def info(id):
    global players, locations, new_location
    dsc = locations[players[id]]["description"]
    img = open(locations[players[id]]["image"], "rb")
    if players[id] == "Отсек со спасательными капсулаими" or players[id] == "Взрыв отсека" or players[id] == "Разгерметизация отсека":
        bot.send_photo(id, photo=img, caption=dsc)
        menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        menu_keyboard.add("/play")
        bot.send_message(id, "Воспоминание воспроизведено.  Желаете повторить воспроизведение?",reply_markup=menu_keyboard)
    else:
        act = list(locations[players[id]]["actions"].keys())
        menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        menu_keyboard.add(*act)
        bot.send_photo(id, photo=img, caption=dsc, reply_markup=menu_keyboard)

bot.polling()