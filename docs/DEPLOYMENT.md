# Self-Hosting the Agents Server

`scripts/python/server.py` exposes the agent over FastAPI. The default dev
workflow (`fastapi dev server.py`) only binds to `localhost`, which is fine
for local testing but leaves you with nothing reachable if you want to check
on your agent, or trigger trades, from another machine.

This guide covers running that server on spare hardware (an old laptop, a
home server, etc.) and exposing it to the internet with
[Caddy](https://caddyserver.com/) and a
[Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) —
no port forwarding, no static IP, and no inbound firewall rules to manage.

## Why a tunnel instead of opening a port

Forwarding a port on your router puts your machine directly on the public
internet: anyone scanning your IP can reach it. A Cloudflare Tunnel instead
runs an outbound-only connection from your machine to Cloudflare, which then
proxies traffic to it over that connection. Nothing needs to be reachable
from the outside, so there's no open port and no exposed IP to attack —
Cloudflare is the only thing the public ever talks to.

## What you need

- A machine to run the server on (any old laptop or desktop works — it just
  needs to stay powered on and connected)
- [Caddy](https://caddyserver.com/docs/install) — reverse proxy in front of
  the FastAPI app
- A free [Cloudflare](https://dash.cloudflare.com/) account with a domain
  added to it, and `cloudflared` installed
- About 30 minutes

## 1. Run the agent server

```bash
cd scripts/python
python setup.py
uvicorn server:app --host 127.0.0.1 --port 8000
```

Keep this bound to `127.0.0.1` — only Caddy, running on the same machine,
needs to reach it. Nothing outside the machine should talk to uvicorn
directly.

## 2. Put Caddy in front of it

Caddy terminates the connection from the tunnel and reverse-proxies to
uvicorn. Create a `Caddyfile`:

```
:8080 {
    reverse_proxy 127.0.0.1:8000
}
```

Then run it:

```bash
caddy run --config Caddyfile
```

## 3. Create the Cloudflare Tunnel

```bash
cloudflared tunnel login
cloudflared tunnel create agents-server
cloudflared tunnel route dns agents-server agents.yourdomain.com
```

Point the tunnel at the Caddy port from step 2:

```yaml
# ~/.cloudflared/config.yml
tunnel: agents-server
credentials-file: /root/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: agents.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
```

Start it:

```bash
cloudflared tunnel run agents-server
```

The server is now reachable at `https://agents.yourdomain.com`, with TLS
handled by Cloudflare, and no inbound port open on the host at all.

## Notes

- Add authentication (e.g. Cloudflare Access, or an API key check in the
  FastAPI app) before exposing anything that can place trades — this guide
  only covers network exposure, not authorization.
- To run both processes unattended, use `systemd` services (or equivalent)
  for `caddy` and `cloudflared` so they restart on boot/crash.
