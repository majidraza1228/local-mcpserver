# Developer Guide: Local to OpenShift Deployment

Complete guide for developers to use the MCP server locally and deploy to OpenShift Container Platform (OCP).

---

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Using the MCP Server Locally](#using-the-mcp-server-locally)
3. [Containerization](#containerization)
4. [OpenShift Deployment](#openshift-deployment)
5. [Production Best Practices](#production-best-practices)

---

## 🏠 Local Development Setup

### Prerequisites

```bash
# Required software
- Python 3.10+
- Git
- Virtual environment support

# Optional for containerization
- Docker or Podman
- OpenShift CLI (oc)
```

### Step 1: Clone and Setup

```bash
# Clone repository
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate  # Windows

# Install dependencies
pip install fastmcp markitdown fastapi uvicorn python-multipart sqlalchemy watchdog
```

### Step 2: Verify Installation

```bash
# Test Python environment
python --version  # Should be 3.10+

# Test imports
python -c "import fastmcp, markitdown, fastapi; print('✅ All imports successful')"

# Quick test script
./quick_test.sh
```

---

## 💻 Using the MCP Server Locally

### Option 1: MCP STDIO (for AI Assistants)

**Use Case:** Integrate with Claude Desktop, VS Code Copilot, or other MCP-compatible AI tools.

**Start Server:**
```bash
.venv/bin/python markitdown_server/server.py
```

**Configure AI Assistant:**

Edit `~/.config/mcp/config.json`:
```json
{
  "version": "1.0",
  "servers": {
    "markitdown": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["./markitdown_server/server.py"],
      "cwd": "/absolute/path/to/local-mcpserver"
    }
  }
}
```

**Test in VS Code:**
```
@workspace Convert myfile.pdf to markdown
```

📖 **[Complete STDIO Guide →](TESTING_MCP.md)**

---

### Option 2: HTTP Streaming Server (Unified)

**Use Case:** Web UI + REST API + Real-time streaming for applications.

**Start Server:**
```bash
./markitdown_server/start_http_streaming.sh
# Server starts on http://localhost:8080
```

**Access Web UI:**
```bash
# Open in browser
open http://localhost:8080

# Features:
# ✅ Drag-and-drop file uploads
# ✅ Real-time progress bar
# ✅ Download converted files
# ✅ Built-in API documentation
```

**Test API Endpoints:**

```bash
# 1. List available tools
curl http://localhost:8080/api/tools

# 2. Get supported formats
curl http://localhost:8080/api/formats

# 3. Upload file with streaming (Server-Sent Events)
curl -N -X POST http://localhost:8080/api/stream/convert \
  -F "file=@document.pdf"

# 4. Convert local file (JSON response)
curl -X POST http://localhost:8080/api/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/absolute/path/to/file.pdf"}'

# 5. Convert URL
curl -X POST http://localhost:8080/api/call/convert_url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/page"}'

# 6. Batch convert multiple files
curl -X POST http://localhost:8080/api/call/convert_batch \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/1.pdf", "/path/2.docx"]}'
```

---

### Developer Integration Examples

#### Python Client

```python
import requests
import json

class MarkItDownClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
    
    def convert_file(self, file_path):
        """Convert a file to Markdown"""
        response = requests.post(
            f"{self.base_url}/api/call/convert_file",
            json={"path": file_path}
        )
        return response.json()["result"]
    
    def convert_with_streaming(self, file_path):
        """Convert with streaming progress"""
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{self.base_url}/api/stream/convert",
                files={'file': f},
                stream=True
            )
            
            for line in response.iter_lines():
                if line.startswith(b'data: '):
                    data = json.loads(line[6:])
                    print(f"Progress: {data.get('percent', 0)}%")
                    
                    if data['type'] == 'complete':
                        return data['content']
    
    def get_tools(self):
        """List available tools"""
        response = requests.get(f"{self.base_url}/api/tools")
        return response.json()

# Usage
client = MarkItDownClient()

# Simple conversion
markdown = client.convert_file("/path/to/document.pdf")
print(markdown)

# With streaming
markdown = client.convert_with_streaming("/path/to/document.pdf")
print(markdown)

# List tools
tools = client.get_tools()
print(f"Available tools: {tools}")
```

#### JavaScript Client

```javascript
// Simple conversion
async function convertFile(filePath) {
  const response = await fetch('http://localhost:8080/api/call/convert_file', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: filePath })
  });
  
  const data = await response.json();
  return data.result;
}

// Upload with streaming
async function convertWithStreaming(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8080/api/stream/convert', {
    method: 'POST',
    body: formData
  });
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    const lines = chunk.split('\n\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        console.log(`Progress: ${data.percent}%`);
        
        if (data.type === 'complete') {
          return data.content;
        }
      }
    }
  }
}

// Usage
const markdown = await convertFile('/path/to/document.pdf');
console.log(markdown);
```

#### cURL Examples

```bash
# Convert PDF to Markdown
curl -X POST http://localhost:8080/api/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/dev/documents/report.pdf"}' \
  | jq -r '.result'

# Convert web page
curl -X POST http://localhost:8080/api/call/convert_url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/microsoft/markitdown"}' \
  | jq -r '.result'

# Upload and convert with progress
curl -N -X POST http://localhost:8080/api/stream/convert \
  -F "file=@document.pdf" \
  2>/dev/null | grep "data:" | sed 's/data: //'
```

---

## 🐳 Containerization

### Step 1: Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY markitdown_server/ ./markitdown_server/
COPY db_server/ ./db_server/
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create temp directory for file uploads
RUN mkdir -p /tmp/uploads && chmod 777 /tmp/uploads

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run server
CMD ["python", "markitdown_server/http_streaming_server.py"]
```

### Step 2: Create requirements.txt

```bash
# Generate requirements
cat > requirements.txt << EOF
fastmcp==2.13.1
markitdown==0.0.2
fastapi==0.115.5
uvicorn==0.32.1
python-multipart==0.0.20
sqlalchemy==2.0.36
watchdog==6.0.0
requests==2.32.3
EOF
```

### Step 3: Build Container Image

```bash
# Using Docker
docker build -t markitdown-mcp:latest .

# Using Podman (OpenShift-friendly)
podman build -t markitdown-mcp:latest .

# Test locally
docker run -p 8080:8080 markitdown-mcp:latest
# OR
podman run -p 8080:8080 markitdown-mcp:latest

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/api/tools
```

### Step 4: Create .dockerignore

```bash
# .dockerignore
.venv/
__pycache__/
*.pyc
.git/
.gitignore
*.md
.DS_Store
.vscode/
*.log
```

---

## ☁️ OpenShift Deployment

### Prerequisites

```bash
# Install OpenShift CLI
# macOS
brew install openshift-cli

# Linux
wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz
tar xvf openshift-client-linux.tar.gz
sudo mv oc /usr/local/bin/

# Verify installation
oc version
```

### Step 1: Login to OpenShift

```bash
# Login to your OpenShift cluster
oc login https://api.your-cluster.com:6443 --token=YOUR_TOKEN

# OR with username/password
oc login https://api.your-cluster.com:6443 -u username -p password

# Verify connection
oc whoami
oc cluster-info
```

### Step 2: Create Project (Namespace)

```bash
# Create new project
oc new-project markitdown-mcp

# OR switch to existing project
oc project markitdown-mcp

# Verify current project
oc project
```

### Step 3: Push Image to OpenShift Registry

**Option A: Using OpenShift Internal Registry**

```bash
# Login to internal registry
docker login -u $(oc whoami) -p $(oc whoami -t) \
  default-route-openshift-image-registry.apps.your-cluster.com

# Tag image
docker tag markitdown-mcp:latest \
  default-route-openshift-image-registry.apps.your-cluster.com/markitdown-mcp/markitdown-mcp:latest

# Push image
docker push default-route-openshift-image-registry.apps.your-cluster.com/markitdown-mcp/markitdown-mcp:latest
```

**Option B: Using External Registry (Docker Hub, Quay.io)**

```bash
# Tag for external registry
docker tag markitdown-mcp:latest quay.io/your-username/markitdown-mcp:latest

# Login to registry
docker login quay.io

# Push image
docker push quay.io/your-username/markitdown-mcp:latest
```

### Step 4: Create OpenShift Deployment

**Method 1: Using YAML Manifests**

Create `openshift/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: markitdown-mcp
  labels:
    app: markitdown-mcp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: markitdown-mcp
  template:
    metadata:
      labels:
        app: markitdown-mcp
    spec:
      containers:
      - name: markitdown-mcp
        image: quay.io/your-username/markitdown-mcp:latest
        ports:
        - containerPort: 8080
          protocol: TCP
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        env:
        - name: PORT
          value: "8080"
---
apiVersion: v1
kind: Service
metadata:
  name: markitdown-mcp
  labels:
    app: markitdown-mcp
spec:
  selector:
    app: markitdown-mcp
  ports:
  - port: 8080
    targetPort: 8080
    protocol: TCP
  type: ClusterIP
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: markitdown-mcp
  labels:
    app: markitdown-mcp
spec:
  to:
    kind: Service
    name: markitdown-mcp
  port:
    targetPort: 8080
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

Apply the manifests:

```bash
# Create deployment
oc apply -f openshift/deployment.yaml

# Verify deployment
oc get deployments
oc get pods
oc get services
oc get routes
```

**Method 2: Using OpenShift CLI Commands**

```bash
# Create deployment
oc new-app quay.io/your-username/markitdown-mcp:latest \
  --name=markitdown-mcp

# Scale deployment
oc scale deployment/markitdown-mcp --replicas=2

# Set resource limits
oc set resources deployment/markitdown-mcp \
  --limits=cpu=500m,memory=512Mi \
  --requests=cpu=250m,memory=256Mi

# Add health checks
oc set probe deployment/markitdown-mcp \
  --liveness --get-url=http://:8080/health \
  --initial-delay-seconds=10 --period-seconds=30

oc set probe deployment/markitdown-mcp \
  --readiness --get-url=http://:8080/health \
  --initial-delay-seconds=5 --period-seconds=10

# Expose service
oc expose service/markitdown-mcp

# Enable TLS
oc patch route/markitdown-mcp -p \
  '{"spec":{"tls":{"termination":"edge","insecureEdgeTerminationPolicy":"Redirect"}}}'
```

### Step 5: Verify Deployment

```bash
# Check pod status
oc get pods -l app=markitdown-mcp

# View logs
oc logs -f deployment/markitdown-mcp

# Get route URL
export APP_URL=$(oc get route markitdown-mcp -o jsonpath='{.spec.host}')
echo "Application URL: https://$APP_URL"

# Test endpoints
curl https://$APP_URL/health
curl https://$APP_URL/api/tools
curl https://$APP_URL/api/formats

# Test file conversion
curl -X POST https://$APP_URL/api/call/convert_url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Step 6: Configure Persistent Storage (Optional)

For caching or temporary files:

```yaml
# openshift/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: markitdown-storage
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

Update deployment to use PVC:

```yaml
spec:
  template:
    spec:
      containers:
      - name: markitdown-mcp
        volumeMounts:
        - name: storage
          mountPath: /tmp/uploads
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: markitdown-storage
```

Apply changes:

```bash
oc apply -f openshift/pvc.yaml
oc apply -f openshift/deployment.yaml
```

---

## 🚀 Production Best Practices

### 1. Security

```bash
# Create service account
oc create serviceaccount markitdown-sa

# Use service account in deployment
oc set serviceaccount deployment/markitdown-mcp markitdown-sa

# Add security context constraints
oc adm policy add-scc-to-user anyuid -z markitdown-sa
```

### 2. Secrets Management

```bash
# Create secret for API keys (if needed)
oc create secret generic markitdown-secrets \
  --from-literal=api-key=your-api-key

# Mount secret in deployment
oc set env deployment/markitdown-mcp \
  --from=secret/markitdown-secrets
```

### 3. ConfigMaps

```bash
# Create ConfigMap for configuration
oc create configmap markitdown-config \
  --from-literal=MAX_FILE_SIZE=10485760 \
  --from-literal=LOG_LEVEL=INFO

# Mount ConfigMap
oc set env deployment/markitdown-mcp \
  --from=configmap/markitdown-config
```

### 4. Autoscaling

```bash
# Create Horizontal Pod Autoscaler
oc autoscale deployment/markitdown-mcp \
  --min=2 \
  --max=10 \
  --cpu-percent=80

# Verify HPA
oc get hpa
```

### 5. Monitoring

```bash
# View metrics
oc adm top pods -l app=markitdown-mcp

# View logs with labels
oc logs -l app=markitdown-mcp --tail=100 -f

# Export logs
oc logs deployment/markitdown-mcp --since=1h > logs.txt
```

### 6. CI/CD Pipeline

Create `openshift/pipeline.yaml`:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: markitdown-mcp-pipeline
spec:
  params:
  - name: git-url
    type: string
  - name: image-name
    type: string
  tasks:
  - name: git-clone
    taskRef:
      name: git-clone
    params:
    - name: url
      value: $(params.git-url)
  - name: build-image
    taskRef:
      name: buildah
    params:
    - name: IMAGE
      value: $(params.image-name)
    runAfter:
    - git-clone
  - name: deploy
    taskRef:
      name: openshift-client
    params:
    - name: SCRIPT
      value: |
        oc apply -f openshift/deployment.yaml
        oc rollout status deployment/markitdown-mcp
    runAfter:
    - build-image
```

---

## 📊 Quick Reference

### Local Development

```bash
# Start STDIO server
.venv/bin/python markitdown_server/server.py

# Start HTTP server
./markitdown_server/start_http_streaming.sh

# Test locally
curl http://localhost:8080/health
```

### Container Operations

```bash
# Build
podman build -t markitdown-mcp:latest .

# Run locally
podman run -p 8080:8080 markitdown-mcp:latest

# Push to registry
podman push markitdown-mcp:latest quay.io/your-username/markitdown-mcp:latest
```

### OpenShift Operations

```bash
# Deploy
oc new-app quay.io/your-username/markitdown-mcp:latest

# Scale
oc scale deployment/markitdown-mcp --replicas=3

# Update image
oc set image deployment/markitdown-mcp markitdown-mcp=quay.io/your-username/markitdown-mcp:v2

# Rollback
oc rollout undo deployment/markitdown-mcp

# Delete
oc delete all -l app=markitdown-mcp
```

---

## 🔍 Troubleshooting

### Local Issues

```bash
# Check Python environment
which python
python --version

# Check imports
python -c "import fastmcp, markitdown, fastapi"

# Check port availability
lsof -i :8080
```

### Container Issues

```bash
# Check container logs
podman logs <container-id>

# Enter container
podman exec -it <container-id> /bin/bash

# Check running processes
podman ps
```

### OpenShift Issues

```bash
# Check pod status
oc get pods -l app=markitdown-mcp
oc describe pod <pod-name>

# View logs
oc logs <pod-name> --tail=100
oc logs <pod-name> --previous  # Previous container

# Debug pod
oc debug deployment/markitdown-mcp

# Check events
oc get events --sort-by='.lastTimestamp'

# Port forward for testing
oc port-forward service/markitdown-mcp 8080:8080
```

---

## 📚 Additional Resources

- [OpenShift Documentation](https://docs.openshift.com/)
- [FastMCP Docs](https://gofastmcp.com)
- [MarkItDown Library](https://github.com/microsoft/markitdown)
- [Container Best Practices](https://docs.openshift.com/container-platform/latest/openshift_images/create-images.html)

---

## 💡 Next Steps

1. ✅ **Complete local setup** - Test all features locally
2. ✅ **Build container** - Verify containerized app works
3. ✅ **Deploy to OpenShift** - Get app running in cluster
4. 🚀 **Production hardening** - Add monitoring, autoscaling, CI/CD
5. 📈 **Scale and optimize** - Performance tuning based on usage

---

**Questions?** Open an issue on [GitHub](https://github.com/majidraza1228/local-mcpserver/issues)
