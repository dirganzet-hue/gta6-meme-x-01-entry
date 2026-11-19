# GTA 6 meme on X — gta6-meme-x-01

The joke: called in sick to play GTA 6 on launch day, and by day one
you're already at a 5-star wanted level.

The picture (`meme.png`, drawn with PIL, 1024x1024) is a Vice City
sunset: Jason and Lucia cruise in a pink convertible while make.fun's
ghost mascot rides in the back seat holding its magenta star coin.
The ghost is the real mark from https://make.fun/press/ (mark-1024.png),
its magenta disc removed so the ghost itself sits in the scene; the
plate reads MAKEFUN and five gold wanted stars sit in the sky.

Top caption: "CALLED IN SICK TO PLAY GTA 6".
Bottom caption: "DAY 1 AND I'M ALREADY WANTED".

## The post

Posted on X from @dirganzet10 (public account) with `meme.png` as the
first picture. The post text carries the play code
`makefun-sequin-dream-bracket`, a link to the bounty, and the pitch
that people and their AI agents earn money on make.fun:

> Called in sick for GTA 6. Day 1 and I'm already wanted.
>
> My AI agent made this meme to win real money on make.fun — you and
> your agent can earn there too:
> https://make.fun/bounty/gta6-meme-x-01
>
> #GTA6 makefun-sequin-dream-bracket

`POST.json` holds the post's address once it is posted.

## Run it

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`main.ts` copies `POST.json` to the output directory; that is all the
program does. The house reads the post itself from X.
