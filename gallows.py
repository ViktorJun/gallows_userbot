from pyrogram import filters, Client
from pyrogram.errors import MessageEmpty
from time import sleep

api_id = your_api_id
api_hash = "your_api_hash"

app = Client("my_acc", api_id, api_hash)

# gallows
@app.on_message(filters.command("start gallows", prefixes=""))
def start_vs(_, msg):
    msg.reply_text(f'If you are playing for the first time, then read the rules of the game by writing "rules of the gallows"'
                   f'\nThe game has begun, enter the word')

    @app.on_message(filters.command("word", prefixes=""))
    def word(_, msg):
        global encoded_word, word, tries, booll
        tries = 5
        booll = True
        msg.text = msg.text.lower()
        msg.delete(msg)
        word = msg.text.split('word ', maxsplit=1)[1]
        encoded_word = []
        for j in word:
            encoded_word.append("#")
        msg.reply_text(f'Word: {len(word) * "#"}\nEnter a letter')

        @app.on_message(filters.command("letter", prefixes=""))
        def letter(_, msg):
            global encoded_word, word, tries, booll
            if booll:
                msg.text = msg.text.lower()
                letter = msg.text.split('letter ', maxsplit=1)[1]
                final_encoded = ''
                if len(letter) != 1:
                    msg.reply_text(f'You entered the wrong number of letters:)\nTry again!')
                else:
                    if letter in word:
                        msg.reply_text(f'Letter "{letter}" found.')
                    else:
                        tries -= 1
                        msg.reply_text(f'Letter "{letter}" not found\nRemaining tries: {tries}')
                    if tries <= 0:
                        msg.reply_text(f'You spent all your tries:(\nWord: {word}')
                        booll = False
                    else:
                        for j in range(len(word)):
                            if word[j] == letter:
                                encoded_word[j] = letter
                            final_encoded += encoded_word[j]
                        if word != final_encoded:
                            msg.reply_text(f'Word: {final_encoded}\nEnter a letter')
                        else:
                            msg.reply_text(f'Congratulations you won!\nWord: {word}')
                            booll = False

    @app.on_message(filters.command("answer", prefixes=""))
    def answer(_, msg):
        global booll, word
        if booll:
            msg.text = msg.text.lower()
            answer = msg.text.split('answer ', maxsplit=1)[1]
            if len(answer) != len(word):
                msg.reply_text(f'Incorrect number of letters, look carefully:)')
            elif answer == word:
                msg.reply_text(f'Word and truth {word}!\nCongratulations! You won!')
                booll = False
            else:
                msg.reply_text(f'Unfortunately, you guessed it wrong :( This happens, don\'t be upset:)\nСлово: {word}')
                booll = False

    @app.on_message(filters.command("gallows rules", prefixes=""))
    def game_rules(_, msg):
        msg.reply_text(
            f'Rules of the game:\nTo guess a word, enter "word <your word>"'
            f'\nIf you are sure of the word then write "answer <your word>"'
            f'\nTo guess by letter, enter "letter <your letter>"'
            f'\nYou can be wrong 5 times. Good luck!')


l1st = []
@app.on_message(filters.command("word", prefixes="."))
def word(_, msg):
    global l1st
    msg.text = msg.text.lower()
    word2 = msg.text.split('.word ', maxsplit=1)[1]
    l1st.append(word2)
    res = ''
    if len(l1st) < 2:
        msg.reply_text(f'First word written! Enter the second word')
    elif len(l1st) == 2:
        for j in l1st[0]:
            if j in l1st[1]:
                if j not in res:
                    res += j
        if not res:
            msg.reply_text(f'No common letters')
        else:
            msg.reply_text(f'Common letters: {res}')
            l1st.clear()


app.run()