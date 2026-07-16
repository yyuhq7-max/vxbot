import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import random
import asyncio
import logging
import threading
import time
import aiohttp
from typing import Optional
from http.server import BaseHTTPRequestHandler, HTTPServer

# ==================== LOGGING ====================
# Logs horodatés et bien visibles dans les logs Render (au lieu de simples print()).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("brainrot-bot")

# ==================== GÉNÉRATEUR "GARAMA" ALÉATOIRE ====================
# 18 lignes tirées aléatoirement (sans ordre particulier) dans GARAMA_LINES,
# + 8 lignes "Dragon Cannelloni" dont la rareté (Gold ou Diamond) est tirée
# aléatoirement à chaque fois.

GARAMA_LINES = [
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Lightning","Green Balloon","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"UFO","Fireworks","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Lightning","Green Balloon","Spider","Explosive"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Brazil","RIP Gravestone","Paint"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Bubblegum","Zombie","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Wet","Fire","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Bubblegum","Fire",":3","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Fire","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Claws","Blue Balloon","Shark Fin","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Bubblegum","Sombrero","Paint"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"UFO","Curacao","Matteo Hat","Sun"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Tie","Explosive","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Nyan","New Zealand",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Glitched","United States","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Glitched","Sun","Sombrero","Paint"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Tie","Zombie","Spider","Blue Egg"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Tie","Glitched","RIP Gravestone",":3"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"UFO","Zombie","Spider","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Halo","Pink Balloon","Fire","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched",":3","Matteo Hat","Spider"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"UFO","Spain","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Glitched","Bubblegum","Spider","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Glitched","Tie","Explosive","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Wet","Ecuador","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Wet","Fire","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"UFO","Spider","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Disco","Spain",":3"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Zombie","Fire","Spider","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Galactic","Glitched","Shark Fin","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Tie","Brazil","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Zombie","Fire","Jackolantern Pet"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Lucky","Fire","Paint"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"UFO",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Bubblegum","Claws","Reindeer Pet",":3"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Wet","Fire","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Tie","Blue Egg","Fire","Spider"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Lightning","Granny","Spider"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Claws","Czechia","Fire"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Zombie","Green Balloon","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Galactic","Paint","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Nyan","Spider","Aura Shades"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Claws","Orange Egg",":3","Explosive"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Glitched","Jackolantern Pet","Fire"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Glitched","Shark Fin","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Zombie",":3","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Nyan","Algeria","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Wet","Shark Fin","Fire","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Galactic","Cape Verde","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Nyan","Explosive","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Rose","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Brazil",":3","Paint","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Bubblegum","Matteo Hat","Fire","Chocolate"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Nyan","Wet","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Disco","Nyan","Paint","Granny"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Bubblegum","RIP Gravestone","Paint"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Glitched","UFO","Reindeer Pet",":3"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Nyan","Spider","Shark Fin","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Nyan",":3","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Claws","Curacao","Explosive","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Claws","Zombie","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"UFO","Shark Fin","Paint"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"UFO","Glitched","Egypt","Fire"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Claws","Sombrero","Fire"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Tie","Fire","Paint",":3"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"UFO","Spider",":3","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Glitched","Fire","Matteo Hat","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Disco","Chocolate","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Brazil","United States","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Wet","Chocolate",":3"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Tie","Galactic","Matteo Hat",":3"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Bubblegum","UFO","Explosive","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Glitched","Paint","Pink Egg","Fire"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Brazil","Cape Verde","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Glitched","Spider",":3"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Zombie","Blue Balloon","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Claws","Haiti","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Galactic","Shark Fin","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"UFO",":3","Paint","Spider"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"UFO","Explosive","Uruguay",":3"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Zombie","Fire","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Glitched","Explosive","Fireworks","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Bubblegum","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Tie","Sombrero","Spider"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"UFO","Fire","Paint"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Snowy","Orange Balloon",":3"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Wet","Spider","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Zombie","UFO","Sombrero","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Glitched","Brazil","Pink Balloon","Fire"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Skeleton","Fire",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Wet","Explosive","Granny","Fire"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched","Shark Fin","Burger"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Glitched","Claws","New Zealand",":3"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"UFO","Shark Fin","Paint","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Claws",":3","Pink Balloon"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Tie","Brazil","Switzerland","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Zombie","Sombrero","Shark Fin","Paint"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Claws","Brazil","Fire","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Bubblegum","Spain","Cometstruck","Fire"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Matteo Hat","Reindeer Pet"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Wet","Shark Fin",":3"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Wet","Explosive","Chocolate","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Nyan","Pink Egg",":3"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Nyan",":3","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Brazil","United States","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Claws","Galactic","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Bubblegum","England","Paint"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Wet","Paint","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Tie","Matteo Hat","Spider"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Nyan","Fire","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Disco","Wet","Orange Balloon","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Claws","Belgium","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"UFO","Paint","Aura Shades",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"26","UFO","Fireworks",":3"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Glitched",":3","Blue Egg"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Brazil","Sombrero","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Wet","Blue Balloon","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"UFO",":3","Spider"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Galactic","Nyan","Spider","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Bubblegum","Reindeer Pet","Spider","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"26","Jackolantern Pet",":3","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Glitched","Wet","Fire","Switzerland"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Glitched","Orange Egg","Matteo Hat","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Nyan",":3","Jackolantern Pet"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Nyan","Explosive","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Lucky","Spider","Fire","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Claws","Shark Fin","Fire"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Nyan","Galactic",":3","Red Balloon"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Brazil","Tie","Fire","Paint"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Galactic","Croatia","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Zombie",":3","Burger"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Brazil","Sombrero","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Galactic","Nyan","Shark Fin","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Galactic","Brazil","Green Egg","Spider"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Brazil","Bubblegum","Haiti","Sun"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"UFO","Sombrero","Fire","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"26","Zombie","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Glitched","Shark Fin","Matteo Hat",":3"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Wet","Explosive",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Zombie","Matteo Hat","Blue Balloon"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Tie","Uruguay","Spider","Paint"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"26","UFO","Granny","Paint"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Wet","Zombie","Granny","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Lucky","Glitched","Matteo Hat","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Tie","Paint","Rainbow Balloon"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Brazil","Tie","Sombrero",":3"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"26","Disco","Granny","Fire"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Nyan","Egypt","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Claws","Fire",":3","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Galactic","Fire","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Sombrero","Spider"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Wet","UFO","Fire","England"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Claws","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Claws","Sombrero","Explosive","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Bubblegum","Fire","Paint","Red Balloon"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Claws","Galactic","Paint","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Lucky",":3","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Zombie","Paint","Spider"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Rose","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Santa Hat","Explosive","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Zombie","Spider","Paint"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Glitched","Bosnia and Herzegovina","Spider"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Glitched","Matteo Hat","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Glitched","Zombie","Spider","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Brazil","Galactic","Shark Fin","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Claws","Blue Egg",":3"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Rose","Spider","Fire","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Zombie","Spider",":3"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Zombie","Blue Balloon","Cometstruck","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Brazil","Chocolate","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Brazil","Argentina","Paint"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"26","Reindeer Pet",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Nyan","Snowy","Cometstruck","Fireworks"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Claws","Spain","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Glitched","Fire","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Claws",":3","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Brazil","Green Egg","Spider","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Brazil","Wet","Sweden","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Claws","Wet","Shark Fin","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Bubblegum","Explosive","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Bubblegum","Fire","RIP Gravestone"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"UFO","Sombrero","Fire","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Wet","Switzerland","Matteo Hat",":3"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Tie","Sombrero","Explosive",":3"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Galactic","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Bubblegum","Spider","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Galactic","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Claws","Sombrero","Fire"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Wet","Matteo Hat","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"26","Reindeer Pet","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Claws","Tie",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Wet","Green Egg","Paint","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"UFO","Norway","Paint"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Brazil","UFO","Portugal","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Santa Hat","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Claws","Tie","DR Congo","Fire"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Galactic","Paint",":3"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Wet","Explosive","Granny"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Brazil","Paraguay","Cometstruck","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Glitched","Spider","Paint"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Lucky","Galactic","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Galactic","Bubblegum","RIP Gravestone","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Zombie",":3","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Galactic","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Wet","Sombrero","Paint","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Snowy","Blue Balloon","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Tie","Nyan",":3","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Claws","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Glitched","Granny","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Tie","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Galactic","Paraguay","Sun"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Galactic","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Glitched","Fire","Jackolantern Pet"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Zombie",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Bubblegum","Reindeer Pet","Matteo Hat","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Tie","Explosive","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Wet","Sombrero",":3"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Claws","Wet","Fire",":3"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Tie","Brazil","Granny","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Rose","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Rose","Cometstruck","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Lightning","Reindeer Pet","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Lightning","Jackolantern Pet","Matteo Hat","Spider"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Nyan","Spider","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Brazil","Matteo Hat",":3","Spider"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Nyan",":3","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Wet",":3","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Tie","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Nyan","Mexico","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Nyan","Galactic","Granny","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Brazil","Sombrero",":3","Spider"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Brazil","Bosnia and Herzegovina","Paint"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Lucky","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Glitched","Fire","Paint","Spider"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Tie","Matteo Hat","Paint",":3"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Wet","Sombrero","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Nyan","UFO","Paint",":3"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Bubblegum","Chocolate",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Nyan","Argentina","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Tie","Spider","Explosive","RIP Gravestone"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Nyan","Explosive","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Snowy","Jackolantern Pet","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Wet","Matteo Hat","Reindeer Pet"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Disco","Paint","Rainbow Balloon"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Skeleton","Fire","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Claws","Paint","Red Balloon"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Nyan","Sombrero","Cometstruck","Paint"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Zombie","Fire","Pink Balloon"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Wet","Sombrero","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"26","Zombie","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Zombie","Wet","Shark Fin","Paint"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Nyan","Bubblegum","Red Balloon","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Tie","Bosnia and Herzegovina","Fire"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Claws","Matteo Hat","Uruguay"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Rose","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Santa Hat","Paint",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Disco","Mexico","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Zombie","Spider","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"UFO","Wet","Matteo Hat","RIP Gravestone"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Claws","Bubblegum","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Wet","Paint",":3","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Galactic","Paint","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Snowy","Jackolantern Pet","Paint"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Claws","Czechia","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Disco","South Africa","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Claws","Bubblegum","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Galactic","Orange Balloon",":3","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Bubblegum","Explosive","Paint"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Tie","Bubblegum",":3","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"UFO",":3","Aura Shades","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Tie","Shark Fin","Matteo Hat",":3"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"UFO","Senegal","Spider"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Zombie","Sombrero","Fire"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Claws","Sombrero","Paint"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Claws","Jackolantern Pet","Paint"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Lightning","Santa Hat","Matteo Hat","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Tie",":3","Rainbow Balloon","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Nyan","Wet","Chocolate","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Brazil","Tie","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Claws","Zombie","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Bubblegum","Paint","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Zombie","Red Balloon","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Galactic","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Tie","Matteo Hat","Egypt"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Brazil","Blue Egg","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"26","Explosive","Fire"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"UFO","Nyan","Shark Fin","Fire"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Tie","Explosive","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Bubblegum","Galactic","Sombrero","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Disco","France","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Zombie","Blue Balloon","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Rose","Paint","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Bubblegum","Snowy","Rainbow Balloon","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Bubblegum","Explosive","Fire"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Claws","Paraguay","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Glitched","Tie","Shark Fin","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched","Brazil","Aura Shades","Spider"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Wet","Spider",":3"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Skeleton","Matteo Hat","Paint"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Tie","Explosive","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Disco","Ghana","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Zombie",":3","Shark Fin","Aura Shades"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"UFO","Explosive","Colombia"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Claws","Shark Fin","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Wet","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Lightning","Disco","Rainbow Balloon","Fire"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Claws","Paint","Matteo Hat",":3"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Nyan","Explosive","Red Balloon","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Nyan","Bosnia and Herzegovina","Explosive","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Bubblegum",":3","Chocolate"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"UFO","Matteo Hat","Pink Balloon","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Brazil","Nyan","Sombrero","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Brazil","Uruguay",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Zombie","Cometstruck","Red Balloon","Fire"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Wet","Blue Balloon",":3"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"UFO","Galactic","Spider","Paint"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Rose","Paint",":3","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Zombie","Fire","Shark Fin",":3"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Santa Hat","Paint","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Brazil","Blue Egg","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Galactic","Wet","Sombrero","Paint"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Shark Fin","Reindeer Pet","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"UFO","Sombrero","Paint"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Tie","Paint",":3"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Nyan",":3","Sombrero","Paint"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Nyan","Bubblegum","Scotland","Spider"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Wet","Pink Egg","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Brazil","Explosive","Spider","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Brazil","Switzerland","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Nyan","Chocolate","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Nyan","Spider","Explosive","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Zombie","Matteo Hat","Paint"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Zombie","Rainbow Balloon",":3"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Claws","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Brazil","Nyan","South Korea",":3"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Lightning","Jackolantern Pet","Spider"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Nyan","Tie","Sombrero","Fire"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched","Matteo Hat","Burger"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Tie","Paint","Pink Egg"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Skeleton","Fire","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Bubblegum","Shark Fin","Sombrero","Fire"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Galactic","Germany","Paint"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Wet","Canada","Fire"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Tie","Fireworks","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Claws","Spider","Paint"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Galactic","Claws","Explosive","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Brazil","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Rose","Shark Fin","Paint","Explosive"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Glitched","Explosive","RIP Gravestone"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Wet","Czechia","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Santa Hat","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Glitched","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Tie","Fire","Spider"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Claws","Sombrero",":3"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Nyan","UFO","Sombrero","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"UFO","Aura Shades","Spider","Burger"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Claws","Bubblegum","Sombrero","Fire"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"UFO","Jackolantern Pet","Cometstruck","Paint"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Santa Hat",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Lightning","Green Balloon","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Glitched","Paint","Blue Egg"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Brazil","Algeria","Fire"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Bubblegum","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Lucky","Matteo Hat","Paint"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Zombie","UFO","Jackolantern Pet",":3"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Santa Hat","Spider","Fire","Paint"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Bubblegum","Snowy","Fireworks","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Claws","Shark Fin","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Wet","Tie","Explosive","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"UFO","Explosive","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Galactic","Orange Balloon","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Sombrero","Paint","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Nyan","Ivory Coast","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Rose","Cometstruck","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Claws","Explosive",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Claws","Spider","Fire","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Lightning","Cometstruck","Green Egg"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Brazil","Zombie","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Rose","Explosive","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"UFO","Claws","Shark Fin","Spider"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Tie",":3","England"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Nyan","Fire","Spider",":3"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Tie","Paint","Sombrero","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Glitched","Panama","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Bubblegum","Spider","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Zombie","Bubblegum","Matteo Hat","Paint"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Nyan","Red Balloon","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Nyan","Spider","Fire"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"26","Nyan","Shark Fin","Fire"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Santa Hat","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Tie","Explosive","Sombrero",":3"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Rose",":3","Spider"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Rose","Matteo Hat",":3"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Zombie","Spider","Paint",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Nyan","Argentina",":3","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Wet",":3","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Glitched","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Bubblegum","Fire",":3"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Wet","Brazil","Sombrero","Fire"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"26","Shark Fin","Explosive","Paint"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Bubblegum","Fire","South Africa",":3"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Tie","Spider","Fire"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Tie","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Bubblegum","Senegal","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Glitched","Reindeer Pet","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Glitched",":3","Sombrero","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Brazil","Explosive","Fire"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Galactic","Orange Egg","Explosive","Fire"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched","Fire","Spider"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Nyan","RIP Gravestone","Paint","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Brazil","Spain","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Nyan","Fire",":3"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Wet","Pink Egg","Explosive","Paint"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Bubblegum","Indonesia","Fire"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Tie","Norway","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Galactic","Explosive","Fire"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Glitched","Galactic","Paint","RIP Gravestone"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Nyan","Shark Fin","Fire","Reindeer Pet"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Lucky","Wet","Explosive","Fire"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"26","Fireworks","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Skeleton","Explosive","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Claws","Orange Balloon","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"UFO","Brazil",":3","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"UFO","Spider","Paint"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"UFO","Portugal","Shark Fin","Sun"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Glitched","Fire","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Zombie","Tie","Orange Balloon",":3"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"26","Lucky","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Lucky","Explosive","Paint"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Wet","Bubblegum",":3","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Brazil","Glitched",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Tie","Lightning","Shark Fin","Red Balloon"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Claws","Shark Fin","Spider"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Bubblegum","Green Egg","Spider"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Bubblegum","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"26","Matteo Hat","Spider"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Disco","Uruguay","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Bubblegum","RIP Gravestone","Explosive","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Claws","Pink Egg","Matteo Hat","Spider"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"UFO","Bosnia and Herzegovina","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"UFO","Paint","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Claws","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Tie","Spider","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"UFO","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Nyan","Wet","Paint","Explosive"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Bubblegum","RIP Gravestone","Spider"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Bubblegum","Wet","Japan","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Claws","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Snowy","Pink Balloon","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Bubblegum","Matteo Hat","Shark Fin","Spider"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Lucky","Glitched","Shark Fin","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Snowy","Rainbow Balloon","Paint"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Glitched","Zombie","Shark Fin",":3"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Nyan","Spider","South Africa","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Galactic",":3","Green Balloon"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Nyan","Mexico","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Nyan","Paraguay","Fire","Spider"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Disco","Galactic","England","Sun"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Claws","Chocolate","Paint","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Zombie","Matteo Hat","Spider"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Brazil","Paint","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Tie","Claws","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Zombie","Shark Fin","Paint"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Glitched","Reindeer Pet",":3"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched","Spider","Burger"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"26","Fireworks","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Santa Hat","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Wet","Shark Fin","Spider"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Nyan","Fire","Spider","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Lucky","Paint","Matteo Hat","Spider"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"UFO","Santa Hat","Spider","Fire"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Wet","Qatar",":3"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Zombie","Paint",":3","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Wet","Nyan","Explosive","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Galactic","Zombie","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Lightning","Orange Balloon","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Lucky","Cometstruck","Fire"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Brazil","Zombie","Explosive","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"UFO",":3","Matteo Hat","Paint"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Nyan","Green Balloon","Shark Fin","Paint"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Wet","Spider","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Glitched","Sun","Fire","Spider"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"26","Shark Fin","Fire"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"26","Claws",":3","Fire"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Disco","Lightning","Green Balloon","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Bubblegum","Matteo Hat",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Brazil","Lucky","Paint","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Nyan","Claws",":3","Paint"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Nyan","Brazil","Pink Egg","Fire"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Brazil","Paint","Chocolate",":3"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Lightning","Granny","Fire"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Brazil","Reindeer Pet",":3"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"Galactic","RIP Gravestone","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Nyan","Bubblegum","Fire","Aura Shades"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"26","Santa Hat","Spider",":3"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Glitched","DR Congo","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Nyan","Fire","Sombrero","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Lightning","Orange Balloon","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Nyan","Galactic","Egypt","Paint"}',
    'addbrainrot @s "Garama and Madundung" Normal 1 {"Bubblegum","Fire","Spider","Paint","Shark Fin","Lightning"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Zombie","Explosive","Cometstruck","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Galactic","Fire","Spider","Paint","Shark Fin","Brazil"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Tie","Fire","Spider"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Fire","Germany","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched","Explosive","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Nyan","Fire","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Bubblegum","Spider"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Zombie","Matteo Hat","Fire"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Galactic","Glitched","Paint"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Lucky","Explosive","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Wet","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" YinYang 1 {"26","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"RIP Gravestone","Fire","Spider","Paint","Jackolantern Pet","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Zombie","Explosive","Fire","Lightning","Cometstruck","Paint"}',
    'addbrainrot @s "Garama and Madundung" Normal 1 {"Galactic","Spider","Fire","Matteo Hat","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Tie","Cometstruck","Spider","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Glitched","Algeria","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Bubblegum","Spider","Sombrero"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Disco","Paint","Fire"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Wet","Spider","France"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Nyan","Fire","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Galactic","Paint","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Tie","Spider","Santa Hat"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Bubblegum","Fire","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Normal 1 {"26","Fire","Spider","Paint","Shark Fin","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Bubblegum","Green Balloon","Fire","Explosive","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Glitched","Blue Egg","Spider","Paint","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Galactic","Pink Balloon","Fire"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Tie","Red Balloon","Cometstruck","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Bubblegum","Fire","Lightning","Spider","Paint"}',
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Zombie","Red Balloon","Fire","Shark Fin","Explosive"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Tie","Japan","Paint"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Wet","Blue Egg","Spider"}',
    'addbrainrot @s "Garama and Madundung" Normal 1 {"26","Fire","Spider","Paint","Shark Fin",":3","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Galactic","Orange Balloon","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Glitched","Disco","Fire"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Nyan","Jackolantern Pet","Spider"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Brazil","Fire","Nyan","Indonesia","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Claws","Glitched","Uruguay"}',
    'addbrainrot @s "Garama and Madundung" Cyber 1 {"Zombie","Sombrero","Shark Fin","Paint"}',
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Tie","Switzerland","Cometstruck"}',
    'addbrainrot @s "Garama and Madundung" Divine 1 {"Galactic","Explosive","Green Balloon","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Wet","Fire","Green Egg"}',
    'addbrainrot @s "Garama and Madundung" Galaxy 1 {"Bubblegum","Fire",":3"}',
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"UFO","Snowy","Fire","Spider"}',
    'addbrainrot @s "Garama and Madundung" Normal 1 {"Fire","Sombrero","Japan","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Bloodrot 1 {"Nyan","Spider","Shark Fin"}',
    'addbrainrot @s "Garama and Madundung" Candy 1 {"Reindeer Pet","Fire","26"}',
    'addbrainrot @s "Garama and Madundung" Radioactive 1 {"Fire","Explosive","Cometstruck","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Garama and Madundung" Lava 1 {"Claws","Red Balloon","Paint"}',
    'addbrainrot @s "Garama and Madundung" Cursed 1 {"Chocolate","Explosive"}'
]

