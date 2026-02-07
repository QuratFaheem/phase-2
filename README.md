# Todo Full-Stack Web Application — Phase II

This is a multi-user, full-stack web application with persistent storage, authentication, and a RESTful API. The system transforms a single-user, in-memory Python console Todo application into a secure, scalable web application. The architecture consists of a Next.js frontend, FastAPI backend, SQLModel ORM, Neon PostgreSQL database, and Better Auth authentication system.

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **Poetry** (for Python dependency management) or pip
- **Git**
- **Access to Neon PostgreSQL** (sign up at https://neon.tech)

## Setting Up the Backend (FastAPI)

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Set Up Python Environment

Using Poetry:
```bash
poetry install
poetry shell
```

Or using pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
SECRET_KEY="your-super-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Start the Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

## Setting Up the Frontend (Next.js)

### 1. Navigate to Frontend Directory

```bash
cd frontend  # From the repository root
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 4. Start the Frontend Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Running Both Servers Together

For development, you can run both servers simultaneously using a tool like `concurrently`:

```bash
# From the repository root
npm install -g concurrently
concurrently "cd backend && uvicorn src.main:app --reload" "cd frontend && npm run dev"
```

## API Endpoints

Once both servers are running, you can access the following endpoints:

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **API Redoc**: `http://localhost:8000/redoc`

## Testing the Application

### 1. User Registration

Send a POST request to `/auth/signup` with the following payload:

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "securepassword123"
}
```

### 2. User Login

Send a POST request to `/auth/signin` with the following payload:

```json
{
  "email": "test@example.com",
  "password": "securepassword123"
}
```

### 3. Creating a Todo

After logging in, use the returned token to create a todo by sending a POST request to `/todos` with the header `Authorization: Bearer <token>` and the following payload:

```json
{
  "title": "Sample Todo",
  "description": "This is a sample todo item"
}
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify your Neon PostgreSQL connection string is correct
   - Ensure your IP address is whitelisted in Neon dashboard
   - Check that SSL mode is properly configured

2. **CORS Issues**:
   - Make sure the backend allows requests from the frontend origin
   - Check that `ALLOWED_ORIGINS` in the backend configuration includes `http://localhost:3000`

3. **Authentication Issues**:
   - Ensure tokens are being properly stored and sent with requests
   - Verify that the secret key matches between frontend and backend