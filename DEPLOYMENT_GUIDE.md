# Django Movies App - Kubernetes Deployment Guide

## Summary of Fixes Applied

### Issues Fixed:
1. ✅ **Image name consistency**: Changed `my-django-app:latest` to `mydjangoapp:latest` in deployment.yaml and Jenkinsfile
2. ✅ **ALLOWED_HOSTS**: Updated Django settings to accept all hosts (`ALLOWED_HOSTS = ['*']`)
3. ✅ **Service deployment**: Added `service.yaml` application in Jenkinsfile
4. ✅ **Database migrations**: Updated Dockerfile to run migrations automatically on container startup

---

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Docker Desktop installed and running
- [ ] Jenkins installed and running on localhost:8080
- [ ] Git installed
- [ ] GitHub repository: https://github.com/AhmadYateem/movies-app.git

---

## Part 1: Install Minikube

### Step 1: Download and Install Minikube
```powershell
curl -Lo minikube.exe https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe
```

### Step 2: Add Minikube to PATH
```powershell
# Find where minikube is located
where minikube

# Copy minikube.exe to System32
# Navigate to the path shown (e.g., C:\Users\ahmad\)
# Copy minikube.exe to C:\Windows\System32
```

### Step 3: Verify Installation
```powershell
minikube version
```
Expected output: `minikube version: vX.XX.X`

---

## Part 2: Initial Minikube Setup

### Step 1: Start Minikube
```powershell
# Make sure Docker Desktop is running first!
cd C:\Users\ahmad\OneDrive\Desktop\EECE430-minikube\movies-app

minikube start --driver=docker
```

**Note**: If you see warnings but Docker Desktop shows a running minikube container, you can proceed (CTRL+C the command).

### Step 2: Configure Docker to Use Minikube
```powershell
# Get the environment variables
minikube docker-env --shell=cmd

# Copy and paste ALL 6 lines from the output
# They should look like:
# SET DOCKER_TLS_VERIFY=1
# SET DOCKER_HOST=tcp://...
# etc.
```

### Step 3: Build Docker Image Manually (First Time)
```powershell
docker build -t mydjangoapp:latest .

# Verify the image was created
docker images
```
You should see `mydjangoapp` in the list.

### Step 4: Deploy to Kubernetes
```powershell
# Apply deployment
kubectl apply -f deployment.yaml

# Apply service
kubectl apply -f service.yaml

# Verify pod is running
kubectl get pods
```

Expected output:
```
NAME                                 READY   STATUS    RESTARTS   AGE
django-deployment-xxxxxxxxxx-xxxxx   1/1     Running   0          30s
```

### Step 5: Access Your Application
```powershell
minikube service django-service --url
```

This will output a URL like: `http://127.0.0.1:XXXXX`

**IMPORTANT**: Keep this terminal open! The tunnel only works while the command is running.

Open the URL in your browser - you should see your Django movies app.

**To stop**: Press CTRL+C in the terminal

---

## Part 3: Configure Jenkins

### Step 1: Run Jenkins as Your Windows User

1. Press `Win + R`
2. Type: `services.msc` and press Enter
3. Find "Jenkins" in the services list
4. Right-click → Properties → "Log On" tab
5. Select "This account"
6. Enter your account:
   ```
   Account: .\ahmad  (or run 'whoami' in CMD to get your username)
   Password: Your Windows password (NOT your PIN)
   ```
7. Click Apply
8. Right-click Jenkins → Restart

### Step 2: Access Jenkins
- Open browser: http://localhost:8080
- Enter your Jenkins credentials

### Step 3: Create Jenkins Pipeline

1. Click "New Item"
2. Enter name: `movies-app-pipeline`
3. Select: "Pipeline"
4. Click OK

### Step 4: Configure Pipeline

Scroll to "Pipeline" section:

1. **Definition**: Select "Pipeline script from SCM"
2. **SCM**: Select "Git"
3. **Repository URL**: `https://github.com/AhmadYateem/movies-app.git`
4. **Branch Specifier**: `*/main`
5. **Script Path**: `Jenkinsfile`

Click **Save**

---

## Part 4: Testing the Complete Setup

### Test 1: Manual Jenkins Build

1. In Jenkins, click on your pipeline
2. Click "Build Now"
3. Watch the build progress (click on the build number → Console Output)
4. Wait for "Finished: SUCCESS"

**Expected stages**:
- Checkout ✓
- Build in Minikube Docker ✓
- Deploy to Minikube ✓

