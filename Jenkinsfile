pipeline {
     options {
     buildDiscarder(logRotator(numToKeepStr: '7'))
 }
    agent { label 'ai_back' }
    parameters {
        gitParameter branchFilter: 'origin/(.*)', defaultValue: 'develop', name: 'BRANCH', type: 'PT_BRANCH'
  //      choice(
  //          choices: ['sdk-python' , 'sdk-python-dev'],
  //          description: '',
  //          name: 'REQUESTED_ACTION')   
    }
     
    stages {
        stage('Clone repository sdk-python') {
            steps {
                 git branch: "${params.BRANCH}", url: 'git@github.com:dicomgrid/sdk-python.git', credentialsId: 'centos'
            }
        }
 
        stage('Vault') {
            steps {
                script {
                    withCredentials([[$class: 'VaultTokenCredentialBinding', credentialsId: 'vault1', vaultAddr: 'http://10.10.20.214:8200']]) {
                        sh "vault read -field=configsdk  kv/secret/sdk > .secrets.toml"
                    }
                }
            }
        }

        stage('Remove image') {
            steps {
                sh "docker rmi -f sdk_test || true"
            }
        }

        stage('Build image') {
            steps {
                sh "docker build -t sdk_test ."
            }
        }

        stage ('Flake8') {
      //      when {
      //          expression { params.REQUESTED_ACTION == 'flake8' }
      //  }
            steps {
                sh "docker run sdk_test poetry run flake8"
                sh 'if [ $? -eq 0 ] ; then echo Test flake8 is complited; else echo Test flake8 is broken && exit 1; fi'
        }
    }
        
        stage ('Mypy') {
      //      when {
      //          expression { params.REQUESTED_ACTION == 'mypy' }
      //  }
            steps {
                sh "docker run sdk_test poetry run mypy ambra_sdk"
                sh 'if [ $? -eq 0 ] ; then echo Test mypy is complited; else echo Test mypy is broken && exit 1; fi'
        }
    }
    
       stage ('Pytest') {
    //       when {
    //           expression { params.REQUESTED_ACTION == 'pytest' }
    //   }
           steps {
               sh "pwd && ls -la"               
               sh "docker run --mount type=bind,source=/spool/workspace/sdk-python/.secrets.toml,target=/src/.secrets.toml --mount type=bind,source=/etc/hosts,target=/etc/hosts sdk_test poetry run pytest"
               sh 'if [ $? -eq 0 ] ; then echo Test pytest is complited; else echo Test pytest is broken && exit 1; fi'
       }
   }
        
        stage('show images') {
            steps {
                sh "docker ps -a |grep sdk"
            }
        }

    }
    post {
        always {
            cleanWs()
        }
    }
}
