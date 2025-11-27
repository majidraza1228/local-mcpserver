#!/bin/bash

# OpenShift Deployment Script
# This script automates the deployment of MarkItDown MCP Server to OpenShift

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="markitdown-mcp"
IMAGE_NAME="markitdown-mcp"
IMAGE_TAG="latest"
REGISTRY="quay.io"  # Change to your registry
REGISTRY_USERNAME="${REGISTRY_USERNAME:-your-username}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}MarkItDown MCP - OpenShift Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v oc &> /dev/null; then
    echo -e "${RED}Error: OpenShift CLI (oc) not found${NC}"
    echo "Install from: https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/"
    exit 1
fi

if ! command -v podman &> /dev/null && ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Neither podman nor docker found${NC}"
    echo "Install podman or docker to continue"
    exit 1
fi

# Use podman if available, otherwise docker
if command -v podman &> /dev/null; then
    CONTAINER_TOOL="podman"
else
    CONTAINER_TOOL="docker"
fi

echo -e "${GREEN}✓ Using container tool: $CONTAINER_TOOL${NC}"

# Check if logged in to OpenShift
if ! oc whoami &> /dev/null; then
    echo -e "${RED}Error: Not logged in to OpenShift${NC}"
    echo "Run: oc login https://api.your-cluster.com:6443"
    exit 1
fi

echo -e "${GREEN}✓ Logged in as: $(oc whoami)${NC}"
echo ""

# Step 1: Create or switch to project
echo -e "${YELLOW}Step 1: Setting up OpenShift project...${NC}"
if oc project $PROJECT_NAME &> /dev/null; then
    echo -e "${GREEN}✓ Using existing project: $PROJECT_NAME${NC}"
else
    echo -e "${YELLOW}Creating new project: $PROJECT_NAME${NC}"
    oc new-project $PROJECT_NAME --display-name="MarkItDown MCP Server" \
        --description="Document conversion service with MCP protocol"
    echo -e "${GREEN}✓ Project created${NC}"
fi
echo ""

# Step 2: Build container image
echo -e "${YELLOW}Step 2: Building container image...${NC}"
FULL_IMAGE_NAME="$REGISTRY/$REGISTRY_USERNAME/$IMAGE_NAME:$IMAGE_TAG"

echo "Building: $FULL_IMAGE_NAME"
$CONTAINER_TOOL build -t $IMAGE_NAME:$IMAGE_TAG .
$CONTAINER_TOOL tag $IMAGE_NAME:$IMAGE_TAG $FULL_IMAGE_NAME

echo -e "${GREEN}✓ Image built successfully${NC}"
echo ""

# Step 3: Push image to registry
echo -e "${YELLOW}Step 3: Pushing image to registry...${NC}"
echo "Target: $FULL_IMAGE_NAME"
echo ""
echo "Make sure you're logged in to the registry:"
echo "  $CONTAINER_TOOL login $REGISTRY"
echo ""
read -p "Press Enter to continue with push, or Ctrl+C to cancel..."

$CONTAINER_TOOL push $FULL_IMAGE_NAME
echo -e "${GREEN}✓ Image pushed successfully${NC}"
echo ""

# Step 4: Update deployment YAML with correct image
echo -e "${YELLOW}Step 4: Updating deployment configuration...${NC}"
sed -i.bak "s|image: quay.io/your-username/markitdown-mcp:latest|image: $FULL_IMAGE_NAME|g" openshift/deployment.yaml
echo -e "${GREEN}✓ Configuration updated${NC}"
echo ""

# Step 5: Deploy to OpenShift
echo -e "${YELLOW}Step 5: Deploying to OpenShift...${NC}"

# Apply ConfigMap
echo "Creating ConfigMap..."
oc apply -f openshift/configmap.yaml

# Apply Deployment and Service
echo "Creating Deployment and Service..."
oc apply -f openshift/deployment.yaml

# Apply HPA
echo "Creating Horizontal Pod Autoscaler..."
oc apply -f openshift/hpa.yaml

echo -e "${GREEN}✓ Resources deployed${NC}"
echo ""

# Step 6: Wait for deployment
echo -e "${YELLOW}Step 6: Waiting for deployment to complete...${NC}"
oc rollout status deployment/$PROJECT_NAME --timeout=5m

echo -e "${GREEN}✓ Deployment complete${NC}"
echo ""

# Step 7: Get application URL
echo -e "${YELLOW}Step 7: Getting application information...${NC}"
APP_URL=$(oc get route $PROJECT_NAME -o jsonpath='{.spec.host}')

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${GREEN}Application URL:${NC} https://$APP_URL"
echo ""
echo -e "${YELLOW}Quick Test Commands:${NC}"
echo "curl https://$APP_URL/health"
echo "curl https://$APP_URL/api/tools"
echo "curl https://$APP_URL/api/formats"
echo ""
echo -e "${YELLOW}View Resources:${NC}"
echo "oc get pods -l app=$PROJECT_NAME"
echo "oc get services"
echo "oc get routes"
echo "oc get hpa"
echo ""
echo -e "${YELLOW}View Logs:${NC}"
echo "oc logs -f deployment/$PROJECT_NAME"
echo ""
echo -e "${YELLOW}Scale Application:${NC}"
echo "oc scale deployment/$PROJECT_NAME --replicas=3"
echo ""

# Restore original deployment.yaml
mv openshift/deployment.yaml.bak openshift/deployment.yaml 2>/dev/null || true

echo -e "${GREEN}Deployment script completed successfully!${NC}"
