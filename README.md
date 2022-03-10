# dynatrace-problems

> this project show how integrate Grafana with Dynatrace problems api to improve visualizations

[![Publish Docker image](https://github.com/heimdall-lab/dynatrace-grafana-beagle/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/heimdall-lab/dynatrace-grafana-beagle/actions/workflows/pipeline.yaml)

## Prod 

> replace {{YOUR}} in cluster.yaml with your specific values 

*  kubectl apply -f cluster.yaml

## Develop

* use rancher desktop 
* install and configure python
* create a .env with env variables 
* execute run.ps1 to build and run local cluster 

![Alt text](sample.png?raw=true "Sample dashboard")

![Alt text](sample2.png?raw=true "Sample 2 dashboard")

![Alt text](sample3.png?raw=true "Sample 3 problems widget")

![Alt text](sample4.png?raw=true "Sample 4 association mining")
