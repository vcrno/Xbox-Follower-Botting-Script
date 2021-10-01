from sys import exit
from typing import List
from colorama import init
from sys import platform
from os import system
import asyncio
import aiohttp

if platform == "win32": global clear; clear = "cls"
else: clear = "clear"

init(autoreset=True)

combos = []

class Follow_Bot:
    def __init__(self, token_list: List[str]):
        self.bots = token_list

    async def resolve_xuid(self, session: aiohttp.ClientSession, token: str) -> None:
        headers = {
            "Authorization": token,
            "x-xbl-contract-version": "2",
        }

        async with session.get("https://profile.xboxlive.com/users/me/id", headers=headers) as getXUID:
            if getXUID.status == 200:
                data = await getXUID.json()
                bot_xuid = data["xuid"]
                combos.append(f"{bot_xuid}:{token}")
                print(f"\x1b[1;33m Resolved XUID \x1b[1;37m-> \x1b[1;33m{bot_xuid}")
            else:
                print("\x1b[1;31m XUID Resolve \x1b[1;37m-> \x1b[1;31mFailed")

        
    async def add_friend(self, session: aiohttp.ClientSession, combo: str, target: str) -> None:
        comboN = combo.split(":", 1)

        headers = {
            "Authorization": comboN[1],
            "X-XBL-Contract-Version": "2"
        }

        async with session.put(f"https://social.xboxlive.com/users/xuid({comboN[0]})/people/gt({target})?app_name=xbox_on_windows&app_ctx=user_profile", headers=headers) as response:
            if response.status == 200 or response.status == 204: 
                print(f"\x1b[1;32m {comboN[0]} \x1b[1;37m-> \x1b[1;32mFollowed {target}")   
            else:
                print(f"\x1b[1;31m {comboN[0]} \x1b[1;37m-> \x1b[1;31mFailed to Follow {target}")  


    async def start(self, target):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.resolve_xuid(session, bot) for bot in self.bots])
            return await asyncio.gather(*[self.add_friend(session, bot, target) for bot in combos])


if __name__ == "__main__":
    try:
        system(clear)
        with open('tokens.txt', encoding='UTF-8') as tokenFile:
                token_list = [token.strip() for token in tokenFile]
        target = input(" \x1b[1;37m[ \x1b[1;36mXbox Follower Bot\x1b[1;37m ]\n \x1b[1;37mTarget \x1b[1;35mGamerTag\x1b[1;37m: ")
        follow = Follow_Bot(token_list)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(follow.start(target))
    except KeyboardInterrupt or Exception as ex:
        print(ex)
        exit(0)