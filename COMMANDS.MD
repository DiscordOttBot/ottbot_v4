- [Commands](#commands)
  - [**Format**](#format)
    - [/command \<required argument\> [optional argument]](#command-required-argument-optional-argument)
  - [Help](#help)
    - [/help [command]](#help-command)
  - [Info](#info)
    - [/serverinfo](#serverinfo)
    - [/userinfo](#userinfo)
    - [/stats](#stats)
    - [/seen \<user\>](#seen-user)
    - [/spotlight <user>](#spotlight-user)
  - [Xp](#xp)
    - [/leaderboard](#leaderboard)
    - [/level [@user]](#level-user)
    - [/rank [@user]](#rank-user)
  - [RNG](#rng)
    - [/dice \<count> \<sides>](#dice-count-sides)
    - [/8ball \<question>](#8ball-question)
    - [/coinflip](#coinflip)
    - [/rand [min] [max]](#rand-min-max)
    - [/float](#float)
    - [/wheel \<items>](#wheel-items)
  - [Fun](#fun)
    - [/slap [@user]](#slap-user)
    - [/echo \<text>](#echo-text)
    - [/bababooey](#bababooey)
  - [Server Utility](#server-utility)
    - [/settings [setting] [value]](#settings-setting-value)
      - [ruleschannel](#ruleschannel)
      - [welcomechannel](#welcomechannel)
      - [adminchannel](#adminchannel)
      - [logchanel](#logchanel)
      - [defaultrole](#defaultrole)
      - [activerole](#activerole)
      - [muterole](#muterole)
      - [shadowbanrole](#shadowbanrole)
      - [antispam](#antispam)
      - [profanityfilter](#profanityfilter)
    - [/clear [count] [@user]](#clear-count-user)
    - [/setafk \<time> [reason]](#setafk-time-reason)
    - [/unafk](#unafk)
    - [/temprole \<name> \<duration>](#temprole-name-duration)
  - [Moderation](#moderation)
    - [/kick \<user> [reason]](#kick-user-reason)
    - [/ban \<user> [reason]](#ban-user-reason)
    - [/mute \<user> [duration]](#mute-user-duration)
    - [/shadowban \<user> [duration]](#shadowban-user-duration)
    - [/lock [channel] [duration]](#lock-channel-duration)
    - [/unlock [channel]](#unlock-channel)
  - [Giveaway](#giveaway)
    - [/giveaway \<message> [duration]](#giveaway-message-duration)
    - [/poll \<options> [duration]](#poll-options-duration)
  - [Stock](#stock)
    - [/stock \<ticker> [graph start]](#stock-ticker-graph-start)
  - [Weather](#weather)
    - [/weather \<zip> [days]](#weather-zip-days)
  - [Wiki](#wiki)
    - [/wiki \<word>](#wiki-word)
    - [/urbandictonary \<word>](#urbandictonary-word)
  - [Currency](#currency)
    - [/bal [@user]](#bal-user)
    - [/slots](#slots)
    - [/lootbox](#lootbox)
  - [Code runner](#code-runner)
    - [/run \<code>](#run-code)
  - [Games](#games)
    - [Minesweeper [diffaculty]](#minesweeper-diffaculty)
  - [Owner Only](#owner-only)
    - [setactivity \<message> [type]](#setactivity-message-type)
    - [/shutdown](#shutdown)

# Commands

## **Format**

### /command \<required argument\> [optional argument]

`required argument`: An argument that is required for the command to run.  
`optional argument` _default=command author_: An argument that is optional for the command to run and will default to the command author.

```
/command required_arg

command output...
```

```
/command required_arg optional_arg

different command output...
```

## Help

### /help [command]

Displays the Bot's help page.  
`command`: A specific command to view more details about.

```
/help

<embed>
```

## Info

### /serverinfo

Displays information about the current server.

```
/serverinfo

<embed>
```

### /userinfo

Displays information about the current user.

```
/userinfo

<embed>
```

### /stats

Displays statistics about the bot.

```
/stats

<embed>
```

### /seen \<user\>

Displays the approximate time the user was last online.

`user`: The user that will be checked.

```
/seen @user

user was last online 1:00:00 hour ago
```

### /spotlight <user>

Displays recient messages from a user.

`user`: The user who's messages will be displayed.

```
/spotlight @user

<embed>
```

## Xp

### /leaderboard

Displays the XP leaderboard.

```
/leaderboard

<embed>
```

### /level [@user]

Displays the current XP level for user.

`user` _default=command author_: The user who's level will be displayed.

```
/level

user is level 10 with 1000 xp
```

### /rank [@user]

Displays the current rank on the XP leaderboard.

`user` _default=command author_: The user who's rank will be displayed.

```
/rank

user is rank 1 with 100 levels
```

## RNG

### /dice \<count> \<sides>

Rolls dice and sums the total.

`count`: The number of dice that will be rolled.  
`sides`: The number of sides that are on the die.

```
/dice 5 6

1 + 5 + 3 + 6 + 2 = 17
```

### /8ball \<question>

Answers the question you asked the Bot.

`question`: The question that you want to be answered.

```
/8ball Is OttBot the best discord bot?

Of course
```

### /coinflip

Flips a coin.

```
/coinflip

heads
```

### /rand [min] [max]

Displays a random number between two numbers.

`min` _default=1_: The minimum value that the random number could be (inclusive.)  
`max` _default=10_: The maximum value that the random number could be (inclusive.)

```
/rand 1 100

69
```

### /float

Displays a floating point number between 0 and 1.

```
/float

0.76548654378
```

### /wheel \<items>

Similar to [wheel decide](https://wheeldecide.com/).

`items`: the list of items seperated by spaces which are up for selection.

```
/wheel @user1 @user2 @user3

@user3
```

## Fun

### /slap [@user]

Slap a user (virtually).

`user` _default=last message author_: The user who is being slapped.

```
user1: /slap @user2

OttBot: user2 was slapped by user1
```

### /echo \<text>

Repeats the text given.

`text`: The text that will be repeated.

```
/echo Hello there

Hello there
```

### /bababooey

Sends the file BABABOOEY.MP3.

```
/bababooey

<file>
BABABOOEY.MP3
</file>
```

## Server Utility

### /settings [setting] [value]

Update the OttBot setting for the server.

`setting`: The setting that will be displayed or updated.  
`value`: The new value for `setting`.

```
/settings

list of settings...
```

```
/settings welcomechannel

The current welcome channel is #new-members
```

```
/settings welcomechannel #general

The welcome channel was updated to #general
```

#### ruleschannel

The channel where the rules are located.

#### welcomechannel

The channel where the new member join message appears.

#### adminchannel

The channel where the bot will display admin realted log messages.

#### logchanel

The channel where the bot will log XP level messages.

#### defaultrole

The role given to users when they complete varification. e.g. @member

#### activerole

The role given to people who send messages frequently.

#### muterole

The role that limits users to send messages and speak. See [mute role guide](#).

#### shadowbanrole

The role that limits users access to server channels. See [shadowban role guide](#).

#### antispam

Mute members who send a specific amount of messages in a short period of time.

#### profanityfilter

Delete any message within a list of bad words.

### /clear [count] [@user]

Delete a specific number of message from every users or a specific user and logs the deleted messages if a log channel is set up.

`count` _default=10_: The number of messages that will be deleted.  
`user`: The user who's messages will be deleted

```
/clear 10

10 messages deleted:
    (messages...)
```

### /setafk \<time> [reason]

Displays a message saying that you are away whenever someone mentions you.
This will last until the time runs out or `/unafk` is used.

`time`: The time in days that you will be away.  
`reason`: The reason why you are away.

```
user1: /setafk 7 vacation

...

user2: @user1

OttBot: user1 will be back in 4 days, reason: vacation
```

### /unafk

Remove the user from afk watch.

```
/unafk

You are no longer afk.
```

### /temprole \<name> \<duration>

Creates a temporary role.

`name`: The name of the role.  
`duration`: The duration in hours that the role exists.

```
/temprole tournament 72

@tournament was created and will be deleted in 72 hours.
```

## Moderation

### /kick \<user> [reason]

Kicks a user from the server.

`user`: The user that will be kicked.  
`reason`: The reason why the user was kicked.

```
/kick @user1

user1 has been kicked from the server.
```

### /ban \<user> [reason]

Dans a user from the server.

`user`: The user that will be banned.  
`reason`: The reason why the user was banned.

```
/ban @user1

user1 has been banned.
```

### /mute \<user> [duration]

Gives the [mute role](#muterole) to the user.

`user`: The user that will be muted.  
`duration` _default=until tf2 gets an update (forever)_: The duration in minutes the user us muted.

```
/mute @user1 1
```

### /shadowban \<user> [duration]

Gives the [shadow ban role](#shadowbanrole) to the user.

`user`: The user that will be muted.  
`duration` _default=until tf2 gets an update (forever)_: The duration in minutes the user us banned.

```
/shadowban @user1 1
```

### /lock [channel] [duration]

Disables the ability to send messages in a channel.

`channel` _default=current channel_: The channel that will be locked.  
`duration`: The duration in hours that the channel will be locked.

### /unlock [channel]

Unlocks a channel if it is locked.

`channel` _default=current channel_: The channel that will be unlocked.

## Giveaway

### /giveaway \<message> [duration]

Creates a giveaway where that selects a random user who reacted to the message.

`message`: The message that will be displayed on the giveaway.  
`duration` _default=1_: The duration in days until the giveaway is drawn.

```
/giveaway "PS6 Giveaway" 1

PS6 Giveaway
(reactions)

...

user1 has won the giveaway

```

### /poll \<options> [duration]

Creates a poll with reaction options.

`options`: The options for the poll.  
`duration` _default=1_: The duration in days until the poll ends.

```
/poll "cats dogs"

1. cats
2. dogs
(reactions)

...

cats won the poll
```

## Stock

### /stock \<ticker> [graph start]

Displays the current price and a graph for the given stock.

`ticker`: The ticker symbol for the stock.  
`graph start` _default=7 days ago_: The day the graph should start.

```
/stock AAPL

$154.30
(graph)
```

<!-- ASCII graphs -->

## Weather

### /weather \<zip> [days]

Displays the weather for the zip code.

`zip`: The zip code for the weather.  
`days` _default=7_: The number of days to look ahead.

```
/weather 10001

weather for NEW YORK, New York:
day 1: 54 / 31
day 2...
```

## Wiki

### /wiki \<word>

Looks up the definition of a word on wikipedia.

`word`: The word or phrase to look up.

```
/wiki "underwater basket weaving"

Underwater basket weaving is an idiom referring pejoratively to supposedly useless or absurd college or university courses and often generally to refer to a perceived decline in educational standards.
```

### /urbandictonary \<word>

Looks up the definition of a word on urban dictonary.

`word`: The word or phrase to look up.

```
/urbandictonary pog

A word used to indicate excitement or an epic moment. Comes from Pogchamp.
```

## Currency

### /bal [@user]

Display the balance of a user

`user` _default=command author_: The user who's balance will be displayed.

```
/bal

$1,000
```

### /slots

Use a slot machine.

```

/slots

rolling...
0 0 1

-$10
```

### /lootbox

Claim any lootboxes gained from voting for the bot.

```
/lootbox

Claiming 3 lootboxes...
+$402
```

## Code runner

### /run \<code>

Not sure if this works with slash commands yet...

Runs code.

`code`: The code that will be run.

    /run ```py
    print("hello world")
    ```

    Code output:
    hello world

## Games

### Minesweeper [diffaculty]

Play minesweeper with spoiler messages.

`diffaculty` _default=easy_: The size of the minesweeper board.

```
/minsweeper

⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛
```


## Owner Only

### setactivity \<message> [type]

Sets the bot's activity.

`message`: The message that will be displayed on the bot's profile.  
`type`: The type of activity the bot is doing, e.g. LISTENING, WATCHING

```
/setactivity "over you" WATCHING
```

### /shutdown 
Shuts down the bot.

```
/shutdown

shutting down...
```







<!--
UP FOR DEBATE

    ## Fun

    twerk
    pepega
    bgunjm

    ## Random APIs

    fact -> api
    lmao -> alucard api
    quote

UNKNOWN/TODO

    ## Admin
    warn

    ## Other
    set welcome image

    ## Games
    blackjack  
    connect 4

    ## Misc

    wide -> "０ １ ２ ３ ４ ５ ６ ７ ８ ９ Ａ Ｂ Ｃ Ｄ Ｅ Ｆ Ｇ Ｈ Ｉ Ｊ Ｋ Ｌ Ｍ Ｎ Ｏ Ｐ Ｑ Ｒ Ｓ Ｔ Ｕ Ｖ Ｗ Ｘ Ｙ Ｚ ａ ｂ ｃ ｄ ｅ ｆ ｇ ｈ ｉ ｊ ｋ ｌ ｍ ｎ ｏ ｐ ｑ ｒ ｓ ｔ ｕ ｖ ｗ ｘ ｙ ｚ ， ． ： ； ！ ？ ＂ ＇ ｀ ＾ ～ ￣ ＿ ＆ ＠ ＃ ％ ＋ － ＊ ＝ ＜ ＞ （ ） ［ ］ ｛ ｝ ｟ ｠ ｜ ￤ ／ ＼ ￢ ＄ ￡ ￠ ￦ ￥"  
    prettify -> "𝙦𝙬𝙚𝙧𝙩𝙮𝙪𝙞𝙤𝙥𝙖𝙨𝙙𝙛𝙜𝙝𝙟𝙠𝙡𝙯𝙭𝙘𝙫𝙗𝙣𝙢𝙌𝙒𝙀𝙍𝙏𝙔𝙐𝙄𝙊𝙋𝘼𝙎𝘿𝙁𝙂𝙃𝙆𝙇𝙕𝙓𝘾𝙑𝘽𝙉𝙈𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"  
    color/colorpalette  
    ISS tracker  
    whois
    IRL event tracking: Leap day/second, ISS tracker
 -->
