node {
    def app
    stage('Clone repository') {
        echo "Cloning veerendra2/php-docker-apache-example"
        git url: 'https://github.com/veerendra2/php-docker-apache-example'
    }

    stage "Build Docker Image"
        docker.withServer('tcp://xx.xx.xx.xx:4342'){
            def Img = docker.build("veerendra2/php-docker-apache-example:${env.BUILD_NUMBER}",'.')
            echo "Image id: $Img.id";
            echo "Build no: $BUILD_NUMBER";
        }

    stage('Push Image') {
        sh "sudo docker login quay.io --username <username> --password <password>"
        sh "sudo docker tag veerendra2/php-docker-apache-example:$BUILD_NUMBER quay.io/veerendra2/simple-php-app:$BUILD_NUMBER"
        sh "sudo docker push quay.io/veerendra2/simple-php-app:$BUILD_NUMBER"
        }
}