DRAGON_CANNELLONI_RARITIES = ["Gold", "Diamond"]


# ==================== LISTE VX1B (Digi Narwhal, Moby Bros, etc.) ====================
VX1B_LINES = [
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Shark Fin","Sombrero",":3","Matteo Hat","Fire"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Fire",":3","Matteo Hat","Shark Fin","Spider","Sombrero"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Explosive","Shark Fin","Sombrero","Spider"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Matteo Hat","Spider",":3","Explosive","Sombrero","Fire","Shark Fin"}',
    'addbrainrot @s "Digi Narwhal" Diamond 1 {"Matteo Hat","Explosive","Spider","Shark Fin"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Spider","Sombrero","Matteo Hat"}',
    'addbrainrot @s "Bunny and Eggy" Diamond 1 {"Matteo Hat","Orange Egg","Fire","Explosive","Shark Fin"}',
    'addbrainrot @s "Bunny and Eggy" Diamond 1 {"Fire",":3","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Diamond 1 {"Fire","Sombrero","Matteo Hat"}',
    'addbrainrot @s "Popcuru and Fizzuru" Gold 1 {"Shark Fin",":3","Fire","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Sombrero","Shark Fin","Spider"}',
    'addbrainrot @s "Popcuru and Fizzuru" Diamond 1 {"Matteo Hat","Explosive","Fire","Spider","Shark Fin",":3"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {":3","Explosive","Matteo Hat"}',
    'addbrainrot @s "Popcuru and Fizzuru" Normal 1 {"Fire","Spider","Sombrero","Shark Fin","Explosive",":3","Matteo Hat"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Fire","Shark Fin","Explosive","Matteo Hat","Sombrero",":3","Spider"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {"Spider",":3","Fire","Explosive","Matteo Hat"}',
    'addbrainrot @s "Popcuru and Fizzuru" Normal 1 {"Explosive","Fire","Spider",":3"}',
    'addbrainrot @s "Popcuru and Fizzuru" Diamond 1 {"Fire","Shark Fin","Sombrero",":3"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {"Explosive","Spider","Matteo Hat","Fire","Shark Fin","Sombrero",":3"}',
    'addbrainrot @s "Bunny and Eggy" Diamond 1 {"Spider","Sombrero","Matteo Hat","Fire","Shark Fin"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Sombrero","Matteo Hat","Spider","Shark Fin","Explosive","Fire",":3"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Shark Fin",":3","Fire","Matteo Hat"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Sombrero","Spider","Explosive",":3"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {":3","Shark Fin","Matteo Hat","Sombrero","Spider"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {":3","Matteo Hat","Fire","Explosive","Shark Fin"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {"Shark Fin","Explosive",":3"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {":3","Explosive","Sombrero"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Spider","Explosive","Matteo Hat","Sombrero","Shark Fin",":3"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {":3","Shark Fin","Orange Egg","Sombrero","Explosive","Matteo Hat"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Shark Fin","Explosive","Matteo Hat"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Explosive","Sombrero","Matteo Hat",":3"}',
    'addbrainrot @s "Popcuru and Fizzuru" Gold 1 {"Spider",":3","Fire"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Spider","Fire",":3","Sombrero","Shark Fin"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Matteo Hat","Sombrero",":3","Shark Fin"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {"Sombrero","Fire","Matteo Hat","Explosive"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Sombrero","Shark Fin",":3","Matteo Hat","Spider","Fire"}',
    'addbrainrot @s "Popcuru and Fizzuru" Diamond 1 {"Sombrero","Spider","Shark Fin","Matteo Hat","Fire"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Matteo Hat","Explosive",":3","Orange Egg"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Fire","Sombrero","Shark Fin"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Explosive",":3","Spider","Shark Fin"}',
    'addbrainrot @s "Digi Narwhal" Diamond 1 {"Matteo Hat","Shark Fin","Explosive","Spider",":3","Sombrero","Fire"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {"Matteo Hat",":3","Explosive","Shark Fin","Fire","Spider","Sombrero"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Explosive","Spider","Sombrero","Fire"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {":3","Sombrero","Shark Fin","Fire","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Diamond 1 {"Orange Egg","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Fire",":3","Matteo Hat","Sombrero","Explosive"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {"Shark Fin","Spider","Sombrero",":3"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {"Explosive","Sombrero","Fire"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Fire","Explosive","Spider","Sombrero"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Sombrero","Matteo Hat","Explosive",":3","Spider"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Shark Fin","Matteo Hat","Explosive",":3","Fire","Sombrero","Spider"}',
    'addbrainrot @s "Popcuru and Fizzuru" Gold 1 {":3","Explosive","Spider","Fire","Sombrero","Shark Fin","Matteo Hat"}',
    'addbrainrot @s "Popcuru and Fizzuru" Normal 1 {"Sombrero","Spider","Matteo Hat"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Sombrero","Matteo Hat","Fire"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Explosive",":3","Fire","Shark Fin"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {":3","Matteo Hat","Explosive","Sombrero","Fire","Spider","Shark Fin"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Orange Egg","Matteo Hat","Explosive","Sombrero","Shark Fin"}',
    'addbrainrot @s "Popcuru and Fizzuru" Normal 1 {"Shark Fin","Fire","Matteo Hat","Explosive","Sombrero",":3","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Sombrero","Spider","Explosive","Matteo Hat"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {"Sombrero","Explosive","Fire","Orange Egg","Shark Fin"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Explosive","Matteo Hat",":3","Shark Fin","Fire","Sombrero"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Sombrero","Explosive",":3","Shark Fin","Spider"}',
    'addbrainrot @s "Popcuru and Fizzuru" Gold 1 {"Shark Fin",":3","Sombrero","Fire","Spider","Matteo Hat","Explosive"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {":3","Spider","Matteo Hat","Sombrero","Fire"}',
    'addbrainrot @s "Popcuru and Fizzuru" Gold 1 {"Sombrero","Spider","Matteo Hat",":3","Explosive","Shark Fin","Fire"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Matteo Hat",":3","Spider"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Matteo Hat","Sombrero","Explosive",":3","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Spider","Explosive","Orange Egg","Matteo Hat","Sombrero","Shark Fin",":3"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Shark Fin","Matteo Hat","Sombrero",":3","Spider"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {":3","Explosive","Spider","Fire","Sombrero"}',
    'addbrainrot @s "Moby Bros" Normal 1 {":3","Sombrero","Matteo Hat","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {"Spider","Matteo Hat","Sombrero","Shark Fin",":3","Fire"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Shark Fin","Sombrero","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Fire","Sombrero","Matteo Hat","Explosive","Orange Egg"}',
    'addbrainrot @s "Digi Narwhal" Diamond 1 {"Spider","Explosive","Shark Fin","Sombrero"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Spider",":3","Shark Fin","Sombrero","Explosive","Matteo Hat","Fire"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {":3","Shark Fin","Spider","Sombrero","Explosive"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Sombrero","Spider","Fire"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {"Fire","Shark Fin","Explosive"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Spider","Fire","Sombrero"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Shark Fin","Spider","Fire","Matteo Hat","Explosive"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {"Sombrero","Shark Fin","Explosive","Fire","Spider","Matteo Hat"}',
    'addbrainrot @s "Popcuru and Fizzuru" Diamond 1 {":3","Fire","Sombrero","Shark Fin"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {"Spider","Matteo Hat","Orange Egg","Fire","Explosive"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {"Explosive",":3","Sombrero"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {"Sombrero","Shark Fin","Fire",":3","Explosive","Matteo Hat"}',
    'addbrainrot @s "Digi Narwhal" Diamond 1 {"Spider","Sombrero","Shark Fin","Matteo Hat","Explosive"}',
    'addbrainrot @s "Popcuru and Fizzuru" Normal 1 {":3","Matteo Hat","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {"Spider","Fire","Explosive"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {"Sombrero","Fire",":3","Matteo Hat","Shark Fin","Explosive"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Matteo Hat","Spider","Shark Fin","Explosive","Fire","Orange Egg"}',
    'addbrainrot @s "Popcuru and Fizzuru" Normal 1 {"Matteo Hat","Fire",":3","Explosive","Sombrero","Shark Fin"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Shark Fin","Sombrero","Fire",":3","Matteo Hat"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {"Spider","Fire","Matteo Hat","Explosive","Sombrero",":3","Shark Fin"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {"Sombrero","Fire",":3","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {":3","Sombrero","Fire","Matteo Hat","Explosive","Orange Egg"}',
    'addbrainrot @s "Bunny and Eggy" Diamond 1 {"Matteo Hat","Sombrero","Fire",":3","Explosive","Shark Fin","Orange Egg"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Fire",":3","Explosive","Shark Fin","Sombrero","Spider","Matteo Hat"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {"Matteo Hat","Spider","Sombrero",":3","Fire"}',
    'addbrainrot @s "Popcuru and Fizzuru" Divine 1 {"Matteo Hat","Explosive","Spider","Fire","Shark Fin"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Sombrero",":3","Spider","Shark Fin","Matteo Hat","Fire","Explosive"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Sombrero",":3","Matteo Hat"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {":3","Explosive","Matteo Hat","Spider"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {"Shark Fin","Fire","Spider","Sombrero","Explosive"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Fire",":3","Sombrero","Matteo Hat"}',
    'addbrainrot @s "Bunny and Eggy" Diamond 1 {"Orange Egg","Matteo Hat",":3","Explosive","Sombrero","Spider","Fire"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {"Spider","Shark Fin","Sombrero","Explosive",":3","Matteo Hat"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Shark Fin","Sombrero","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {":3","Matteo Hat","Explosive","Shark Fin","Spider","Fire","Sombrero"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Shark Fin","Explosive",":3"}',
    'addbrainrot @s "Popcuru and Fizzuru" Normal 1 {"Fire","Sombrero","Shark Fin","Matteo Hat",":3","Explosive"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Sombrero","Shark Fin",":3","Fire","Matteo Hat"}',
    'addbrainrot @s "Popcuru and Fizzuru" Divine 1 {"Spider","Matteo Hat","Sombrero",":3","Shark Fin","Explosive","Fire"}',
    'addbrainrot @s "Popcuru and Fizzuru" Gold 1 {"Spider","Matteo Hat","Shark Fin",":3","Explosive"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {"Spider","Explosive","Fire","Sombrero","Matteo Hat",":3"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {":3","Explosive","Shark Fin","Sombrero","Fire"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Fire","Spider","Sombrero","Explosive"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {"Shark Fin","Spider",":3","Sombrero"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {"Sombrero","Shark Fin","Matteo Hat","Spider","Fire",":3"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Sombrero","Explosive","Spider","Shark Fin",":3","Matteo Hat"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Matteo Hat","Spider",":3","Sombrero"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {"Shark Fin",":3","Matteo Hat"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Shark Fin","Spider","Matteo Hat",":3"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Sombrero","Explosive","Fire"}',
    'addbrainrot @s "Popcuru and Fizzuru" Diamond 1 {"Explosive","Fire",":3"}',
    'addbrainrot @s "Digi Narwhal" Diamond 1 {"Sombrero","Matteo Hat",":3","Spider","Explosive","Shark Fin","Fire"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Spider","Fire","Sombrero"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {"Shark Fin","Spider","Fire",":3","Explosive","Sombrero"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Matteo Hat","Spider","Sombrero","Fire","Shark Fin","Explosive"}',
    'addbrainrot @s "Digi Narwhal" Diamond 1 {"Matteo Hat","Sombrero","Spider","Shark Fin",":3","Fire","Explosive"}',
    'addbrainrot @s "Bunny and Eggy" Normal 1 {"Spider","Matteo Hat","Sombrero","Fire","Explosive","Shark Fin",":3"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Shark Fin",":3","Fire"}',
    'addbrainrot @s "Cerberus" Diamond 1 {"Fire","Shark Fin","Spider"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Shark Fin","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Sombrero","Explosive","Matteo Hat","Spider","Fire","Shark Fin",":3"}',
    'addbrainrot @s "Popcuru and Fizzuru" Gold 1 {"Matteo Hat","Sombrero","Fire"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Spider",":3","Sombrero","Explosive","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Digi Narwhal" Normal 1 {"Shark Fin","Explosive","Fire","Matteo Hat","Sombrero"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Matteo Hat",":3","Spider","Fire","Shark Fin"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {"Fire","Matteo Hat",":3","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Gold 1 {"Shark Fin","Explosive","Spider","Orange Egg",":3","Matteo Hat","Fire"}',
    'addbrainrot @s "Ketupat Bros" Diamond 1 {":3","Matteo Hat","Sombrero","Fire"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {"Sombrero","Matteo Hat","Spider",":3","Explosive"}',
    'addbrainrot @s "Digi Narwhal" Gold 1 {"Sombrero","Shark Fin","Fire","Explosive","Matteo Hat",":3"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Explosive","Shark Fin",":3","Spider"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Sombrero","Shark Fin","Explosive",":3"}',
    'addbrainrot @s "Cerberus" Normal 1 {":3","Shark Fin","Explosive","Matteo Hat","Sombrero","Spider"}',
    'addbrainrot @s "Ketupat Bros" Gold 1 {"Matteo Hat","Fire","Sombrero","Explosive",":3","Shark Fin","Spider"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Sombrero","Shark Fin",":3","Fire","Explosive","Spider"}',
    'addbrainrot @s "Bunny and Eggy" Diamond 1 {"Matteo Hat",":3","Spider"}',
    'addbrainrot @s "Cerberus" Gold 1 {"UFO","Galactic","Spider","Explosive","Sombrero","Fire"}',
    'addbrainrot @s "Cerberus" Cursed 1 {"Bubblegum","Brazil","Claws","Chocolate","UFO","Explosive"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Chocolate","Galactic","Bubblegum","Brazil","UFO","Claws","Explosive"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Chocolate","Claws","Shark Fin"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Brazil","Bubblegum","Sombrero","Spider"}',
    'addbrainrot @s "Cerberus" Cyber 1 {"UFO","Claws","Brazil","Galactic"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Brazil","Galactic","Bubblegum","Explosive"}',
    'addbrainrot @s "Cerberus" Diamond 1 {"Galactic","Matteo Hat","Sombrero","Fire","Shark Fin"}',
    'addbrainrot @s "Cerberus" Cyber 1 {"UFO","Galactic","Claws","Explosive","Fire","Spider"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Chocolate","Bubblegum","Claws","Galactic"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Claws","Brazil","Sombrero","Explosive","Shark Fin"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Galactic","UFO","Chocolate","Spider","Sombrero","Shark Fin"}',
    'addbrainrot @s "Cerberus" Normal 1 {"UFO","Claws","Bubblegum","Chocolate","Galactic","Brazil","Explosive"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Galactic","Brazil","UFO","Fire"}',
    'addbrainrot @s "Cerberus" Diamond 1 {"Galactic","Brazil","Bubblegum","Shark Fin","Sombrero","Fire","Spider"}',
    'addbrainrot @s "Cerberus" Diamond 1 {"Bubblegum","UFO","Sombrero"}',
    'addbrainrot @s "Cerberus" Diamond 1 {"Brazil","Claws","Bubblegum"}',
    'addbrainrot @s "Cerberus" Cyber 1 {"Galactic","Matteo Hat","Explosive",":3","Sombrero","Shark Fin","Spider"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Claws","Brazil","UFO"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Brazil","Galactic","Chocolate","Claws"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Claws","Chocolate","Brazil","UFO"}',
    'addbrainrot @s "Cerberus" Normal 1 {"UFO","Brazil","Chocolate","Shark Fin",":3"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Galactic","Chocolate","Explosive","Shark Fin"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Claws","Spider",":3"}',
    'addbrainrot @s "Cerberus" Cursed 1 {"Brazil","Claws","Galactic","Chocolate","Matteo Hat","Explosive"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Galactic","Brazil","Bubblegum"}',
    'addbrainrot @s "Cerberus" Diamond 1 {"Bubblegum","Galactic","Spider","Matteo Hat","Sombrero","Explosive","Shark Fin"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Bubblegum","Galactic","Brazil","Chocolate","Spider","Sombrero","Shark Fin"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Chocolate","UFO","Claws","Bubblegum","Explosive"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Galactic","Explosive",":3","Matteo Hat","Spider"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Galactic","Bubblegum","UFO","Explosive"}',
    'addbrainrot @s "Cerberus" Cyber 1 {"Brazil","Spider",":3","Sombrero"}',
    'addbrainrot @s "Cerberus" Gold 1 {"UFO","Sombrero","Spider"}',
    'addbrainrot @s "Cerberus" Diamond 1 {"UFO","Bubblegum","Galactic","Fire","Explosive","Matteo Hat","Shark Fin"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Bubblegum","Brazil","Claws","Galactic","Sombrero","Fire"}',
    'addbrainrot @s "Cerberus" Cyber 1 {"Galactic",":3","Shark Fin"}',
    'addbrainrot @s "Cerberus" Cursed 1 {"UFO","Brazil","Explosive","Spider"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Brazil","Bubblegum","Galactic","UFO",":3","Matteo Hat"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Galactic","Chocolate","UFO","Explosive","Matteo Hat","Shark Fin","Sombrero"}',
    'addbrainrot @s "Cerberus" Gold 1 {"UFO","Spider","Fire",":3"}',
    'addbrainrot @s "Cerberus" Cursed 1 {"Brazil","Spider","Shark Fin",":3","Matteo Hat"}',
    'addbrainrot @s "Cerberus" Normal 1 {"Claws","Bubblegum","Matteo Hat","Shark Fin","Fire","Spider","Explosive"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Sombrero","Matteo Hat","Spider","Explosive","Shark Fin"}',
    'addbrainrot @s "Cerberus" Gold 1 {"Galactic","Explosive","Spider"}',
    'addbrainrot @s "Popcuru and Fizzuru" Normal 1 {"Spider","Explosive","Matteo Hat","Fire"}',
    'addbrainrot @s "Moby Bros" Diamond 1 {"Sombrero","Spider",":3","Shark Fin","Matteo Hat","Explosive","Fire"}',
    'addbrainrot @s "Digi Narwhal" Diamond 1 {"Matteo Hat","Fire","Explosive","Sombrero"}',
    'addbrainrot @s "Moby Bros" Gold 1 {"Sombrero","Fire","Explosive","Matteo Hat"}',
    'addbrainrot @s "Moby Bros" Normal 1 {"Spider","Sombrero","Fire","Explosive","Shark Fin"}',
    'addbrainrot @s "Ketupat Bros" Normal 1 {"Shark Fin","Spider","Fire","Matteo Hat","Explosive","Sombrero"}',
]


