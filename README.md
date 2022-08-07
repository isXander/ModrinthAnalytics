# Modrinth Analytics
CLI application to collect and view analytics for any modrinth user.

## Collecting analytic data
Currently, there is no way to automatically collect data, you have to manually collect
every day, every hour, whatever you want. (though you could create a systemd service on linux)

```sh
./mranalytics.py --token yourmodrinthtoken collect --user slug_or_id --db path_to_json (optional)
```

This automatically gathers downloads for all the user's projects and adds an entry to the JSON DB.
You can do this whenever you want, the graphing function automatically filters results to fit the timescale.

## Generating graphs
When you have enough data, you can then create a graph.

```shell
./mranalytics.py --token yourmodrinthtoken graph <total,individual> --time hourly,daily,weekly,monthly,annually (default daily) --user slug_or_id_you_collected --db path_to_json (optional)
```
