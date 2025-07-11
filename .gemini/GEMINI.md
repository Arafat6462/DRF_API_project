# Practice Project Blueprint: The "Mini-Trello" API (Docker-First Edition)

## 1. Core Philosophy

This document outlines the plan for a practice project designed to provide a deep, hands-on understanding of the technologies and principles required for the main "AI Job Tracker" application.

Our focus is not just on writing code, but on understanding **how and why things work under the hood**, following industry best practices at every step. This project is our training ground. We will prioritize learning and comprehension over speed. Each piece of code will be followed by an explanation of its role, its inner workings, and its place in the larger workflow.

## 2. Project Overview

We will build the backend API for a simple "Trello-like" project management tool. The entire development environment will run inside Docker containers from the very beginning.

**Core Features:**
- User registration and login (Authentication).
- Users can create, read, update, and delete their own **Projects**.
- Each Project can have associated **Tasks**.
- Users can only see and manage their own data (Authorization).

## 3. Core Learning Objectives

By the end of this project, we will have mastered the practical application of:
- **The Django vs. DRF Distinction:** We will deeply understand that **Django** is the core web framework used to build the application's foundation (models, ORM, admin), while **Django REST Framework (DRF)** is a powerful toolkit that sits *on top of Django* to efficiently build the Web API layer that serves JSON data.
- **Docker & Docker Compose:** Building and running a multi-service development environment (Django + PostgreSQL).
- **Basic Automated API Testing:** Writing simple, effective tests for our API endpoints using `pytest` to ensure our logic is working correctly and prevent future bugs.
- **PostgreSQL:** Using a production-grade relational database, specifically leveraging the `JSONField`.
- **JWT Authentication:** Implementing modern, stateless user authentication.
- **API Best Practices:** Data serialization, validation, permissions, and custom endpoints using DRF.
- **Industry-Standard Workflows:** Managing dependencies, running commands inside containers, and structuring a project for maintainability.

## 4. Step-by-Step Implementation & Learning Plan

---

### **Step 1: The Dockerized Foundation**
- **What We Will Build:**
    1. A `Dockerfile` that defines the environment for our Django application.
    2. A `docker-compose.yml` to orchestrate our services: a `backend` service (from the Dockerfile) and a `db` service (using the official PostgreSQL image).
    3. A `requirements.txt` file to manage Python dependencies (including `pytest`).
    4. A `.gitignore` and `.dockerignore` to keep our repository and image clean.
- **Learning Scope & "Under the Hood":**
    - **Images vs. Containers:** We'll solidify the difference between a blueprint (image) and a running instance (container).
    - **Docker Compose Networking:** Understand how `docker-compose` creates a private network, allowing our `backend` container to talk to the `db` container using its service name as a hostname.
    - **Volumes:** Learn how to use volumes to mount our local source code into the container, enabling live-reloading as we edit files.
    - **Environment Variables:** How to securely pass configuration like database credentials from `docker-compose.yml` into the Django application.
- **Connection to Final Project:** This creates the **exact** local development environment specified in the main project plan. This entire setup is directly reusable.

---

### **Step 2: Django Project Initialization & Database Connection**
- **What We Will Build:**
    1. Using `docker-compose exec`, we will run `django-admin startproject` and `startapp` to create the project structure *inside* the running container.
    2. We will configure Django's `settings.py` to connect to the PostgreSQL container.
    3. We will define a simple `Project` model and run our first `makemigrations` and `migrate`.
- **Learning Scope & "Under the Hood":**
    - **Container Entrypoint:** Understand how `docker-compose exec` gives us a shell inside our running container, which is the standard way to run management commands.
    - **Django ORM & Migrations:** See how Django translates our Python model class into SQL `CREATE TABLE` statements and applies them to the PostgreSQL database running in a separate container.
    - **Database Driver:** Understand the role of the `psycopg2-binary` library as the translator between Django's ORM and the PostgreSQL database protocol.
- **Connection to Final Project:** This is the identical process for initializing the main project and creating its models.

---

### **Step 3: Full CRUD API with DRF & Basic Testing**
- **What We Will Build:**
    1. A `/api/projects/` endpoint that supports full CRUD for the `Project` model using a `ModelSerializer` and a `ModelViewSet`.
    2. A simple test file using `pytest` and DRF's `APIClient` to verify that we can successfully create and retrieve a project via the API.
- **Learning Scope & "Under the Hood":**
    - **Serialization/Deserialization:** We'll dive deep into how a `Serializer` inspects a model and its fields to automatically create a JSON representation, and how it validates incoming JSON data before converting it back into a Python object.
    - **DRF Request/Response Cycle:** Trace an HTTP request from the moment it enters the container to when it hits the Django development server, is routed by URLs to our `ViewSet`, processed, and sent back as a JSON response.
    - **API Testing Principles:** Understand the "Arrange, Act, Assert" pattern for writing clean tests. Learn how a test client can simulate API requests without needing a real browser.
- **Connection to Final Project:** This is the exact pattern for building and testing the `/api/jobs/` endpoint.

---

### **Step 4: User Authentication & Permissions**
- **What We Will Build:**
    1. `/api/auth/` endpoints for registration and JWT-based login.
    2. We will link the `Project` model to the `User` model with a `ForeignKey`.
    3. We will implement a custom permission to ensure users can only edit/view their own projects.
    4. We will write tests to verify that unauthenticated users are denied access.
- **Learning Scope & "Under the Hood":**
    - **JWT Internals:** We'll discuss the three parts of a JWT (Header, Payload, Signature) and the cryptographic signature that prevents tampering.
    - **DRF Auth & Permission Flow:** See the exact order in which DRF checks for a token, authenticates the user, and then runs permission checks before allowing access to the view logic. This is a critical security concept.
- **Connection to Final Project:** This is the core security model for the entire final application.

---

### **Step 5: Advanced Modeling & Custom Endpoints**
- **What We Will Build:**
    1. A `metadata` `JSONField` on our `Project` model.
    2. A custom endpoint using the `@action` decorator, like `/api/projects/{id}/complete/`.
    3. A test for our custom action.
- **Learning Scope & "Under the Hood":**
    - **Querying JSONField:** Learn how the ORM translates Python lookups like `Project.objects.filter(metadata__priority='high')` into PostgreSQL-specific SQL queries that can efficiently search inside JSON data.
    - **DRF Routers:** Understand how the `@action` decorator dynamically adds a new route to the list of URLs managed by the `ViewSet`'s router.
- **Connection to Final Project:** This directly prepares us for the `resume_data` `JSONField` and the `/api/resumes/{id}/download/` custom action.

## 5. The Learning Notebook Workflow

To maximize our learning, we will maintain a `learning_log.md` file throughout the project. This will be our shared, dynamic notebook.

- **Process:** At the end of each major step, I will generate a summary containing key commands, core concepts, "under-the-hood" explanations, and best practices.
- **Action:** Upon your approval, I will append this summary to the `learning_log.md` file.
- **Outcome:** By the end of the project, you will have a comprehensive, personalized logbook detailing every part of our journey, serving as an invaluable reference for all future projects.

## 6. My Guiding Principles

- I will always explain the concepts behind a piece of code before or during its implementation.
- I will focus on the data flow and the "why" behind a design choice.
- I will maintain a clean, industry-standard project structure.
- I will encourage questions to ensure deep understanding at every step.
- All commands will be run through the lens of our containerized Docker environment.
- I will actively contribute to our shared `learning_log.md` at each step.
