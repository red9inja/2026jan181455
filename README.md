# 🚀 Docker + GitHub Actions Hello World

Simple HTML page deployed using lightweight Docker container with automated CI/CD pipeline.

## 📁 Project Structure
```
.
├── index.html                 # Simple HTML page
├── Dockerfile                 # Lightweight Docker configuration
├── .dockerignore             # Docker ignore rules
├── .github/
│   └── workflows/
│       └── docker-build.yml  # GitHub Actions workflow
└── README.md                 # This file
```

## 🐳 Docker Setup

### Dockerfile Features:
- **Base Image**: `nginx:alpine` (~5MB only)
- **Multi-platform**: Supports AMD64 and ARM64
- **Optimized**: Minimal layers for faster builds

### Local Testing:
```bash
# Build image locally
docker build -t hello-world-app .

# Run container
docker run -p 8080:80 hello-world-app

# Access at http://localhost:8080
```

## 🔧 GitHub Actions Setup

### Required Secrets:
Go to GitHub Repository → Settings → Secrets and Variables → Actions

Add these secrets:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token

### Workflow Features:
- **Triggers**: Push to main/master branch, Pull requests
- **Multi-platform builds**: AMD64 and ARM64
- **Caching**: GitHub Actions cache for faster builds
- **Tagging**: Automatic versioning with branch names and SHA

## 📋 Step-by-Step Setup Guide

### Step 1: Docker Hub Account Setup
1. Create account at [hub.docker.com](https://hub.docker.com)
2. Go to Account Settings → Security
3. Create Access Token (not password!)
4. Copy username and token

### Step 2: GitHub Repository Setup
1. Push this code to your GitHub repository
2. Go to Repository Settings → Secrets and Variables → Actions
3. Add secrets:
   - Name: `DOCKER_USERNAME`, Value: your-docker-username
   - Name: `DOCKER_PASSWORD`, Value: your-access-token

### Step 3: Trigger Build
1. Push code to main/master branch
2. Check Actions tab in GitHub
3. Monitor build progress
4. Image will be pushed to Docker Hub automatically

### Step 4: Verify Deployment
1. Check your Docker Hub repository
2. Pull and run image:
```bash
docker pull your-username/hello-world-app:latest
docker run -p 8080:80 your-username/hello-world-app:latest
```

## 🏷️ Image Tagging Strategy

The workflow creates multiple tags:
- `latest` - Latest version from main branch
- `main-<sha>` - Branch name with commit SHA
- `<branch-name>` - Branch name for feature branches

## 🔒 Security Best Practices

1. **Never use Docker password** - Use access tokens only
2. **Secrets management** - Store credentials in GitHub Secrets
3. **Multi-platform builds** - Support different architectures
4. **Cache optimization** - Faster builds with GitHub Actions cache

## 📊 Build Optimization

- **Image size**: ~15MB (nginx:alpine + HTML)
- **Build time**: ~2-3 minutes with cache
- **Platforms**: linux/amd64, linux/arm64
- **Caching**: GitHub Actions cache enabled

## 🚀 Usage Examples

### Production Deployment:
```bash
docker run -d -p 80:80 --name hello-app your-username/hello-world-app:latest
```

### Development with Volume Mount:
```bash
docker run -p 8080:80 -v $(pwd)/index.html:/usr/share/nginx/html/index.html your-username/hello-world-app:latest
```

## 🔍 Troubleshooting

### Common Issues:

1. **Build fails with authentication error**
   - Check Docker Hub credentials in GitHub Secrets
   - Ensure using access token, not password

2. **Image not found on Docker Hub**
   - Check workflow logs in GitHub Actions
   - Verify repository name matches secrets

3. **Local build fails**
   - Ensure Docker is running
   - Check Dockerfile syntax

### Debug Commands:
```bash
# Check running containers
docker ps

# View container logs
docker logs <container-id>

# Inspect image
docker inspect your-username/hello-world-app:latest
```

## 📈 Next Steps

- Add health checks to Dockerfile
- Implement staging environment
- Add automated testing
- Set up monitoring and logging
- Configure custom domain

---
**Built with ❤️ using Docker + GitHub Actions**
