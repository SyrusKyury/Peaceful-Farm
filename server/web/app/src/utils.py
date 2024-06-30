import random

nouns = [
    'Napoletano', 'Pizzaiolo', 'San Gennaro', 'Vesuvio', 'Mandolino', 'Lavezzi', 'Maradona', 
    'Hamsik', 'Mertens', 'Insigne', 'D10S', 'Cavallo','Babà', 'Pulcinella', 'Limoncello',
    'Cane', 'Asino', 'Gatto', 'Sofia', 'Raffaele', 'Lorenzo', 'Alessio', 'Federico', 'Luca', 'Gennaro',
    'Drago'
]


adjectives = [
    'incazzato', 'monello', 'assassino', 'pazzo', 'scatenato', 'furioso', 'ubriaco', 'sbronzo', 'magico',
    'invisibile', 'misericordioso', 'veloce', 'ignorante', 'arrabbiato', 'godurioso', 'sorridente',
    'drogato', 'malato del napoli', 'dopo aver pippato', 'dopo una sbronza', 'dopo aver mangiato la pizza',
    'dopo aver flaggato', 'sul motorino senza casco', 'con la maglia del napoli', 'con la maglia di Maradona',
    'che mangia il ragù di mammà', 'allo stadio', 'che guarda la partita in streaming', 'che scappa in Messico',
    'divino', 'santo', 'sacro', 'misterioso', 'che picchia uno juventino', 'inseguito da un vuo cumprà',
    'con tre persone sul motorino', 'che festeggia lo scudetto del Napoli', 'che compra il cocco bello'
]    

def generate_exploit_name():
    return random.choice(nouns) + ' ' + random.choice(adjectives) + ' ' + str(random.randint(1, 10000))