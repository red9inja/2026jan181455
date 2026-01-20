# AWS Demo Application

A comprehensive full-stack application demonstrating modern AWS services integration with React frontend, Node.js backend, Python Lambda functions, and complete infrastructure automation.

## Architecture

```
Internet
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud                                │
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │   Amplify   │    │     ALB      │    │   API Gateway   │   │
│  │  (Frontend) │    │ (Load Balancer)   │   (Lambda API)  │   │
│  └─────────────┘    └──────────────┘    └─────────────────┘   │
│         │                   │                     │           │
│         ▼                   ▼                     ▼           │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │   Cognito   │    │     ECS      │    │     Lambda      │   │
│  │    (Auth)   │    │  (Backend)   │    │   (Functions)   │   │
│  └─────────────┘    └──────────────┘    └─────────────────┘   │
│         │                   │                     │           │
│         └───────────────────┼─────────────────────┘           │
│                             ▼                                 │
│                    ┌──────────────┐                          │
│                    │  DynamoDB    │                          │
│                    │ (Database)   │                          │
│                    └──────────────┘                          │
│                             │                                 │
│                             ▼                                 │
│                    ┌──────────────┐                          │
│                    │      S3      │                          │
│                    │  (Storage)   │                          │
│                    └──────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

## Features

### Frontend (React + Amplify)
- Authentication: Cognito-powered login/signup with MFA support
- File Upload: Direct S3 upload with progress tracking
- Real-time API: Integration with both ECS backend and Lambda functions
- Responsive Design: Mobile-first approach with modern UI
- Auto-deployment: GitHub Actions integration with Amplify

### Backend (Node.js + ECS)
- REST API: Express.js with comprehensive error handling
- Database Integration: DynamoDB operations with AWS SDK
- File Management: S3 operations for file storage
- Health Monitoring: Built-in health checks and metrics
- Container Orchestration: ECS Fargate with auto-scaling

### Lambda Functions (Python)
- Serverless Processing: Event-driven data processing
- Email Notifications: SES integration for user communications
- API Gateway: RESTful endpoints with IAM authentication
- Error Handling: Comprehensive logging and error management

### Infrastructure (Terraform)
- Infrastructure as Code: Complete AWS infrastructure automation
- Multi-Environment: Staging (Spot) and Production (On-Demand)
- Security: VPC, Security Groups, IAM roles with least privilege
- Monitoring: CloudWatch integration with custom metrics

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18, Amplify UI | User interface and authentication |
| **Backend** | Node.js, Express.js | REST API and business logic |
| **Serverless** | Python 3.9, Lambda | Event processing and notifications |
| **Database** | DynamoDB | NoSQL data storage |
| **Storage** | S3 | File storage and static assets |
| **Authentication** | Cognito | User management and authorization |
| **Infrastructure** | Terraform | Infrastructure as Code |
| **CI/CD** | GitHub Actions | Automated deployment pipeline |
| **Monitoring** | CloudWatch, X-Ray | Observability and tracing |

## 🏃‍♂️ Quick Start

### Prerequisites
- Node.js 18+
- Docker
- AWS CLI configured
- Terraform 1.6+

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd 2026jan181455
   ```

2. **Install dependencies**:
   ```bash
   # Frontend
   npm install
   
   # Backend
   cd backend
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env file in backend/
   cp backend/.env.example backend/.env
   # Update with your AWS configuration
   ```

4. **Run locally**:
   ```bash
   # Frontend (port 3000)
   npm start
   
   # Backend (port 3001)
   cd backend
   npm run dev
   ```

### Production Deployment

1. **Deploy Infrastructure**:
   ```bash
   cd ../2026jan201246
   terraform init
   terraform apply -var-file="terraform.production.tfvars"
   ```

2. **Push Code**:
   ```bash
   git push origin main
   # GitHub Actions will automatically build and deploy
   ```

## 📁 Project Structure

```
/root/2026jan181455/                 # Application Repository
├── src/                             # React frontend source
│   ├── App.js                       # Main React component
│   ├── App.css                      # Styling
│   └── index.js                     # Entry point
├── backend/                         # Node.js backend
│   ├── server.js                    # Express server
│   └── package.json                 # Backend dependencies
├── lambda/                          # Python Lambda functions
│   ├── user_handler.py              # User operations
│   └── requirements.txt             # Python dependencies
├── public/                          # Static assets
├── .github/workflows/               # CI/CD pipelines
│   └── docker-build.yml             # Docker build and deploy
├── Dockerfile                       # Multi-stage container build
├── nginx.conf                       # Nginx configuration
└── package.json                     # Frontend dependencies

/root/2026jan201246/                 # Infrastructure Repository
├── main.tf                          # Main Terraform configuration
├── networking.tf                    # VPC and networking
├── security-groups.tf               # Security group definitions
├── ecs.tf                          # ECS cluster and services
├── lambda.tf                       # Lambda functions
├── cognito.tf                      # Authentication setup
├── storage.tf                      # S3 and DynamoDB
├── amplify.tf                      # Frontend hosting
├── iam.tf                          # IAM roles and policies
├── outputs.tf                      # Terraform outputs
├── terraform.staging.tfvars        # Staging variables
├── terraform.production.tfvars     # Production variables
└── .github/workflows/              # Infrastructure CI/CD
    └── deploy-infrastructure.yml    # Terraform deployment
```