### Test 2: Verify Deployment
```powershell
# Check pod status
kubectl get pods

# Check pod age - should match your build time
# NAME                                 READY   STATUS    RESTARTS   AGE
# django-deployment-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

### Test 3: Access Application
```powershell
minikube service django-service --url
```
Open the returned URL and verify the movies app loads correctly.

### Test 4: Automatic Build (GitHub Polling)

1. Make a small change to your code (e.g., edit `templates/index.html`)
2. Commit and push to GitHub:
   ```powershell
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```
3. Wait 2 minutes (Jenkins polls every 2 minutes)
4. Check Jenkins - a new build should start automatically
5. After build completes, verify the pod age updated:
   ```powershell
   kubectl get pods
   ```

### Test 5: Multiple Replicas (Optional)

1. Edit `deployment.yaml`, change `replicas: 1` to `replicas: 3`
2. Commit and push
3. Wait for automatic build
4. Verify multiple pods:
   ```powershell
   kubectl get pods
   ```
   You should see 3 pods running!

---

## Common Commands Reference

### Minikube Commands
```powershell
# Start minikube
minikube start --driver=docker

# Stop minikube
minikube stop

# Check status
minikube status

# Access service
minikube service django-service --url

# Open Kubernetes dashboard
minikube dashboard
```

### Kubectl Commands
```powershell
# Get all pods
kubectl get pods

# Get detailed pod info
kubectl get pods -o wide

# Describe a pod (replace <pod-name>)
kubectl describe pod <pod-name>

# Get pod logs (replace <pod-name>)
kubectl logs <pod-name>

# Get deployments
kubectl get deployments

# Get services
kubectl get services
```

### Docker Commands (in Minikube context)
```powershell
# Switch to Minikube Docker
minikube docker-env --shell=cmd
# Then copy-paste the output

# List images
docker images

# Build image
docker build -t mydjangoapp:latest .
```

---

## Troubleshooting

### Issue: Pod is in CrashLoopBackOff
```powershell
# Check pod logs
kubectl get pods
kubectl logs <pod-name>

# Common causes:
# - Database migration errors
# - Missing dependencies in requirements.txt
# - Syntax errors in Django code
```

### Issue: Cannot access application via URL
- Make sure you're running `minikube service django-service --url`
- Don't close the terminal - it needs to stay open
- Try: `minikube service django-service` (opens browser automatically)

### Issue: Jenkins build fails at "Build in Minikube Docker"
```powershell
# Make sure minikube is running
minikube status

# Restart minikube if needed
minikube stop
minikube start --driver=docker
```

### Issue: kubectl command not found in Jenkins
- Verify Jenkins is running as your Windows user (see Part 3, Step 1)
- Restart Jenkins service
- The Jenkinsfile uses `minikube kubectl --` which should work

### Issue: Image pull errors
- Verify `imagePullPolicy: Never` is set in deployment.yaml
- Make sure you built the image in Minikube's Docker context
- Check images: `docker images` (after switching to Minikube Docker)

---

## Clean Up / Start Fresh

If you need to reset everything:

```powershell
# Delete all Kubernetes resources
kubectl delete deployment --all
kubectl delete replicaset --all
kubectl delete pods --all
kubectl delete service --all

# Stop and delete Minikube
minikube stop
minikube delete --all --purge

# Then start over from Part 2
```

---

## Expected Final State

When everything is working correctly:

1. ✅ Minikube running in Docker Desktop
2. ✅ Jenkins pipeline configured and polling GitHub every 2 minutes
3. ✅ Django app deployed in Kubernetes pod(s)
4. ✅ Service exposing the app
5. ✅ Automatic rebuilds on GitHub commits
6. ✅ Application accessible via `minikube service django-service --url`

---

## Success Criteria

- [ ] Manual Jenkins build succeeds
- [ ] Pod shows "Running" status
- [ ] Can access movies app via browser
- [ ] Code changes trigger automatic rebuild within 2 minutes
- [ ] New pod created after automatic rebuild
- [ ] App still accessible after rebuild

---

## Additional Notes

- The polling interval is set to 2 minutes in Jenkinsfile: `pollSCM('H/2 * * * *')`
- To change to 5 minutes, use: `pollSCM('H/5 * * * *')`
- The app uses SQLite database (stored in container - data lost on pod restart)
- For production, consider using persistent volumes
- Current setup allows any host to access (`ALLOWED_HOSTS = ['*']`) - OK for development

---

## Files Modified

1. **deployment.yaml** - Image name corrected to `mydjangoapp:latest`
2. **Jenkinsfile** - Image name corrected, service.yaml deployment added
3. **website/website/settings.py** - ALLOWED_HOSTS set to `['*']`
4. **Dockerfile** - Added automatic database migrations on startup

All changes have been applied to your local files. Don't forget to commit and push to GitHub!
