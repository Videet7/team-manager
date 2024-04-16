from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import random

class WelcomeOptions(Screen):
    def __init__(self, **kwargs):
        super(WelcomeOptions, self).__init__(**kwargs)
        self.name = "welcomeoptions"
        self.layout = "layout_welcomeoptions"

        main_layout = BoxLayout(orientation="vertical")
       
        label = Label(text='Welcome To Team Manager',
                        size_hint=(9, 9),
                        pos_hint={'center_x': .5, 'center_y': .5})  

        button_1 = Button(text='Team Formation',
                        pos_hint={'center_x': .5, 'center_y': .5})
        button_1.bind(on_press=self.button_1)

        button_2 = Button(text='Team Manager',
                        pos_hint={'center_x': .5, 'center_y': .5})
        button_2.bind(on_press=self.button_2)

        button_3 = Button(text='Game Manager',
                        pos_hint={'center_x': .5, 'center_y': .5})
        button_3.bind(on_press=self.button_2)

        for fun in [label, button_1, button_2, button_3]:
            main_layout.add_widget(fun)
        self.add_widget(main_layout)
    
    def button_1(self, button_2):
        self.manager.current = "teamformation"
        self.manager.transition.direction = "up"

    def button_2(self, button_2):
        self.manager.current = "comingsoon"
        self.manager.transition.direction = "up" 

