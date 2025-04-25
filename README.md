# Shreegaud Connect

A community engagement platform for the Shreegaud community, built with AWS services and modern DevOps practices.

## Project Structure

```
shreegoud-app/
├── frontend/                 # Flutter mobile application
├── admin-panel/             # React-based admin dashboard
├── backend/                 # Serverless backend services
│   ├── api/                # API Gateway + Lambda functions
│   ├── database/           # RDS and DynamoDB schemas
│   └── auth/               # Cognito configurations
├── infrastructure/          # Terraform configurations
│   ├── modules/            # Reusable Terraform modules
│   ├── environments/       # Environment-specific configs
│   └── main.tf             # Main Terraform configuration
├── kubernetes/             # Kubernetes manifests
│   ├── charts/            # Helm charts
│   └── base/              # Kustomize base configurations
└── ci-cd/                  # CI/CD pipeline configurations
    ├── gitlab-ci/         # GitLab CI configurations
    └── argocd/            # ArgoCD application manifests
```

## Technology Stack

### Frontend
- Flutter (Mobile App)
- React (Admin Panel)

### Backend
- AWS Lambda
- API Gateway
- Amazon Cognito
- Amazon RDS (PostgreSQL)
- Amazon DynamoDB
- Amazon S3
- Amazon SNS
- Amazon CloudFront

### DevOps
- GitLab
- Docker
- Kubernetes (EKS)
- ArgoCD
- Terraform
- AWS CodePipeline/CodeBuild

## Getting Started

1. Clone the repository
2. Set up AWS credentials
3. Install required tools:
   - Terraform
   - AWS CLI
   - kubectl
   - Helm
   - Docker
   - Flutter
   - Node.js

## Development Workflow

1. Infrastructure Setup:
   ```bash
   cd infrastructure
   terraform init
   terraform plan
   terraform apply
   ```

2. Backend Development:
   ```bash
   cd backend
   npm install
   npm run dev
   ```

3. Frontend Development:
   ```bash
   cd frontend
   flutter pub get
   flutter run
   ```

4. Admin Panel Development:
   ```bash
   cd admin-panel
   npm install
   npm start
   ```

## Deployment

The project uses GitOps principles with ArgoCD for deployment. Changes pushed to the main branch will trigger the CI/CD pipeline.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details 