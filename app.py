import argparse
import sys
import time
import warnings
from argparse import RawTextHelpFormatter

import PySimpleGUI as sg
import pyperclip
import translators as ts
from pynput.keyboard import Key, Controller

warnings.filterwarnings("error")

epilog = """examples:
    app --show-themes
    app --selected-text
    app -bf Arial -tf "Lucida Console" -lf En -lt Ru Hello, world!
    app -t Default -bf "Arial 13" -tf "Lucida Console 13" -lf English -lt Russian --nl2sp Hello, world!
    app --theme Default --button-font "Arial 13" --text-font "'Lucida Console' 13" --language-from English --language-to Russian --nl2sp Hello, world!
    app -t Default -bf "Roboto,arial,sans-serif 12" -tf "Roboto,RobotoDraft,Helvetica,Arial,sans-serif 12" -lf English -lt Russian --nl2sp Hello, world!
"""

parser = argparse.ArgumentParser(prog='app', description="Text translator",
                                 epilog=epilog, formatter_class=RawTextHelpFormatter)
parser.add_argument("-t", "--theme", metavar="theme", type=str, nargs="?", default=None,
                    help="PySimpleGUI theme")
parser.add_argument("-bf", "--button-font", metavar="button_font", type=str, nargs="?", default="\"Arial 12\"",
                    help="button font, default: \"\'Arial\' 12\"")
parser.add_argument("-tf", "--text-font", metavar="text_font", type=str, nargs="?", default="\"Lucida Console\" 12",
                    help="text font, default: \"\'Lucida Console\' 12\"")
parser.add_argument("-lf", "--language-from", metavar="language_from", type=str, nargs="?", default='auto',
                    help="source language, ex. \"english\" or \"en\", default: \"auto\"")
parser.add_argument("-lt", "--language-to", metavar="language_to", type=str, nargs="?", default='ru',
                    help="target language, ex. \"russian\" or \"ru\", default: \"ru\"")
parser.add_argument("--nl2sp", action='store_true', default=False,
                    help="replace newline with space")
parser.add_argument("--show-themes", action='store_true', default=False,
                    help="show PySimpleGUI themes")
parser.add_argument("--selected-text", action='store_true', default=False,
                    help="emulates pressing Ctrl+C and gets the text to be translated from the clipboard "
                         "(previous clipboard text data is restored)")
parser.add_argument("--from-clipboard", action='store_true', default=False,
                    help="gets the text to be translated from the clipboard")
parser.add_argument("text", metavar="text", type=str, nargs="*", default=None,
                    help="example: app <text>")

try:
    args = parser.parse_args()
except:
    sys.exit(1)

if args.from_clipboard:
    args.text = pyperclip.paste()
elif args.selected_text:
    data = pyperclip.paste()
    keyboard = Controller()
    keyboard.press(Key.ctrl.value)
    keyboard.press('c')
    keyboard.release('c')
    keyboard.release(Key.ctrl.value)
    time.sleep(1)
    args.text = pyperclip.paste()
    pyperclip.copy(data)

args.button_font = args.button_font.replace("'", '"')
args.text_font = args.text_font.replace("'", '"')

splitted = args.button_font.split()
b0 = len(splitted) > 0 and not splitted[-1].isdigit()
b1 = len(splitted) > 0 and splitted[0][0] != '"'
b2 = len(splitted) >= 1 and b0 and splitted[-1][-1] != '"' or len(splitted) > 1 and not b0 and splitted[-2][-1] != '"'
if b0 or b1 or b2:
    if len(splitted) >= 2 and (b1 or b2):
        p = None if b0 else -1
        splitted = ['"' * b1 + ' '.join(splitted[:p]) + '"' * b2] + [splitted[-1]] * (p == -1)
    elif len(splitted) == 1:
        splitted = ['"' * b1 + ' '.join(splitted) + '"' * b2]
    splitted += ['12'] * b0
args.button_font = ' '.join(splitted)

splitted = args.text_font.split()
b0 = len(splitted) > 0 and not splitted[-1].isdigit()
b1 = len(splitted) > 0 and splitted[0][0] != '"'
b2 = len(splitted) >= 1 and b0 and splitted[-1][-1] != '"' or len(splitted) > 1 and not b0 and splitted[-2][-1] != '"'
if b0 or b1 or b2:
    if len(splitted) >= 2 and (b1 or b2):
        p = None if b0 else -1
        splitted = ['"' * b1 + ' '.join(splitted[:p]) + '"' * b2] + [splitted[-1]] * (p == -1)
    elif len(splitted) == 1:
        splitted = ['"' * b1 + ' '.join(splitted) + '"' * b2]
    splitted += ['12'] * b0
args.text_font = ' '.join(splitted)

args.language_from = args.language_from.lower()
args.language_to = args.language_to.lower()

print(args)

if args.theme is not None:
    sg.theme(args.theme)

if args.show_themes:
    sg.theme_previewer(scrollable=True)
    sys.exit(0)

services = ["google", "deepl", "yandex", "reverso", "bing",
            "alibaba", "argos", "baidu", "caiyun",
            "iciba", "iflytek", "itranslate", "lingvanex", "mglip", "niutrans",
            "papago", "sogou", "tencent", "translateCom", "utibet", "youdao"]
services = list(x for x in services if x in ts.__dict__)

