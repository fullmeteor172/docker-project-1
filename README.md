# trimlink.org
A minimal URL shortener built with **FastAPI** & **Redis**.

## 🚀 Features

* Shorten long URLs into short codes
* Redirect back to original URLs
* Minimal frontend (`index.html`) with Tailwind + Lucide icons
* FastAPI endpoints:

  * `GET /api/v1/status` → health check
  * `GET /api/v1/time` → current UTC time
  * `POST /api/v1/shorten` → shorten a URL
  * `GET /{code}` → redirect

---

## 🛠️ Development (Local)

```bash
# start services (API + Redis)
docker compose up
```

This uses **`docker-compose.override.yml`**:

* Builds `trimlink-api` from `Dockerfile`
* Mounts source code → live reload with Uvicorn
* Redis exposed on `localhost:6379`

Visit 👉 [http://localhost:80](http://localhost:80)

---

## 🚢 Production (VPS)

On your server:

```bash
git clone https://github.com/fullmeteor172/docker-project-1
cd docker-project-1
docker compose -f docker-compose.yml up -d
```

Production uses:

* `fullmeteor172/trimlink-api` image from Docker Hub
* No bind mounts (image contains the code)
* **Watchtower** auto-updates the API container

---

## 🔄 Deployments

* GitHub Actions CI/CD builds and pushes `trimlink-api` to Docker Hub on every push to `main`.
* VPS pulls updated images automatically via Watchtower.

---

## 📂 Project Structure

```
.
├── docker-compose.yml          # prod (pulls image + watchtower)
├── docker-compose.override.yml # dev (local build + bind mounts)
├── Dockerfile                  # trimlink-api build
├── main.py                     # FastAPI app
├── index.html                  # frontend
├── pyproject.toml / uv.lock    # deps
└── sync.sh                     # optional rsync deploy script
```