# Quick Start Commands - Movies App Kubernetes Deployment

## 🚀 Initial Setup (One Time)

### 1. Install Minikube
```powershell
curl -Lo minikube.exe https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe
# Copy minikube.exe to C:\Windows\System32
minikube version
```

### 2. Start Minikube
```powershell
cd C:\Users\ahmad\OneDrive\Desktop\EECE430-minikube\movies-app
minikube start --driver=docker
```

### 3. Configure Docker for Minikube
```powershell
minikube docker-env --shell=cmd
# COPY AND PASTE ALL 6 OUTPUT LINES
```

### 4. Build and Deploy
```powershell
docker build -t mydjangoapp:latest .
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 5. Access App
```powershell
minikube service django-service --url
# Keep terminal open, open URL in browser
```

---

## 🔧 Jenkins Setup (One Time)

1. **Configure Jenkins to run as Windows user:**
   - Win+R → `services.msc`
   - Jenkins → Properties → Log On → This account: `.\ahmad`
   - Restart Jenkins

2. **Create Pipeline:**
   - New Item → Pipeline
   - Pipeline from SCM
   - Git: `https://github.com/AhmadYateem/movies-app.git`
   - Branch: `*/main`
   - Save

3. **Test Build:**
   - Build Now → Wait for SUCCESS

---

## 📝 Daily Testing Workflow

### Test Automatic Deployment
```powershell
# 1. Make a code change
cd C:\Users\ahmad\OneDrive\Desktop\EECE430-minikube\movies-app
# Edit any file (e.g., templates/index.html)

# 2. Commit and push
git add .
git commit -m "Test deployment"
git push origin main

# 3. Wait 2 minutes, then check Jenkins
# New build should start automatically

# 4. Verify new pod
kubectl get pods
# Check AGE column - should be recent

# 5. Access app
minikube service django-service --url
```

---

## 🔍 Monitoring Commands

```powershell
# Check pod status
kubectl get pods

# Check pod details
kubectl get pods -o wide

# View pod logs
kubectl logs <pod-name>

# Check deployments
kubectl get deployments

# Check services
kubectl get services

# Minikube status
minikube status
```

---

## 🧹 Cleanup Commands

```powershell
# Delete everything
kubectl delete deployment --all
kubectl delete service --all
minikube stop
minikube delete --all --purge
```

---

## ⚡ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Cannot access app | Run `minikube service django-service --url` and keep terminal open |
| Pod CrashLoopBackOff | Check logs: `kubectl logs <pod-name>` |
| Jenkins build fails | Verify minikube is running: `minikube status` |
| Docker env not working | Re-run `minikube docker-env --shell=cmd` and paste output |

---

## ✅ Success Checklist

- [ ] Minikube running: `minikube status`
- [ ] Pod running: `kubectl get pods` shows "Running"
- [ ] Can access app via browser
- [ ] Jenkins build succeeds manually
- [ ] Git push triggers automatic build (wait 2 min)
- [ ] New pod created after auto-build

---

## 📊 Testing Scale (Optional)

```powershell
# Edit deployment.yaml: replicas: 3
# Commit and push
git add deployment.yaml
git commit -m "Scale to 3 replicas"
git push

# Wait for auto-build (2 min)
# Check 3 pods running
kubectl get pods
```
