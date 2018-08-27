# Shoeby sales and stocks - Dashboard

The dashboard is made with plotly's dash within a docker container.

To build the docker: <br>
```docker build -t dash-plotly --build-arg USER_ID=(id -u) .```

To run the app: <br>
```docker run -d --name shoeby-dashboard -v (echo $PWD)/data:/home/patrick/project/data --network=host -p 8050:8050 dash-plotly```

The dashboard is available at [http://localhost:8050/](http://localhost:8050/)

