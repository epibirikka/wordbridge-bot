import discord
from discord.ext import tasks

import os

class PrivateData:
    token: str
    channel: int

    @staticmethod
    def from_os():
        priv = PrivateData()
        priv.token = os.getenv("WB_TOKEN")
        priv.channel = int(os.getenv("WB_CHANNEL"))

        return priv


from time import sleep
from time import perf_counter

import math
import random

class Player:
    def __init__(self, user, channel:discord.TextChannel=None):
        self.user = user
        self.channel = channel
        self.sent_time = -1
        self.current_question = None

        self.bridge = ""

    def replace_question(self, delay=0):
        self.current_question = None
        self.sent_time = perf_counter() + delay

    def ask_question(self):
        if self.current_question:
            return

        self.on_question = True
        self.current_question = random.choice(questions)
        

    def answer(self, answer_prompt):
        l = len(answer_prompt)

        is_close = False

        for answer, distance in zip(self.current_question.answers, self.current_question.how_close(answer_prompt)):
            if distance <= 0:
                self.bridge += answer
                return AnswerQualifiation.CORRECT
            elif distance <= 4:
                is_close = True

        return AnswerQualifiation.CLOSE if is_close else AnswerQualifiation.NOT_QUITE

    def get_time(self, time=perf_counter()):
        return time - self.sent_time

from enum import Enum
from long import *
from question import *

from emoji import *

class GameStartError(Enum):
    NOT_ENOUGH_PLAYERS = 1
    GAME_GOING = 2

class GameOver(Enum):
    NOT_ENOUGH_PLAYERS = 1
    WINNER = 2

class AnswerQualifiation(Enum):
    CORRECT = 1
    CLOSE = 2
    NOT_QUITE = 3

required_players = 1
viewport_size = 33

