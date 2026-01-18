# Use lightweight nginx alpine image (only ~5MB)
FROM nginx:alpine

# Copy HTML file to nginx default directory
COPY index.html /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start nginx (default command in nginx:alpine)
CMD ["nginx", "-g", "daemon off;"]
