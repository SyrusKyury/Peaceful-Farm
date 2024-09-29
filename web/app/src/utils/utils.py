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
    'Napoletano', 'Pizzaiolo', 'San Gennaro', 'Vesuvio', 'Mandolino', 'Lavezzi', 'Maradona', 
    'Hamsik', 'Mertens', 'Insigne', 'D10S', 'Cavallo','Babà', 'Pulcinella', 'Limoncello',
    'Cane', 'Asino', 'Gatto', 'Sofia', 'Raffaele', 'Lorenzo', 'Alessio', 'Federico', 'Luca', 'Gennaro',
    'Drago', 'Spalletti', 'Koulibaly', 'ADL', 'Antonio Conte', 'Kim Kim Kim', 'Kvara'
]


adjectives = [
    'incazzato', 'monello', 'assassino', 'pazzo', 'scatenato', 'furioso', 'ubriaco', 'sbronzo', 'magico',
    'invisibile', 'misericordioso', 'veloce', 'ignorante', 'arrabbiato', 'godurioso', 'sorridente',
    'drogato', 'malato del napoli', 'dopo aver pippato', 'dopo una sbronza', 'dopo aver mangiato la diavola',
    'dopo aver flaggato', 'sul motorino senza casco', 'con la maglia del napoli', 'con la maglia di Maradona',
    'che mangia il ragù di mammà', 'allo stadio', 'che guarda la partita in streaming', 'che scappa in Messico',
    'divino', 'santo', 'sacro', 'misterioso', 'che picchia uno juventino', 'inseguito da un vuo cumprà',
    'con tre persone sul motorino', 'che festeggia lo scudetto del Napoli', 'che compra il cocco bello',
    'picchia Agnelli', 'fa cacca nello Juventus Stadium', 'esulta per un gol', 'fa la dab con Obama',
    'che insulta la Meloni', 'scappa col motorino', 'scippa la borsa a una vecchietta'
]    

def generate_exploit_name():
    return random.choice(nouns) + ' ' + random.choice(adjectives) + ' ' + str(random.randint(1, 10)) + str(random.randint(1, 10)) + str(random.randint(1, 10)) + str(random.randint(1, 10))

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