# Grandma Greeting Generator

## Document Purpose

This file is the **single source of truth** for the Grandma Greeting Generator project.

Any developer or AI assistant working on this repository must read this document first before making changes. It defines what the project is, why it exists, what is required, what is forbidden, how development is phased, and what success looks like at each stage.

**Current project stage:** Phase 2 complete (Terraform infrastructure code prepared). Phase 3 (RDS creation and integration) is postponed until a few days before the final presentation.

---

## What This Project Is

Grandma Greeting Generator is a cloud-native web application developed as the final project for the university course **"Cloud Computing with Cloud Services Management"**.

The application allows users to generate funny, personalized greetings in different "grandma styles" (Polish Grandma, Moroccan Grandma, etc.) and store generated greetings in a database.

### Example

**Input:**

- Greeting Type: שבת שלום
- Recipient: נכדים
- Grandma Style: סבתא פולניה

**Output:**

> שבת שלום נכדים שלי היקרים ❤️
>
> אכלתם היום משהו? אתם נראים רזים מדי בתמונה האחרונה.

Plus a matching local GIF displayed alongside the greeting text.

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
| Phase 3+ database | **RDS (MySQL)** — instructor-supplied, created manually |
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

The application is a **Hebrew-first**, right-to-left single-page web application targeting Israeli users and grandmothers.

#### Greeting Type (dropdown) — סוג ברכה

- שבת שלום
- מזל טוב
- חג שמח
- מתגעגעת אליכם
- ברכות

#### Recipient (dropdown) — למי הברכה?

- נכדים
- נכד
- נכדה
- משפחה
- בן
- בת

#### Grandma Style (dropdown) — סגנון סבתא

- סבתא פולניה
- סבתא מרוקאית
- סבתא עיראקית
- סבתא רוסיה

#### Generate Button — צור ברכה

When pressed:

- Generate a greeting using **predefined templates** (in Hebrew)
- Select a matching **local static GIF** based on greeting type and grandma style
- Use **pure Python logic** — no AI, no external APIs
- **Store every generated greeting** in the database
- Display the greeting text and GIF on the page (no history list in the UI)

### GIF Requirements (Phase 1)

- GIFs are **predefined local static files** in `frontend/static/gifs/`
- GIF selection is based on **greeting type + grandma style** (20 combinations)
- Each GIF shows a grandma illustration, Hebrew greeting title, and a short blessing phrase
- GIFs are **not animated** (single frame)
- Do **not** store GIF binary data in the database
- Do **not** use external APIs or AI image generation
- GIFs can be regenerated with `scripts/generate_gifs.py`

| Grandma Style | Greeting Type | GIF File Example |
|---------------|---------------|------------------|
| סבתא פולניה | שבת שלום | `polish_shabbat.gif` |
| סבתא מרוקאית | מזל טוב | `moroccan_birthday.gif` |
| סבתא עיראקית | חג שמח | `iraqi_holiday.gif` |
| סבתא רוסיה | מתגעגעת אליכם | `russian_miss_you.gif` |
| (any style) | ברכות | `{style}_blessings.gif` |

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

- Every greeting is **saved to SQLite** on generation (write operation)
- Greeting history is **not displayed** in the Phase 1 UI (by design)
- Database read operations for history will be demonstrated in Phase 3 and at final presentation

---

## Development Phases

Development follows a strict phased approach. **Complete each phase fully before moving to the next.**

```mermaid
flowchart LR
    Phase1[Phase1_Local] --> Phase2[Phase2_Terraform]
    Phase2 --> Phase3[Phase3_RDS]
    Phase3 --> FinalDeploy[Final_Deployment]
```

---

### Phase 1 — Local Development

**Status:** Complete (June 2026)

**Repository:** https://github.com/Shaharmayster/Shahar_Daniel_AWSAPP

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
- Hebrew-first HTML + CSS frontend (Jinja templates, RTL, dark blue theme)
- SQLite database for persistence
- Greeting generation from predefined Python templates (Hebrew, 20 combinations)
- Static local GIF assets (grandma illustration + Hebrew text per style and greeting type)
- Form with three dropdowns and a Generate button
- `RUN.SH` script for local startup
- Local development and testing only

#### What Was Delivered in Phase 1

