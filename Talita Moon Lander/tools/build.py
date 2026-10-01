"""Embed the Talita face sprites into the game. Run from the project folder:  python3 tools/build.py"""
import base64, json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
names = {'neutral': '1_neutral', 'happy': '2_happy', 'surprised': '3_surprised', 'angry': '4_angry',
         'hurt': '5_hurt', 'sad': '6_sad', 'super': '7_super'}
faces = {k: 'data:image/png;base64,' + base64.b64encode(open(os.path.join(root, 'assets', 'faces', f'talita_{v}_32.png'), 'rb').read()).decode()
         for k, v in names.items()}
src = open(os.path.join(root, 'tools', 'index_template.html'), encoding='utf-8').read()
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(src.replace('/*FACES*/', json.dumps(faces)))
print('index.html rebuilt')
