# System architecture

GigOrbit ATS uses a **microservices** architecture to provide a modular,
scalable foundation for an applicant tracking system.  In this design, the
application is split into small, autonomous services, each responsible for a
well‑defined capability.  This section describes the key components and
rationale behind the chosen architecture.

## Why microservices?

Microservices are an alternative to monolithic application designs.  They
consist of **small, independent and loosely coupled components** that a
single team can build and maintain.  Each service has its own codebase and can
be deployed separately, which allows teams to update services without
redeploying the entire system.  Microsoft’s architecture guide explains that
a microservices architecture consists of a collection of small services; each
service implements a single business capability within a bounded context and
communicates through well‑defined APIs【671146846353065†L289-L326】.  Because each
service owns its own data and database schema, the system avoids the
tight coupling and shared data layers common in monoliths【671146846353065†L316-L326】.

The benefits of this approach include agility, independent scaling, fault
isolation and the ability to use different technologies per service
【671146846353065†L374-L404】.  However, it also introduces complexity in
orchestration, data consistency and observability【671146846353065†L417-L427】.  The
design presented here includes patterns to mitigate these challenges (e.g.
an API gateway, observability stack and Kubernetes for orchestration).

## High‑level design

At a high level, GigOrbit ATS consists of five major components:

1. **User service** – manages user registration, authentication and profile
   data.  It exposes REST endpoints for creating and retrieving user
   accounts.  Data is stored in its own SQLite or PostgreSQL database.
2. **Job service** – handles creation and listing of job postings.  Employers
   (suppliers) can post remote and cloud‑oriented roles.  The service owns
   its own database and exposes REST APIs for CRUD operations.
3. **Application service** – records applications submitted by users for
   specific jobs.  It links user IDs to job IDs and stores status flags
   (applied, in review, rejected, hired).
4. **Resume parser service** – accepts uploaded resumes (PDFs) and extracts
   structured fields such as name, email and phone number.  It uses open
   source libraries (`pdfminer.six` and `regex`) to perform basic parsing.
5. **Front‑end client** – a React application that provides a modern,
   responsive user interface.  It connects to the back‑end services via
   HTTP.  The UI uses a custom colour palette to convey a remote‑first
   energy: dark teal (`#004F5A`), electric blue (`#2F80ED`), lime green
   (`#7ED957`) and off‑white (`#FAFBFD`).

These components are containerised and run within a **Kubernetes** cluster.
Kubernetes provides orchestration, auto‑scaling and service discovery.  Each
service runs in its own pod and is exposed via a Kubernetes `Service` object.
An optional API gateway (e.g. Nginx or AWS ALB) routes incoming requests to
the appropriate service.

### Communication

Services communicate primarily through **HTTP/REST**.  For example, when
a user applies for a job, the front‑end client sends a POST request to
`/applications` on the Application Service.  The Application Service
stores the record in its database.  Microservices remain independent; they do
not share databases or call each other's internal storage.  Instead, they
interact via their APIs.  This aligns with the recommendation that services
communicate through well‑defined APIs and hide their internal
implementation details【671146846353065†L316-L324】.

### Observability and monitoring

To handle the complexity introduced by microservices, observability is
essential.  The architecture includes a **Prometheus** and **Grafana** stack
(not implemented in the code but described in the deployment instructions).
Prometheus scrapes metrics from each service, while Grafana provides
dashboards.  Logs should be centralised (e.g. with the EFK stack) to trace
requests across services【671146846353065†L356-L362】.

### Data storage

Each microservice manages its own database, following the **bounded context**
principle【671146846353065†L289-L327】.  In this example, SQLite is used for
simplicity.  In a production environment on AWS, you can replace SQLite with
Amazon RDS (PostgreSQL) or DynamoDB.  This approach allows each service to
choose the data store that fits its needs (polyglot persistence)
【671146846353065†L364-L370】.

### API gateway

Although the front‑end can call each service directly in this example,
larger deployments benefit from an API gateway.  The gateway serves as the
entry point for clients and can handle cross‑cutting concerns such as
authentication, rate limiting and request routing【671146846353065†L341-L344】.  In
AWS, you can use **AWS Application Load Balancer** or **API Gateway**.  For
local development, the provided `docker-compose.yml` proxies the `/api/*`
routes to the appropriate back‑end services.

## Future improvements

GigOrbit ATS provides a foundation that you can extend.  Potential
enhancements include:

* Implementing full authentication (e.g. JWT) and role‑based access control.
* Integrating a third‑party resume parsing API for improved accuracy.
* Adding asynchronous messaging (e.g. Kafka or RabbitMQ) for long‑running
  tasks and better decoupling【671146846353065†L350-L353】.
* Implementing an advanced search service for jobs and candidates.
* Adding more granular status tracking (interview stages, feedback, etc.)
  within the Application Service.

This architecture is intended as a starting point.  You can adapt and scale
it to meet your organisation’s needs.