## 🔐 Security Features

### Network Security
- **VPC Isolation**: Private subnets for compute resources
- **Security Groups**: Layered security with minimal required access
- **NAT Gateways**: Secure internet access for private resources

### Application Security
- **Authentication**: Cognito User Pools with configurable password policies
- **Authorization**: Identity Pools for AWS resource access
- **API Security**: IAM-based API Gateway authentication
- **Data Encryption**: S3 and DynamoDB encryption at rest

### Infrastructure Security
- **Least Privilege**: IAM roles with minimal required permissions
- **Secrets Management**: Environment variables for sensitive data
- **Security Scanning**: Automated vulnerability scanning in CI/CD
- **Compliance**: AWS Config rules for compliance monitoring

## 📊 Monitoring & Observability

### Application Monitoring
- **Health Checks**: ECS task and ALB target group health monitoring
- **Custom Metrics**: Application-specific CloudWatch metrics
- **Distributed Tracing**: X-Ray integration for request tracing
- **Log Aggregation**: Centralized logging with CloudWatch Logs

### Infrastructure Monitoring
- **Resource Utilization**: CPU, memory, and network metrics
- **Cost Monitoring**: AWS Cost Explorer integration
- **Alerting**: CloudWatch alarms for critical thresholds
- **Performance**: Application Load Balancer metrics

## 🌍 Environment Management

### Staging Environment
- **Purpose**: Development and testing
- **Compute**: ECS Fargate Spot (cost-optimized)
- **Scaling**: Single instance, manual scaling
- **Features**: Reduced logging, minimal backups

### Production Environment
- **Purpose**: Live application serving users
- **Compute**: ECS Fargate On-Demand (reliability-focused)
- **Scaling**: Multi-instance with auto-scaling
- **Features**: Enhanced monitoring, automated backups, advanced security

## 🔄 CI/CD Pipeline

### Application Pipeline (`2026jan181455`)
```
Code Push → GitHub Actions → Docker Build → Security Scan → Deploy to ECS
```

### Infrastructure Pipeline (`2026jan201246`)
```
Terraform Changes → Plan → Security Scan → Apply → Resource Updates
```

### Branch Strategy
- **`develop`** → Staging environment deployment
- **`main`** → Production environment deployment
- **Feature branches** → Automatic preview environments

## 📈 Scaling Considerations

### Horizontal Scaling
- **ECS Services**: Auto-scaling based on CPU/memory utilization
- **Lambda Functions**: Automatic scaling with concurrent execution limits
- **DynamoDB**: On-demand billing with automatic scaling

### Vertical Scaling
- **ECS Tasks**: Configurable CPU and memory allocation
- **Lambda Memory**: Adjustable memory allocation (128MB - 10GB)
- **Database**: DynamoDB capacity modes (On-Demand vs Provisioned)

## 💰 Cost Optimization

### Development/Staging
- Fargate Spot instances (up to 70% savings)
- Reduced log retention periods
- Minimal backup and versioning
- Single-instance deployments

### Production
- Reserved capacity for predictable workloads
- Lifecycle policies for S3 storage classes
- DynamoDB on-demand for variable workloads
- CloudWatch cost monitoring and alerts

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Check Cognito User Pool configuration
   - Verify callback URLs in Amplify configuration
   - Ensure IAM roles have correct permissions

2. **API Connection Issues**
   - Verify security group rules
   - Check ALB target group health
   - Review CloudWatch logs for errors

3. **File Upload Problems**
   - Confirm S3 bucket policies
   - Check CORS configuration
   - Verify Cognito Identity Pool permissions

### Debugging Commands

```bash
# Check ECS service status
aws ecs describe-services --cluster demo-staging-cluster --services demo-staging-service

# View application logs
aws logs tail /ecs/demo-staging --follow

# Check Lambda function logs
aws logs tail /aws/lambda/demo-staging-user-handler --follow

# Monitor Amplify build
aws amplify list-jobs --app-id <app-id> --branch-name main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AWS for providing comprehensive cloud services
- React team for the excellent frontend framework
- Terraform for infrastructure as code capabilities
- GitHub Actions for seamless CI/CD integration

---

**Built with ❤️ for learning AWS services integration and modern application architecture patterns.**
