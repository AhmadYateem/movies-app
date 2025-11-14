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
    bat """
    REM === Switch Docker to Minikube Docker ===
    call minikube docker-env --shell=cmd > docker_env.bat
    call docker_env.bat

    REM === Build Django image inside Minikube Docker with unique tag ===
    docker build -t mydjangoapp:%BUILD_NUMBER% .
    """
  }
}

stage('Deploy to Minikube') {
  steps {
    bat """
    REM === Ensure deployment and service exist at least once ===
    minikube kubectl -- apply -f deployment.yaml
    minikube kubectl -- apply -f service.yaml

    REM === Update deployment to use new image tag ===
    minikube kubectl -- set image deployment/django-deployment django-container=mydjangoapp:%BUILD_NUMBER%

    REM === Ensure the rollout completes ===
    minikube kubectl -- rollout status deployment/django-deployment --timeout=180s
    """
  }
}
  }
} 