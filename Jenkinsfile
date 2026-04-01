pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {

        stage('Check Python') {
            steps {
                sh 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Install Docker CLI') {
            steps {
                sh '''
                apt-get update
                apt-get install -y docker.io
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker --version'
                sh 'docker build -t aceest-gym .'
            }
        }
    }
}