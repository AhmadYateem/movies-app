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
        REM === Switch Docker to Minikube Docker ===
        call minikube docker-env --shell=cmd > docker_env.bat
        call docker_env.bat

        REM === Build Django image inside Minikube Docker ===
        docker build -t my-django-app:latest .
        '''
      }
    }

    stage('Deploy to Minikube') {
      steps {
        bat '''
        REM === Make sure Minikube is running ===
        minikube status || minikube start --driver=docker

        REM === Apply manifests using Minikube's kubectl ===
        minikube kubectl -- apply -f deployment.yaml
        minikube kubectl -- apply -f service.yaml

        REM === Wait for the rollout to finish ===
        minikube kubectl -- rollout status deployment/django-deployment
        '''
      }
    }

  }

}
