# Terraform — Grandma Greeting Generator Infrastructure

This directory contains Infrastructure as Code (Terraform) for hosting the Flask application on AWS with high availability.

**Phase 2 scope:** This is infrastructure **preparation only**. The Terraform code is ready for future execution. No AWS resources are created until someone runs `terraform apply` with valid AWS credentials.

---

## What This Terraform Project Creates

When `terraform apply` is executed (at final deployment, before the presentation), the following AWS resources are provisioned:

| Resource | Purpose |
|----------|---------|
| **VPC** | Isolated network (`10.0.0.0/16` by default) |
| **Public Subnets** | Two subnets across two Availability Zones |
| **Internet Gateway** | Internet access for public subnets |
| **Route Tables** | Public routing (`0.0.0.0/0` → IGW) |
| **Security Groups** | ALB (HTTP 80 from internet), EC2 (app port from ALB only) |
| **Launch Template** | Amazon Linux 2023 EC2 configuration |
| **Auto Scaling Group** | Minimum 2 EC2 instances for high availability |
| **Application Load Balancer** | Public HTTP entry point |
| **Target Group** | Routes ALB traffic to EC2 instances on port 5000 |
| **Listener** | HTTP port 80 → target group |

### Architecture

```
Internet
    │
    ▼
Application Load Balancer (HTTP :80)
    │
    ▼
Target Group (:5000)
    │
    ├── EC2 Instance #1 (ASG, AZ-a)
    └── EC2 Instance #2 (ASG, AZ-b)
```

Default region: **us-east-1** (configurable via `terraform.tfvars`).

---

## What This Terraform Project Does NOT Create

The following are **intentionally excluded** from this Terraform code:

| Not Included | Reason |
|--------------|--------|
| **RDS** | Created manually in Phase 3 (instructor-supplied); minimizes cost during development |
| **Application deployment** | Flask app is deployed manually on EC2 at final presentation week |
| **Database schema** | Managed by the application (`init_db()` in `backend/database.py`) |
| **Route53** | Not required for course demo; access via ALB DNS name |
| **CloudFront** | Not required |
| **ECS / EKS / Lambda** | Course requires EC2 + ASG |
| **SQS / SNS / DynamoDB** | Not part of course requirements |
| **NAT Gateway** | Omitted to keep costs and complexity low; EC2 instances use public subnets |

The Launch Template includes **placeholder user_data only** — no `git clone`, no dependency installation, no application startup script.

---

## File Structure

```
terraform/
├── provider.tf              # Terraform and AWS provider configuration
├── variables.tf               # Input variables
├── outputs.tf                 # Output values (ALB DNS, VPC ID, etc.)
├── networking.tf              # VPC, subnets, IGW, route tables
├── security.tf                # Security groups
├── alb.tf                     # ALB, target group, listener
├── launch_template.tf         # EC2 launch template
├── asg.tf                     # Auto Scaling Group
├── terraform.tfvars.example   # Example variable values
├── .gitignore                 # Ignores state files and secrets
└── README.md                  # This file
```

---

## AWS Requirements Before Running

Before executing Terraform against AWS, prepare the following:

### 1. AWS Account

- An active AWS account with billing enabled
- Sufficient permissions to create VPC, EC2, ELB, and IAM-related resources

### 2. IAM User

Create an IAM user (or use an existing one) with programmatic access. Minimum permissions should include:

- `ec2:*` (or scoped EC2, VPC, ELB permissions)
- `elasticloadbalancing:*`
- `autoscaling:*`

For a course project, `AdministratorAccess` on a dedicated IAM user is acceptable if your instructor allows it.

### 3. Access Key and Secret Key

- In the AWS Console: **IAM → Users → Security credentials → Create access key**
- Store the Access Key ID and Secret Access Key securely
- **Never commit credentials to Git**

### 4. AWS CLI

Install and configure the AWS CLI:

```bash
# macOS (Homebrew)
brew install awscli

# Configure credentials
aws configure
```

You will be prompted for:

- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g. `us-east-1`)
- Default output format (`json`)

