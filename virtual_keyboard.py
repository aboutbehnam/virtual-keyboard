# GitHub Repository: https://github.com/aboutbehnam
import os
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.logger import Logger

# Set transparent background for the Kivy window
Window.clearcolor = (1, 1, 1, 0.1)  # Slightly transparent white background

# Get absolute path for font to avoid path issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "fonts")
CONFIG = {
    'fonts': {
        'default': os.path.join(FONT_PATH, "Vazir.ttf"),
        'fallback': "Arial"  # Changed to Arial for better compatibility
    },
    'languages': {
        'EN': ['1234567890', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm'],
        'FA': ['۱۲۳۴۵۶۷۸۹۰', 'ضصثقفغعهخح', 'شسیبلاتنم', 'ظطزرذدپو'],
        'AR': ['١٢٣٤٥٦٧٨٩٠', 'ضصثقفغعهخح', 'شسیبلاتنم', 'ظطزرذدپو'],
        'NUM': ['1234567890', '!@#$%^&*()', '+-*/=.,', '<>[]{}']
    },
    'themes': {
        'light': {
            'background': (1, 1, 1, 0.3),  # Semi-transparent
            'button_bg': (0.9, 0.9, 0.9, 0.5),  # More transparent buttons
            'button_text': (0, 0, 0, 1),
            'input_bg': (0.95, 0.95, 0.95, 0.7),
            'glow_color': (0.8, 0.8, 1, 0.3)  # Soft glow for light theme
        },
        'dark': {
            'background': (0.2, 0.2, 0.2, 0.3),  # Semi-transparent
            'button_bg': (0.3, 0.3, 0.3, 0.5),  # More transparent buttons
            'button_text': (1, 1, 1, 1),
            'input_bg': (0.25, 0.25, 0.25, 0.7),
            'glow_color': (0.4, 0.4, 0.8, 0.3)  # Soft glow for dark theme
        }
    }
}

# Debug font path
if os.path.exists(CONFIG['fonts']['default']):
    Logger.info(f"Font: Found Vazir.ttf at {CONFIG['fonts']['default']}")
else:
    Logger.warning(f"Font: Vazir.ttf not found at {CONFIG['fonts']['default']}, falling back to {CONFIG['fonts']['fallback']}")

class GlowButton(Button):
    """Custom button with glow effect."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_glow, pos=self.update_glow)
        self.update_glow()

    def update_glow(self, *args):
        """Update the glow effect based on button size and position."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*CONFIG['themes'][self.parent.theme]['glow_color'] if hasattr(self.parent, 'theme') else (0.8, 0.8, 1, 0.3))
            RoundedRectangle(
                pos=(self.pos[0] - 2, self.pos[1] - 2),
                size=(self.size[0] + 4, self.size[1] + 4),
                radius=[dp(5)],
            )
            Color(*self.background_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(5)],
            )

