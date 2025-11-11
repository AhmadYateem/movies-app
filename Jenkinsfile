pipeline {
  agent any

  triggers {
    // Poll GitHub every 2 minutes
    pollSCM('H/2 * * * *')
  }

  environment {
    // Optionally override if kind.exe not in PATH
    KIND_CMD = 'kind'
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/AhmadYateem/movies-app.git'
      }
    }

    stage('Ensure kind cluster') {
      steps {
        bat '''
        kind version || exit /b 1
        kind get clusters | findstr /I movies || kind create cluster --name movies
        '''
      }
    }

    stage('Build & Load Image') {
      steps {
        bat '''
        docker build -t mydjangoapp:latest .
        kind load docker-image mydjangoapp:latest --name movies
        '''
      }
    }

    stage('Deploy to cluster') {
      steps {
        bat '''
        kubectl apply -f deployment.yaml
        kubectl apply -f service.yaml
        kubectl rollout status deployment/django-deployment
        '''
      }
    }

    stage('Service URL') {
      steps {
        bat '''
        for /f %%p in ('kubectl get svc django-service -o jsonpath="{.spec.ports[0].nodePort}"') do set PORT=%%p
        echo Service reachable at: http://localhost:%PORT%
        '''
      }
    }
  }
}
