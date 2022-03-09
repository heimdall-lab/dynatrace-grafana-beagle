FROM grafana/grafana

COPY ./grafana/dashboards/provider.yaml /etc/grafana/provisioning/dashboards/provider.yaml
   
COPY ./grafana/datasources /etc/grafana/provisioning/datasources
   
COPY ./grafana/dashboards /etc/dashboards
