from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.text import LabelBase
Window.size= (350, 550)

from chatbot import get_answer_for_mistake, load_knowledge_base
from chatbot import save_knowledge_base
from chatbot import find_best_match
from chatbot import get_answer_for_question


class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins-SemiBold.ttf"
    font_size = 17

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins-SemiBold.ttf"
    font_size = 17



class ChatBot(MDApp):
    
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    learn_response= False
    learn= False
    new_question = ''    

    def change_screen(self, name):
        screen_manager.curent = name

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("Chats.kv"))
        return screen_manager
    
    def bot_name(self):
        if screen_manager.get_screen('main').bot_name.text != "":
            screen_manager.get_screen('chats').bot_name.text = screen_manager.get_screen('main').bot_name.text
            screen_manager.current = "chats"

    def response(self, *args):
        question= ""
        response= ""
        best_match: str | None = find_best_match(value, [q["question"] for q in self.knowledge_base["question"]])

        if any(ban["ban"] in value.lower() for ban in self.knowledge_base["ban"]):
            response = "Lo siento, no puedo responder a esa pregunta."
            return response
        if self.learn:
            # value
            # Imprimir aprendí algo nuevo
            print('=============')
            question =self.new_question
            print(question)
            print(value)
            self.learn = False
            response = self.learn_answer()

            
        else: 
            if value.lower() == 'salir':
                response = "Adios! Que tengas un gran día"

            if best_match:
                mistake_answer = get_answer_for_mistake(value, self.knowledge_base)
                response = mistake_answer if mistake_answer else get_answer_for_question(best_match, self.knowledge_base)
            else:
                response = f"No sé la respuesta. ¿Puede enseñármela?\nSolamente debes de digitar la respuesta debajo {screen_manager.get_screen('chats').text_input.text}"
                self.learn = True
                self.new_question = value

        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x=.75))

    def send(self):
        global size, halign, value
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
            
            if value.lower() == 'salir':
                response = "Adios! Que tengas un gran dia"

            if len(value) < 6:
                size = .22
                halign = "center"
            elif len(value) < 11:
                size = .32
                halign = "center"
            elif len(value) < 16:
                size = .45
                halign = "center"
            elif len(value) < 21:
                size = .58
                halign = "center"
            elif len(value) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

        

        screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x=size,halign=halign))
        Clock.schedule_once(self.response, 2)
        screen_manager.get_screen('chats').text_input.text = ""

    def learn_answer(self):
        question = self.new_question
        response = ''
        if value.lower() != 'omitir':
            self.knowledge_base["question"].append({"question": question, "answer": value})
            save_knowledge_base('knowledge_base.json', self.knowledge_base)
            response = '¡Gracias! ¡He aprendido algo nuevo!'
        
        return response

    
if __name__ == '__main__':
    ChatBot().run()