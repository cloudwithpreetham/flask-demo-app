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
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running pytest inside an isolated Python container...'
                sh '''
                    # 1. Create a container and copy workspace files into it
                    docker create --name flask-test-runner -w /app python:3.11-alpine tail -f /dev/null
                    docker cp . flask-test-runner:/app
                    docker start flask-test-runner

                    # 2. Install dependencies and run tests inside the container
                    docker exec flask-test-runner pip install --no-cache-dir -r requirements.txt
                    docker exec flask-test-runner pytest -v

                    # 3. Clean up the test container
                    docker stop flask-test-runner
                    docker rm flask-test-runner
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER}..."
                sh """
                    docker build -t ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} ${DOCKER_IMAGE_NAME}:latest
                """
            }
        }

        stage('Push to Registry') {
            steps {
                echo 'Pushing image to Docker Hub...'
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
                echo "Deploying application on port ${APP_PORT}..."
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
            echo 'Pruning dangling images and cleaning test remnants...'
            sh '''
                docker rm -f flask-test-runner || true
                docker image prune -f || true
            '''
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check stage console logs.'
        }
    }
}
