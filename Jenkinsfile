pipeline {
    agent {docker { image 'python:3.7.2' }
    }
    stages {
        stage('Checkout project') {
            steps {
                script {
                    git branch: "master",
                        credentialsId: 'git-muladzevitali',
                        url: 'https://github.com/muladzevitali/flowersngin.git'
                }
            }
        }
        stage('Installing packages') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Migrate') {
            steps {
                script {
                    sh 'python manage.py makemigrations && python manage.py migrage && python manage.py init_defaults'
                }
            }
        }

    }
}
