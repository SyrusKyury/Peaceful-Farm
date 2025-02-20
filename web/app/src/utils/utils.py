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
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

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

def plot_flag_statistics(accepted: list[int], rejected: list[int], type: str, value: str, t1: datetime, t2: datetime) -> bytes:
    # Bar width
    width = 0.35

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(accepted))
    ax.bar(x, accepted, width, color='#0D8D39', label='Accepted')
    ax.bar([i + width for i in x], rejected, width, color='#55A5C0', label='Rejected')

    # Setting the x-axis labels
    ax.set_xlabel('Ticks')
    ax.set_ylabel('Number of flags')
    ax.set_title(f"Flags statistics for {type} {value} from {t1.strftime('%H:%M')} to {t2.strftime('%H:%M')}")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    # Saving the plot to a buffer
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)  # Close the figure to free up memory

    return base64.b64encode(img.read()).decode('utf-8')


def datetime_to_int(t: datetime) -> int:
    return t.hour * 3600 + t.minute * 60 + t.second