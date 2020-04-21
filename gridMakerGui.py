import kivy
import gridMaker as GM
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button 
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from plyer import filechooser

Window.size = (600, 700);

class MyApp(App):
    def pickColor(self, instance, value):
        self.colorButton.background_color = tuple(value);

    def selectFile(self, event):
        imgPath = filechooser.open_file(title="Pick a CSV file..", filters=[]);
        if len(imgPath):
            self.outputImage.source = imgPath[0];
            self.imageInput.text = imgPath[0];

    def resetAll(self, event):
        self.imageInput.text = "";
        self.rowsInput.text = "";
        self.columnsInput.text = "";
        self.xOffsetInput.text = "";
        self.yOffsetInput.text = "";
        self.thicknessInput.text = "";
        self.squareCheckBox.active = False;
        self.yAxisPrioCheckBox.active = False;
        self.bnwCheckBox.active = False;
        self.invertCheckBox.active = False;
        self.colorButton.background_color = (1, 0, 0, 1);

    def apply(self, event):
        img = self.imageInput.text;
        rows = self.rowsInput.text if (self.rowsInput.text) else 10;
        cols = self.columnsInput.text if (self.columnsInput.text) else 10;
        offset = (self.xOffsetInput.text if (self.xOffsetInput.text) else 0, self.yOffsetInput.text if (self.yOffsetInput.text) else 0)
        thickness = self.thicknessInput.text if (self.thicknessInput.text) else 1;
        bnw = self.bnwCheckBox.active;
        invert = self.invertCheckBox.active;
        square = self.squareCheckBox.active;
        yAxisPrio = self.yAxisPrioCheckBox.active;
        color = [ l*255 for l in list(self.colorButton.background_color)[:2]];
        color.append(self.colorButton.background_color[3]);

        outputFilePath = GM.make_grid(imgPath=img,rows=rows, cols=cols, offset=offset, square=square, bnw=bnw, invert=invert,
                            yPrio=yAxisPrio, thickness=thickness, color=tuple(color));

        if outputFilePath == "VALUE_ERROR":
            self.disclaimerLabel.text = "Please provide valid number inputs!!!";
        elif outputFilePath == "FILE_ERROR":
            self.disclaimerLabel.text = "Please provide complete and valid image source.";
        else:
            self.disclaimerLabel.text = "Successful, you can find the grid image in the gridImages folder.";
            self.outputImage.source = outputFilePath;

    def colorDialog(self, button): 
        layout = GridLayout(cols = 1, padding = 10);
        layout.spacing = [0, 5];
        clr_picker = ColorPicker();
        closeButton = Button(text ='Close', size_hint=(1, 0.075));

        layout.add_widget(clr_picker);          
        layout.add_widget(closeButton);      
  
        # Instantiate the modal popup and display 
        popup = Popup(title ='Demo Popup', content = layout, auto_dismiss=False)   
        popup.open();
        clr_picker.bind(color=self.pickColor);
        closeButton.bind(on_press=popup.dismiss);

    def build(self):
        SL = StackLayout(orientation ='lr-tb');
        SL.spacing = [0, 2];

        self.imageLabel = Label(text="Image Path:", size_hint=(0.25, 0.075));
        self.imageInput = TextInput(multiline=False, size_hint=(0.50, 0.075));
        self.browseButton = Button(text ='Browse', size_hint=(0.25, 0.075));
        self.browseButton.bind(on_press = self.selectFile);

        self.rowsLabel = Label(text="Rows:", size_hint=(0.25, 0.075));
        self.rowsInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="10");
        self.xOffsetLabel = Label(text="X-offset:", size_hint=(0.25, 0.075));
        self.xOffsetInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="0");

        self.columnsLabel = Label(text="Columns:", size_hint=(0.25, 0.075));
        self.columnsInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="10");
        self.yOffsetLabel = Label(text="Y-offset:", size_hint=(0.25, 0.075));
        self.yOffsetInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="0");

        self.bnwLabel = Label(text ='Grayscale', size_hint =(0.125, 0.075));
        self.bnwCheckBox = CheckBox(active = False, size_hint =(0.125, 0.075));
        self.invertLabel = Label(text ='Invert', size_hint =(0.125, 0.075));
        self.invertCheckBox = CheckBox(active = False, size_hint =(0.125, 0.075));

        self.squareLabel = Label(text ='Square', size_hint =(0.125, 0.075));
        self.squareCheckBox = CheckBox(active = False, size_hint =(0.125, 0.075));
        self.yAxisPrioLabel = Label(text ='Y-axis priority', size_hint =(0.125, 0.075));
        self.yAxisPrioCheckBox = CheckBox(active = False, size_hint =(0.125, 0.075));

        self.thicknessLabel = Label(text="Thickness:", size_hint=(0.25, 0.075));
        self.thicknessInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="1");
        self.colorButton = Button(text="Color", size_hint=(0.5, 0.075), background_color =(1, 0, 0, 1));
        self.colorButton.bind(on_press = self.colorDialog);

        self.resetButton = Button(text ='Reset', size_hint = (0.5, 0.075));
        self.resetButton.bind(on_press = self.resetAll);

        self.applyButton = Button(text ='Apply', size_hint =(0.5, 0.075));
        self.applyButton.bind(on_press = self.apply);

        self.ioLabel = Label(text="Input/Output", size_hint=(1, 0.075));
        self.outputImage = Image(source ='grr', size_hint = (1, 0.4));
        self.disclaimerLabel = Label(text="", size_hint=(1, 0.075));

        SL.add_widget(self.imageLabel);
        SL.add_widget(self.imageInput);
        SL.add_widget(self.browseButton);
        SL.add_widget(self.rowsLabel);
        SL.add_widget(self.rowsInput);
        SL.add_widget(self.xOffsetLabel);
        SL.add_widget(self.xOffsetInput);
        SL.add_widget(self.columnsLabel);
        SL.add_widget(self.columnsInput);
        SL.add_widget(self.yOffsetLabel);
        SL.add_widget(self.yOffsetInput);
        SL.add_widget(self.bnwLabel);
        SL.add_widget(self.bnwCheckBox);
        SL.add_widget(self.invertLabel);
        SL.add_widget(self.invertCheckBox);
        SL.add_widget(self.squareLabel);
        SL.add_widget(self.squareCheckBox);
        SL.add_widget(self.yAxisPrioLabel);
        SL.add_widget(self.yAxisPrioCheckBox);
        SL.add_widget(self.thicknessLabel);
        SL.add_widget(self.thicknessInput);
        SL.add_widget(self.colorButton);
        SL.add_widget(self.resetButton);
        SL.add_widget(self.applyButton);
        SL.add_widget(self.ioLabel);
        SL.add_widget(self.outputImage);
        SL.add_widget(self.disclaimerLabel);

        return SL;
        

if __name__ == "__main__":
    MyApp().run()
