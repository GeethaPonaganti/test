node {
    def app;
    def ip;
    def container;
    stage('Clone repository') {
        echo "Cloning springboot sample application and building with maven.."
        //git url: 'https://github.com/OpsMx/gs-rest-service.git'
          git url:'https://github.com/OpsMx/restapp.git'
        def mvnHome = tool 'M3'
        sh "${mvnHome}/bin/mvn -Dmaven.repo.local=${pwd tmp: true}/m2repo  -B -DskipTests clean package"
    }
    stage('Build Docker Image'){
            docker.withServer('tcp://xx.xx.xx.xx:4342'){
            echo "Baking jar to docker image ..."
            def Img = docker.build("restapp:${env.BUILD_NUMBER}")
            echo "Image id: $Img.id";
            echo "Build no: $BUILD_NUMBER";
            echo "Launching container using this image.."
            //container = Img.run("--volume=/opt/test:/opt/")
            container = Img.run()
            echo "Container id: $container.id";
            sh "sudo docker inspect -f '{{ .NetworkSettings.IPAddress }}' ${container.id} > cont_ip";
            ip=readFile('cont_ip').trim()
            echo "Container ip: $ip";
        }
    }
    stage('Push Image') {
        sh "sudo docker login quay.io --username xxxxxxxx --password xxxxxx"
        //sh "sudo docker tag gs-rest-service:$BUILD_NUMBER quay.io/veerendra2/gs-rest-service"
       // sh "sudo docker push quay.io/veerendra2/gs-rest-service"
          sh "sudo docker tag restapp:$BUILD_NUMBER quay.io/veerendra2/restapp"
          sh "sudo docker push quay.io/veerendra2/restapp"
        }
}