languages_dict = {
    "auto": "auto",
    "afrikaans": "af", "amharic": "am", "arabic": "ar", "azerbaijani": "az", "bashkir": "ba",
    "basque": "eu", "belarusian": "be", "bengali": "bn", "bosnian": "bs", "bulgarian": "bg",
    "catalan": "ca", "cebuano ceb": "Y", "chinese": "zh", "chuvash": "cv", "croatian": "hr",
    "czech": "cs", "danish": "da", "dutch": "nl", "emoji": "emj", "english": "en", "esperanto": "eo",
    "estonian": "et", "fijian": "fj", "filipino": "tl", "finnish": "fi", "french": "fr", "german": "de",
    "greek": "el", "gujarati": "gu", "haitiancreole": "ht", "hebrew": "he", "hindi": "hi", "hungarian": "hu",
    "indonesian": "id", "irish": "ga", "italian": "it", "japanese": "ja", "klingon/tlhingan": "hol",
    "korean": "ko", "latvian": "lv", "lithuanian": "lt", "malagasy": "mg", "malay": "ms", "maltese": "mt",
    "mongolian": "mn", "norwegian": "no", "persian/farsi": "fa", "polish": "pl", "portuguese": "pt",
    "punjabi": "pa", "queretaro otomi": "otq", "romanian": "ro", "russian": "ru", "samoan": "sm",
    "serbian": "sr", "slovak": "sk", "slovenian": "sl", "spanish": "es", "swahili": "sw", "swedish": "sv",
    "tahiti": "ty", "tamil": "ta", "telugu": "te", "thai": "th", "tongan": "to", "turkish": "tr",
    "ukrainian": "uk", "urdu": "ur", "vietnamese": "vi", "welsh": "cy"
}
languages_inv_dict = {v: k for k, v in languages_dict.items()}
languages_from = ["auto", "english", "russian"] + sorted(set(languages_dict) - {"auto", "english", "russian"})
languages_to = ["russian", "english"] + sorted(set(languages_dict) - {"auto", "english", "russian"})

layout = [[sg.InputCombo(values=services, default_value=services[0], readonly=True, font=args.button_font,
                         key="-SERVICES-COMBO-"),
           sg.Combo(values=languages_from, default_value=languages_from[0], readonly=False,
                    font=args.button_font, key="-LANGUAGES-FROM-COMBO-", expand_x=True),
           sg.Combo(values=languages_to, default_value=languages_to[0], readonly=False,
                    font=args.button_font, key="-LANGUAGES-TO-COMBO-", expand_x=True)],
          [sg.Multiline(expand_x=True, expand_y=True, do_not_clear=True, font=args.text_font, key="-FROM-")],
          [sg.Button("Translate", expand_x=True, key="-TRANSLATE-", font=args.button_font),
           sg.Button("Swap", expand_x=False, key="-SWAP-", font=args.button_font, size=(10, None)),
           sg.Checkbox("Replace newline with space", default=args.nl2sp, font=args.button_font, key="-REPLACE-")],
          [sg.Multiline(expand_x=True, expand_y=True, write_only=False, font=args.text_font, key="-TO-")]]

try:
    window = sg.Window("Translator", layout, resizable=True, element_padding=2, margins=(2, 2), size=(600, 400),
                       finalize=True, return_keyboard_events=True)
    window.keep_on_top_set()
except BaseException as e:
    sg.PopupOK(e, title="Error", keep_on_top=True)
    sys.exit(1)

current_language_from = languages_dict.get(args.language_from, args.language_from)
current_language_to = languages_dict.get(args.language_to, args.language_to)
current_language_from = current_language_from if current_language_from in languages_dict.values() else "auto"
current_language_to = current_language_to if current_language_to in languages_dict.values() else "ru"
window['-LANGUAGES-FROM-COMBO-'].update(languages_inv_dict.get(current_language_from, current_language_from))
window['-LANGUAGES-TO-COMBO-'].update(languages_inv_dict.get(current_language_to, current_language_to))

if args.text is not None and args.text:
    text = " ".join(args.text) if isinstance(args.text, list) else args.text
    current_service = "google"
    current_text = text
    current_text = " ".join(current_text.replace('\t', ' ').split()) if args.nl2sp else current_text
    window['-FROM-'].update(current_text)
    try:
        if len(current_text) > 5000:
            raise ValueError(f'Too many characters: {len(current_text)} > 5000')
        result = getattr(ts, current_service)(current_text, current_language_from, current_language_to,
                                              sleep_seconds=1.)
        window['-TO-'].update(str(result))
    except BaseException as e:
        window.keep_on_top_clear()
        sg.PopupOK(e, title="Error", keep_on_top=True)
        window.keep_on_top_set()

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Quit", "Exit"):
        break
    elif event == "-TRANSLATE-":
        current_service = values["-SERVICES-COMBO-"]
        current_language_from = languages_dict.get(values["-LANGUAGES-FROM-COMBO-"],
                                                   values["-LANGUAGES-FROM-COMBO-"])
        current_language_to = languages_dict.get(values["-LANGUAGES-TO-COMBO-"],
                                                 values["-LANGUAGES-TO-COMBO-"])
        current_text = values["-FROM-"]
        current_text = " ".join(current_text.replace('\t', ' ').split()) if values["-REPLACE-"] else current_text
        try:
            if len(current_text) > 5000:
                raise ValueError(f'Too many characters: {len(current_text)} > 5000')
            result = getattr(ts, current_service)(current_text, current_language_from, current_language_to,
                                                  timeout=10., sleep_seconds=0.)
            window['-TO-'].update(str(result))
        except BaseException as e:
            window.keep_on_top_clear()
            sg.PopupOK(e, title="Error", keep_on_top=True)
            window.keep_on_top_set()
    elif event == "-SWAP-":
        text = window['-FROM-'].get()
        window['-FROM-'].update(window['-TO-'].get())
        window['-TO-'].update(text)

window.close()