# ==================== BOT DISCORD MINIMAL ====================
class MiniBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Synchronisation des commandes slash. Isolée dans un try/except :
        # un échec ici (ex: 429 rate limit Discord) ne doit jamais empêcher
        # le bot de démarrer et de rester connecté — les commandes existantes
        # resteront simplement inchangées jusqu'au prochain sync réussi,
        # plutôt que de faire planter tout le process.
        try:
            await self.tree.sync()
            log.info("✅ Commandes slash synchronisées avec succès.")
        except discord.errors.HTTPException as e:
            if e.status == 429:
                log.warning(
                    "⚠️ Rate limit Discord (429) lors de la synchronisation des commandes "
                    "slash. Le bot démarre quand même normalement ; la sync sera "
                    "retentée automatiquement au prochain redémarrage."
                )
            else:
                log.warning(f"⚠️ Échec de la synchronisation des commandes slash : {e}")


bot = MiniBot()


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="vxsecret", description="Affiche une sélection secrète et aléatoire. Réservé aux administrateurs.")
@app_commands.default_permissions(administrator=True)
async def vxsecret(interaction: discord.Interaction):
    if interaction.guild is not None and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Cette commande est réservée aux administrateurs du serveur.",
            ephemeral=True
        )
        return

    nb_garama = min(18, len(GARAMA_LINES))
    chosen_garama = random.sample(GARAMA_LINES, nb_garama)

    dragon_lines = [
        f'addbrainrot @s "Dragon Cannelloni" {random.choice(DRAGON_CANNELLONI_RARITIES)} 1'
        for _ in range(8)
    ]

    base_lines = chosen_garama + dragon_lines

    all_lines = []
    for i, line in enumerate(base_lines, start=1):
        all_lines.append(line)
        if i % 5 == 0:
            all_lines.append(random.choice(VX1B_LINES))

    content_block = "\n".join(all_lines)

    embed = discord.Embed(
        title="🔒 VX Secret",
        description=f"```\n{content_block}\n```",
        color=discord.Color.dark_purple()
    )
    embed.set_footer(text=f"Généré pour {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="pentinbase", description="Comme /vxsecret + Balai de Sorcière offert en tête. Réservé aux admins.")
@app_commands.default_permissions(administrator=True)
async def pentinbase(interaction: discord.Interaction):
    if interaction.guild is not None and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Cette commande est réservée aux administrateurs du serveur.",
            ephemeral=True
        )
        return

    nb_garama = min(18, len(GARAMA_LINES))
    chosen_garama = random.sample(GARAMA_LINES, nb_garama)

    dragon_lines = [
        f'addbrainrot @s "Dragon Cannelloni" {random.choice(DRAGON_CANNELLONI_RARITIES)} 1'
        for _ in range(8)
    ]

    base_lines = chosen_garama + dragon_lines

    all_lines = []
    for i, line in enumerate(base_lines, start=1):
        all_lines.append(line)
        if i % 5 == 0:
            all_lines.append(random.choice(VX1B_LINES))

    all_lines = ['giveitem @s "Witch\'s Broom"'] + all_lines

    content_block = "\n".join(all_lines)

    embed = discord.Embed(
        title="🔒 Pentinbase",
        description=f"```\n{content_block}\n```",
        color=discord.Color.dark_purple()
    )
    embed.set_footer(text=f"Généré pour {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="vx1b", description="Affiche une sélection secrète et aléatoire (liste VX1B). Réservé aux administrateurs.")
@app_commands.default_permissions(administrator=True)
async def vx1b(interaction: discord.Interaction):
    if interaction.guild is not None and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Cette commande est réservée aux administrateurs du serveur.",
            ephemeral=True
        )
        return

    nb_vx1b = min(18, len(VX1B_LINES))
    chosen_vx1b = random.sample(VX1B_LINES, nb_vx1b)
    content_block = "\n".join(chosen_vx1b)

    embed = discord.Embed(
        title="🔒 VX1B",
        description=f"```\n{content_block}\n```",
        color=discord.Color.dark_teal()
    )
    embed.set_footer(text=f"Généré pour {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed, ephemeral=True)


# ==================== SYSTÈME ANTI-VEILLE POUR RENDER (Free Web Service) — RENFORCÉ ====================
# Render met en veille les Web Services gratuits après ~15 minutes sans requête
# HTTP entrante. Version renforcée par rapport à la précédente :
#   1) Le serveur HTTP keep-alive répond toujours (nécessaire pour que Render
#      considère le service comme un vrai Web Service actif).
#   2) La tâche self_ping s'exécute toutes les 4 minutes (au lieu de 10) —
#      marge de sécurité large sous le seuil de 15 min de Render — avec
#      plusieurs tentatives (retries) et une session HTTP réutilisée.
#   3) Le bot Discord lui-même est enveloppé dans une boucle de redémarrage
#      automatique : si `bot.run()` plante (perte réseau, erreur Discord,
#      exception non gérée...), il est relancé automatiquement après une
#      courte pause, au lieu de laisser le process s'arrêter définitivement.
#
# ⚠️ Important : ce système ne peut rien faire si Render tue carrément le
# process (ex. dépassement du quota gratuit de 750h/mois, ou "Manual/Auto
# Deploy" qui redémarre le service). Dans ce cas Render doit relancer lui-même
# le service. En complément de ce code, il est recommandé d'ajouter un
# ping externe (UptimeRobot, cron-job.org, etc.) toutes les 5 minutes vers
# ton URL Render : ça donne une deuxième source de trafic entrant en plus du
# self-ping, ce qui rend la mise en veille quasiment impossible.

RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

# Session HTTP persistante pour le self-ping (évite de recréer une connexion
# TCP/TLS à chaque tentative, plus rapide et plus fiable).
_ping_session: Optional[aiohttp.ClientSession] = None


async def _get_ping_session() -> aiohttp.ClientSession:
    global _ping_session
    if _ping_session is None or _ping_session.closed:
        _ping_session = aiohttp.ClientSession()
    return _ping_session


@tasks.loop(minutes=4)
async def self_ping():
    if not RENDER_EXTERNAL_URL:
        return

    session = await _get_ping_session()
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            async with session.get(RENDER_EXTERNAL_URL, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                log.info(f"🔁 Self-ping OK (statut {resp.status}, tentative {attempt})")
                return
        except Exception as e:
            log.warning(f"⚠️ Self-ping échoué (tentative {attempt}/{max_attempts}) : {e}")
            if attempt < max_attempts:
                await asyncio.sleep(5)

    log.error("❌ Self-ping : toutes les tentatives ont échoué ce cycle.")


@self_ping.before_loop
async def before_self_ping():
    await bot.wait_until_ready()


@self_ping.error
async def self_ping_error(error):
    # Empêche la tâche périodique de s'arrêter définitivement si une exception
    # inattendue remonte : on log et on laisse discord.py.tasks la relancer.
    log.error(f"❌ Erreur non gérée dans self_ping : {error}")


@bot.event
async def on_disconnect():
    log.warning("🔌 Déconnecté de Discord (tentative de reconnexion automatique en cours)...")


@bot.event
async def on_resumed():
    log.info("✅ Session Discord reprise avec succès après une coupure.")


@bot.event
async def on_ready():
    log.info(f"✅ Bot connecté avec succès en tant que {bot.user.name}")
    if not self_ping.is_running():
        self_ping.start()

    log.info("Prêt et synchronisé !")


class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot Discord actif !")

    def do_HEAD(self):
        # Certains services de ping externes (UptimeRobot, cron-job.org en mode
        # HEAD) utilisent HEAD plutôt que GET : on répond aussi 200 ici.
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def log_message(self, format, *args):
        pass


def run_keep_alive_server():
    port = int(os.getenv("PORT", 8080))
    while True:
        try:
            server = HTTPServer(("0.0.0.0", port), KeepAliveHandler)
            log.info(f"🌐 Serveur keep-alive lancé sur le port {port}")
            server.serve_forever()
        except Exception as e:
            # Si le petit serveur HTTP plante pour une raison quelconque, on le
            # relance après une courte pause plutôt que de laisser le thread mourir.
            log.error(f"⚠️ Serveur keep-alive interrompu ({e}), redémarrage dans 5s...")
            time.sleep(5)


def start_keep_alive():
    thread = threading.Thread(target=run_keep_alive_server, daemon=True)
    thread.start()


def run_bot_forever(token: str):
    """Lance le bot Discord avec redémarrage automatique en cas de plantage
    (erreur réseau, exception non gérée, perte de connexion Discord...).
    Une pause croissante (backoff) évite de spammer Discord/Render en cas
    d'échecs répétés."""
    backoff = 15  # secondes, avant la première tentative de reconnexion
    max_backoff = 600  # 10 minutes max entre deux tentatives

    while True:
        try:
            log.info("🚀 Démarrage du bot Discord...")
            bot.run(token, log_handler=None)
            # bot.run() ne revient normalement que si le bot s'est arrêté
            # proprement (ex. bot.close()). On considère ça comme un arrêt
            # volontaire et on sort de la boucle.
            log.info("ℹ️ bot.run() s'est terminé normalement, arrêt du superviseur.")
            break
        except discord.errors.LoginFailure:
            # Token invalide : inutile de boucler indéfiniment.
            log.critical("❌ Échec de connexion : DISCORD_TOKEN invalide. Arrêt du bot.")
            raise
        except discord.errors.HTTPException as e:
            if e.status == 429:
                # Rate limit global Discord : il ne faut surtout PAS réessayer
                # rapidement, sous peine d'aggraver le blocage. On attend une
                # pause longue et fixe (2 minutes minimum), indépendante du
                # backoff normal.
                wait_time = max(120, backoff)
                log.error(
                    f"🚫 Rate limit Discord (429) reçu : "
                    f"{getattr(e, 'text', str(e))}. Attente de {wait_time}s avant de réessayer."
                )
                time.sleep(wait_time)
                backoff = min(backoff * 2, max_backoff)
            else:
                log.error(f"💥 Erreur HTTP Discord ({e.status}): {e}. "
                          f"Redémarrage automatique dans {backoff}s...")
                time.sleep(backoff)
                backoff = min(backoff * 2, max_backoff)
            continue
        except Exception as e:
            log.error(f"💥 Le bot a planté ({type(e).__name__}: {e}). "
                      f"Redémarrage automatique dans {backoff}s...")
            time.sleep(backoff)
            backoff = min(backoff * 2, max_backoff)
            continue

        # Si on arrive ici après un run() propre sans exception, on réinitialise
        # le backoff au cas où on redémarrerait plus tard pour une autre raison.
        backoff = 15


# --- Démarrage du bot ---
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise RuntimeError("La variable d'environnement DISCORD_TOKEN n'est pas définie.")

    start_keep_alive()  # Lance le petit serveur HTTP en parallèle pour rester actif sur Render
    run_bot_forever(TOKEN)  # Lance le bot avec redémarrage automatique en cas de plantage
