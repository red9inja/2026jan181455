# AWS Demo Application

A comprehensive full-stack application demonstrating modern AWS services integration with React frontend, Node.js backend, Python Lambda functions, and complete infrastructure automation.

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

## Complete Deployment Flow

### 1. Code Push to Docker Image Build

```
Developer Push Code → GitHub Actions → Docker Build → Container Registry
```

**Process:**
```bash
# When you push code
git push origin master

# GitHub Actions automatically:
1. Checkout code
2. Build Docker image with multi-stage build:
   - Stage 1: React build (npm run build)
   - Stage 2: Node.js backend setup
   - Stage 3: Nginx + Node.js combined image
3. Push to GitHub Container Registry: ghcr.io/red9inja/2026jan181455:master
```

### 2. Docker Image Deployment Location

**Container Registry:**
```
ghcr.io/red9inja/2026jan181455:master
```

**Deployment Target:**
- ECS Fargate Cluster deployment
- Application Load Balancer accessibility

### 3. Application Architecture with Cloudflare Integration

```
Internet (vmind.online)
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Cloudflare                                   │
│  ┌─────────────────┐    ┌─────────────────┐                   │
│  │   Cloudflare    │    │   Cloudflare    │                   │
│  │     Proxy       │    │      DNS        │                   │
│  │  (Full Strict)  │    │   Management    │                   │
│  └─────────────────┘    └─────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
    │                               │
    ▼                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AWS Cloud                                   │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐                   │
│  │   CloudFront    │    │   Route 53      │                   │
│  │     (CDN)       │    │     (DNS)       │                   │
│  └─────────────────┘    └─────────────────┘                   │
│           │                       │                           │
│           ▼                       ▼                           │
│  ┌─────────────────┐    ┌─────────────────┐                   │
│  │   Amplify       │    │      ALB        │                   │
│  │  (Frontend)     │    │ (Load Balancer) │                   │
│  │ vmind.online    │    │api.vmind.online │                   │
│  └─────────────────┘    └─────────────────┘                   │
│           │                       │                           │
│           ▼                       ▼                           │
│  ┌─────────────────┐    ┌─────────────────┐                   │
│  │   Cognito       │    │   ECS Fargate   │                   │
│  │ (Authentication)│    │   (Backend)     │                   │
│  └─────────────────┘    └─────────────────┘                   │
│           │                       │                           │
│           └───────────────────────┼───────────────────────────┘
│                                   ▼                           │
│                          ┌─────────────────┐                   │
│                          │   DynamoDB      │                   │
│                          │   (Database)    │                   │
│                          └─────────────────┘                   │
│                                   │                           │
│                                   ▼                           │
│                          ┌─────────────────┐                   │
│                          │       S3        │                   │
│                          │   (Storage)     │                   │
│                          └─────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Terraform Resources

**Infrastructure Components:**
```bash
# Networking
- VPC (10.0.0.0/16)
- Public Subnets (2 AZs)
- Private Subnets (2 AZs)
- Internet Gateway
- NAT Gateways
- Route Tables

# Compute
- ECS Cluster
- ECS Service (Fargate)
- Application Load Balancer
- Target Groups

# Security
- Security Groups (ALB, ECS, Lambda)
- IAM Roles (ECS, Lambda, Cognito)
- IAM Policies

# Storage & Database
- S3 Buckets (with encryption)
- DynamoDB Tables
- CloudWatch Log Groups

# Authentication
- Cognito User Pool
- Cognito Identity Pool
- Cognito User Pool Client

# Frontend Hosting
- Amplify App
- Amplify Branches (prod/stage)

# Serverless
- Lambda Functions
- API Gateway
```

### 5. Domain Configuration with Cloudflare (vmind.online)

**DNS Setup with Cloudflare Integration:**
```bash
# Cloudflare DNS Records (Proxied - Orange Cloud)
vmind.online          → CNAME → Amplify Distribution (Proxied)
api.vmind.online      → CNAME → ALB DNS Name (Proxied)
lambda.vmind.online   → CNAME → API Gateway Domain (Proxied)

# SSL/TLS Configuration
- Cloudflare: Full (Strict) SSL Mode
- AWS: ACM Certificates for backend services
- End-to-end encryption maintained
```

**Terraform Domain Configuration:**
```hcl
# Update terraform.production.tfvars
domain_name = "vmind.online"

