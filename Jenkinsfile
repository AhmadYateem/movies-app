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

    REM === Force a new rollout by bumping an annotation ===
    minikube kubectl -- patch deployment django-deployment -p "{ \\"spec\\": { \\"template\\": { \\"metadata\\": { \\"annotations\\": { \\"buildNumber\\": \\"%BUILD_NUMBER%\\" } } } } }"

    REM === Ensure the rollout completes ===
    minikube kubectl -- rollout status deployment/django-deployment --timeout=180s
    '''
  }
}
  }
} 