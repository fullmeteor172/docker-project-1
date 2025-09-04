# trimlink.org
A minimal URL shortener built with **FastAPI**.

## 🚀 Features

* Shorten long URLs into simple short codes.
* Redirect from short codes back to the original URL.
* Minimal frontend (`index.html`) with Tailwind + Lucide icons.
* FastAPI endpoints:

  * `GET /api/v1/status` → health check
  * `GET /api/v1/time` → current UTC time
  * `POST /api/v1/shorten` → shorten a URL
  * `GET /{code}` → redirect to original URL

---

## 🛠️ Setup (Local)

1. **Clone repo**
```bash
git clone https://github.com/fullmeteor172/docker-project-1
cd docker-project-1
```

2. **Run app locally using UV**
```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

   Visit 👉 [http://localhost:8000](http://localhost:8000)

---

## 🔄 Sync to VPS

This project uses **rsync** for deployment.
Your VPS runs the app inside a Docker container with **bind mounts**.

1. **Edit `sync.sh`**
   Update:

```bash
REMOTE_USER="your-ssh-user"
REMOTE_HOST="your-vps-ip"
REMOTE_DIR="/home/your-ssh-user/trimlink"
```

2. **Sync project**

```bash
./sync.sh
```

3. **On VPS**

```bash
cd ~/trimlink
docker compose up -d --build
```

   Now your app runs at `http://your-vps-ip`

---

## 📂 Project Structure

```
.
├── index.html        # frontend
├── main.py           # FastAPI app
├── pyproject.toml    # dependencies
├── uv.lock           # lock file
├── sync.sh           # rsync deploy script
└── README.md
```