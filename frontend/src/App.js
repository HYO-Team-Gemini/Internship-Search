import React, { useState, useEffect } from 'react';
import axios from 'axios';
import values from 'lodash/values';
import JobPosting from './components/JobPosting.js';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const url = "http://127.0.0.1:5000";

  // React effect hook for getting all jobs - does not use any values from component scope
  useEffect(() => {
    const getData = () => {
      axios.get(url + "/jobs").then(response => {
        setJobs(values(response.data.jobs));
      });
    };
    
    getData();
  }, []);

  return (
    <div className="App">
      <div className="jobs-grid">
        {jobs.map((job, i) => <div className="col"><JobPosting key={i} job={job} /></div>)}
      </div>
    </div>
  );
}

export default App;
