pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKER_IMAGE_NAME        = 'cloudwithpreetham/flask-demo-app'
        APP_PORT                 = '5000'
        CONTAINER_NAME           = 'flask-app-prod'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Executing pytest unit tests inside a Python container...'
                sh '''
                    docker run --rm -v "$(pwd):/app" -w /app python:3.11-alpine \
                    sh -c "pip install --no-cache-dir -r requirements.txt && pytest -v"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker container image: ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER}..."
                sh """
                    docker build -t ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} ${DOCKER_IMAGE_NAME}:latest
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Authenticating and pushing container image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKERHUB_CREDENTIALS_ID}",
                    passwordVariable: 'DOCKER_PASS',
                    usernameVariable: 'DOCKER_USER'
                )]) {
                    sh """
                        echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${DOCKER_IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying container locally on port ${APP_PORT}..."
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d -p ${APP_PORT}:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        always {
            echo 'Pruning dangling images...'
            sh 'docker image prune -f || true'
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check stage console logs.'
        }
    }
}
