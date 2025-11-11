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

    stage('Ensure Minikube running') {
      steps {
        bat '''
        REM === Check Minikube and start if needed (Docker Desktop must be running) ===
        minikube version
        minikube status || minikube start --driver=docker
        '''
      }
    }

    stage('Build in Minikube Docker') {
      steps {
        bat '''
        REM === Switch Docker to Minikube Docker ===
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
        REM === Apply manifests using Minikube's kubectl and wait for rollout ===
        minikube kubectl -- apply -f deployment.yaml
        minikube kubectl -- apply -f service.yaml
        minikube kubectl -- rollout status deployment/django-deployment
        '''
      }
    }

    stage('Show Service URL') {
      steps {
        bat '''
        REM === Print the service URL (open it in your browser) ===
        minikube service django-service --url
        '''
      }
    }
  }

  post {
    always {
      bat '''
      if exist docker_env.bat del /f /q docker_env.bat
      '''
    }
  }
}
