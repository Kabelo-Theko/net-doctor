# net-doctor

A structured network troubleshooting assistant for first-line support.

It is not a chatbot. It is a decision tree that walks the same layered method I
use by hand: start at the physical link, then IP, gateway, DNS and finally the
application, one check at a time, and stop at the first thing that is actually
broken. At each step it tells you what to check, the command to run, and how to
read the result. At the end it gives a structured conclusion: the likely cause,
the fix, and when to escalate.

I built it because "the internet is down" is rarely one problem. The value of a
good technician is the order they check things in, and that order is exactly
what this encodes.

## Symptoms it covers

- One PC has no internet while others are fine
- A whole office or store is offline
- Can't reach an internal site or SharePoint while on VPN
- Wi-Fi keeps dropping or is slow

## How to run it

Standard library only. Python 3.10+.

```bash
# interactive: pick a symptom, answer each check y/n
python -m net_doctor.cli

# jump straight to one flow
python -m net_doctor.cli --flow one-pc-no-internet

# list the available flows
python -m net_doctor.cli --list
```

Example session (abridged):

```
CHECK: Is the network link up? ...
  run:        ipconfig
  Did this pass / look healthy? (y/n): y

CHECK: Does the PC have a valid IP address from DHCP?
  run:        ipconfig /all
  read it as: A 169.254.x.x address (APIPA) means DHCP failed.
  Did this pass / look healthy? (y/n): n

----------------------------------------------
LIKELY CAUSE
  The PC did not get an address from DHCP (self-assigned 169.254.x.x).
FIX
  Run 'ipconfig /release' then 'ipconfig /renew'. ...
WHEN TO ESCALATE
  If multiple PCs later show APIPA, escalate ...
```

## The web UI

There is a guided web version: pick a symptom and answer each check, and a
vertical "diagnostic spine" fills in as you go, ending on the cause/fix/escalate
card. It runs as a plain static page (host `docs/` free on GitHub Pages), or
behind the Python engine:

```bash
pip install -r requirements.txt
uvicorn web.server:app --reload
# open http://127.0.0.1:8000
```

With the server running, `GET /api/flows` returns the trees straight from
`net_doctor/flows.py`, so the page and the Python module never drift. A
`Dockerfile` and `render.yaml` are included for a free deploy.

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest
```

The tests check two things: every branch in every flow points at a real step
(no dead ends), and a scripted set of answers lands on the expected conclusion.

## How it is put together

```
net_doctor/
    flows.py    the decision trees as data (steps, branches, conclusions)
    engine.py   walks a tree; interactive or replaying a fixed set of answers
    cli.py      the interactive prompt
web/
    server.py   FastAPI: serves the UI and exposes the trees at /api/flows
docs/
    index.html  the guided web UI (also the static demo)
tests/
    test_flows.py
Dockerfile, render.yaml   free one-click deploy
```

Adding a symptom means adding one entry to `flows.py`. The engine and CLI do not
change, which is the point of keeping the logic as data.

## Honest limitations

- The commands assume a Windows desktop (ipconfig, nslookup). The method is the
  same on macOS/Linux; the command names differ (ifconfig/ip, dig).
- It guides a human through checks. It does not run the commands for you, by
  design: on a live network you want a person reading each result.

## Licence

MIT. See [LICENSE](LICENSE).
