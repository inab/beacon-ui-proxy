# Beacon Proxy

This is a **simple web proxy** that allows you to access the  
[Beacon Network OMOP API](https://unicas.imib.es/beacon-network-omop/api)  
from your browser or web applications **without CORS problems**.

You don’t need to know Python or Docker details — just follow the instructions below.

---

## 🚀 Quick Start

### 1. Install Docker
Make sure [Docker](https://www.docker.com/) is installed on your computer.  
(If you can run `docker --version` in a terminal, it’s ready.)

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

## ⚙️ Configuration

If you ever need to change something (normally you don’t):

- Open the `docker-compose.yml` file.
- You can change:

| Variable          | Description                                               | Default                              |
|-------------------|-----------------------------------------------------------|--------------------------------------|
| REAL_API_BASE     | URL of the real Beacon API                                | HERE_YOUR_API_ENDPOINT               |
| PROXY_BASE_PATH   | Path prefix for the proxy                                 | /api                                 |
| ALLOWED_ORIGINS   | Which websites are allowed to use this proxy (CORS)       | http://localhost:3000                |
| PORT              | Internal port used by the container                       | 8080 (exposed as 3001 on your PC)    |

---

## 👥 Authors

- Jessica Fernández Martínez — Barcelona Supercomputing Center (BSC)

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE).
