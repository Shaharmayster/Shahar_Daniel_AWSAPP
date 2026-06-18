# Grandma Greeting Generator

## Document Purpose

This file is the **single source of truth** for the Grandma Greeting Generator project.

Any developer or AI assistant working on this repository must read this document first before making changes. It defines what the project is, why it exists, what is required, what is forbidden, how development is phased, and what success looks like at each stage.

**Current project stage:** Phase 1 complete. Local Flask + SQLite application is implemented.

---

## What This Project Is

Grandma Greeting Generator is a cloud-native web application developed as the final project for the university course **"Cloud Computing with Cloud Services Management"**.

The application allows users to generate funny, personalized greetings in different "grandma styles" (Polish Grandma, Moroccan Grandma, etc.) and store generated greetings in a database.

### Example

**Input:**

- Greeting Type: Shabbat Shalom
- Recipient: Grandchildren
- Grandma Style: Polish Grandma

**Output:**

> Shabbat Shalom my dear grandchildren ❤️
>
> Did you eat today? You look too skinny in the last picture.

---

## Why This Project Exists

The purpose of this project is **not** to build a complex product.

The purpose is to demonstrate the ability to:

- Deploy a highly available cloud application using managed AWS services
- Manage infrastructure using Infrastructure as Code (Terraform)
- Operate a production-style architecture with load balancing, auto scaling, and a managed database

**Application complexity is intentionally low. Infrastructure quality is the primary goal.**

---

## Academic Context

**Course:** Cloud Computing with Cloud Services Management

**Main topics covered in the course:**

- AWS
- VPC
- EC2
- RDS
- ELB (Elastic Load Balancer)
- ASG (Auto Scaling Group)
- IAM
- Terraform
- Managed Cloud Services

**Grading focus:** Demonstrating cloud architecture and infrastructure management, not application sophistication.

---

## University / Final Project Requirements

The final solution **must** satisfy all course requirements listed below.

### Mandatory AWS Services

The final deployed solution must include:

| Service | Required |
|---------|----------|
| VPC | Yes |
| EC2 | Yes |
| RDS | Yes |
| ELB | Yes |
| ASG | Yes |
| Terraform | Yes |
| S3 | Optional |

### Infrastructure Requirements

The application must:

- Be deployed using **Terraform**
- Run on **at least 2 EC2 instances**
- Use a **pre-existing RDS database supplied by the instructor**
- Be accessible through an **ELB**
- Run behind an **ASG (Auto Scaling Group)**
- **Continue functioning if one EC2 instance is terminated**
- **Demonstrate read and write operations** to the database

### Demonstration Requirements (Final Presentation)

During the final presentation (maximum 15 minutes), the following must be demonstrated:

1. Terraform deployment
2. AWS resource creation
3. EC2 instances running
4. Auto Scaling Group in operation
5. Load Balancer routing traffic
6. Application functionality (greeting generation)
7. Database updates (greeting persisted to RDS)
8. Terminating one EC2 instance
9. Continued system availability after instance failure

**Success on the availability test = passing the high-availability requirement.**

### Repository Requirements

- The GitHub repository must be **PRIVATE**
- Repository must contain top-level directories: `frontend/`, `backend/`, `terraform/`
- Repository must be submitted **at least 3 days before** the presentation date
- **No code changes are allowed** during the final 3 days before the presentation

---

## Technology Constraints

### Allowed Technologies

| Layer | Technology |
|-------|------------|
| Language | **Python only** (application code) |
| Backend framework | **Flask** |
| Frontend markup | **HTML** |
| Frontend styling | **CSS** |
| Frontend scripting | **Minimal JavaScript** — only if absolutely necessary |
| Templates | **Jinja** (server-side, rendered by Flask) |
| Phase 1 database | **SQLite** |
| Phase 2+ database | **RDS (MySQL)** — instructor-supplied |
| Infrastructure | **Terraform** |
| Cloud provider | **AWS** (mandatory services listed above) |

### Forbidden Technologies

The following must **not** be used unless explicitly approved later in writing:

| Forbidden | Reason |
|-----------|--------|
| React | Frontend must be standard HTML/CSS |
| Angular | Frontend must be standard HTML/CSS |
| Vue | Frontend must be standard HTML/CSS |
| Node.js backend | Backend must be Python/Flask only |
| TypeScript | Python-only application stack |
| Docker | Not part of course requirements |
| Kubernetes | Not part of course requirements |
| AI integrations | Greetings use predefined Python templates only |
| External APIs | No third-party service dependencies |
| Additional AWS services | Beyond mandatory list, unless explicitly approved |

