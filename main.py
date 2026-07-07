import os
import sys
import struct
__version__ = '0.3'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase
from PIL import Image as PILImage
import threading
#from tensorflow.lite.python.interpreter import Interpreter

if 'android' in sys.modules or os.path.exists('/sdcard/'):
    try:
        LabelBase.register(name='droidsans', fn_regular='/system/fonts/DroidSansFallback.ttf')
        FONT_NAME = 'droidsans'
    except:
        FONT_NAME = 'Roboto'
else:
    FONT_NAME = 'Roboto'

IMAGENET_LABELS = {
    # Fish / Marine
    0: 'tench', 1: 'goldfish', 2: 'great_white_shark', 3: 'tiger_shark',
    4: 'hammerhead_shark', 5: 'electric_ray', 6: 'stingray',
    7: 'cock', 8: 'hen', 9: 'ostrich', 10: 'brambling',
    11: 'goldfinch', 12: 'house_finch', 13: 'junco',
    14: 'indigo_bunting', 15: 'robin', 16: 'bulbul',
    17: 'jay', 18: 'magpie', 19: 'chickadee',
    20: 'duck', 21: 'hen', 22: 'cock', 23: 'ptarmigan',
    24: 'peacock', 25: 'quail', 26: 'partridge',
    # Birds (continued)
    80: 'black_grouse', 81: 'ptarmigan', 82: 'ruffed_grouse',
    83: 'prairie_chicken', 84: 'peacock', 85: 'quail',
    86: 'partridge', 87: 'grey_whale', 88: 'killer_whale',
    89: 'dugong', 90: 'sea_lion',
    96: 'howler_monkey', 97: 'capuchin', 98: 'spider_monkey',
    99: 'squirrel_monkey', 100: 'woolly_monkey',
    # Dog breeds
    207: 'golden_retriever', 208: 'Labrador_retriever',
    209: 'Chesapeake_Bay_retriever', 210: 'curly_coated_retriever',
    211: 'flat_coated_retriever', 212: 'Nova_Scotia_duck_tolling_retriever',
    213: 'German_short-haired_pointer', 214: 'German_wire-haired_pointer',
    215: 'vizsla', 216: 'weimaraner', 217: 'griffon',
    218: 'Chihuahua', 219: 'Japanese_Chin', 220: 'Maltese',
    221: 'Pekingese', 222: 'Shih_Tzu', 223: 'King_Charles_spaniel',
    224: 'Papillon', 225: 'toy_terrier', 226: 'Rhodesian_ridgeback',
    227: 'Afghan_hound', 228: 'basset_hound', 229: 'beagle',
    230: 'bloodhound', 231: 'bluetick', 232: 'black_and_tan_coonhound',
    233: 'otterhound', 234: 'Norwegian_elkhound', 235: 'German_shepherd',
    236: 'Belgian_sheepdog', 237: 'Malinois', 238: 'briard',
    239: 'kelpie', 240: 'komondor', 241: 'Old_English_sheepdog',
    242: 'Shetland_sheepdog', 243: 'collie', 244: 'border_collie',
    245: 'Bouvier_des_Flandres', 246: 'Rottweiler', 247: 'Doberman',
    248: 'miniature_pinscher', 249: 'Greater_Swiss_Mountain_dog',
    250: 'Bernese_mountain_dog', 251: 'Appenzeller', 252: 'Entlebucher',
    253: 'boxer', 254: 'bull_mastiff', 255: 'tibetan_mastiff',
    256: 'French_bulldog', 257: 'Great_Dane', 258: 'Saint_Bernard',
    259: 'husky', 260: 'malamute', 261: 'Siberian_husky',
    262: 'dalmatian', 263: 'affenpinscher', 264: 'basenji',
    265: 'pug', 266: 'Leonberger', 267: 'Newfoundland',
    268: 'Pyrenean_mountain_dog', 269: 'Samoyed', 270: 'Pomeranian',
    271: 'chow_chow', 272: 'keeshond', 273: 'Brabancon_griffon',
    274: 'Pembroke_Corgi', 275: 'Cardigan_Corgi', 276: 'toy_poodle',
    277: 'miniature_poodle', 278: 'standard_poodle', 279: 'Mexican_hairless',
    # Cats & Big Cats
    281: 'tabby_cat', 282: 'tiger_cat', 283: 'Persian_cat',
    284: 'Siamese_cat', 285: 'Egyptian_cat',
    286: 'cougar', 287: 'lynx', 288: 'leopard',
    289: 'snow_leopard', 290: 'jaguar',
    291: 'lion', 292: 'tiger', 293: 'cheetah', 294: 'lion',
    # Bears
    295: 'brown_bear', 296: 'American_black_bear', 297: 'polar_bear',
    298: 'sloth_bear', 299: 'mongoose', 300: 'meerkat',
    301: 'tiger_beetle', 302: 'ladybug', 303: 'ground_beetle',
    304: 'longhorn_beetle', 305: 'leaf_beetle', 306: 'dung_beetle',
    307: 'rhinoceros_beetle', 308: 'weevil', 309: 'fly',
    310: 'bee', 311: 'ant', 312: 'grasshopper',
    313: 'cricket', 314: 'walking_stick', 315: 'cockroach',
    316: 'mantis', 317: 'cricket', 318: 'cicada',
    319: 'leafhopper', 320: 'lacewing',
    325: 'ringlet', 326: 'monarch_butterfly', 327: 'swallowtail',
    328: 'cabbage_butterfly', 329: 'sulphur_butterfly',
    330: 'lycaenid_butterfly',
    340: 'zebra', 341: 'pig', 342: 'wild_boar',
    343: 'warthog', 344: 'hippopotamus', 345: 'ox',
    346: 'water_buffalo', 347: 'bison', 348: 'ram',
    349: 'bighorn_sheep', 350: 'mountain_goat', 351: 'alpaca',
    352: 'llama', 353: 'gazelle', 354: 'camel',
    355: 'llama', 356: 'giraffe', 357: 'elephant',
    358: 'rhinoceros', 359: 'tapir',
    360: 'cat', 361: 'dog', 362: 'kangaroo',
    363: 'koala', 364: 'wombat', 365: 'jellyfish',
    366: 'sea_anemone', 367: 'brain_coral', 368: 'flatworm',
    369: 'nematode', 370: 'conch', 371: 'snail',
    372: 'slug', 373: 'sea_slug', 374: 'chiton',
    375: 'chambered_nautilus', 376: 'crab', 377: 'lobster',
    378: 'spider', 379: 'scorpion', 380: 'crayfish',
    381: 'hermit_crab', 382: 'isopod', 383: 'white_stork',
    384: 'black_stork', 385: 'spoonbill', 386: 'African_elephant',
    387: 'Indian_elephant', 388: 'bear', 389: 'polar_bear',
    390: 'badger', 391: 'weasel', 392: 'mink',
    393: 'ferret', 394: 'otter', 395: 'skunk',
    396: 'badger', 397: 'horse', 398: 'sorrel_horse',
    399: 'arabian_horse', 400: 'pony',
    401: 'zebra', 402: 'pig', 403: 'wild_boar',
    404: 'warthog',
    408: 'fox', 409: 'wolf', 410: 'coyote',
    411: 'dingo', 412: 'red_wolf', 413: 'hyena',
    414: 'fox', 415: 'bear', 416: 'grizzly_bear',
    417: 'Kodiak_bear',
    418: 'squirrel', 419: 'chipmunk', 420: 'gopher',
    421: 'beaver', 422: 'guinea_pig', 423: 'porcupine',
    424: 'hedgehog', 425: 'rabbit', 426: 'hare',
    427: 'armadillo', 428: 'pangolin', 429: 'anteater',
    430: 'sloth', 431: 'lemur', 432: 'indri',
    433: 'monkey', 434: 'gorilla', 435: 'chimpanzee',
    436: 'orangutan', 437: 'gibbon', 438: 'siamang',
    439: 'tamarin', 440: 'marmoset', 441: 'spider_monkey',
    442: 'howler_monkey', 443: 'capuchin', 444: 'squirrel_monkey',
    445: 'woolly_monkey', 446: 'macaque', 447: 'baboon',
    448: 'mandrill', 449: 'proboscis_monkey', 450: 'langur',
    451: 'colobus', 452: 'monkey',
    453: 'crocodile', 454: 'alligator', 455: 'gavial',
    456: 'lizard', 457: 'gecko', 458: 'komodo_dragon',
    459: 'iguana', 460: 'chameleon', 461: 'snake',
    462: 'python', 463: 'cobra', 464: 'viper',
    465: 'rattlesnake', 466: 'turtle', 467: 'tortoise',
    468: 'terrapin', 469: 'frog', 470: 'toad',
    471: 'salamander', 472: 'newt', 473: 'axolotl',
    474: 'frog', 475: 'tadpole',
    476: 'eel', 477: 'salmon', 478: 'trout',
    479: 'pike', 480: 'catfish', 481: 'goldfish',
    482: 'angelfish', 483: 'clownfish', 484: 'pufferfish',
    485: 'sturgeon', 486: 'swordfish', 487: 'whale_shark',
    488: 'manta_ray', 489: 'stingray', 490: 'octopus',
    491: 'squid', 492: 'cuttlefish', 493: 'nautilus',
    494: 'jellyfish', 495: 'starfish', 496: 'sea_urchin',
    497: 'sea_cucumber', 498: 'coral', 499: 'sponge',
}


class AnimalRecognitionApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interpreter = None
        self.captured_image_path = None
        self.is_android = False

    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)

        if 'android' in sys.modules or os.path.exists('/sdcard/'):
            self.is_android = True
            try:
                from plyer import camera as plyer_camera
                self.plyer_camera = plyer_camera
            except ImportError:
                pass

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=8)

        self.title_label = Label(
            text='Animal Recognition',
            font_name=FONT_NAME,
            font_size='22sp',
            bold=True,
            size_hint=(1, None),
            height=45,
            color=(0.2, 0.2, 0.8, 1)
        )
        main_layout.add_widget(self.title_label)

        self.image_widget = Image(
            source='',
            size_hint=(1, 0.55),
            allow_stretch=True
        )
        main_layout.add_widget(self.image_widget)

        self.result_label = Label(
            text='Click "Camera" to start',
            font_name=FONT_NAME,
            font_size='15sp',
            size_hint=(1, 0.25),
            halign='center',
            valign='middle',
            color=(0.3, 0.3, 0.3, 1)
        )
        main_layout.add_widget(self.result_label)

        button_layout = BoxLayout(size_hint=(1, None), height=55, spacing=10)

        self.capture_btn = Button(
            text='Camera',
            font_name=FONT_NAME,
            font_size='18sp',
            background_color=(0.2, 0.6, 1, 1)
        )
        self.capture_btn.bind(on_press=self.take_photo)
        button_layout.add_widget(self.capture_btn)

        self.recognize_btn = Button(
            text='Recognize',
            font_name=FONT_NAME,
            font_size='18sp',
            background_color=(0.2, 0.8, 0.4, 1),
            disabled=True
        )
        self.recognize_btn.bind(on_press=self.recognize_animal)
        button_layout.add_widget(self.recognize_btn)

        main_layout.add_widget(button_layout)

        return main_layout

    def on_start(self):
        Clock.schedule_once(lambda dt: threading.Thread(target=self.load_model, daemon=True).start(), 0)

    def load_model(self):
        try:
            Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', 'Loading model...'), 0)

            if self.is_android:
                import os as os_module
                model_path = os_module.path.join(os_module.path.dirname(os_module.path.abspath(__file__)), 'resnet50.tflite')

                if not os_module.path.exists(model_path):
                    possible_paths = [
                        os_module.path.join('/data/data', os_module.path.basename(os_module.path.dirname(os_module.path.abspath(__file__))), 'files', 'app', 'resnet50.tflite'),
                        os_module.path.join(os_module.path.dirname(os_module.path.abspath(__file__)), '..', 'resnet50.tflite'),
                    ]
                    found = False
                    for alt_path in possible_paths:
                        alt_path = os_module.path.normpath(alt_path)
                        if os_module.path.exists(alt_path):
                            model_path = alt_path
                            found = True
                            break
                    if not found:
                        raise FileNotFoundError(f'Model not found')

                from tflite_c_api import TFLiteInterpreter
                self.interpreter = TFLiteInterpreter(model_path)
            else:
                try:
                    from tensorflow.lite.python.interpreter import Interpreter
                    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resnet50.tflite')
                    self.interpreter = Interpreter(model_path=model_path)
                    self.interpreter.allocate_tensors()
                except ImportError:
                    raise RuntimeError('Desktop mode requires: pip install tflite-runtime')

            mode = 'Android' if self.is_android else 'Desktop'
            Clock.schedule_once(lambda dt: setattr(
                self.result_label, 'text',
                f'Model loaded! ({mode} mode)\nClick "{self.capture_btn.text}" to start'
            ), 0)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            err_msg = f'Model load failed: {str(e)}'
            Clock.schedule_once(lambda dt: setattr(
                self.result_label, 'text', err_msg
            ), 0)

    def take_photo(self, instance):
        if self.is_android:
            self._take_photo_android()
        else:
            self._take_photo_desktop()

    def _take_photo_android(self):
        """Android: Camera without EXTRA_OUTPUT, get bitmap from result"""
        try:
            from jnius import autoclass
            import android.activity

            Intent = autoclass('android.content.Intent')
            MediaStore = autoclass('android.provider.MediaStore')
            context = self._get_android_activity()

            # 不传 EXTRA_OUTPUT -> 相机返回缩略图 Bitmap
            intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)

            android.activity.bind(on_activity_result=self._on_camera_result)
            context.startActivityForResult(intent, 0)
            self.result_label.text = '📷 Taking photo...'

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.result_label.text = f'Camera failed: {str(e)}'

    def _get_android_activity(self):
        from jnius import autoclass
        return autoclass('org.kivy.android.PythonActivity').mActivity

    def _on_camera_result(self, request_code, result_code, intent):
        """Camera finished: save bitmap to local file"""
        import android.activity
        android.activity.unbind(on_activity_result=self._on_camera_result)

        if result_code == -1:  # RESULT_OK
            try:
                from jnius import autoclass
                extras = intent.getExtras()
                if extras is None or not extras.containsKey('data'):
                    self.result_label.text = 'No image from camera'
                    return

                bitmap = extras.get('data')
                if bitmap is None:
                    self.result_label.text = 'No image from camera'
                    return

                # 保存缩略图到私有目录（224x224 识别足够用）
                context = self._get_android_activity()
                photo_dir = context.getExternalFilesDir(None).getAbsolutePath()
                photo_path = os.path.join(photo_dir, 'temp_animal.jpg')

                FileOutputStream = autoclass('java.io.FileOutputStream')
                Bitmap_CompressFormat = autoclass('android.graphics.Bitmap$CompressFormat')

                out = FileOutputStream(photo_path)
                bitmap.compress(Bitmap_CompressFormat.JPEG, 95, out)
                out.close()

                self.on_photo_taken(photo_path)
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.result_label.text = f'Camera result error: {str(e)}'
        else:
            self.result_label.text = 'Camera cancelled'

    def _take_photo_desktop(self):
        """Desktop: file chooser"""
        try:
            from plyer import filechooser
            filechooser.open_file(filters=['*.jpg', '*.png', '*.jpeg'],
                                  on_selection=self._on_file_selected)
        except Exception as e:
            self.result_label.text = f'Select failed: {str(e)}'

    def _on_file_selected(self, selection):
        if selection:
            self.on_photo_taken(selection[0])

    def on_photo_taken(self, filename):
        self.captured_image_path = filename
        # 强制刷新图片显示（先清空再设置，再 reload）
        self.image_widget.source = ''
        Clock.schedule_once(lambda dt: self._show_image(filename), 0.1)
        self.recognize_btn.disabled = False
        self.result_label.text = '📸 Photo taken, click "Recognize"'

    def _show_image(self, filename):
        self.image_widget.source = filename
        self.image_widget.reload()

    def recognize_animal(self, instance):
        if not self.captured_image_path or not self.interpreter:
            self.result_label.text = 'Please select image or wait for model loading'
            return

        try:
            self.result_label.text = 'Recognizing...'
            Clock.schedule_once(lambda dt: threading.Thread(target=self._do_recognition, daemon=True).start(), 0.1)
        except Exception as e:
            self.result_label.text = f'Recognition failed: {str(e)}'

    def _preprocess(self, img_path):
        img = PILImage.open(img_path).convert('RGB').resize((224, 224))
        # MobileNetV2 preprocessing: scale RGB values from [0,255] to [-1,1]
        pixels = list(img.getdata())  # list of (R, G, B) tuples
        flat = []
        for r, g, b in pixels:
            flat.append(r / 127.5 - 1.0)
            flat.append(g / 127.5 - 1.0)
            flat.append(b / 127.5 - 1.0)
        return flat  # list of 224*224*3 = 150528 floats

    def _do_recognition(self):
        try:
            flat_data = self._preprocess(self.captured_image_path)
            NUM_CLASSES = 1000

            if self.is_android:
                import ctypes
                input_array = (ctypes.c_float * len(flat_data))(*flat_data)
                output_array = (ctypes.c_float * NUM_CLASSES)()
                self.interpreter.run(input_array, output_array)
                predictions = list(output_array)
            else:
                import numpy as np
                input_details = self.interpreter.get_input_details()
                output_details = self.interpreter.get_output_details()

                input_data = np.array(flat_data, dtype=np.float32).reshape(input_details[0]['shape'])
                self.interpreter.set_tensor(input_details[0]['index'], input_data)
                self.interpreter.invoke()

                output_data = self.interpreter.get_tensor(output_details[0]['index'])
                predictions = output_data[0].tolist()

            # Get top 5 indices (pure Python argsort)
            top_indices = sorted(range(NUM_CLASSES), key=lambda i: predictions[i], reverse=True)[:5]
            results = [(str(idx), IMAGENET_LABELS.get(idx, f'class_{idx}'), float(predictions[idx])) for idx in top_indices]

            display_text = 'Recognition Results:\n\n'
            horse_found = False
            best_result = None

            for rank, (id, name, score) in enumerate(results):
                confidence = score * 100
                translated_name = self.translate_animal_name(name)

                if self.is_horse(name):
                    horse_found = True
                    emoji = '[OK]'
                    if best_result is None or confidence > best_result[1]:
                        best_result = (translated_name, confidence)
                else:
                    emoji = ''

                display_text += f'{rank + 1}. {translated_name}\n   Confidence: {confidence:.2f}% {emoji}\n\n'

            if horse_found and best_result:
                display_text += f'\nSuccess: {best_result[0]} (Confidence: {best_result[1]:.2f}%)'

            Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', display_text), 0)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            err_msg = f'Recognition failed: {str(e)}'
            Clock.schedule_once(lambda dt: setattr(
                self.result_label, 'text', err_msg
            ), 0)

    def is_horse(self, name):
        horse_keywords = ['sorrel', 'arabian', 'quarter_horse', 'horse']
        return any(keyword in name.lower() for keyword in horse_keywords)

    def translate_animal_name(self, name):
        translations = {
            'sorrel': 'Horse (Sorrel)',
            'arabian': 'Horse (Arabian)',
            'quarter_horse': 'Horse (Quarter Horse)',
            'horse': 'Horse',
            'horse_cart': 'Horse Cart',
            'hartebeest': 'Antelope',
            'dog': 'Dog',
            'retriever': 'Retriever Dog',
            'shepherd': 'Shepherd Dog',
            'cat': 'Cat',
            'tabby': 'Tabby Cat',
            'elephant': 'Elephant',
            'lion': 'Lion',
            'tiger': 'Tiger',
            'cheetah': 'Cheetah',
            'bear': 'Bear',
            'polar_bear': 'Polar Bear',
            'bird': 'Bird',
            'peacock': 'Peacock',
            'duck': 'Duck',
            'fish': 'Fish',
            'shark': 'Shark',
        }

        for key, value in translations.items():
            if key in name.lower():
                return value

        return name


if __name__ == '__main__':
    AnimalRecognitionApp().run()