# This will create:
- Amplify custom domain: vmind.online
- ALB custom domain: api.vmind.online
- API Gateway custom domain: lambda.vmind.online
```

### 6. Component Interactions

**Frontend (Amplify) ↔ Backend (ECS):**
```javascript
// React App calls
const response = await API.get('api', '/users');
// Goes to: https://api.vmind.online/users
```

**Frontend ↔ Cognito:**
```javascript
// User login
const user = await Auth.signIn('user@email.com', 'password');
// Cognito returns JWT token
```

**Frontend ↔ S3:**
```javascript
// File upload (direct to S3)
const result = await Storage.put('file.jpg', file);
// Uses Cognito Identity Pool credentials
```

**Backend ↔ DynamoDB:**
```javascript
// ECS backend saves data
await dynamodb.put({
  TableName: 'demo-users',
  Item: userData
}).promise();
```

### 7. Live Site Access Flow with Cloudflare

**Complete User Journey:**
```
1. User visits: https://vmind.online
   ↓
2. Cloudflare Proxy intercepts request (Full Strict SSL)
   ↓
3. Cloudflare forwards to AWS Amplify
   ↓
4. Amplify serves React app with SSL certificate
   ↓
5. User clicks "Login"
   ↓
6. Cognito authentication popup (AWS managed)
   ↓
7. User authenticated, gets JWT token
   ↓
8. React app calls API: https://api.vmind.online/users
   ↓
9. Cloudflare Proxy forwards API request to AWS ALB
   ↓
10. ALB forwards to ECS container with SSL termination
    ↓
11. Node.js backend processes request
    ↓
12. Backend queries DynamoDB
    ↓
13. Response sent back through ALB → Cloudflare → User
    ↓
14. User sees data on vmind.online
```

**Cloudflare Security Features:**
- DDoS Protection
- Web Application Firewall (WAF)
- Bot Management
- Rate Limiting
- SSL/TLS Encryption (Full Strict Mode)

### 8. Complete Deployment Process

**Step 1: Infrastructure Deployment**
```bash
# Push to prod branch
git checkout -b prod
git push origin prod

# Terraform creates:
- VPC and networking
- ECS cluster
- Load balancer
- Cognito setup
- S3 buckets
- DynamoDB tables
- Amplify app
```

**Step 2: Application Deployment**
```bash
# Same prod branch push triggers:
- Docker image build
- Push to container registry
- ECS service update with new image
- Amplify build and deploy
```

**Step 3: Domain Configuration**
```bash
# Cloudflare DNS Configuration (Manual - One-time)
1. Keep vmind.online nameservers with Cloudflare
2. Add CNAME records pointing to AWS resources
3. Enable Cloudflare Proxy (Orange Cloud)
4. Set SSL/TLS to Full (Strict)
5. Configure security rules and caching
```

### 9. What Gets Deployed

**Frontend (vmind.online):**
- React application
- Cognito authentication UI
- File upload interface
- API integration

**Backend (api.vmind.online):**
- Node.js Express server
- REST API endpoints
- Database operations
- File management

**Lambda (lambda.vmind.online):**
- User management functions
- Data processing
- Email notifications

**Infrastructure:**
- Auto-scaling ECS service
- Load balancer with health checks
- Secure VPC with private subnets
- Encrypted storage and database

### 10. Live Site Features

**User Experience:**
```
https://vmind.online
├── Login/Signup (Cognito)
├── Dashboard (React)
├── File Upload (S3)
├── User Management (API)
└── Real-time Updates (WebSocket optional)
```

**Admin Features:**
```
https://vmind.online/admin
├── User Analytics
├── System Health
├── Resource Monitoring
└── Cost Tracking
```

### 11. Cloudflare Integration Benefits

**Performance:**
- Global CDN caching
- Optimized content delivery
- Reduced latency worldwide

**Security:**
- DDoS protection
- SSL/TLS encryption
- Web Application Firewall
- Bot protection

**Reliability:**
- 100% uptime SLA
- Automatic failover
- Load balancing
- Health monitoring

**Cost Optimization:**
- Reduced AWS data transfer costs
- Cached static content
- Optimized bandwidth usage

This complete flow ensures your vmind.online domain works seamlessly with Cloudflare proxy enabled while maintaining full SSL encryption and optimal performance through the entire AWS infrastructure stack.

## Technology Stack

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

## Quick Start

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

## Project Structure

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

## Security Features

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

## Monitoring & Observability

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

## Environment Management

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

## CI/CD Pipeline

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

## Scaling Considerations

### Horizontal Scaling
- **ECS Services**: Auto-scaling based on CPU/memory utilization
- **Lambda Functions**: Automatic scaling with concurrent execution limits
- **DynamoDB**: On-demand billing with automatic scaling

### Vertical Scaling
- **ECS Tasks**: Configurable CPU and memory allocation
- **Lambda Memory**: Adjustable memory allocation (128MB - 10GB)
- **Database**: DynamoDB capacity modes (On-Demand vs Provisioned)

## Cost Optimization

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

## Troubleshooting

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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- AWS for providing comprehensive cloud services
- React team for the excellent frontend framework
- Terraform for infrastructure as code capabilities
- GitHub Actions for seamless CI/CD integration

---

**Built for learning AWS services integration and modern application architecture patterns.**
# Trigger build