### Design Principles

1. **Reliability** — the system must survive a single EC2 failure
2. **Simplicity** — keep the application intentionally simple
3. **Terraform compatibility** — infrastructure must be fully provisioned via Terraform
4. **Easy deployment** — straightforward to deploy and demonstrate
5. **Easy migration** — SQLite to RDS must require minimal code changes
6. **Stateless application** — no server-side session state; all persistence in the database

---

## Application Requirements

### User Interface (Single Page)

The application is a single-page web application with the following controls:

#### Greeting Type (dropdown)

- Shabbat Shalom
- Happy Birthday
- Holiday Greeting
- Missing You
- Congratulations

#### Recipient (dropdown)

- Grandchildren
- Grandson
- Granddaughter
- Family
- Son
- Daughter

#### Grandma Style (dropdown)

- Polish Grandma
- Moroccan Grandma
- Iraqi Grandma
- Russian Grandma

#### Generate Button

When pressed:

- Generate a greeting using **predefined templates**
- Use **pure Python logic** — no AI, no external APIs
- **Store every generated greeting** in the database
- Display the result on the page

### Greeting Generation Rules

- Greetings are produced from a fixed set of templates keyed by greeting type and grandma style
- The selected recipient is interpolated into the template
- Each grandma style should produce a distinct tone and personality
- No randomness from external services; all logic is local Python

### Database Requirements

#### Table: `greetings`

| Column | Description |
|--------|-------------|
| `id` | Primary key, auto-increment |
| `created_at` | Timestamp of generation |
| `greeting_type` | Selected greeting type |
| `recipient` | Selected recipient |
| `grandma_style` | Selected grandma style |
| `generated_text` | The full generated greeting text |

**Every generated greeting must be stored.** No exceptions.

### Greeting History

- Display the most recent generated greetings on the home page
- Show the **latest 20 greetings**
- This feature exists to support demonstration of database **read** operations in later phases

---

## Development Phases

Development follows a strict phased approach. **Complete each phase fully before moving to the next.**

```mermaid
flowchart LR
    Phase1[Phase1_Local] --> Phase2[Phase2_RDS]
    Phase2 --> Phase3[Phase3_AWS]
```

---

### Phase 1 — Local Development

**Status:** Complete

**Goal:** Build a complete, working application locally with no cloud dependencies.

#### Infrastructure (Phase 1)

```
User Browser
    ↓
Flask Application
    ↓
SQLite Database
```

#### What Phase 1 Includes

- Flask backend serving the application
- HTML + CSS frontend (Jinja templates)
- SQLite database for persistence
- Greeting generation from predefined Python templates
- Form with three dropdowns and a Generate button
- Greeting history showing the latest 20 entries
- Local development and testing only

#### What Phase 1 Does NOT Include

- AWS (any service)
- Terraform
- RDS
- Docker
- ELB, ASG, EC2, VPC
- Any cloud infrastructure

#### Phase 1 Success Criteria

- [x] Application runs locally without errors
- [x] User can select greeting type, recipient, and grandma style
- [x] Generate button produces a humorous, personalized greeting
- [x] Every generated greeting is saved to SQLite
- [x] Latest 20 greetings are displayed on the page
- [x] Data persists across application restarts
- [x] No forbidden technologies are used

---

### Phase 2 — Database Migration

**Status:** Not started (depends on Phase 1 completion)

**Goal:** Replace SQLite with the instructor-supplied RDS database without changing application logic.

#### What Changes

- Database connection layer only
- Connection string moved to environment variables

#### What Does NOT Change

- Application business logic
- Greeting generation logic
- Frontend
- Routes and user-facing behavior

#### Connection String Migration

| Phase | Connection |
|-------|------------|
| Phase 1 | `sqlite:///local.db` |
| Phase 2 | `mysql://user:password@rds-endpoint/database` (via environment variable) |

The application must read the database connection string from an environment variable (e.g. `DATABASE_URL`) so that switching between SQLite and RDS requires **no code changes** — only a configuration change.

#### Phase 2 Success Criteria

- [ ] Application connects to RDS successfully
- [ ] Greeting generation works identically to Phase 1
- [ ] Greetings are written to RDS
- [ ] Greeting history reads from RDS
- [ ] Application logic (beyond the database layer) is unchanged
- [ ] Connection string is configured via environment variable

---

