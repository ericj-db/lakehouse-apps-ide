import React, {useRef} from 'react';
import {useEffect, useState} from "react"
import MUIDataTable from "mui-datatables"
import PlayCircleIcon from '@mui/icons-material/PlayCircle';
import StopCircleIcon from '@mui/icons-material/StopCircle';
import logo from './logo.svg';
import './App.css';
import {IconButton} from "@mui/material";

declare global {
  interface Window { env: any; }
}

const clusterId: string = window.env.REACT_APP_CLUSTER_ID || ""

function updateClusterState(setClusters: any, start: boolean) {
  let api = start ? "/api/2.0/clusters/start" : "/api/2.0/clusters/delete"
  fetch(api,
    {
      method: 'POST',
      headers: {
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        cluster_id: clusterId
      })
    }
  )
    .then(response => {

    })
    .finally(() => {
      fetchClusters(setClusters)
    })
}

function fetchClusters(setClusters: any) {
  fetch(`/api/2.0/clusters/get?cluster_id=${clusterId}`,
    {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
    .then(response => {
      console.log("response: " + response)
      return response.json()
    })
    .then((data: any) => {
      console.log("data: " + data)
      setClusters([[
        data["state"],
        data["state"],
        data["cluster_name"],
        data["cluster_id"],
        data["node_type_id"],
        data["spark_version"],
        data["creator_user_name"]
      ]])
    })
    .catch(err => {
      console.log(err)
    })
}

function App() {
  console.log("Cluster id: " + clusterId)
  const [clusters, setClusters] = useState<any>([])
  const timeoutIdRef: any = useRef(null)

  useEffect(() => {
    fetchClusters(setClusters)
    timeoutIdRef.current = setInterval(() => fetchClusters(setClusters), 10000);
  }, []);

  const options = {
    download: false,
    print: false,
    filter: false,
    selectableRowsHideCheckboxes: true
  }

  const columns = [
    {
      name: "Start/Stop",
      options: {
        filter: false,
        customBodyRender: (value: any, tableMeta: any, updateValue: any) => {
          if (value === "PENDING" || value === "RUNNING") {
            return (
              <IconButton aria-label="delete" size="large" onClick={() => updateClusterState(setClusters, false)}>
                <StopCircleIcon style={{fill: "red"}}/>
              </IconButton>
            );
          } else {
            return (
              <IconButton aria-label="start" size="large" onClick={() => updateClusterState(setClusters, true)}>
                <PlayCircleIcon style={{fill: "green"}}/>
              </IconButton>
            );
          }
        }
      }
    },
    "State",
    "Cluster Name",
    "Cluster ID",
    "Node Type",
    "Spark Version",
    "Creator"];

  return (
    <div className="App">
      <h1>🏖️🏠 Cluster App</h1>
      <MUIDataTable
        title={"Your Spark Cluster"}
        data={clusters}
        columns={columns}
        options={options}
      />
      <img src={logo} className="App-logo" alt="logo" />
    </div>
  );
}

export default App;
