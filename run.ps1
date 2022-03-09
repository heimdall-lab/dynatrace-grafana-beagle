$CURRENT = $env:PWD
$VERSION = Get-Date -Format "MMddHHmmss"
write-host $VERSION
write-host $CURRENT

python ./prepare.py

nerdctl build -f Dockerfile --namespace k8s.io -t dynatrace-problems-reader:$VERSION  .
nerdctl tag --namespace k8s.io dynatrace-problems-reader:$VERSION dynatrace-problems-reader:latest
nerdctl build -f Grafana.Dockerfile --namespace k8s.io -t dynatrace-problems-grafana:$VERSION .
nerdctl tag --namespace k8s.io dynatrace-problems-grafana:$VERSION dynatrace-problems-grafana:latest

((Get-Content -path template.yaml -Raw) -replace '{{pwd}}', $CURRENT -replace '{{version}}', $VERSION)  | Set-Content -Path infrastructure.yaml

kubectl delete namespace beagle

kubectl apply -f ./infrastructure.yaml

kubectl get pods -n beagle  

#kubectl logs -l app=agent -n beagle