| Component | Status |
|-----------|--------|
| `backend/app.py` — Flask routes | Done |
| `backend/config.py` — Hebrew constants, `DATABASE_URL` | Done |
| `backend/database.py` — isolated SQLite layer | Done |
| `backend/greeting_generator.py` — 20 Hebrew templates | Done |
| `backend/gif_selector.py` — GIF mapping by style + type | Done |
| `frontend/templates/index.html` — Hebrew RTL UI | Done |
| `frontend/static/css/style.css` — dark blue theme | Done |
| `frontend/static/gifs/` — 21 static GIF files | Done |
| `scripts/generate_gifs.py` — GIF asset generator | Done |
| `terraform/` — placeholder directory | Done (Phase 1) |

#### What Phase 1 Does NOT Include

- AWS (any service)
- Terraform
- RDS
- Docker
- ELB, ASG, EC2, VPC
- Any cloud infrastructure

#### Phase 1 Success Criteria

- [x] Application runs locally without errors
- [x] User can select greeting type, recipient, and grandma style (Hebrew UI)
- [x] Generate button produces a humorous, personalized Hebrew greeting
- [x] Matching static GIF is displayed (grandma + Hebrew blessing text)
- [x] Every generated greeting is saved to SQLite
- [x] Data persists across application restarts
- [x] No forbidden technologies are used
- [x] Database layer isolated in `database.py` (Phase 2 ready)
- [x] `DATABASE_URL` configured via environment variable
- [x] Code pushed to GitHub repository

---

### Phase 2 — Terraform Infrastructure Preparation

**Status:** Complete (June 2026)

**Goal:** Create all Terraform code required for the final AWS infrastructure **without deploying anything**. No AWS credentials, no `terraform apply`, and no resources created during this phase.

#### What Phase 2 Includes

- Complete Terraform project under `terraform/`
- VPC, public subnets (2 AZs), Internet Gateway, route tables
- Security groups (ALB + EC2)
- Launch Template with placeholder `user_data`
- Auto Scaling Group (minimum 2 instances)
- Application Load Balancer, target group, HTTP listener
- `terraform.tfvars.example` and operational `terraform/README.md`

#### What Phase 2 Does NOT Include

- `terraform apply` or any AWS resource creation
- RDS (Phase 3)
- Application deployment on EC2
- Route53, CloudFront, ECS, EKS, Lambda, or other extra AWS services
- AWS credentials or CLI configuration

#### Infrastructure Architecture (Terraform Code)

```
Internet
    ↓
Application Load Balancer (HTTP :80)
    ↓
Target Group (:5000)
    ↓
EC2 Instance #1    EC2 Instance #2
    (ASG, AZ-a)        (ASG, AZ-b)
```

RDS is **not** provisioned by Terraform. Database connection is added in Phase 3.

#### Terraform File Structure

```
terraform/
├── provider.tf
├── variables.tf
├── outputs.tf
├── networking.tf
├── security.tf
├── alb.tf
├── launch_template.tf
├── asg.tf
├── terraform.tfvars.example
├── .gitignore
└── README.md
```

#### What Was Delivered in Phase 2

| Component | Status |
|-----------|--------|
| `provider.tf` — AWS provider, default tags | Done |
| `variables.tf` — region, CIDRs, instance type, app port | Done |
| `networking.tf` — VPC, subnets, IGW, routes | Done |
| `security.tf` — ALB and EC2 security groups | Done |
| `alb.tf` — ALB, target group, listener | Done |
| `launch_template.tf` — Amazon Linux 2023, placeholder user_data | Done |
| `asg.tf` — ASG with min/desired/max = 2 | Done |
| `outputs.tf` — ALB DNS, VPC ID, subnet IDs | Done |
| `terraform.tfvars.example` | Done |
| `terraform/README.md` — execution guide, costs, cleanup | Done |

#### Phase 2 Success Criteria

- [x] All Terraform `.tf` files exist under `terraform/`
- [x] Infrastructure covers VPC, subnets, IGW, routes, security groups, ALB, ASG, EC2 launch template
- [x] No RDS, Route53, CloudFront, or other forbidden services in Terraform code
- [x] Launch Template uses placeholder `user_data` only (no app deployment)
- [x] `terraform/README.md` documents scope, prerequisites, steps, costs, and cleanup
- [x] No `terraform apply` executed during Phase 2
- [x] No AWS credentials required during Phase 2 development

---

### Phase 3 — RDS Creation and Integration

**Status:** Postponed — planned a few days before the final presentation

