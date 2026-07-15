import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import random
import asyncio
import threading
import aiohttp
from http.server import BaseHTTPRequestHandler, HTTPServer

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
    'addbrainrot @s "Garama and Madundung" Gold 1 {"Tie","Paint","Balloon"}',
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
    'addbrainrot @s "Garama and Madundung" Rainbow 1 {"Disco","Paint","Balloon"}',
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
    'addbrainrot @s "Garama and Madundung" Diamond 1 {"Snowy","Balloon","Paint"}',
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
    'addbrainrot @s "Garama and Madundung" Phantom 1 {"Nyan","Galactic","Egypt","Paint"}'
]

DRAGON_CANNELLONI_RARITIES = ["Gold", "Diamond"]


# ==================== BOT DISCORD MINIMAL ====================
class MiniBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Synchronisation globale des commandes slash
        await self.tree.sync()


bot = MiniBot()


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="vxsecret", description="Affiche une sélection secrète et aléatoire. Réservé aux administrateurs.")
@app_commands.default_permissions(administrator=True)
async def vxsecret(interaction: discord.Interaction):
    # Vérification explicite en plus de default_permissions : celle-ci ne fait que
    # masquer la commande par défaut dans l'UI Discord, mais un membre du serveur
    # peut reconfigurer les permissions de la commande depuis les paramètres
    # d'intégrations. Cette vérification garantit que seuls les membres ayant
    # réellement la permission "Administrateur" peuvent l'utiliser.
    if interaction.guild is not None and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Cette commande est réservée aux administrateurs du serveur.",
            ephemeral=True
        )
        return

    # 18 lignes "Garama and Madundung" tirées aléatoirement dans la liste (sans ordre particulier)
    nb_garama = min(18, len(GARAMA_LINES))
    chosen_garama = random.sample(GARAMA_LINES, nb_garama)

    # 8 lignes "Dragon Cannelloni" avec une rareté aléatoire (Gold ou Diamond) à chaque fois
    dragon_lines = [
        f'addbrainrot @s "Dragon Cannelloni" {random.choice(DRAGON_CANNELLONI_RARITIES)} 1'
        for _ in range(8)
    ]

    all_lines = chosen_garama + dragon_lines
    content_block = "\n".join(all_lines)

    embed = discord.Embed(
        title="🔒 VX Secret",
        description=f"```\n{content_block}\n```",
        color=discord.Color.dark_purple()
    )
    embed.set_footer(text=f"Généré pour {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed, ephemeral=True)


# ==================== SYSTÈME ANTI-VEILLE POUR RENDER (Free Web Service) ====================
# Render met en veille les Web Services gratuits après ~15 minutes sans requête
# HTTP entrante. On contourne ça de deux façons complémentaires :
#  1) un petit serveur HTTP qui répond "Bot Discord actif !" (nécessaire pour
#     que Render considère le service comme un vrai Web Service qui écoute) ;
#  2) une tâche de fond qui s'auto-ping toutes les 10 minutes sur sa propre
#     URL publique (RENDER_EXTERNAL_URL, fournie automatiquement par Render).

RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")


@tasks.loop(minutes=10)
async def self_ping():
    if not RENDER_EXTERNAL_URL:
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(RENDER_EXTERNAL_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                print(f"🔁 Self-ping effectué avec succès (statut {resp.status})")
    except Exception as e:
        print(f"⚠️ Self-ping échoué : {e}")


@self_ping.before_loop
async def before_self_ping():
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    print(f"✅ Bot connecté avec succès en tant que {bot.user.name}")
    if not self_ping.is_running():
        self_ping.start()
    print("Prêt et synchronisé !")


class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot Discord actif !")

    def log_message(self, format, *args):
        # Empêche de spammer les logs Render à chaque ping
        pass


def run_keep_alive_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), KeepAliveHandler)
    print(f"🌐 Serveur keep-alive lancé sur le port {port}")
    server.serve_forever()


def start_keep_alive():
    thread = threading.Thread(target=run_keep_alive_server, daemon=True)
    thread.start()


# --- Démarrage du bot ---
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise RuntimeError("La variable d'environnement DISCORD_TOKEN n'est pas définie.")

    start_keep_alive()  # Lance le petit serveur HTTP en parallèle pour rester actif sur Render
    bot.run(TOKEN)
