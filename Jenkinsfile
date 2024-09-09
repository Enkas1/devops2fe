pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', 
                          branches: [[name: '*/dev']],
                          userRemoteConfigs: [[url: 'https://github.com/Vedmastaren/devops2fe.git']]
                ])
            }
        }
        stage('Install Dependencies') {
            steps {
                // Installera nödvändiga paket
                sh '''
                # Uppdatera paketlistan
                sudo apt update
                
                # Installera Python 3 och pip
                sudo apt install -y python3 python3-pip

                # Installera och uppdatera pytest
                sudo pip3 install -U pytest --break-system-packages

                # Installera Docker
                sudo apt install -y docker.io
                
                # Lägg till Jenkins-användare till Docker-gruppen
                sudo usermod -aG docker jenkins
                
                # Installera Docker Compose
                sudo apt install -y docker-compose
                '''
            }
        }

        stage('Setup') {
            steps {
                // Skapa en virtuell miljö och installera beroenden
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                // Linting med flake8 på specifika filer
                sh '''
                . venv/bin/activate
                flake8 app.py functions.py
                '''
            }
        }

        stage('Build') {
            steps {
                // Bygg med make (om tillämpligt)
                sh 'make'
            }
        }

        stage('Test') {
            steps {
                // Kör tester med pytest
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Bygget lyckades!'
        }
        failure {
            echo 'Bygget misslyckades.'
        }
    }
}
