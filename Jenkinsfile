pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'myapp'
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

        stage('Run Unit Tests') {
            steps {
                // Run the tests inside the Docker container
                sh 'docker run --rm $DOCKER_IMAGE_NAME pytest tests/'
            }
        }

        stage('Deploy to Test Server') {
            steps {
                script {
                    // Directly SSH using the private key
                    sh """
                    ssh -i /var/lib/jenkins/.ssh/id_rsa -o StrictHostKeyChecking=no ec2-user@44.223.169.199 \\
                        'docker pull buffy1809/myapp:latest && \\
                        docker stop myapp || true && \\
                        docker rm myapp || true && \\
                        docker run -d --name myapp -p 80:80 buffy1809/myapp:latest'
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
