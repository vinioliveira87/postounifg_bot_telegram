import telebot
from telebot import types

bot = telebot.TeleBot("1084492818:AAHu9cOrpH3P1zeHHugkKcOlMwqhCOK_ruo")

user_dict = {}

class User:
    def __init__(self, nome):
        self.nome = nome
        self.menu_id = None
        self.especialidade = None
        self.data = None
        self.hora = None
        self.cpf = None

@bot.message_handler(commands=['agendar', 'start', 'inicio'])
def send_welcome(message):
    msg = bot.reply_to(message, "Olá, somos do posto de saúde da UNIFG. Qual o seu nome?")
    bot.register_next_step_handler(msg, processo_menu)
	

def processo_menu(message):
    try:
        chat_id = message.chat.id
        name = message.text
        if name.isdigit():
            msg = bot.reply_to(message, 'Por favor informe o seu nome verdadeiro, qual o seu nome?')
            bot.register_next_step_handler(msg, processo_menu)
            return
        user = User(name)
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Marcar consulta')
        msg = bot.reply_to(message, "Olá "+message.text+", seja bem vindo. Digite a opção desejada: ", reply_markup=markup)
        bot.register_next_step_handler(msg, escolher_especialidade)
    except Exception as e:
        bot.reply_to(message, 'oooops! aconteceu algum erro.')

def escolher_especialidade(message):
    try:
        chat_id = message.chat.id
        menu_id = message.text
        user = user_dict[chat_id]
        user.menu_id = menu_id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Infectologista', 'dentista', 'Clinico geral')
        msg = bot.reply_to(message, 'Qual a especialidade? ', reply_markup=markup)
        bot.register_next_step_handler(msg, escolher_data)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def escolher_data(message):
    try:
        chat_id = message.chat.id
        especialidade = message.text
        user = user_dict[chat_id]
        user.especialidade = especialidade
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('12/06/2020', '19/06/2020', '26/06/2020')
        msg = bot.reply_to(message, 'Temos essas datas disponiveis, qual fica melhor para você? ', reply_markup=markup)
        bot.register_next_step_handler(msg, escolher_hora)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def escolher_hora(message):
    try:
        chat_id = message.chat.id
        data = message.text
        user = user_dict[chat_id]
        user.data = data
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('08:00', '10:00', '14:00', '16:00')
        msg = bot.reply_to(message, 'Qual melhor horario? ', reply_markup=markup)
        bot.register_next_step_handler(msg, digitar_cpf)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def digitar_cpf(message):
    try:
        chat_id = message.chat.id
        hora = message.text
        user = user_dict[chat_id]
        user.hora = hora
        msg = bot.reply_to(message, 'Para finalizarmos, digite o seu CPF sem caracter especial: ')
        bot.register_next_step_handler(msg, finalizar_agendamento)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def finalizar_agendamento(message):
    try:
        chat_id = message.chat.id
        cpf = message.text
        if not cpf.isdigit():
            msg = bot.reply_to(message, 'Por favor digite o seu cpf corretamente (somente números): ')
            bot.register_next_step_handler(msg, finalizar_agendamento)
            return
        user = user_dict[chat_id]
        user.cpf = cpf
        msg = bot.send_message(chat_id, "Obrigado! A sua consulta foi marcada para o dia "+user.data+" no horario "+user.hora+" para especialidade de "+user.especialidade + ".")
    except Exception as e:
        bot.reply_to(message, 'Aconteceu algum erro...')
        
bot.polling()
