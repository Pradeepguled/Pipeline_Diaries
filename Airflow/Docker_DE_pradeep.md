
---

```md
# 🚢 Docker for Data Engineers – Complete Notes by Pradeep Guled

---

Hey! 👋 I'm **Pradeep Guled**, and these are my personal notes while learning and using Docker as a Data Engineer.  
I wanted to keep things super simple and crystal clear — just like how I’d explain it to a friend.  
Let’s go! 💪

---

## 📌 What is Docker?

Docker is a tool that lets you **run software in clean, isolated environments**, called containers.  
Think of it as a **Tupperware box** where your software and all its ingredients (dependencies, libraries, OS) are packed neatly.

🔁 That way, it works the same:
- On my laptop
- On your laptop
- On a production server

---

## ✅ Why I Use Docker as a Data Engineer

- I can spin up **Airflow, Postgres, Spark** easily
- I don’t have to install 100 things locally
- I can simulate real data pipelines on my laptop
- It makes my code **portable and reproducible**
- It saves me hours of “setup” time

---

## 🔑 Docker Basics (My Simple Understanding)

| Term        | What It Means (My Notes)                                     |
|-------------|---------------------------------------------------------------|
| **Image**   | The **blueprint** of what to run                              |
| **Container** | A **live running copy** of an image                         |
| **Dockerfile** | A step-by-step **recipe** to build an image                |
| **Volume**  | Saves data **outside the container** (so it won’t be lost)   |
| **Port**    | Lets me **access apps** like Airflow UI from the browser     |
| **Docker Compose** | A tool to run **multiple containers** easily           |

---

## ⚙️ Tools I Use with Docker as a Data Engineer

Here’s what I regularly run using Docker:

- 🌀 **Apache Airflow** → For orchestrating ETL pipelines
- 🐘 **PostgreSQL** → For storing metadata and raw data
- ⚡ **Apache Kafka** → For real-time data pipelines
- ⚙️ **Apache Spark** → For big data transformations
- 📓 **Jupyter** → For data exploration
- 🪣 **MinIO** → For object storage (S3 alternative)
- 📊 **Superset / Metabase** → For dashboards

---

## 🧪 My Go-To PostgreSQL Docker Command

```bash
docker run --name pg-db \
  -e POSTGRES_PASSWORD=mypass \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres
```

💡 Why I like it:

* It saves data using volume
* I can connect from DBeaver, Airflow, Python, etc.

---

## 📂 My Dockerfile for a Simple Python ETL App

```Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main_etl.py"]
```

🛠️ Build and Run:

```bash
docker build -t etl-job .
docker run etl-job
```

---

## 🧱 Docker Compose: My Airflow + Postgres + Spark Setup

```yaml
version: '3'
services:
  postgres:
    image: postgres
    environment:
      POSTGRES_PASSWORD: airflow
    ports:
      - "5432:5432"

  airflow:
    image: apache/airflow:2.8.1
    depends_on:
      - postgres
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://postgres:airflow@postgres:5432/postgres
    volumes:
      - ./dags:/opt/airflow/dags
    ports:
      - "8080:8080"
    command: webserver

  spark:
    image: bitnami/spark:latest
    ports:
      - "4040:4040"
```

Run it all in one shot:

```bash
docker-compose up
```

---

## 📊 Run Jupyter for Data Exploration

```bash
docker run -p 8888:8888 jupyter/base-notebook
```

Then go to:

👉 [http://localhost:8888](http://localhost:8888/)

---

## 🔥 My Most Used Docker Commands

```bash
# Pull image
docker pull <image-name>

# Run container
docker run <image-name>

# Show running containers
docker ps

# Show all containers
docker ps -a

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# Remove image
docker rmi <image-id>

# See logs
docker logs <container-id>

# Open shell in container
docker exec -it <container-id> bash
```

---

## 🧹 Cleanup Commands (I use these when things get messy)

```bash
# Stop everything
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Clean up unused stuff
docker system prune
```

---

## 🧰My Docker Tips 💡

* Use official images from Docker Hub (e.g., `postgres`, `apache/airflow`)
* Keep Dockerfile **simple and focused**
* Always use `.dockerignore`
* Mount volumes to avoid data loss
* Expose only required ports
* Use **tags** like `:2.8.1` to avoid surprise updates

---

## 🏗️ My Folder Structure for Airflow Projects

```
my-etl-project/
│
├── dags/
│   └── my_dag.py
├── data/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ✨ Quick Airflow Setup (My Personal Flow)

1. Make folder `airflow-lab`
2. Add `dags/` folder and a `docker-compose.yml`
3. Add a sample DAG like `hello_dag.py`
4. Run:

```bash
docker-compose up
```

5. Visit → `http://localhost:8080`

---

## 📈 Docker vs VM (Simple View I Keep in Mind)

| Feature          | Docker             | VM            |
| ---------------- | ------------------ | ------------- |
| Speed            | Fast 🏎️          | Slow 🐢       |
| Size             | Small 🧊           | Large 🧱      |
| OS Isolation     | No (shares kernel) | Yes (full OS) |
| Startup Time     | Seconds ⏱️       | Minutes ⏳    |
| Use in pipelines | ✅ Great           | ❌ Not ideal  |

---

## 📋 Docker Checklist for Data Engineers (My Tracker ✅)

| Topic / Skill                        | ✅ Learned |
| ------------------------------------ | ---------- |
| Basic Docker Commands (pull, run)    |            |
| Writing Dockerfile for ETL Jobs      |            |
| Docker Compose Usage                 |            |
| Connecting Airflow + Postgres        |            |
| Mounting Volumes                     |            |
| Running Spark / Kafka in Docker      |            |
| Using Docker with Jupyter            |            |
| Docker Cleanup Techniques            |            |
| Building & Pushing Images (optional) |            |

---

## 🧠 Final Thoughts 

Docker is now a **non-negotiable skill** for me as a data engineer.

It:

* Makes my work portable 🧳
* Keeps things clean and isolated 🧼
* Helps me test full pipelines locally ⚙️
* Saves time and headaches 🤯

> "If it runs on Docker, it’ll run anywhere — confidently."

Keep building, keep learning.


```

---

Let me know if you'd also like:
- A **GitHub README template**
- A `.env` integration example
- A **Docker + Airflow project** ready to run

Just say the word!
```
