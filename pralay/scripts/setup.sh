#!/bin/bash

# Pralay Project Setup Script
# Sets up the complete development environment

set -e  # Exit on error

echo "🌊 Pralay Flash Flood Prediction System - Setup Script"
echo "======================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
echo -e "${BLUE}📦 Checking Docker...${NC}"
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker is running${NC}"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}📝 Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please review .env and update with your configuration${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi
echo ""

# Start Docker services
echo -e "${BLUE}🐳 Starting Docker services...${NC}"
docker-compose up -d postgres redis mosquitto
echo -e "${GREEN}✅ Core services started${NC}"
echo ""

# Wait for PostgreSQL to be ready
echo -e "${BLUE}⏳ Waiting for PostgreSQL to be ready...${NC}"
sleep 10
until docker-compose exec -T postgres pg_isready -U pralay_user -d pralay_db > /dev/null 2>&1; do
    echo "Waiting for database connection..."
    sleep 2
done
echo -e "${GREEN}✅ PostgreSQL is ready${NC}"
echo ""

# Check if we should install Python dependencies
read -p "Install Python dependencies for backend? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🐍 Setting up Python backend...${NC}"
    cd backend

    # Create virtual environment
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

    # Install dependencies
    pip install --upgrade pip
    pip install -r requirements.txt

    echo -e "${GREEN}✅ Python dependencies installed${NC}"

    # Run migrations
    echo -e "${BLUE}🗄️  Running database migrations...${NC}"
    alembic upgrade head
    echo -e "${GREEN}✅ Database schema created${NC}"

    cd ..
fi
echo ""

# Check if we should install Node dependencies
read -p "Install Node dependencies for frontend? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}⚛️  Setting up React frontend...${NC}"
    cd frontend
    npm install
    echo -e "${GREEN}✅ Node dependencies installed${NC}"
    cd ..
fi
echo ""

# Create necessary directories
echo -e "${BLUE}📁 Creating data directories...${NC}"
mkdir -p data/raw/{imd_rainfall,srtm_elevation,landslide_inventory,soil_data}
mkdir -p data/processed/{features,labels}
mkdir -p ml/models/trained
echo -e "${GREEN}✅ Data directories created${NC}"
echo ""

# Start all services
echo -e "${BLUE}🚀 Starting all services...${NC}"
docker-compose up -d
echo ""

# Show status
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "======================================================="
echo "🎯 Services are running at:"
echo ""
echo "  Frontend:      http://localhost:5173"
echo "  Backend API:   http://localhost:8000"
echo "  API Docs:      http://localhost:8000/docs"
echo "  PostgreSQL:    localhost:5432"
echo "  Redis:         localhost:6379"
echo "  MQTT Broker:   localhost:1883"
echo ""
echo "======================================================="
echo ""
echo "📚 Quick Commands:"
echo ""
echo "  View logs:           docker-compose logs -f [service]"
echo "  Stop services:       docker-compose down"
echo "  Restart services:    docker-compose restart"
echo "  Run backend tests:   cd backend && pytest"
echo "  Run frontend:        cd frontend && npm run dev"
echo ""
echo "🔧 Development:"
echo ""
echo "  Backend shell:       cd backend && source venv/bin/activate"
echo "  Database shell:      docker-compose exec postgres psql -U pralay_user -d pralay_db"
echo "  Redis CLI:           docker-compose exec redis redis-cli"
echo "  MQTT subscribe:      mosquitto_sub -h localhost -t 'sensors/#'"
echo ""
echo "======================================================="
echo ""
echo -e "${BLUE}📖 Check PROGRESS.md for implementation status${NC}"
echo -e "${BLUE}📘 Check README.md for full documentation${NC}"
echo ""
