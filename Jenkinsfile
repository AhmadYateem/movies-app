pipeline {
  agent any

  triggers {
    pollSCM('H/2 * * * *')
  }

  stages {

    stage('Checkout') {
      steps {
        git branch: 'main', url: "https://github.com/AhmadYateem/movies-app.git"
      }
    }

    stage('Build in Minikube Docker') {
      steps {
        bat '''
        REM === Ensure Minikube is running (ADDED) ===
        minikube status || minikube start --driver=docker --wait=all

        REM === Switch Docker to Minikube Docker (UNCHANGED, but now works) ===
        call minikube docker-env --shell=cmd > docker_env.bat
        call docker_env.bat

        REM === Build Django image inside Minikube Docker ===
        docker build -t mydjangoapp:latest .
        '''
      }
    }

    stage('Deploy to Minikube') {
      steps {
        bat '''
        REM === Apply deployment and service ===
        minikube kubectl -- apply -f deployment.yaml
        minikube kubectl -- apply -f service.yaml

        REM === Wait for rollout ===
        minikube kubectl -- rollout status deployment/django-deployment --timeout=180s
        '''
      }
    }
  }
}