class VirtualKeyboard(Popup):
    """A customizable virtual keyboard with multi-language support and themes."""
    
    theme = StringProperty('light')
    language = StringProperty('EN')
    uppercase = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.title = ''
        self.size_hint = (None, None)
        self.size = (Window.width * 0.9, dp(450))
        self.auto_dismiss = False
        self.background = ''
        self.separator_height = 0
        
        self.apply_theme()
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(5), spacing=dp(5))
        
        # Text input
        font = CONFIG['fonts']['default'] if os.path.exists(CONFIG['fonts']['default']) else CONFIG['fonts']['fallback']
        Logger.info(f"Font: Using {font} for TextInput")
        self.username_input = TextInput(
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            font_name=font,
            padding=[dp(10), dp(10)],
            line_height=1.5,
            halign='center',
            background_color=CONFIG['themes'][self.theme]['input_bg']
        )
        main_layout.add_widget(self.username_input)
        
        # Keyboard layout
        self.keyboard_layout = BoxLayout(orientation='vertical', padding=dp(5), spacing=dp(5))
        self.build_keyboard()
        main_layout.add_widget(self.keyboard_layout)
        
        # Close button
        close_btn_text = 'Close' if self.language == 'EN' else 'بستن'
        close_btn = GlowButton(
            text=close_btn_text,
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            font_size=dp(16),
            font_name=font,
            background_color=CONFIG['themes'][self.theme]['button_bg'],
            color=CONFIG['themes'][self.theme]['button_text']
        )
        close_btn.bind(on_press=self.dismiss)
        
        close_container = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint_y=None, height=dp(60))
        close_container.add_widget(close_btn)
        main_layout.add_widget(close_container)
        
        self.content = main_layout
        
        # Animation for opening
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self)
    
    def apply_theme(self):
        """Apply the selected theme to the keyboard."""
        self.background_color = CONFIG['themes'][self.theme]['background']
    
    def build_keyboard(self):
        """Build the keyboard layout based on the selected language."""
        self.keyboard_layout.clear_widgets()
        current_layout = CONFIG['languages'][self.language]
        font = CONFIG['fonts']['default'] if os.path.exists(CONFIG['fonts']['default']) else CONFIG['fonts']['fallback']
        Logger.info(f"Font: Using {font} for keyboard buttons")
        
        for row in current_layout:
            row_layout = BoxLayout(orientation='horizontal', spacing=dp(2), size_hint_y=None, height=dp(40))
            for char in row:
                text = char.upper() if self.uppercase else char
                btn = GlowButton(
                    text=text,
                    size_hint=(1, None),
                    height=dp(40),
                    font_size=dp(16),
                    font_name=font,
                    background_color=CONFIG['themes'][self.theme]['button_bg'],
                    color=CONFIG['themes'][self.theme]['button_text']
                )
                btn.bind(on_press=self.key_pressed)
                row_layout.add_widget(btn)
            self.keyboard_layout.add_widget(row_layout)
        
        # Special buttons
        special_row = BoxLayout(orientation='horizontal', spacing=dp(2), size_hint_y=None, height=dp(40))
        buttons = [
            ('del', self.backspace_pressed, 1),
            ('space', self.space_pressed, 2),
            ('EN/FA/AR/NUM', self.toggle_language, 1),
            ('ABC/abc', self.toggle_case, 1),
            ('Theme', self.toggle_theme, 1),
            ('Enter', self.on_submit, 1)
        ]
        
        for label, callback, stretch in buttons:
            btn = GlowButton(
                text=label,
                size_hint=(stretch, None),
                height=dp(40),
                font_size=dp(14),
                font_name=font,
                background_color=CONFIG['themes'][self.theme]['button_bg'],
                color=CONFIG['themes'][self.theme]['button_text']
            )
            btn.bind(on_press=callback)
            special_row.add_widget(btn)
        
        self.keyboard_layout.add_widget(special_row)
    
    def key_pressed(self, instance):
        """Handle key press events."""
        if len(self.username_input.text) < 20:
            self.username_input.text += instance.text
        self.username_input.focus = True
    
    def space_pressed(self, instance):
        """Handle space key press."""
        if len(self.username_input.text) < 20:
            self.username_input.text += ' '
        self.username_input.focus = True
    
    def backspace_pressed(self, instance):
        """Handle backspace key press."""
        if self.username_input.text:
            self.username_input.text = self.username_input.text[:-1]
        self.username_input.focus = True
    
    def toggle_language(self, instance):
        """Toggle between available languages."""
        languages = list(CONFIG['languages'].keys())
        current_idx = languages.index(self.language)
        self.language = languages[(current_idx + 1) % len(languages)]
        self.build_keyboard()
    
    def toggle_case(self, instance):
        """Toggle between uppercase and lowercase."""
        self.uppercase = not self.uppercase
        self.build_keyboard()
    
    def toggle_theme(self, instance):
        """Toggle between light and dark themes."""
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.apply_theme()
        self.build_keyboard()
    
    def on_submit(self, instance):
        """Handle form submission."""
        username = self.username_input.text.strip()
        print(f"Submitted: {username}")
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *args: self.dismiss())
        anim.start(self)

class KeyboardApp(App):
    """Main Kivy application for the virtual keyboard."""
    
    def build(self):
        # Create a root layout with transparent background
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        with root.canvas.before:
            Color(1, 1, 1, 0.1)  # Transparent background for root
            Rectangle(pos=root.pos, size=root.size)
        
        # Add a button to open the keyboard
        font = CONFIG['fonts']['default'] if os.path.exists(CONFIG['fonts']['default']) else CONFIG['fonts']['fallback']
        Logger.info(f"Font: Using {font} for open button")
        open_button = GlowButton(
            text='Open Virtual Keyboard',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            font_name=font,
            background_color=CONFIG['themes']['light']['button_bg'],
            color=CONFIG['themes']['light']['button_text']
        )
        open_button.bind(on_press=self.open_keyboard)
        root.add_widget(open_button)
        
        return root
    
    def open_keyboard(self, instance):
        """Open the virtual keyboard popup."""
        keyboard = VirtualKeyboard()
        keyboard.open()

if __name__ == '__main__':
    KeyboardApp().run()