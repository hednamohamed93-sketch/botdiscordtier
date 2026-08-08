# AllTiers Discord Bot

A Minecraft PvP tier-testing bot for Discord, built with `discord.py`.

## Structure

```
AllTiersBot/
├── bot.py            # Entrypoint: loads cogs, syncs slash commands, starts the bot
├── requirements.txt
├── .env.example      # Documents expected env vars (Replit already injects the real ones)
├── cogs/
│   ├── queue_cog.py    # /join, /leave, /queue, /panel, /claim + panel refresh loop
│   └── testing_cog.py  # /result, /rank, /leaderboard
├── utils/
│   ├── constants.py    # Gamemodes + 11-tier rank ladder
│   ├── permissions.py  # Staff/tester role + permission checks
│   ├── embeds.py       # Queue panel + test result embed builders
│   └── views.py        # Persistent "Join Queue" button view
├── database/
│   ├── db.py          # asyncpg connection pool (uses DATABASE_URL)
│   └── queries.py      # All reads/writes against the tier_* Postgres tables
├── assets/
└── logs/               # bot.log written here at runtime
```

## Data

This bot reads/writes the same Postgres tables created by the project's
Drizzle schema (`lib/db/src/schema/tier*.ts`): `tier_players`,
`tier_player_ranks`, `tier_test_results`, `tier_queue_entries`,
`tier_active_testers`, `tier_queue_panels`. It does not run its own
migrations -- the schema is the source of truth.

## Secrets

`DISCORD_BOT_TOKEN`, `DISCORD_CLIENT_ID`, and `DATABASE_URL` are already
configured as Replit secrets/env vars in this project -- no `.env` file is
needed to run it here.

## Inviting the bot

In the Discord Developer Portal, under your application's OAuth2 -> URL
Generator, select the `bot` and `applications.commands` scopes, plus Send
Messages / Embed Links / Use Slash Commands permissions, then use the
generated link to add the bot to your server. Slash commands register
automatically per-guild as soon as the bot joins.