Terraform uses the same credential chain as the AWS CLI (`~/.aws/credentials` or environment variables).

### 5. Terraform Installation

Install Terraform >= 1.5:

```bash
# macOS (Homebrew)
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Verify
terraform version
```

---

## Terraform Execution Steps

All commands below are run from the `terraform/` directory.

### 1. Configure Variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars if you need to change region, project name, or CIDR blocks
```

### 2. Initialize

Downloads the AWS provider and prepares the working directory:

```bash
terraform init
```

### 3. Validate

Checks syntax and internal consistency (does not contact AWS for resource creation):

```bash
terraform validate
```

### 4. Plan

Shows what Terraform **would** create, change, or destroy. Requires AWS credentials:

```bash
terraform plan
```

Review the output carefully before applying.

### 5. Apply

Creates AWS resources. Requires confirmation:

```bash
terraform apply
```

After a successful apply, note the outputs:

```bash
terraform output alb_dns_name
```

Open `http://<alb_dns_name>` in a browser once the Flask application is deployed on the EC2 instances.

### 6. Destroy

Removes all resources created by this Terraform project:

```bash
terraform destroy
```

Confirm when prompted. Verify in the AWS Console that VPC, EC2, and ALB resources are gone.

---

## Expected AWS Costs

**Warning:** Costs begin accruing as soon as `terraform apply` succeeds. Destroy resources when not actively testing.

Approximate monthly cost while infrastructure is running (us-east-1, as of 2026):

| Resource | Approximate Cost |
|----------|------------------|
| 2× `t3.micro` EC2 (on-demand) | ~$15/month |
| Application Load Balancer | ~$16/month + LCU charges |
| Data transfer | Variable (usually low for demos) |
| **Estimated total** | **~$30–35/month** while running |

Cost-saving tips:

- Run `terraform destroy` immediately after testing
- Do not leave infrastructure running between development sessions
- Phase 2 (this task) creates **no costs** — code only, no `apply`

RDS costs are separate and handled in Phase 3.

---

## Cleanup Instructions

To avoid ongoing charges after testing or the final presentation:

1. Run from the `terraform/` directory:

   ```bash
   terraform destroy
   ```

2. Type `yes` when prompted.

3. Verify in the AWS Console:

   - **EC2 → Instances** — no instances from this project
   - **EC2 → Load Balancers** — ALB removed
   - **VPC → Your VPCs** — project VPC removed

4. If `terraform destroy` fails (e.g. dependency issues), identify remaining resources in the Console and delete manually, then run `terraform destroy` again.

---

## Application Deployment (Final Presentation Week)

This Terraform code prepares infrastructure only. Before the final demo:

1. Run `terraform apply` to create AWS resources
2. SSH or use Session Manager to access EC2 instances
3. Deploy the Flask application (clone repo, install dependencies, set `DATABASE_URL` for RDS)
4. Start the app on port **5000** (must match `app_port` variable and target group)
5. Confirm ALB health checks pass (targets show **healthy**)
6. Access the app via the ALB DNS name

Phase 3 covers RDS connection. The application code in `backend/database.py` already supports MySQL via `DATABASE_URL`.

---

## Phase Notes

| Phase | Description |
|-------|-------------|
| **Phase 1** | Local Flask + SQLite — complete |
| **Phase 2** | Terraform code preparation — this directory |
| **Phase 3** | Manual RDS creation and Flask integration — a few days before presentation |
| **Final deployment** | `terraform apply` + app on EC2 + HA demo — presentation week |

During Phase 2 development, **no AWS credentials are required** and **no Terraform commands need to be run**.

---

## Troubleshooting

| Issue | Possible Fix |
|-------|----------------|
| `terraform init` fails | Check internet access; verify Terraform >= 1.5 |
| `terraform plan` — credentials error | Run `aws configure` or set `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` |
| ALB targets unhealthy | Flask app not running on port 5000, or security group mismatch |
| `terraform destroy` leaves resources | Delete orphaned resources in Console; check for dependencies outside Terraform |

For project requirements and phase definitions, see [`../PROJECT.md`](../PROJECT.md).