**Goal:** Create an RDS MySQL instance manually in AWS, connect the Flask application, verify read/write operations, and retire SQLite for production usage.

**Reason for postponement:** Minimize AWS costs; avoid paying for RDS during development; keep the database active only when needed.

#### What Phase 3 Includes

1. Create an RDS MySQL instance manually in AWS (instructor-supplied or self-created per course instructions)
2. Obtain endpoint, username, password, and database name
3. Connect the Flask application via `DATABASE_URL` environment variable
4. Verify greeting write and read operations against RDS
5. Remove SQLite from production usage (local development may still use SQLite)

#### What Phase 3 Does NOT Include

- Terraform provisioning of RDS (RDS is created manually, not via this Terraform project)
- `terraform apply` (that happens at final deployment, before presentation)

#### Pre-existing Code (Ready for Phase 3)

The application database layer already supports both SQLite and MySQL:

| Component | Status |
|-----------|--------|
| `backend/database.py` — dual SQLite + MySQL support | Done |
| `PyMySQL` dependency in `requirements.txt` | Done |
| `.env.example` — `DATABASE_URL` template | Done |

#### Connection String

| Environment | Connection |
|-------------|------------|
| Local development (Phase 1) | `sqlite:///local.db` |
| Production (Phase 3+) | `mysql://user:password@rds-endpoint:3306/database_name` |

#### Switching to RDS

1. Copy `.env.example` to `.env`
2. Set `DATABASE_URL=mysql://user:password@rds-endpoint:3306/database_name`
3. Run `./RUN.SH` (local test) or deploy to EC2 with the same variable
4. Generate a greeting — data is written to RDS
5. Verify with: `SELECT * FROM greetings ORDER BY id DESC LIMIT 5;`

#### Phase 3 Success Criteria

- [ ] RDS MySQL instance created and accessible
- [ ] Application connects to RDS successfully
- [ ] Greeting generation works identically to Phase 1
- [ ] Greetings are written to RDS
- [ ] Greeting history reads from RDS
- [ ] SQLite is not used in production deployment

---

### Final Deployment and Presentation

**Status:** Pending — after Phases 2 and 3, at presentation week

**Goal:** Deploy infrastructure to AWS, run the application on EC2 behind the ALB/ASG, connect to RDS, and demonstrate high availability.

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
         (manual / instructor-supplied)
```

#### Final Deployment Steps

1. Run `terraform init`, `terraform plan`, `terraform apply` (from `terraform/`)
2. Deploy Flask application to EC2 instances (manual; not in Terraform user_data)
3. Set `DATABASE_URL` on each EC2 instance to point to RDS
4. Confirm ALB health checks pass and app is accessible via ALB DNS name
5. Demonstrate HA: terminate one EC2 instance; confirm app remains available

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

#### Final Deployment Success Criteria

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
| Local application works end-to-end | Phase 1 | Done |
| Terraform infrastructure code prepared | Phase 2 | Done |
| Application works with RDS | Phase 3 | Pending |
| Terraform deploys full AWS infrastructure | Final deployment | Pending |
| Application runs on AWS behind ELB and ASG | Final deployment | Pending |
| Database read/write demonstrated live | Final deployment | Pending |
| System survives EC2 instance termination | Final deployment | Pending |
| Final presentation requirements met | All | Pending |

**Ultimate goal:** Pass the course project with a fully working, highly available cloud deployment.

---

## Implementation Guidelines for Future Developers and AI Assistants

When implementing this project, follow these rules:

1. **Read this file first.** Do not assume requirements from prior conversations.
2. **Respect the current phase.** Do not run `terraform apply` during Phase 2 preparation. Do not create RDS until Phase 3.
3. **Do not add complexity.** The application is a vehicle for demonstrating infrastructure skills.
4. **Keep the database layer isolated.** All database access must go through `backend/database.py` (MySQL support already implemented).
5. **Use environment variables for configuration.** Database URLs, ports, and secrets must not be hardcoded.
6. **Do not use forbidden technologies** listed in this document.
7. **Do not add AWS services** beyond the mandatory list without explicit approval.
8. **Do not use AI or external APIs** for greeting generation.
9. **Store every greeting.** The history feature and the final demo both depend on persistent writes.
10. **Prioritize demonstrability.** Every feature should be easy to show in a 15-minute presentation.

---

## Presentation Checklist

Use this checklist when preparing for the final presentation:

- [x] Terraform code is ready (`terraform/` directory)
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