class TeamFormation(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'teamformation'
        self.layout = "layout_teamformation"

 
        box1 = BoxLayout(orientation ='vertical')
        label = Label(text="Enter the names of Players",pos_hint={'center_x': .5, 'center_y': .5},halign="center" ,size_hint=(2, 2))
        self.text_input = TextInput(multiline=False)

        label_1 = Label(text="Enter the number of Teams to be formed",pos_hint={'center_x': .5, 'center_y': .5},halign="center" ,size_hint=(2, 2))
        self.text_input_2 = TextInput(on_text_validate=self.validator,multiline=False)

        label_2= Label(text="Enter the number of players to be in a team",pos_hint={'center_x': .5, 'center_y': .5},halign="center" ,size_hint=(2, 2))
        self.text_input_3 = TextInput(multiline=False)

        box1.add_widget(label)
        box1.add_widget(self.text_input)
        box1.add_widget(label_1)
        box1.add_widget(self.text_input_2)
        box1.add_widget(label_2)
        box1.add_widget(self.text_input_3)
        button_1 = Button(text='Generate',
                        pos_hint={'center_x': .5, 'center_y': .5})
        button_1.bind(on_press=self.button_1)

        button_2 = Button(text='Home',
                        pos_hint={'center_x': .5, 'center_y': .5})
        button_2.bind(on_press=self.button_2)

        box1.add_widget(button_1)
        box1.add_widget(button_2)
        self.add_widget(box1)

    def button_1(self,instance):
        FINAL_TEAMS = {}  
        PLAYERS_LIST = self.text_input.text.replace(' ','').split(',')
        print(PLAYERS_LIST)
        TEAM = self.text_input_2.text
        NO_OF_PLAYERS = self.text_input_3.text
        is_even = True if (len(PLAYERS_LIST)% 2) == 0 else False
        try:
            if is_even and TEAM.isnumeric() and NO_OF_PLAYERS.isnumeric():
                for t in range(0,int(TEAM)):
                    team = random.sample(PLAYERS_LIST, int(NO_OF_PLAYERS)) if len(PLAYERS_LIST) > 2 else PLAYERS_LIST
                    FINAL_TEAMS[t] = team
                    PLAYERS_LIST = [player for player in PLAYERS_LIST if player not in team]
                    print(PLAYERS_LIST)
            else:   
                common = random.choice(PLAYERS_LIST)
                FINAL_TEAMS["Error"] = f"The count of players is odd! We suggest to make {common.upper()} as common player. \U0001F606"
                PLAYERS_LIST = [player for player in PLAYERS_LIST if player not in common]
                for t in range(0,int(TEAM)):
                    team = random.sample(PLAYERS_LIST, int(NO_OF_PLAYERS)) if len(PLAYERS_LIST) > 2 else PLAYERS_LIST
                    FINAL_TEAMS[t] = team
                    PLAYERS_LIST = [player for player in PLAYERS_LIST if player not in team]
            print(FINAL_TEAMS) 
        except Exception as e:
            print(f'Error due to {str(e)}')

        self.final_teams = FINAL_TEAMS
        self.manager.current = "finalteams"
        self.manager.transition.direction = "left"
    
    def button_2(self, instance):
        self.manager.current = "welcomeoptions"
        self.manager.transition.direction = "down"

    def validator(self, instance):
        if self.text_input_2.text.isnumeric() and  int(self.text_input_2.text) > 10:
            self.msg = "Please enter teams less than 10."
            self.manager.current = "comingsoon"
            self.manager.transition.direction = "up"


class FinalTeams(Screen):
    def __init__(self, **kwargs):
        super(FinalTeams, self).__init__(**kwargs)
        self.name = 'finalteams'
        self.layout = "layout_finalteams"

    def on_enter(self, *args):
        self.clear_widgets()
        box2 = BoxLayout(orientation ='vertical')

        ss = self.manager.get_screen('teamformation')
        sucesslabel = Label(text=f"Team Formation",pos_hint={'center_x': .5, 'center_y': .5},halign="center" ,size_hint=(8, 1))               
        box2.add_widget(sucesslabel)
        final_teams = ss.final_teams
        if final_teams != {}:
            for k,v in final_teams.items():
                if k !=  "Error":
                    label = Label(text=f"Team {int(k)+1} -- {' '.join(v)}",pos_hint={'center_x': .5, 'center_y': .5}) 
                    box2.add_widget(label)
                elif k ==  "Error":
                    label = Label(text=v,pos_hint={'center_x': .5, 'center_y': .5}) 
                    box2.add_widget(label)
                else:
                    label = Label(text=f"Team Formation Failed",pos_hint={'center_x': .5, 'center_y': .5},halign="center" ,size_hint=(8, 2))               
                    box2.add_widget(label)      
        print(final_teams)
        
        button_1 = Button(text='Back',
                            pos_hint={'center_x': .5, 'center_y': .5},size_hint=(1, 0.5))
        button_1.bind(on_press=self.button_1)
        button_2 = Button(text='Home',
                            pos_hint={'center_x': .5, 'center_y': .5},size_hint=(1, 0.5))
        button_2.bind(on_press=self.button_2)
               
        box2.add_widget(button_1)
        box2.add_widget(button_2)
        self.add_widget(box2)
        

    def button_1(self,instance):
        self.manager.current = "teamformation"
        self.manager.transition.direction = "right"
    
    def button_2(self, instance):
        self.manager.current = "welcomeoptions"
        self.manager.transition.direction = "down"

class ComingSoon(Screen):
    def __init__(self, **kwargs):
        super(ComingSoon, self).__init__(**kwargs)
        self.name = 'comingsoon'
        self.layout = "layout_comingsoon"

    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation ='vertical')

        ss = self.manager.get_screen('teamformation')
        if 'msg' in dir(ss) and ss.msg:
            sucesslabel = Label(text=f"{ss.msg} \U0001F92D",
                            pos_hint={'center_x': .5, 'center_y': .5},halign="center" ,size_hint=(10, 10)) 
            box.add_widget(sucesslabel)
        sucesslabel = Label(text=f"Development in Progress. This feature will be availble soon to use. \U0001F92D",
                            pos_hint={'center_x': .5, 'center_y': .5},halign="center" ,size_hint=(10, 10))               
        box.add_widget(sucesslabel)
        
    
        button_1 = Button(text='Home',
                            pos_hint={'center_x': .5, 'center_y': .5},size_hint=(1, 1))
        button_1.bind(on_press=self.button_1)
        box.add_widget(button_1)

        self.add_widget(box)
    
    def button_1(self, instance):
        self.manager.current = "welcomeoptions"
        self.manager.transition.direction = "down"

WindowManager = ScreenManager()
WindowManager.add_widget(WelcomeOptions())
WindowManager.add_widget(TeamFormation())
WindowManager.add_widget(FinalTeams())
WindowManager.add_widget(ComingSoon())

class Main(App):
    def build(self):
        return WindowManager

if __name__ == "__main__":
    Main().run()