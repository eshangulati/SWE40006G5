pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'myapp'
        TEST_SERVER_IP = '3.213.22.15'
        PRODUCTION_SERVER_IP = '44.223.169.199'
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
                script {
                    sh "docker tag $DOCKER_IMAGE_NAME:latest $DOCKER_REPO:latest"
                    sh "docker push $DOCKER_REPO:latest"
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'docker run --rm $DOCKER_IMAGE_NAME pytest unittests/'
            }
        }

        stage('Trigger Ansible Playbook') {
            steps {
                ansiblePlaybook inventory: 'ansible/inventory.ini', playbook: 'ansible/docker-setup.yml'
                ansiblePlaybook inventory: 'ansible/inventory.ini', playbook: 'ansible/nginx-setup.yml'
            }
        }

        stage('Deploy to Test Server') {
            steps {
                sh """
                ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ec2-user@$TEST_SERVER_IP \\
                    'docker pull buffy1809/myapp:latest && \\
                    docker stop myapp || true && \\
                    docker rm myapp || true && \\
                    docker run -d --name myapp -p 8081:80 buffy1809/myapp:latest'
                """
            }
        }

        stage('Run Selenium Tests') {
            steps {
                // // Start both app and Selenium services with Docker Compose
                // sh 'docker-compose -f seleniumtests/docker-compose.yml up -d'

                // // Run Selenium tests inside the app container
                // sh 'docker-compose -f seleniumtests/docker-compose.yml run --rm app pytest selenium_tests/'

                // // Stop and clean up the containers
                // sh 'docker-compose -f seleniumtests/docker-compose.yml down'

                echo 'Selenium tests are skipped for now'
            }
        }

        stage('Deploy to Production Server') {
            steps {
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
