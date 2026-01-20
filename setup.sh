#!/bin/bash

# AWS Demo Application Setup Script
# This script helps set up the complete AWS demo application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command_exists "node"; then
        missing_tools+=("Node.js")
    fi
    
    if ! command_exists "npm"; then
        missing_tools+=("npm")
    fi
    
    if ! command_exists "docker"; then
        missing_tools+=("Docker")
    fi
    
    if ! command_exists "aws"; then
        missing_tools+=("AWS CLI")
    fi
    
    if ! command_exists "terraform"; then
        missing_tools+=("Terraform")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_status "Please install the missing tools and run this script again."
        exit 1
    fi
    
    print_success "All prerequisites are installed!"
}

# Function to setup application
setup_application() {
    print_status "Setting up application..."
    
    # Install frontend dependencies
    print_status "Installing frontend dependencies..."
    npm install
    
    # Install backend dependencies
    print_status "Installing backend dependencies..."
    cd backend
    npm install
    cd ..
    
    # Create environment files
    print_status "Creating environment files..."
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_warning "Created .env file. Please update it with your AWS configuration."
    fi
    
    if [ ! -f "backend/.env" ]; then
        cp backend/.env.example backend/.env
        print_warning "Created backend/.env file. Please update it with your AWS configuration."
    fi
    
    print_success "Application setup completed!"
}

# Function to setup infrastructure
setup_infrastructure() {
    print_status "Setting up infrastructure..."
    
    cd ../2026jan201246
    
    # Initialize Terraform
    print_status "Initializing Terraform..."
    terraform init
    
    # Validate Terraform configuration
    print_status "Validating Terraform configuration..."
    terraform validate
    
    print_success "Infrastructure setup completed!"
    print_warning "Remember to configure your AWS credentials and update terraform.tfvars files."
    
    cd ../2026jan181455
}

# Function to build and test locally
build_and_test() {
    print_status "Building and testing application..."
    
    # Build Docker image
    print_status "Building Docker image..."
    docker build -t aws-demo-app .
    
    print_success "Docker image built successfully!"
    
    # Test frontend build
    print_status "Testing frontend build..."
    npm run build
    
    print_success "Frontend build completed successfully!"
}

# Function to display next steps
display_next_steps() {
    print_success "Setup completed successfully!"
    echo
    print_status "Next steps:"
    echo "1. Configure AWS credentials: aws configure"
    echo "2. Update environment files with your AWS resources:"
    echo "   - .env (frontend configuration)"
    echo "   - backend/.env (backend configuration)"
    echo "3. Update Terraform variables:"
    echo "   - ../2026jan201246/terraform.staging.tfvars"
    echo "   - ../2026jan201246/terraform.production.tfvars"
    echo "4. Deploy infrastructure:"
    echo "   cd ../2026jan201246"
    echo "   terraform plan -var-file=\"terraform.staging.tfvars\""
    echo "   terraform apply -var-file=\"terraform.staging.tfvars\""
    echo "5. Push code to GitHub to trigger CI/CD pipeline"
    echo
    print_status "For local development:"
    echo "Frontend: npm start (runs on http://localhost:3000)"
    echo "Backend: cd backend && npm run dev (runs on http://localhost:3001)"
    echo
    print_status "For Docker testing:"
    echo "docker run -p 8080:80 aws-demo-app"
    echo "Access at http://localhost:8080"
}

# Main execution
main() {
    echo "=========================================="
    echo "   AWS Demo Application Setup Script"
    echo "=========================================="
    echo
    
    check_prerequisites
    setup_application
    setup_infrastructure
    build_and_test
    display_next_steps
}

# Run main function
main "$@"
