# Import required modules
import os
import kivy
import gridMaker as GM
from kivy.app import App
from plyer import filechooser
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button 
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout 
from kivy.graphics import Color, Rectangle
from kivy.uix.stacklayout import StackLayout
from kivy.uix.colorpicker import ColorPicker

# Set application window size
Window.size = (600, 700);

# Application class
class MyApp(App):

    # API to choose color from the color picker
    def pickColor(self, instance, value):
        # Set the choosen color as the button background
        self.colorButton.background_color = tuple(value);
            
    # API to select image file path
    def selectFile(self, event):
        # Open up the file explorer
        imgPath = filechooser.open_file(title="Pick a CSV file..");
        # Check if a file is selected
        if len(imgPath):
            # Set the image and image path to display
            self.outputImage.source = imgPath[0];
            self.imageInput.text = imgPath[0];
        else:
            # Else clear them
            self.imageInput.text = "";
            self.outputImage.source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets\\welcome.jpg");
            
    # API to reset all written values
    def resetAll(self, event):
        self.imageInput.text = "";
        self.outputImage.source = ".\\assets\\welcome.jpg";
        self.rowsInput.text = "";
        self.columnsInput.text = "";
        self.xOffsetInput.text = "";
        self.yOffsetInput.text = "";
        self.thicknessInput.text = "";
        self.squareCheckBox.active = False;
        self.rowPrioCheckBox.active = False;
        self.bnwCheckBox.active = False;
        self.invertCheckBox.active = False;
        self.colorButton.background_color = (1, 0, 0, 1);

    # API to apply the grid config
    def apply(self, event):
        # Read in the inputs from the input fields
        img = self.imageInput.text;
        # Set to default values if no calue is provided
        rows = self.rowsInput.text if (self.rowsInput.text) else int(self.rowsInput.hint_text);
        cols = self.columnsInput.text if (self.columnsInput.text) else int(self.columnsInput.hint_text);
        offset = (self.xOffsetInput.text if (self.xOffsetInput.text) else int(self.xOffsetInput.hint_text), self.yOffsetInput.text if (self.yOffsetInput.text) else int(self.yOffsetInput.hint_text))
        thickness = self.thicknessInput.text if (self.thicknessInput.text) else int(self.thicknessInput.hint_text);
        # Read checkbox statuses
        bnw = self.bnwCheckBox.active;
        invert = self.invertCheckBox.active;
        square = self.squareCheckBox.active;
        rowPrio = self.rowPrioCheckBox.active;
        # Scale up the colors and retain the opacity factor
        color = [ l*255 for l in list(self.colorButton.background_color)[:2]];
        color.append(self.colorButton.background_color[3]);

        # Call the grid creation API and collect the error or the output file path
        outputFilePath = GM.make_grid(imgPath=img,rows=rows, cols=cols, offset=offset, square=square, bnw=bnw, invert=invert,
                            rowPrio=rowPrio, thickness=thickness, color=tuple(color));

        # Error handling for invalid input values 
        if outputFilePath == "VALUE_ERROR":
            self.disclaimerLabel.text = "Please provide valid number inputs!!!";
        # Error handling for wrong type of file
        elif outputFilePath == "FILE_ERROR":
            self.disclaimerLabel.text = "Please provide complete and valid image source.";
        # Error handling for unknown reasons
        elif outputFilePath == "UNKNOWN_ERROR":
            self.disclaimerLabel.text = "Something went wrong, please provide a supported image file.";
        else:
        # Dsiplay the output image
            self.disclaimerLabel.text = "Successful, you can find the grid image in the gridImages folder.";
            self.outputImage.source = outputFilePath;

    # Color Dialog popup window
    def colorDialog(self, button): 
        # Create a layout for the widget
        layout = GridLayout(cols = 1, padding = 10);
        layout.spacing = [0, 5];
        # Add widget and close button
        clr_picker = ColorPicker();
        closeButton = Button(text ='Close', size_hint=(1, 0.075));
        layout.add_widget(clr_picker);          
        layout.add_widget(closeButton);      
  
        # Instantiate the modal popup and display 
        popup = Popup(title ='Pick a Color', content = layout, auto_dismiss=False);
        popup.open();
        # Bind the widgets with respective functions
        clr_picker.bind(color=self.pickColor);
        closeButton.bind(on_press=popup.dismiss);

    # Run the GUI
    def build(self):
        # Set title and icon for the application
        self.title = 'Grid Maker';
        self.icon = "./assets/icon.png";
        # Create a Stack layout
        SL = StackLayout(orientation ='lr-tb', padding=5);
        SL.spacing = [0, 2];

        # First row of the GUI
        self.imageLabel = Label(text="Image Path:", size_hint=(0.25, 0.075));
        self.imageInput = TextInput(multiline=False, size_hint=(0.50, 0.075));
        self.browseButton = Button(text ='Browse', size_hint=(0.25, 0.075));
        self.browseButton.bind(on_press = self.selectFile);

        # Second row of the GUI
        self.rowsLabel = Label(text="Rows:", size_hint=(0.25, 0.075));
        self.rowsInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="10");
        self.xOffsetLabel = Label(text="X-offset:", size_hint=(0.25, 0.075));
        self.xOffsetInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="0");

        # Third row of the GUI
        self.columnsLabel = Label(text="Columns:", size_hint=(0.25, 0.075));
        self.columnsInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="10");
        self.yOffsetLabel = Label(text="Y-offset:", size_hint=(0.25, 0.075));
        self.yOffsetInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="0");

        # Fourth row of the GUI
        self.bnwLabel = Label(text ='Grayscale', size_hint =(0.125, 0.075));
        self.bnwCheckBox = CheckBox(active = False, size_hint =(0.125, 0.075));
        self.invertLabel = Label(text ='Invert', size_hint =(0.125, 0.075));
        self.invertCheckBox = CheckBox(active = False, size_hint =(0.125, 0.075));
        self.squareLabel = Label(text ='Square', size_hint =(0.125, 0.075));
        self.squareCheckBox = CheckBox(active = False, size_hint =(0.125, 0.075));
        self.rowPrioLabel = Label(text ='Row priority', size_hint =(0.125, 0.075));
        self.rowPrioCheckBox = CheckBox(active = False, size_hint =(0.125, 0.075));
        # Disable the checkbox by default 
        # self.rowPrioLabel.disabled = True;
        # self.rowPrioCheckBox.disabled = True;

        # Fifth row of the GUI
        self.thicknessLabel = Label(text="Thickness:", size_hint=(0.25, 0.075));
        self.thicknessInput = TextInput(multiline=False, size_hint=(0.25, 0.075), hint_text="1");
        self.colorButton = Button(text="Color", size_hint=(0.5, 0.075), background_color =(1, 0, 0, 1));
        self.colorButton.bind(on_press = self.colorDialog);

        # Sixth row of the GUI
        self.resetButton = Button(text ='Reset', size_hint = (0.5, 0.075));
        self.resetButton.bind(on_press = self.resetAll);
        self.applyButton = Button(text ='Apply', size_hint =(0.5, 0.075));
        self.applyButton.bind(on_press = self.apply);

        # Image canvas at the bottom of the GUI
        self.outputImage = Image(source ='assets\\welcome.jpg', size_hint = (1, 0.4));
        self.disclaimerLabel = Label(text="", size_hint=(1, 0.075));

        # Add all the defined widgets accordingly
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
        SL.add_widget(self.rowPrioLabel);
        SL.add_widget(self.rowPrioCheckBox);
        SL.add_widget(self.thicknessLabel);
        SL.add_widget(self.thicknessInput);
        SL.add_widget(self.colorButton);
        SL.add_widget(self.resetButton);
        SL.add_widget(self.applyButton);
        SL.add_widget(self.disclaimerLabel);
        SL.add_widget(self.outputImage);

        # Return and run the application
        return SL;
        
# Main function
if __name__ == "__main__":
    # Create an app instance and run
    MyApp().run()
