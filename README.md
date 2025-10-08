# Beacon Proxy for Frontend UI App

This is a **simple web proxy** that allows you to access the  [Beacon Network OMOP API](https://unicas.imib.es/beacon-network-omop/api) from your browser or web applications **without CORS problems**.

You don't need to know Python or Docker details — just follow the instructions below.

---

## 🚀 Quick Start


### 0. Install Docker
Make sure [Docker](https://www.docker.com/) is installed on your computer.  
(If you can run `docker --version` in a terminal, it's ready.)

---

### 1. ⚙️ Configuration (You MUST set this)

Before you can use the proxy, you **must tell it where your Beacon API is**.

Open the file `docker-compose.yml` and replace the value of `REAL_API_BASE`
(currently `MY_API_ENDPOINT`) with the URL of your real Beacon API.

For example:

```yaml
services:
  beacon-proxy:
    build: .
    ports:
      - "3001:8080"
    environment:
      REAL_API_BASE: HERE_YOUR_API_ENDPOINT    # ← CHANGE THIS
      PROXY_BASE_PATH: /api
      ALLOWED_ORIGINS: http://localhost:3000
      UPSTREAM_TIMEOUT: 60
      PORT: 8080
```

| Variable          | Description                                               | Default                              |
|-------------------|-----------------------------------------------------------|--------------------------------------|
| REAL_API_BASE     | Required — URL of your real Beacon API (must be changed). | HERE_YOUR_API_ENDPOINT               |
| PROXY_BASE_PATH   | Path prefix used by your web app (default /api).          | /api                                 |
| ALLOWED_ORIGINS   | Which websites are allowed to use this proxy (CORS)       | http://localhost:3000                |
| PORT              | Internal port used by the container                       | 8080 (exposed as 3001 on your PC)    |

##### ⚠️ Important: If you don't change REAL_API_BASE, the proxy will not know where to forward the requests.

---

### 2. Start the Proxy

In the folder where this project is located, just run:

```bash
docker compose up --build
```

- The first time, this will **build** the Docker image and start the proxy.
- Next time, you can simply use:

```bash
docker compose up -d
```

The proxy will run in the background.

---

### 3. Use it

Once running, the proxy is available at:

```
http://localhost:3001/api
```

Your web application (running on your computer, usually at `http://localhost:3000`)
should use this URL as its API base.

Example in JavaScript:

```js
const CONFIG = {
  apiUrl: "http://localhost:3001/api"
};
```

Now any request like:

```
GET  http://localhost:3001/api/service-info
POST http://localhost:3001/api/individuals
```

will be **forwarded automatically** to the real Beacon API:
`HERE_YOUR_API_ENDPOINT like http://MY_API or https://MY_API`

---

## 🧪 Check if it Works

Open your browser and go to:

```
http://localhost:3001/health
```

You should see:

```json
{ "ok": true }
```

You can also test with:

```bash
curl http://localhost:3001/api/service-info
```

---
---

## 👥 Authors

- Jessica Fernández Martínez — Barcelona Supercomputing Center (BSC)

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE).
