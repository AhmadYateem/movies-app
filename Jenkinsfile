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
        REM === Switch Docker to Minikube Docker ===
        call minikube docker-env --shell=cmd > docker_env.bat
        call docker_env.bat
        
        REM === Disable TLS verification for local Minikube ===
        SET DOCKER_TLS_VERIFY=

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
