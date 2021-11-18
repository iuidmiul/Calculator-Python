import math
from os import error
import cocos
from cocos import sprite
from cocos.actions import *
from cocos.sprite import Sprite
from cocos.text import *
import pyglet
from pyglet.text import *
from pyglet.window import key
from pyglet.window import mouse

class Calc_Interface(cocos.layer.Layer):
    is_event_handler = True

    global button_size
    button_size  = 0.38

    global input_size
    input_size = 0.37

    global mouse_x
    global mouse_y
    global mouse_over
    global operand_selected
    operand_selected = 0
    mouse_over = ""

    global digits_limit
    digits_limit = 4

    global result_array
    result_array = []

	#Create All Objects
    #region
    def __init__(self):
        super(Calc_Interface,self).__init__()

        #Background
        SpriteBackground = cocos.sprite.Sprite('images/Background.png')
        SpriteBackground.position = (200,300)
        SpriteBackground.scale = 1.02
        self.add(SpriteBackground)

        #Operand1
        Operand_1 = cocos.sprite.Sprite('images/Operand1_text.png')
        Operand_1.position = (102,540)
        Operand_1.scale = 0.4
        self.add(Operand_1)

        #Operand2
        Operand_2 = cocos.sprite.Sprite('images/Operand2_text.png')
        Operand_2.position = (102,460)
        Operand_2.scale = 0.4
        self.add(Operand_2)

        #Operand1 Input Background
        Operand_1_input_bg = cocos.sprite.Sprite('images/Input_background.png')
        Operand_1_input_bg.position = (289,540)
        Operand_1_input_bg.scale = 0.4
        self.add(Operand_1_input_bg)
        
        #Operand2 Input Background
        Operand_2_input_bg = cocos.sprite.Sprite('images/Input_background.png')
        Operand_2_input_bg.position = (289,460)
        Operand_2_input_bg.scale = 0.4
        self.add(Operand_2_input_bg)

        #Operand1 Input
        global Operand_1_input
        Operand_1_input = cocos.text.Label('',font_size = 50)
        Operand_1_input.position = (214,531)
        Operand_1_input.scale = input_size
        self.add(Operand_1_input)

        #Operand2 Input
        global Operand_2_input
        Operand_2_input = cocos.text.Label('',font_size = 50)
        Operand_2_input.position = (214,451)
        Operand_2_input.scale = input_size
        self.add(Operand_2_input)

        #Add
        Add = cocos.sprite.Sprite('images/Add_button.png')
        Add.position = (102,360)
        Add.scale = button_size
        self.add(Add)

        #Sub
        Sub = cocos.sprite.Sprite('images/Sub_button.png')
        Sub.position = (306,360)
        Sub.scale = button_size
        self.add(Sub)

        #Mul
        Mul = cocos.sprite.Sprite('images/Mul_button.png')
        Mul.position = (102,260)
        Mul.scale = button_size
        self.add(Mul)

        #Div
        Div = cocos.sprite.Sprite('images/Div_button.png')
        Div.position = (306,260)
        Div.scale = button_size
        self.add(Div)

        #Clear
        Clear = cocos.sprite.Sprite('images/Clear_button.png')
        Clear.position = (202,40)
        Clear.scale = button_size
        self.add(Clear)
        
        #Result BG
        Result_bg = cocos.sprite.Sprite('images/Result_background.png')
        Result_bg.position = (202,150)
        Result_bg.scale = button_size
        Result_bg.scale_y = 1.1
        self.add(Result_bg)

        #Result text
        global result_text
        result_text = cocos.text.Label('',(202,146),font_size = 50,anchor_x = 'center',anchor_y = 'center')
        result_text.scale = input_size
        self.add(result_text)

        #Error Bg
        global error
        error = cocos.sprite.Sprite('images/Error.png')
        error.opacity = 0
        error.position = (202,80)
        error.scale = 0.5
        self.add(error)
    #endregion
    
    #Loop
    #region
    def _step(self, dt):
        super(Calc_Interface,self)._step
        #error anim
        if error.opacity > 0:
            error.opacity = error.opacity - 100 * dt
        elif error.opacity < 0:
            error.opacity = 0
    #endregion

    #Update/clear result
    #region
    global update_result_array
    def update_result_array(result):
        result_array.append(result)
    #endregion

    #mouse pressed
    #region
    def on_mouse_press(self,x,y,button,modifiers):
        global operand_selected
        if button == mouse.LEFT:
            if mouse_over == "op1":
                operand_selected = 1

            elif mouse_over == "op2":
                operand_selected = 2
                return

            elif mouse_over == "add":
                temporary_input1 = ''
                temporary_input2 = ''
                temporary_result = 0
                input1_comma = False
                input2_comma = False
                operand_selected = 0
                #check for empty inputs
                if len(Operand_1_input.element.text) == 0 or len(Operand_2_input.element.text) == 0:
                    return

                #input 1
                #nothing before comma
                if Operand_1_input.element.text[0] == ".":
                    #just the comma
                    if len(Operand_1_input.element.text) == 1:
                        temporary_input1 = '0'
                    else:
                        #something before comma
                        temporary_input1 = "0" + Operand_1_input.element.text
                #nothing after comma
                elif Operand_1_input.element.text[-1] == ".":
                    for i in range(0,len(Operand_1_input.element.text) - 1):
                        temporary_input1 = temporary_input1 + Operand_1_input.element.text[i]
                else:
                    temporary_input1 = Operand_1_input.element.text
                #check for comma
                for i in range(0,len(Operand_1_input.element.text)):
                    if Operand_1_input.element.text[i] == ".":
                        input1_comma = True

                #input 2
                #nothing before comma
                if Operand_2_input.element.text[0] == ".":
                    #just the comma
                    if len(Operand_2_input.element.text) == 1:
                        temporary_input2 = '0'
                    else:
                        #something before comma
                        temporary_input2 = "0" + Operand_2_input.element.text
                #nothing after comma
                elif Operand_2_input.element.text[-1] == ".":
                    for i in range(0,len(Operand_2_input.element.text) - 1):
                        temporary_input2 = temporary_input2 + Operand_2_input.element.text[i]
                else:
                    temporary_input2 = Operand_2_input.element.text
                #check for comma
                for i in range(0,len(Operand_2_input.element.text)):
                    if Operand_2_input.element.text[i] == ".":
                        input2_comma = True

                #calculate result
                if input1_comma == True or input2_comma == True:
                    temporary_result = float(temporary_input1) + float(temporary_input2)
                    #limit digits after comma
                    before_comma = 0
                    print(temporary_result)
                    string_result = str(temporary_result)
                    if len(string_result) > 5:
                        for i in range(0,len(string_result)):
                            before_comma = before_comma + 1
                            if string_result[i] == ".":
                                overwrite_result = ""
                                for i in range(0,before_comma + digits_limit):
                                    overwrite_result = overwrite_result + string_result[i]
                                temporary_result = float(overwrite_result)
                        result_text.element.text = str(temporary_result)
                        update_result_array(temporary_result)
                        print(result_array)
                    else:
                        result_text.element.text = str(temporary_result)
                        update_result_array(temporary_result)
                        print(result_array)
                else:
                    temporary_result = int(temporary_input1) + int(temporary_input2)
                    result_text.element.text = str(temporary_result)
                    update_result_array(temporary_result)
                    print(result_array)

            elif mouse_over == "sub":
                temporary_input1 = ''
                temporary_input2 = ''
                temporary_result = 0
                input1_comma = False
                input2_comma = False
                operand_selected = 0
                #check for empty inputs
                if len(Operand_1_input.element.text) == 0 or len(Operand_2_input.element.text) == 0:
                    return

                #input 1
                #nothing before comma
                if Operand_1_input.element.text[0] == ".":
                    #just the comma
                    if len(Operand_1_input.element.text) == 1:
                        temporary_input1 = '0'
                    else:
                        #something before comma
                        temporary_input1 = "0" + Operand_1_input.element.text
                #nothing after comma
                elif Operand_1_input.element.text[-1] == ".":
                    for i in range(0,len(Operand_1_input.element.text) - 1):
                        temporary_input1 = temporary_input1 + Operand_1_input.element.text[i]
                else:
                    temporary_input1 = Operand_1_input.element.text
                #check for comma
                for i in range(0,len(Operand_1_input.element.text)):
                    if Operand_1_input.element.text[i] == ".":
                        input1_comma = True

                #input 2
                #nothing before comma
                if Operand_2_input.element.text[0] == ".":
                    #just the comma
                    if len(Operand_2_input.element.text) == 1:
                        temporary_input2 = '0'
                    else:
                        #something before comma
                        temporary_input2 = "0" + Operand_2_input.element.text
                #nothing after comma
                elif Operand_2_input.element.text[-1] == ".":
                    for i in range(0,len(Operand_2_input.element.text) - 1):
                        temporary_input2 = temporary_input2 + Operand_2_input.element.text[i]
                else:
                    temporary_input2 = Operand_2_input.element.text
                #check for comma
                for i in range(0,len(Operand_2_input.element.text)):
                    if Operand_2_input.element.text[i] == ".":
                        input2_comma = True

                #calculate result
                if input1_comma == True or input2_comma == True:
                    temporary_result = (float(temporary_input1) - float(temporary_input2))
                    #limit digits after comma
                    before_comma = 0
                    string_result = str(temporary_result)
                    if len(string_result) > 5:
                        for i in range(0,len(string_result)):
                            before_comma = before_comma + 1
                            if string_result[i] == ".":
                                overwrite_result = ""
                                for i in range(0,before_comma + digits_limit):
                                    overwrite_result = overwrite_result + string_result[i]
                                temporary_result = float(overwrite_result)
                        result_text.element.text = str(temporary_result)
                        update_result_array(temporary_result)
                        print(result_array)
                    else:
                        result_text.element.text = str(temporary_result)
                        update_result_array(temporary_result)
                        print(result_array)
                else:
                    temporary_result = int(temporary_input1) - int(temporary_input2)
                    result_text.element.text = str(temporary_result)
                    update_result_array(temporary_result)
                    print(result_array)

            elif mouse_over == "mul":
                temporary_input1 = ''
                temporary_input2 = ''
                temporary_result = 0
                input1_comma = False
                input2_comma = False
                add_temporary = 0
                operand_selected = 0
                #check for empty inputs
                if len(Operand_1_input.element.text) == 0 or len(Operand_2_input.element.text) == 0:
                    return

                #input 1
                #nothing before comma
                if Operand_1_input.element.text[0] == ".":
                    #just the comma
                    if len(Operand_1_input.element.text) == 1:
                        temporary_input1 = '0'
                    else:
                        #something before comma
                        temporary_input1 = "0" + Operand_1_input.element.text
                #nothing after comma
                elif Operand_1_input.element.text[-1] == ".":
                    for i in range(0,len(Operand_1_input.element.text) - 1):
                        temporary_input1 = temporary_input1 + Operand_1_input.element.text[i]
                else:
                    temporary_input1 = Operand_1_input.element.text
                #check for comma
                for i in range(0,len(Operand_1_input.element.text)):
                    if Operand_1_input.element.text[i] == ".":
                        input1_comma = True

                #input 2
                #nothing before comma
                if Operand_2_input.element.text[0] == ".":
                    #just the comma
                    if len(Operand_2_input.element.text) == 1:
                        temporary_input2 = '0'
                    else:
                        #something before comma
                        temporary_input2 = "0" + Operand_2_input.element.text
                #nothing after comma
                elif Operand_2_input.element.text[-1] == ".":
                    for i in range(0,len(Operand_2_input.element.text) - 1):
                        temporary_input2 = temporary_input2 + Operand_2_input.element.text[i]
                else:
                    temporary_input2 = Operand_2_input.element.text
                #check for comma
                for i in range(0,len(Operand_2_input.element.text)):
                    if Operand_2_input.element.text[i] == ".":
                        input2_comma = True

                #calculate result
                if input1_comma == True or input2_comma == True:
                    temporary_result = (float(temporary_input1) * float(temporary_input2))
                    #limit digits after comma
                    before_comma = 0
                    string_result = str(temporary_result)
                    if len(string_result) > 5:
                        for i in range(0,len(string_result)):
                            before_comma = before_comma + 1
                            if string_result[i] == ".":
                                overwrite_result = ""
                                for i in range(0,before_comma + digits_limit):
                                    overwrite_result = overwrite_result + string_result[i]
                                temporary_result = float(overwrite_result)
                        result_text.element.text = str(temporary_result)
                        update_result_array(temporary_result)
                        print(result_array)
                    else:
                        result_text.element.text = str(temporary_result)
                        update_result_array(temporary_result)
                        print(result_array)
                else:
                    temporary_result = int(temporary_input1) * int(temporary_input2)
                    result_text.element.text = str(temporary_result)
                    update_result_array(temporary_result)
                    print(result_array)

            elif mouse_over == "div":
                temporary_input1 = ''
                temporary_input2 = ''
                temporary_result = 0
                input1_comma = False
                input2_comma = False
                add_temporary = 0
                operand_selected = 0
                #check for empty inputs
                if len(Operand_1_input.element.text) == 0 or len(Operand_2_input.element.text) == 0:
                    return

                #input 1
                #nothing before comma
                if Operand_1_input.element.text[0] == ".":
                    #just the comma
                    if len(Operand_1_input.element.text) == 1:
                        temporary_input1 = '0'
                    else:
                        #something before comma
                        temporary_input1 = "0" + Operand_1_input.element.text
                #nothing after comma
                elif Operand_1_input.element.text[-1] == ".":
                    for i in range(0,len(Operand_1_input.element.text) - 1):
                        temporary_input1 = temporary_input1 + Operand_1_input.element.text[i]
                else:
                    temporary_input1 = Operand_1_input.element.text
                #check for comma
                for i in range(0,len(Operand_1_input.element.text)):
                    if Operand_1_input.element.text[i] == ".":
                        input1_comma = True

                #input 2
                #nothing before comma
                if Operand_2_input.element.text[0] == ".":
                    #just the comma
                    if len(Operand_2_input.element.text) == 1:
                        temporary_input2 = '0'
                    else:
                        #something before comma
                        temporary_input2 = "0" + Operand_2_input.element.text
                #nothing after comma
                elif Operand_2_input.element.text[-1] == ".":
                    for i in range(0,len(Operand_2_input.element.text) - 1):
                        temporary_input2 = temporary_input2 + Operand_2_input.element.text[i]
                else:
                    temporary_input2 = Operand_2_input.element.text
                #check for comma
                for i in range(0,len(Operand_2_input.element.text)):
                    if Operand_2_input.element.text[i] == ".":
                        input2_comma = True

                #calculate result
                if input1_comma == True or input2_comma == True and (temporary_input2 != '0' or temporary_input1 != '0'):
                    if float(temporary_input1) != 0 and float(temporary_input2) != 0:
                        temporary_result = (float(temporary_input1) / float(temporary_input2))
                    else:
                        error.opacity = 255
                        return

                    #limit digits after comma
                    before_comma = 0
                    string_result = str(temporary_result)
                    if len(string_result) > 5:
                        for i in range(0,len(string_result)):
                            before_comma = before_comma + 1
                            if string_result[i] == ".":
                                overwrite_result = ""
                                for i in range(0,before_comma + digits_limit):
                                    overwrite_result = overwrite_result + string_result[i]
                                temporary_result = float(overwrite_result)
                        result_text.element.text = str(temporary_result)
                        update_result_array(temporary_result)
                        print(result_array)
                    else:
                        result_text.element.text = str(temporary_result)
                        update_result_array(temporary_result)
                        print(result_array)
                else:
                    if temporary_input1 == '0' or temporary_input2 == '0':
                        error.opacity = 255
                        return
                    temporary_result = int(temporary_input1) / int(temporary_input2)
                    result_text.element.text = str(temporary_result)
                    update_result_array(temporary_result)
                    print(result_array)

            elif mouse_over == "clear":
                operand_selected = 0
                result_text.element.text = ''
                Operand_1_input.element.text = ''
                Operand_2_input.element.text = ''
                result_array.clear()
                print(result_array)
                return

            else:
                operand_selected = 0
                return
    #endregion

    #mouse over buttons
    #region
    def on_mouse_motion(self,x,y,dx,dy):
        global mouse_x
        global mouse_y
        global mouse_over
        mouse_x = x
        mouse_y = y
        """ print("Mouse X: " + str(mouse_x) + " " + "Mouse Y: " + str(mouse_y)) """
        #Operand 1 input
        if (mouse_x >= 210 and mouse_x <= 369) and (mouse_y >= 527 and mouse_y <= 556):
            mouse_over = "op1"
            return

        #Operand 2 input
        elif (mouse_x >= 210 and mouse_x <= 369) and (mouse_y >= 446 and mouse_y <= 474):
            mouse_over = "op2"
            return

        #Add button collide
        elif (mouse_x >= 41 and mouse_x <= 161) and (mouse_y >= 338 and mouse_y <= 383):
            mouse_over = "add"
            return

        #Sub button collide
        elif (mouse_x >= 244 and mouse_x <= 363) and (mouse_y >= 338 and mouse_y <= 383):
            mouse_over = "sub"
            return

        #Mul button collide
        elif (mouse_x >= 41 and mouse_x <= 161) and (mouse_y >= 240 and mouse_y <= 280):
            mouse_over = "mul"
            return
        
        #Div button collide
        elif (mouse_x >= 244 and mouse_x <= 363) and (mouse_y >= 240 and mouse_y <= 280):
            mouse_over = "div"
            return

        #Clear button collide
        elif (mouse_x >= 140 and mouse_x <= 261) and (mouse_y >= 19 and mouse_y <= 60):
            mouse_over = "clear"
            return
        
        else:
            mouse_over = ""
    #endregion

    #key pressed
    #region
    def on_key_release(self,keys,modi):
        Number_Conv = pyglet.window.key.symbol_string(keys)[-1]
        global operand_selected
        #Check if it's a number
        for a in range(0,11):
            if Number_Conv == str(a):
                #operand 1
                if operand_selected == 1:
                    #limit input numbers
                    if len(Operand_1_input.element.text) < 11:
                        Operand_1_input.element.text = Operand_1_input.element.text + str(Number_Conv)

                #operand 2
                if operand_selected == 2:
                    #limit input numbers
                    if len(Operand_2_input.element.text) < 11:
                        Operand_2_input.element.text = Operand_2_input.element.text + str(Number_Conv)

        if keys == 46:
            if operand_selected == 1:
                #verify for other commas
                for a in range(0,len(Operand_1_input.element.text)):
                    if Operand_1_input.element.text[a] == ".":
                        return
                #limit input numbers
                if len(Operand_1_input.element.text) < 11:
                    Operand_1_input.element.text = Operand_1_input.element.text + "."

            if operand_selected == 2:
                #verify for other commas
                for a in range(0,len(Operand_2_input.element.text)):
                    if Operand_2_input.element.text[a] == ".":
                        return
                #limit input numbers
                if len(Operand_2_input.element.text) < 11:
                    Operand_2_input.element.text = Operand_2_input.element.text + "."

        #empty the inputs
        if operand_selected == 1 and keys == key.BACKSPACE:
            global op1_text
            op1_text = ''
            #if the last digit isn't a comma
            if keys != '46':
                for i in range(0,len(Operand_1_input.element.text) - 1):
                    op1_text = op1_text + Operand_1_input.element.text[i]
                Operand_1_input.element.text = op1_text
            else:
                for i in range(0,len(Operand_1_input.element.text) - 2):
                    op1_text = op1_text + Operand_1_input.element.text[i]
                Operand_1_input.element.text = op1_text

        if operand_selected == 2 and keys == key.BACKSPACE:
            global op2_text
            op2_text = ''
            #if the last digit isn't a comma
            if keys != '46':
                for i in range(0,len(Operand_2_input.element.text) - 1):
                    op2_text = op2_text + Operand_2_input.element.text[i]
                Operand_2_input.element.text = op2_text
            else:
                for i in range(0,len(Operand_2_input.element.text) - 2):
                    op2_text = op2_text + Operand_2_input.element.text[i]
                Operand_2_input.element.text = op2_text
    #endregion

cocos.director.director.init(404,603,caption = "Calculator")
Calc_scene = cocos.scene.Scene(Calc_Interface())
cocos.director.director.run(Calc_scene)