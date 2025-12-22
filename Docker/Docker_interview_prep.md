# 🐳 DOCKER INTERVIEW QUESTIONS WITH ANSWERS

*(Simple English, interview-ready)*

---

## 🔹 BASIC LEVEL (Must Know)

### 1️⃣ What is Docker?

**Answer:**
Docker is a platform that packages an application and its dependencies into containers so it runs the same in all environments.

---

### 2️⃣ Why do we need Docker?

**Answer:**
To avoid “works on my machine” problems, manage dependencies easily, and deploy applications faster.

---

### 3️⃣ What is a Docker Image?

**Answer:**
A Docker image is a **read-only template** that contains application code, libraries, and runtime.

👉 Images are used to create containers.

---

### 4️⃣ What is a Docker Container?

**Answer:**
A container is a **running instance of a Docker image**.

👉 Image = blueprint
👉 Container = running app

---

### 5️⃣ Difference between Docker and Virtual Machine?

**Answer:**
Docker containers share the host OS kernel and are lightweight, while VMs have a full OS and are heavy.

---

### 6️⃣ What does `docker ps` do?

**Answer:**
It shows all **currently running containers**.

(`ps` = Process Status)

---

### 7️⃣ What does `docker ps -a` do?

**Answer:**
It shows **all containers**, including stopped ones.

---

### 8️⃣ What is Docker Hub?

**Answer:**
Docker Hub is a public registry where Docker images are stored and shared.

---

### 9️⃣ What is a Dockerfile?

**Answer:**
A Dockerfile is a text file with instructions to build a Docker image.

---

### 🔟 Difference between `RUN` and `CMD`?

**Answer:**

* `RUN` → executes while **building** the image
* `CMD` → executes when the **container starts**

---

## 🔹 INTERMEDIATE LEVEL

### 11️⃣ What is `ENTRYPOINT`?

**Answer:**
`ENTRYPOINT` defines the main command that **always runs** when the container starts.

---

### 12️⃣ Difference between `CMD` and `ENTRYPOINT`?

**Answer:**

* `CMD` can be overridden
* `ENTRYPOINT` cannot be overridden easily

👉 Often used together.

---

### 13️⃣ What are Docker Volumes?

**Answer:**
Volumes store data **outside containers**, so data is not lost when containers stop or restart.

---

### 14️⃣ Why do we need volumes?

**Answer:**
Containers are temporary. Volumes ensure **data persistence**.

---

### 15️⃣ What is Docker Compose?

**Answer:**
Docker Compose is used to run **multiple containers** using a single YAML file.

---

### 16️⃣ How do containers communicate with each other?

**Answer:**
Through Docker networks using **container names** as hostnames.

---

### 17️⃣ What is Docker Networking?

**Answer:**
Docker provides networking so containers can communicate internally and externally.

Default network: **bridge**

---

### 18️⃣ What is Port Mapping?

**Answer:**
It maps container port to host port.

Example:

```bash
-p 8080:80
```

---

### 19️⃣ How to check container logs?

**Answer:**

```bash
docker logs <container_id>
```

---

### 20️⃣ What is `docker exec`?

**Answer:**
Used to run commands inside a running container.

```bash
docker exec -it <container_id> bash
```

---

## 🔹 ADVANCED LEVEL

### 21️⃣ How does Docker achieve isolation?

**Answer:**
Using **Linux namespaces** (process, network, filesystem) and **cgroups** (CPU, memory control).

---

### 22️⃣ What are namespaces?

**Answer:**
Namespaces isolate system resources so containers think they have their own OS.

---

### 23️⃣ What are cgroups?

**Answer:**
Control how much CPU, memory, and disk a container can use.

---

### 24️⃣ What is a multi-stage Docker build?

**Answer:**
Using multiple `FROM` statements to reduce image size.

👉 Build tools in one stage, runtime only in final stage.

---

### 25️⃣ How to reduce Docker image size?

**Answer:**

* Use alpine images
* Use multi-stage builds
* Remove unnecessary packages

---

### 26️⃣ Docker vs Kubernetes?

**Answer:**

* Docker → creates containers
* Kubernetes → manages and orchestrates containers

---

### 27️⃣ How does Docker fit in CI/CD?

**Answer:**
Docker ensures the same build artifact moves from dev → test → prod.

---

### 28️⃣ How do you secure Docker containers?

**Answer:**

* Don’t run as root
* Use trusted images
* Scan images
* Limit resources

---

### 29️⃣ What is `.dockerignore`?

**Answer:**
It prevents unnecessary files from being copied into the image.

---

### 30️⃣ Difference between `COPY` and `ADD`?

**Answer:**

* `COPY` → simple file copy (recommended)
* `ADD` → extra features (URL, extract)

---

## 🔹 SCENARIO-BASED QUESTIONS (VERY IMPORTANT)

### 31️⃣ Container exits immediately — why?

**Answer:**
Main process finished execution. Containers live as long as the main process runs.

---

### 32️⃣ App works locally but not in Docker — why?

**Answer:**

* Missing dependency
* Wrong environment variables
* Port issues
* OS differences

---

### 33️⃣ Data lost after container restart — reason?

**Answer:**
No volume attached. Containers are ephemeral.

---

### 34️⃣ How to fix port already in use error?

**Answer:**
Use a different host port or stop the process using that port.

---

### 35️⃣ High memory usage in container — solution?

**Answer:**
Limit resources using:

```bash
--memory="512m"
```

---

### 36️⃣ How do you debug a failing container?

**Answer:**

* Check logs
* Exec into container
* Inspect Dockerfile
* Check environment variables

---

### 37️⃣ What happens when Docker daemon stops?

**Answer:**
All running containers stop.

---

### 38️⃣ Can multiple containers use same image?

**Answer:**
Yes, images are reusable.

---

### 39️⃣ Difference between image and container lifecycle?

**Answer:**
Images are static, containers are dynamic.

---

### 40️⃣ Real-world Docker use case?

**Answer:**
Running Airflow, Spark, Kafka, databases consistently across environments.

---

## ⭐ PERFECT INTERVIEW SUMMARY (Say This)

> “Docker helps package applications with all dependencies into lightweight containers, ensuring consistency, fast deployment, and efficient resource usage compared to virtual machines.”

---
