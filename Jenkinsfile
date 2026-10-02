pipeline {
    agent any

    environment {
        // Update with your Docker Hub username
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKER_IMAGE_NAME        = 'cloudwithpreetham/flask-demo-app'
        APP_PORT                 = '5000'
        CONTAINER_NAME           = 'flask-app-prod'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scms
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests with pytest inside a Python container...'
                sh '''
                    docker run --rm -v $(pwd):/app -w /app python:3.11-alpine \
                    sh -c "pip install --no-cache-dir -r requirements.txt && pytest"
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

        stage('Push to Registry') {
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS_ID}", passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
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
                echo "Deploying application container on port ${APP_PORT}..."
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
            echo 'Jenkins pipeline completed successfully!'
        }
        failure {
            echo 'Jenkins pipeline failed. Check console output for logs.'
        }
    }
}
