import kivy
kivy.require('1.8.0')

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from kivy.uix.settings import (Settings, SettingsWithSidebar,
                               SettingsWithSpinner,
                               SettingsWithTabbedPanel)
from kivy.uix.popup import Popup
from functools import partial
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

try:
    engine = create_engine('mysql://root:password@localhost/ckdb', echo=True)
    DBSession = sessionmaker()
    DBSession.configure(bind=engine)
    session = DBSession()
except:
    print ' no connection'


student_list = [
    ("0", "fruit_images/Apple.64.jpg","Apple","Apple: Super Sweet"),
    ("1", "fruit_images/Banana.64.jpg","Banana","Banana: Want a bunch"),
    ("2", "fruit_images/Strawberry.64.jpg", "Strawberry", "Strawberry: Yummy"),
    ("3", "fruit_images/Orange.64.jpg","Orange","Orange: Florida's BesT"),
    ("4", "fruit_images/Pear.64.jpg","Pear","Pear: Perfect"),
    ("5", "fruit_images/Lime.64.jpg","Lime","Sharp: NZ BesT"),
    ("6", "fruit_images/Apple.64.jpg","Apple","Apple: Super Sweet"),
    ("7", "fruit_images/Banana.64.jpg","Banana","Banana: Want a bunch"),
    ("8", "fruit_images/Strawberry.64.jpg", "Strawberry", "Strawberry: Yummy"),
    ("9", "fruit_images/Orange.64.jpg","Orange","Orange: Florida's BesT"),
    ("10", "fruit_images/Pear.64.jpg","Pear","Pear: Perfect"),
    ("11", "fruit_images/Lime.64.jpg","Lime","Sharp: NZ BesT"),
    ("12", "fruit_images/Apple.64.jpg","Apple","Apple: Super Sweet"),
    ("13", "fruit_images/Banana.64.jpg","Banana","Banana: Want a bunch"),
    ("14", "fruit_images/Strawberry.64.jpg", "Strawberry", "Strawberry: Yummy"),
    ("15", "fruit_images/Orange.64.jpg","Orange","Orange: Florida's BesT"),
    ("16", "fruit_images/Pear.64.jpg","Pear","Pear: Perfect"),
    ("17", "fruit_images/Lime.64.jpg","Lime","Sharp: NZ BesT")
    ]


        
class ScreenMain(Screen):
    settings_popup = ObjectProperty(None, allownone=True)

    def __init__ (self,**kwargs):
        super (ScreenMain, self).__init__(**kwargs)
        # Clock

        self.add_classes()
        self.add_students(student_list)

    def add_classes(self):
        # sql  get classes for user
        # is user a from teacher ?
        # change spinner text & values
        spinner = self.ids.class_spinner
        spinner.text= "test"
        spinner.values = ("test", "2", "3")

    def class_selected(self):
        spinner = self.ids.class_spinner
        class_name = spinner.text
        # sql to  get list of students for this class/teacher
        self.add_students()


    def build_student_button(self, item):
        print item
        btn = StudentListItemButton(
                wid=item[0], 
              image=item[1], 
              title=item[2], 
              label=item[3]
            )
        btn.size_hint=(1, None)
        btn.height = 42
        return btn


    def changer2(self, result, *args):
        self.manager.get_screen('ScreenStudentDetails').update(result)
        self.manager.current = 'ScreenStudentDetails'
            
        
    def add_students(self, lst=[]):
        student_list = self.ids.student_list
        student_list.clear_widgets()
        for item in lst:
            txt = lst[0]
            btn = self.build_student_button(item)
            student_list.add_widget(btn)
            btn.bind(on_press=partial(self.changer2, txt))
        student_list.bind(minimum_height=student_list.setter('height'))
    
class CustomPopup(Popup):
    pass

class ScreenLogin(Screen):

    def __init__(self,**kwargs):
        super (ScreenLogin,self).__init__(**kwargs)
    def popupwrong_password(self):
        #popup = Popup(title = "Warning!!", 
        #        content = Label(text = "Wrong Password, Please Correct the password!"), 
        #        size = (200,200), 
        #        size_hint=(None, None),
        #        auto_dismiss=True)
        p = CustomPopup()
        p.open()

    def login(self, *args):
        
        email_input = self.ids.email_input
        user_email = email_input.text

        password_input =  self.ids.password_input
        password = password_input.text

        for a in session.query(User).filter(User.email == user_email):
            if a.password != password:
                #pint "Wrong Password"
                self.popupwrong_password()
                email_input.text = ''
                password_input.text = ''
                return
            app.my_screenmanager.current = 'ScreenMain'




class StudentListItemButton(Button):
    wid = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')
    pass

    def click(button):
        global app
        print 'selected student'
        return
        app.clearSelection()
        button.background_color = (0,160,66,.9)
        Logger.info(button.title + ": wid=" + button.wid)

class ScreenAttend(Screen):
    pass

class ScreenTag(Screen):
    pass

class ScreenAction(Screen):
    pass


class ScreenStudentDetails(Screen):

    def __init__(self,**kwargs):
        super (ScreenStudentDetails,self).__init__(**kwargs)
        

    def changer(self,*args):
        self.manager.current = 'ScreenStudents'

    def changer2(self,*args):
        self.manager.current = 'ScreenAttend'

    def update(self, current_student):
        details_grid = self.ids.details_grid
        print 'update called, current_student = ', current_student
        
        sl = self.ids.studentname_label
        #sl.text = current_student

        #'In School'   
        lbl = Label( text = 'In School')
        btn = Button(text = 'YES')
        
        details_grid.add_widget(lbl)
        details_grid.add_widget(btn)
        
        btn.bind(on_press=partial(self.changer2))

        
        for i in [1,2,3]:
            
            txt ='Label'
            lbl = Label(text = txt)
            
            txt ='Info'
            btn = Button(text = txt)
            
            details_grid.add_widget(lbl)
            details_grid.add_widget(btn)

            

class xx4_testApp(App):

    def build(self):
        self.my_screenmanager = ScreenManager()
        
        screenMain   = ScreenMain(  name='ScreenMain')
        screenLogin  = ScreenLogin( name='ScreenLogin')
        screenAttend = ScreenAttend(name='ScreenAttend') 
        screenAction = ScreenAction(name='ScreenAction')
        #screenTagStudents    = ScreenTagStudents(   name='ScreenTagStudents')
        screenStudentDetails = ScreenStudentDetails(name='ScreenStudentDetails')

        screenTag = ScreenTag(name='ScreenTag')
               
        self.my_screenmanager.add_widget(screenMain)
        self.my_screenmanager.add_widget(screenLogin)
        self.my_screenmanager.add_widget(screenStudentDetails)
        self.my_screenmanager.add_widget(screenAction)
        #self.my_screenmanager.add_widget(screenTagStudents)
        self.my_screenmanager.add_widget(screenAttend)
        self.my_screenmanager.add_widget(screenTag)
        return self.my_screenmanager


if __name__ == '__main__':
    app=xx4_testApp()
    app.run()
