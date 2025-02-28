# --------------------------------------------------------------------------------------------------------------------------
# Desc: This file contains multiple snippets of code that are used to execute specific tasks. The code snippets are used to
# generate exploit names and to plot flag statistics.
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/utils/utils.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------
import random

nouns = [
    'panda', 'cow', 'dog', 'cat', 'elephant', 'tiger', 'lion', 'cheetah', 'wolf', 'fox', 'bear', 'penguin', 'dolphin',
    'whale', 'shark', 'octopus', 'squid', 'jellyfish', 'starfish', 'seahorse', 'crab', 'lobster', 'scorpion', 'spider',
    'ant', 'bee', 'wasp', 'butterfly', 'moth', 'dragonfly', 'grasshopper', 'beetle', 'ladybug', 'fly', 'mosquito',
    'cockroach', 'mantis', 'cicada', 'aphid', 'cricket', 'termite', 'antelope', 'buffalo', 'camel', 'deer', 'giraffe',
    'hippopotamus', 'horse', 'kangaroo', 'koala', 'leopard', 'monkey', 'orangutan', 'panda', 'penguin', 'rhinoceros',
    'sloth', 'tiger', 'zebra', 'bat', 'bear', 'beaver', 'boar', 'cat', 'chinchilla', 'chipmunk', 'coyote', 'dog',
    'ferret', 'fox', 'gerbil', 'guinea pig', 'hamster', 'hedgehog', 'mouse', 'rabbit', 'rat', 'squirrel', 'weasel',
    'badger', 'otter', 'raccoon', 'skunk', 'wolf', 'blue jay', 'cardinal', 'crow', 'dove', 'eagle', 'falcon', 'finch',
    'goose', 'hawk', 'hummingbird', 'kingfisher', 'owl', 'parrot', 'peacock', 'pelican', 'penguin', 'robin', 'sparrow'
]


adjectives = [
    'crazy', 'lazy', 'sleepy', 'happy', 'sad', 'angry', 'hungry', 'thirsty', 'dirty', 'clean', 'fast', 'slow', 'big',
    'small', 'tiny', 'huge', 'fat', 'skinny', 'short', 'tall', 'long', 'short', 'old', 'young', 'new', 'fresh', 'rotten',
    'hot', 'cold', 'warm', 'cool', 'dry', 'wet', 'damp', 'moist', 'hard', 'soft', 'rough', 'smooth', 'sharp', 'dull',
    'clean', 'dirty', 'clear', 'cloudy', 'foggy', 'sunny', 'rainy', 'windy', 'stormy', 'snowy', 'icy', 'slippery',
    'noisy', 'quiet', 'loud', 'soft', 'sweet', 'sour', 'bitter', 'salty', 'spicy', 'tasty', 'delicious', 'yummy',
    'disgusting', 'gross', 'nasty', 'beautiful', 'ugly', 'pretty', 'handsome', 'cute', 'adorable', 'lovely', 'nice',
    'mean', 'evil', 'wicked', 'good', 'bad', 'great', 'awesome', 'fantastic', 'amazing', 'wonderful', 'excellent'
]    

def generate_exploit_name():
    return random.choice(adjectives) + ' ' + random.choice(nouns)