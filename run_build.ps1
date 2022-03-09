nerdctl image rm --namespace k8s.io dynatrace-problems-reader:latest
nerdctl build -f Dockerfile --namespace k8s.io -t dynatrace-problems-reader:latest .
nerdctl build -f Grafana.Dockerfile --namespace k8s.io -t dynatrace-problems-grafana:latest .
nerdctl run dynatrace-problems-reader:latest --namespace k8s.io -p 5000:5000 

