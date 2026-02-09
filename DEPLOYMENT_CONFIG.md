# Deployment Configuration for Todo Application

## Production Environment

### Backend Configuration
```env
# Database
DATABASE_URL="postgresql://username:password@prod-db.cluster.region.rds.amazonaws.com/todo_prod?sslmode=require"

# Security
SECRET_KEY="super-long-and-secure-secret-key-changed-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
OPENAI_API_KEY="sk-production-key"
MCP_SERVER_URL="https://mcp.todoapp.com"

# Performance
WORKERS=4
TIMEOUT=300
MAX_WORKERS=8
```

### Frontend Configuration
```env
NEXT_PUBLIC_API_BASE_URL=https://api.todoapp.com
NEXT_PUBLIC_MCP_SERVER_URL=https://mcp.todoapp.com
```

### Deployment Script (deploy.sh)
```bash
#!/bin/bash

# Build frontend
cd frontend
npm install
npm run build

# Build backend
cd ../backend
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start services
cd src
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 &
cd ../../mcp_server
python -m server &
```

## Staging Environment

### Backend Configuration
```env
# Database
DATABASE_URL="postgresql://username:password@staging-db.cluster.region.rds.amazonaws.com/todo_staging?sslmode=require"

# Security
SECRET_KEY="staging-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
OPENAI_API_KEY="sk-staging-key"
MCP_SERVER_URL="https://staging-mcp.todoapp.com"

# Performance
WORKERS=2
TIMEOUT=300
MAX_WORKERS=4
```

### Frontend Configuration
```env
NEXT_PUBLIC_API_BASE_URL=https://staging-api.todoapp.com
NEXT_PUBLIC_MCP_SERVER_URL=https://staging-mcp.todoapp.com
```

## Development Environment

### Backend Configuration
```env
# Database
DATABASE_URL="sqlite:///./todo_app_dev.db"

# Security
SECRET_KEY="dev-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
OPENAI_API_KEY="sk-dev-key"
MCP_SERVER_URL="http://localhost:8080"

# Performance
WORKERS=1
TIMEOUT=300
MAX_WORKERS=2
```

### Frontend Configuration
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:8080
```

## Docker Configuration

### Dockerfile for Backend
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src/ ./src/
COPY backend/alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db

  mcp-server:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}
      - NEXT_PUBLIC_MCP_SERVER_URL=${NEXT_PUBLIC_MCP_SERVER_URL}

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: todo_app
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Kubernetes Configuration (Optional)

### Deployment for Backend
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
      - name: backend
        image: todo/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend-service
spec:
  selector:
    app: todo-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```