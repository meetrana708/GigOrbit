# GigOrbit ATS

**GigOrbit ATS** is a minimal applicant tracking system (ATS) designed for
cloud‑native deployments.  It targets cloud and remote job postings and is
optimised for freelancing and project based hiring.  The application uses a
**microservices** architecture, which makes it easy to scale individual
components independently and to integrate new services in the future.  Each
service runs in its own container and can be deployed separately to a
Kubernetes cluster.

This repository contains the source code for the front‑end web client, four
back‑end microservices and the necessary Docker and Kubernetes configuration.
It also includes basic CI/CD workflow files and documentation explaining how
to build, run and deploy the system.

## Features

* **User profiles** – job seekers can register, log in and maintain a profile.
* **Job postings** – employers can create new job listings targeted at remote
  and cloud‑based roles.
* **Applications** – candidates can apply for a job; records are stored
  per job and per user.
* **Resume parsing** – resumes (PDFs) can be uploaded; the parser service
  extracts basic fields (name, email, phone) using open‑source libraries.  More
  advanced parsing can be added easily via third‑party APIs.
* **Modern UI** – the front‑end uses React and a custom colour palette:
  * Dark teal `#004F5A` for primary navigation
  * Electric blue `#2F80ED` for interactive elements
  * Lime green `#7ED957` for success states
  * Off‑white `#FAFBFD` for backgrounds
* **Microservices** – each service owns its own database and API.  They
  communicate over HTTP and are exposed via an API gateway (Nginx) or directly
  from the front‑end.
* **Docker & Kubernetes** – services are containerised with individual
  `Dockerfile`s.  Kubernetes manifests (deployments and services) are
  provided for each component.
* **CI/CD pipeline** – a sample GitHub Actions workflow demonstrates how to
  build the Docker images and push them to an AWS Elastic Container Registry
  (ECR).  It also shows how to deploy to an EKS cluster using `kubectl`.

## Repository structure

```
gigorbit-ats/
├── README.md                  – project overview (this file)
├── docs/
│   └── architecture.md        – architectural overview and design rationale
├── services/
│   ├── user-service/          – Flask service for user accounts
│   ├── job-service/           – Flask service for job postings
│   ├── application-service/   – Flask service for job applications
│   └── resume-parser-service/ – Flask service for resume parsing
├── frontend/                  – React client application
├── k8s/                       – Kubernetes manifests
├── docker-compose.yml         – local multi‑container configuration
└── .github/
    └── workflows/ci-cd.yml   – sample GitHub Actions pipeline
```

## Quick start

To run the entire stack locally using Docker Compose:

```bash
cd gigorbit-ats
docker-compose up --build
```

The services will be reachable on the following ports by default:

| Service                 | Description            | Port |
|-------------------------|------------------------|------|
| front‑end               | React web client       | 3000 |
| user‑service            | API for user accounts  | 5001 |
| job‑service             | API for job postings   | 5002 |
| application‑service     | API for applications   | 5003 |
| resume‑parser‑service   | API for resume parsing | 5004 |

Open your browser to `http://localhost:3000` to view the UI.  The client
connects to the back‑end services via the relative paths `/api/users`,
`/api/jobs`, `/api/applications` and `/api/parse` (these are proxied in
`frontend/package.json`).

## Deployment

The `k8s/` directory contains Kubernetes manifests for each service and the
front‑end.  These files create deployments, services and ingress resources.
To deploy to a cluster:

```bash
kubectl apply -f k8s/
```

For production deployments on AWS EKS, an ingress controller such as AWS
Load Balancer Controller or Nginx Ingress is recommended.  The included
manifests are basic and intended as a starting point.

### CI/CD pipeline

The `.github/workflows/ci-cd.yml` workflow demonstrates a simple pipeline
to build Docker images, push them to ECR and deploy them to EKS.  It
assumes the following secrets are defined in your GitHub repository:

| Secret                   | Purpose                                 |
|--------------------------|-----------------------------------------|
| `AWS_ACCESS_KEY_ID`      | AWS access key for ECR/EKS              |
| `AWS_SECRET_ACCESS_KEY`  | AWS secret key                          |
| `AWS_REGION`             | AWS region (e.g. `us-east-1`)            |
| `ECR_REGISTRY`           | ECR registry URI                        |
| `KUBECONFIG`             | Base64‑encoded kubeconfig for EKS       |

The pipeline is triggered on pushes to the `main` branch.  You may adapt
it to suit your own workflow and infrastructure.

## Licence

This project is released under the MIT licence.  Feel free to use and
extend it for your own purposes.