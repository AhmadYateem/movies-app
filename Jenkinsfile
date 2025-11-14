pipeline {
  agent any

  triggers {
    // Poll GitHub every 2 minutes
    pollSCM('H/2 * * * *')
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/AhmadYateem/movies-app.git'
      }
    }

    stage('Build in Minikube Docker') {
      steps {
        bat '''
        REM === Get Minikube Docker host without TLS ===
        for /f "tokens=2 delims==" %%i in ('minikube docker-env --shell=cmd ^| findstr DOCKER_HOST') do set DOCKER_HOST=%%i
        
        REM === Strip quotes and use without TLS ===
        set DOCKER_HOST=%DOCKER_HOST:"=%
        set DOCKER_TLS_VERIFY=
        set DOCKER_CERT_PATH=

        REM === Build Django image inside Minikube Docker ===
        docker build -t mydjangoapp:latest .
        '''
      }
    }

    stage('Deploy to Minikube') {
      steps {
        bat '''
        REM === Apply the updated deployment manifest ===
        minikube kubectl -- apply -f deployment.yaml
        minikube kubectl -- apply -f service.yaml

        REM === Ensure the rollout completes ===
        minikube kubectl -- rollout status deployment/django-deployment
        '''
      }
    }
  }
}
