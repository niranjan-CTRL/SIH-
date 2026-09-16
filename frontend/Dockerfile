# Stage 1: Build the React application
FROM node:20-alpine as build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy application source and environment variables
COPY . .

# Set VITE_API_URL empty so axios uses relative paths, relying on the Nginx proxy
ENV VITE_API_URL=""

# Build the application
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:alpine

# Copy the build output from the first stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
