# Schedule File Format

## Cron

Parameters:
- year (int|str) – 4-digit year
- month (int|str) – month (1-12)
- day (int|str) – day of month (1-31)
- week (int|str) – ISO week (1-53)
- day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
- hour (int|str) – hour (0-23)
- minute (int|str) – minute (0-59)
- second (int|str) – second (0-59)

Example: this cron job runs every second at the 5th second of each minute.

```
cron
year=*
month=*
day=*
week=*
day_of_week=*
hour=*
minute=*
second=5
```


## Interval

Parameters:
- weeks (int) – number of weeks to wait
- days (int) – number of days to wait
- hours (int) – number of hours to wait
- minutes (int) – number of minutes to wait
- seconds (int) – number of seconds to wait

Example: Run the job every hour

```
interval
hours=1
```

## Date

> **WARNING**: Unsupport, use API instead