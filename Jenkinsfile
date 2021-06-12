// pipeline best practices
// https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/#general

pipeline {

    agent any


    stages {

        stage('Build') {
            steps {
                sh '''
                    docker run --rm -v ${WORKSPACE}:/workspace \
                               --entrypoint /workspace/build.sh \
                               tech7/ubuntu_python3  
                '''
            }
            post {
                always {
                    cleanWs()
                }
            }
        }

    }
}