### Phase 3 — AWS Infrastructure Deployment

**Status:** Not started (depends on Phase 2 completion)

**Goal:** Deploy the application to AWS using Terraform, demonstrating high availability.

#### Production Architecture (Final)

```
User Browser
    ↓
Application Load Balancer (ELB)
    ↓
Auto Scaling Group (ASG)
    ↓
EC2 Instance #1    EC2 Instance #2
    ↓                    ↓
         RDS Database
         (instructor-supplied)
```

#### What Terraform Must Provision

- VPC
- Subnets (public and/or private as appropriate)
- Security Groups
- Launch Template
- Auto Scaling Group (minimum 2 instances)
- Target Group
- Application Load Balancer (ELB)

#### What Terraform Does NOT Provision

- **RDS** — supplied by the instructor; referenced via configuration only

#### Application Deployment Model

- The application must be **stateless** — any EC2 instance can handle any request
- Database persistence is handled entirely by RDS
- If one EC2 instance is terminated, the ASG replaces it and the ELB routes traffic to surviving instances
- The application on each EC2 instance connects to the same RDS endpoint

#### Availability Test Scenario (Final Exam)

This is the definitive pass/fail test for the project:

1. User accesses the application through the ELB URL
2. Application runs on two EC2 instances
3. User generates a greeting
4. Greeting is written to RDS
5. One EC2 instance is manually terminated
6. Application remains operational
7. ELB routes traffic to the surviving instance
8. Previously stored greetings are still readable from RDS

**Pass = system survives single server failure with no data loss.**

#### Phase 3 Success Criteria

- [ ] `terraform apply` provisions all required AWS resources
- [ ] Application is accessible via ELB DNS name
- [ ] At least 2 EC2 instances are running in the ASG
- [ ] Greeting generation works through the ELB
- [ ] Greetings are written to RDS
- [ ] Greeting history reads from RDS
- [ ] Terminating one EC2 instance does not break the application
- [ ] ASG launches a replacement instance (or traffic continues on surviving instance)
- [ ] All mandatory AWS services are in use: VPC, EC2, RDS, ELB, ASG, Terraform

---

## Final Success Definition

The project is considered fully successful when:

| Criterion | Phase |
|-----------|-------|
| Local application works end-to-end | Phase 1 |
| Application works with RDS | Phase 2 |
| Terraform deploys full AWS infrastructure | Phase 3 |
| Application runs on AWS behind ELB and ASG | Phase 3 |
| Database read/write demonstrated live | Phase 3 |
| System survives EC2 instance termination | Phase 3 |
| Final presentation requirements met | All |

**Ultimate goal:** Pass the course project with a fully working, highly available cloud deployment.

---

## Implementation Guidelines for Future Developers and AI Assistants

When implementing this project, follow these rules:

1. **Read this file first.** Do not assume requirements from prior conversations.
2. **Respect the current phase.** Do not introduce AWS, Terraform, or RDS during Phase 1.
3. **Do not add complexity.** The application is a vehicle for demonstrating infrastructure skills.
4. **Keep the database layer isolated.** All database access must go through a dedicated module so Phase 2 migration is a single-layer change.
5. **Use environment variables for configuration.** Database URLs, ports, and secrets must not be hardcoded.
6. **Do not use forbidden technologies** listed in this document.
7. **Do not add AWS services** beyond the mandatory list without explicit approval.
8. **Do not use AI or external APIs** for greeting generation.
9. **Store every greeting.** The history feature and the final demo both depend on persistent writes.
10. **Prioritize demonstrability.** Every feature should be easy to show in a 15-minute presentation.

---

## Presentation Checklist

Use this checklist when preparing for the final presentation:

- [ ] Terraform code is ready and tested
- [ ] `terraform apply` completes without errors
- [ ] ELB URL is accessible from a browser
- [ ] Two EC2 instances visible in ASG
- [ ] Generate a greeting live — confirm it appears in history
- [ ] Confirm greeting exists in RDS (read operation)
- [ ] Terminate one EC2 instance in AWS Console
- [ ] Confirm application still responds via ELB
- [ ] Confirm greeting history still loads (RDS read after failure)
- [ ] Presentation fits within 15 minutes

---

## Change Control

- No code changes are permitted during the **final 3 days** before the presentation date
- Any deviation from this document (new technologies, additional AWS services, architecture changes) requires explicit approval before implementation
- Changes to this document should be made deliberately and reflect agreed decisions, not ad-hoc implementation choices
