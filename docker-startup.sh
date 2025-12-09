#!/bin/bash

# NextGenTeamBlue Docker Startup Script
# Handles initial setup and container management

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed"
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is installed"
    
    if [ ! -f ".env" ]; then
        print_warning ".env file not found"
        if [ -f ".env.example" ]; then
            print_warning "Creating .env from .env.example"
            cp .env.example .env
            print_warning "Please edit .env with your configuration!"
            exit 1
        fi
    fi
    print_success ".env file exists"
}

# Validate GCP credentials
validate_gcp_credentials() {
    print_header "Validating GCP Credentials"
    
    GCP_KEY_PATH=$(grep GCP_KEY_PATH .env | cut -d '=' -f 2 | sed 's/"//g' | sed "s/'//g")
    
    if [ -z "$GCP_KEY_PATH" ]; then
        print_error "GCP_KEY_PATH not found in .env"
        exit 1
    fi
    
    if [ ! -f "$GCP_KEY_PATH" ]; then
        print_error "GCP key file not found at: $GCP_KEY_PATH"
        echo "Please place your GCP service account JSON key at: $GCP_KEY_PATH"
        exit 1
    fi
    print_success "GCP credentials found at: $GCP_KEY_PATH"
}

# Create required directories
create_directories() {
    print_header "Creating Required Directories"
    
    mkdir -p logs/backend
    print_success "Created logs directory"
}

# Build Docker images
build_images() {
    print_header "Building Docker Images"
    
    docker-compose build
    print_success "Docker images built successfully"
}

# Start services
start_services() {
    print_header "Starting Services"
    
    docker-compose up -d
    print_success "Services started"
}

# Wait for services to be healthy
wait_for_services() {
    print_header "Waiting for Services to be Healthy"
    
    echo "Waiting for backend..."
    for i in {1..30}; do
        if docker-compose exec backend curl -f http://localhost:8000/ > /dev/null 2>&1; then
            print_success "Backend is healthy"
            break
        fi
        echo "Attempt $i/30..."
        sleep 2
    done
    
    echo "Waiting for frontend..."
    for i in {1..30}; do
        if docker-compose exec frontend wget --quiet --tries=1 --spider http://localhost > /dev/null 2>&1; then
            print_success "Frontend is healthy"
            break
        fi
        echo "Attempt $i/30..."
        sleep 2
    done
}

# Display service information
show_service_info() {
    print_header "Service Information"
    
    echo "Frontend:  http://localhost"
    echo "Backend:   http://localhost:8000"
    echo "API Docs:  http://localhost:8000/docs"
    echo ""
    echo "View logs:"
    echo "  All:      docker-compose logs -f"
    echo "  Backend:  docker-compose logs -f backend"
    echo "  Frontend: docker-compose logs -f frontend"
    echo ""
}

# Main menu
show_menu() {
    print_header "NextGenTeamBlue Docker Manager"
    echo ""
    echo "1) Start services"
    echo "2) Stop services"
    echo "3) Restart services"
    echo "4) View logs"
    echo "5) Rebuild images"
    echo "6) Full setup (build + start)"
    echo "7) Status"
    echo "8) Exit"
    echo ""
}

handle_command() {
    case $1 in
        1)
            print_header "Starting Services"
            docker-compose up -d
            print_success "Services started"
            docker-compose ps
            ;;
        2)
            print_header "Stopping Services"
            docker-compose down
            print_success "Services stopped"
            ;;
        3)
            print_header "Restarting Services"
            docker-compose restart
            print_success "Services restarted"
            docker-compose ps
            ;;
        4)
            docker-compose logs -f
            ;;
        5)
            build_images
            docker-compose up -d
            print_success "Images rebuilt and services restarted"
            ;;
        6)
            check_prerequisites
            validate_gcp_credentials
            create_directories
            build_images
            start_services
            wait_for_services
            show_service_info
            ;;
        7)
            docker-compose ps
            ;;
        8)
            echo "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid option"
            ;;
    esac
}

# Main execution
main() {
    if [ "$1" == "setup" ]; then
        # Automated setup mode
        check_prerequisites
        validate_gcp_credentials
        create_directories
        build_images
        start_services
        wait_for_services
        show_service_info
    else
        # Interactive mode
        while true; do
            show_menu
            read -p "Select an option: " choice
            echo ""
            handle_command "$choice"
            echo ""
            read -p "Press Enter to continue..."
            clear
        done
    fi
}

# Run main function
main "$@"
