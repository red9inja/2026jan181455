# Multi-stage build for React frontend and Node.js backend

# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY package*.json ./
RUN npm ci
COPY src/ ./src/
COPY public/ ./public/
RUN npm run build

# Stage 2: Build Node.js backend
FROM node:18-alpine AS backend-build
WORKDIR /app/backend
COPY backend/package*.json ./
RUN npm ci
COPY backend/ ./

# Stage 3: Production image
FROM node:18-alpine AS production
WORKDIR /app

# Install nginx for serving frontend
RUN apk add --no-cache nginx curl

# Copy backend
COPY --from=backend-build /app/backend ./backend
WORKDIR /app/backend

# Copy frontend build to nginx directory
COPY --from=frontend-build /app/frontend/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create startup script
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'nginx &' >> /app/start.sh && \
    echo 'cd /app/backend && npm start' >> /app/start.sh && \
    chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3001/health || exit 1

EXPOSE 80 3001

CMD ["/app/start.sh"]