class WordBridge(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._private = PrivateData.from_os()

        self.going_on = False
        self.players = []

        self.send_stuff = []

        self.channel : discord.TextChannel = None
        self.winner : Player = None

        self.start_time = -1

        self.goal = 55
    
    @tasks.loop(seconds=0.2)
    async def game_update(self):
        if self.send_stuff:
            for s in self.send_stuff:
                if not s:
                    continue
                await self.channel.send(s)
            self.send_stuff.clear()

        if not self.going_on:
            return

        if len(self.players) < required_players:
            self.reset_game(GameOver.NOT_ENOUGH_PLAYERS)
            return

        current_time = perf_counter()

        for player in self.players:
            t = player.get_time(current_time)

            if len(player.bridge) >= self.goal:
                self.winner = player
                self.reset_game(GameOver.WINNER)
                return

            if t > 2 and not player.current_question:
                player.ask_question()
                await self.remind_player(player)

    async def remind_player(self, player):
        await player.user.send(f"*Prompt:* {player.current_question.prompt}")

    def reset_game(self, over_state, *args):
        self.going_on = False
        self.players.clear()
        
        self.send_stuff.append({
            GameOver.NOT_ENOUGH_PLAYERS: "**Game over!** Not enough players to participate",
            GameOver.WINNER: "**Game over**, it looks we have a winner!",
        }.get(over_state) or "ok")

        self.send_stuff.append("Nobody won!" if self.winner is None else f"Congrats to {self.winner.user.mention} for winning!\n\n" + self.game_as_poetic())

    def bootstrap(self):
        self.run(self._private.token)

    async def on_ready(self):
        print(f"Logged as {self.user}")
        self.game_update.start()

    def filter_mentions(self, mentions, author=None):
        return [x for x in mentions if (author is None or author != x) and not x.bot]

    def start_game(self, channel, user_mentions):
        if self.going_on:
            return GameStartError.GAME_GOING

        user_mentions = self.filter_mentions(user_mentions)

        if len(user_mentions) < required_players:
            return GameStartError.NOT_ENOUGH_PLAYERS

        self.start_time = perf_counter()
        self.players.clear()

        random.seed(perf_counter())

        for user in user_mentions:
            n_player = Player(user, channel)
            n_player.sent_time = self.start_time + 1.5
            self.players.append(n_player)
        
        self.going_on = True

    def player_from_user(self, user):
        for player in self.players:
            if user.id != player.user.id:
                continue
            return player

    def emoji_text(self, bridge=""):
        s = ""

        for c in bridge:
            s += ":blue_square:" if c == " " else f":regional_indicator_{c}:"

        return s

    # haha
    def game_as_poetic(self):
        s = ""

        for player in self.players:
            sliced_bridge = player.bridge[:self.goal]
            bridge_len = len(sliced_bridge)

            # string stuff

            actual_viewport_size = min(viewport_size, self.goal)

            clamp_x = self.goal-actual_viewport_size
            offset_x = min(max(bridge_len - (viewport_size//2), 0), clamp_x)
            viewport = [b'\xf0\x9f\x9f\xa9'.decode("utf-8") for _ in range(actual_viewport_size)]
            
            for i, char in enumerate(sliced_bridge[offset_x:]):
                viewport[i] = (ALPHABET.get(char) or "?")

            if offset_x >= clamp_x:
                viewport[-1] = ":checkered_flag:"
            else:
                viewport[-1] = ":arrow_right:"

                i = -2

                for number in list(str(int(self.goal-bridge_len)))[::-1]:
                    viewport[i] = (":" + str({
                            "1": "one",
                            "2": "two",
                            "3": "three",
                            "4": "four",
                            "5": "five",
                            "6": "six",
                            "7": "seven",
                            "8": "eight",
                            "9": "nine",
                            "0": "zero",
                        }.get(number)) + ":")

                    i -= 1

            viewport[max(min(bridge_len-offset_x, viewport_size-1), 0)] = ":partying_face:" if bridge_len>=self.goal else ":person_standing:"
            
            s += f"{player.user.name}#{player.user.discriminator}: {' '.join(viewport)}\n"

        return s

    async def on_message(self, message):
        is_dm = isinstance(message.channel, discord.channel.DMChannel)

        if message.author == self.user or (message.channel.id != self._private.channel and not is_dm):
            return

        if not is_dm:
            self.channel = message.channel

        content = message.content

        if content.startswith("!"):
            syntax = content.split()[0]
            command = syntax.split("!")[1].strip()
            player = self.player_from_user(message.author)

            if is_dm:
                if command == "leave" and player is not None:
                    self.players.pop(self.players.index(player))

                    await message.reply(f"Alright, you're now out of the game.\n\n{self.game_as_poetic()}")
                elif command == "skip" and player is not None:
                    if player.current_question is not None:
                        player.replace_question(random.uniform(5, 10))

                        await message.reply("Question skipped, you will have to wait a bit longer for a question.")
                    else:
                        await message.reply("You don't have a question to answer right now.")
                elif command == "question" and player is not None:
                    if player.current_question is not None:
                        await self.remind_player(player)
                    else:
                        await message.reply("You don't have a question to answer right now.")
            else:
                if command == "start":
                    error = self.start_game(message.channel, message.mentions)

                    if error is None:
                        await message.reply(f"The game starts ***now***!\n\n{self.game_as_poetic()}")

                        for player in self.players:
                            await player.user.send(f"*A new game has been set by* **{message.author.name}#{message.author.discriminator}**:\n\n" + self.game_as_poetic())
                    elif error == GameStartError.NOT_ENOUGH_PLAYERS:
                        await message.reply(f"At least 2 or more players can join, you can ping more players"+
                                "along with the `!start` command at the beginning.\n`!start @foo @bar`")
                    elif error == GameStartError.GAME_GOING:
                        await message.reply(f"There's a match going on now.")
                elif command == "help":
                    await message.reply(HELP_MESSAGE)
                elif command == "howto":
                    await message.reply(HOW_TO_MESSAGE)
        elif content.startswith("> ") and is_dm:
            answer = content[2:].lower()
            player = self.player_from_user(message.author)

            if player is not None:
                answer_state = player.answer(answer)
                
                if answer_state == AnswerQualifiation.CORRECT:
                    player.replace_question(random.randint(2, 4))
                    await message.reply(f"***Advance!***\n\n{self.game_as_poetic()}")
                elif answer_state == AnswerQualifiation.CLOSE:
                    await message.reply("You're close :eyes:")
                elif answer_state == AnswerQualifiation.NOT_QUITE:
                    await message.reply("Not quite. :x::man_gesturing_no:")



