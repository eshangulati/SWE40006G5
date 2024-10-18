pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'myapp'
        TEST_SERVER_IP = '44.223.169.199'
        PRODUCTION_SERVER_IP = '3.213.22.15'
        SSH_KEY_PATH = '/var/lib/jenkins/.ssh/id_rsa'
        DOCKER_REPO = 'buffy1809/myapp'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/eshangulati/SWE40006G5.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE_NAME:latest .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    script {
                        // Login to Docker Hub
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME"
                
                        // Tag the image with the Docker Hub repo
                        sh "docker tag $DOCKER_IMAGE_NAME:latest $DOCKER_REPO:latest"
                
                        // Push the new image to Docker Hub
                        sh "docker push $DOCKER_REPO:latest"
                    }
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'docker run --rm $DOCKER_IMAGE_NAME pytest tests/'
            }
        }

        stage('Deploy to Test Server') {
            steps {
                script {
                    sh """
                    ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ec2-user@$TEST_SERVER_IP \\
                        'docker pull buffy1809/myapp:latest && \\
                        docker stop myapp || true && \\
                        docker rm myapp || true && \\
                        docker run -d --name myapp -p 80:80 buffy1809/myapp:latest'
                    """
                }
            }
        }

        stage('Deploy to Production Server') {
            steps {
                script {
                    sh """
                    ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ec2-user@$PRODUCTION_SERVER_IP \\
                        'docker pull buffy1809/myapp:latest && \\
                        docker stop myapp || true && \\
                        docker rm myapp || true && \\
                        docker run -d --name myapp -p 8081:80 buffy1809/myapp:latest'
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
