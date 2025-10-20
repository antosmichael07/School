'''
Konstanty v Pythonu

Konstanta je vlastně speciální typ proměnné, jejíž hodnota nemůže být změněna.
V Pythonu jsou konstanty obvykle deklarovány a přiřazovány v modulu, který bývá importován do souboru aplikace.
Konstanty jsou pojmenovány velkými písmeny a jednotlivá slova jsou oddělována podtržítky.
'''

EARTH_GRAVITY = 9.81 #? normální pozemské tíhové zrychlení
MOON_GRAVITY = 1.62 #? měsíční gravitace
SPEED_OF_LIGHT = 299792458 #? rychlost světla ve vakuu
SPEED_OF_SOUND = 343 #? rychlost zvuku při teplotě 20 °C v suchém vzduchu

''' 
Úkol:
1. Doplňte správně hodnoty uvedených konstant.
2. Doplňte physics.py o několik výpočtových funkcí (opatřené docstrings), v nichž využijete minimálně všechny výše uvedené konstanty.
Samozřejmě můžete své řešení rozšířit i o jiné fyzikální konstanty.
3. Vytvořte z tohoto souboru samostatný modul v Pythonu podle návodu, který si sami najdete na internetu.      
4. Vytvořte vlastní aplikaci myapp.py, do níž tento modul importujte. Demonstrujte v ní na jednoduchých příkladech využití vámi
připravených funkcí.  
'''

def weight_on_earth(mass: float) -> float:
    """Vrátí váhu tělesa na Zemi v newtonech."""
    return mass * EARTH_GRAVITY


def weight_on_moon(mass: float) -> float:
    """Vrátí váhu tělesa na Měsíci v newtonech."""
    return mass * MOON_GRAVITY


def time_for_light(distance: float) -> float:
    """Vrátí dobu (v sekundách), za kterou světlo urazí danou vzdálenost."""
    return distance / SPEED_OF_LIGHT


def time_for_sound(distance: float) -> float:
    """Vrátí dobu (v sekundách), za kterou zvuk urazí danou vzdálenost."""
    return distance / SPEED_OF_SOUND
