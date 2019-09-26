def label = "jenkins-slave-${UUID.randomUUID().toString()}"
podTemplate(label: label, containers: [
    containerTemplate(name: 'slave1', image: 'gcr.io/sentrifugo/jenkins-slave:v1', ttyEnabled: true, command: 'cat')
],
volumes: [
  hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock')
]) {
    node(label) {
        def APP_NAME = "interactive bot"
        def tag = "dev"
        def gitBranch = env.BRANCH_NAME
           
          stage("Checking Branch") {
                container('slave1') {  
                    sh """
                    echo "branch is"  ${gitBranch}          
                    """
                }
  }
                    stage('checkout scm') {
                        container('slave1') {
                               checkout scm
                            
 }
                    }
                    
       
        stage('Build image') {
            container('slave1') {
                sh """
                docker build -t gcr.io/sentrifugo/${APP_NAME}-${tag}:$BUILD_NUMBER .
                """
                
  
}
}

stage('Push image') {
    container('slave1') {
  docker.withRegistry('https://gcr.io', 'gcr:sentrifugo') {
      sh "docker push gcr.io/sentrifugo/${APP_NAME}-${tag}:$BUILD_NUMBER"
    
    
  }
    }
}

                }
            }