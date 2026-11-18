# Reserve Dial

See EcoFlow DELTA 2 charge and the time available before your chosen reserve.

Set ECOFLOW_ACCESS_KEY, ECOFLOW_SECRET_KEY and ECOFLOW_SERIAL locally for your own station. The JSON config accepts reserve_percent and the official API origin for your region. Time to reserve scales the reported time to empty by the usable charge fraction at the current load. Charging or unknown telemetry shows no countdown. Vendor documentation: https://developer-eu.ecoflow.com/us/document/delta2.

## Connect the bar

Copy companion/example.json to a private config.json and adjust it for your source. From the project folder run `python3 companion/serve.py --config config.json`. Use Python 3.10+. Set Local companion URL to `http://127.0.0.1:8770/reading` on the emulator and allow local port 8770. On hardware, bind the companion to a trusted LAN interface and set its reachable address. The wheel browses pages. Click refreshes. Start pins or unpins the current page. The last good reading is labeled offline after a source error.

## Run locally

From this folder, run `~/.busy-emulator/bin/busy-emulator dev --once` with BUSY Bar Emulator open. Back exits.

![BUSY Bar front display](screenshots/front-1.png)
