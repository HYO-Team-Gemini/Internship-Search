import React from 'react';
import JobPosting from './components/JobPosting.js';
import './App.css';

function App() {
  const job = {
    name: "Software Engineering Intern",
    employer: "Exxon Mobil",
    description: "Working as an intern for the summer of 2020",
    date: 20200425,
    link: "https://exxonmobil.com",
  };

  const jobsArray = {
    "num_jobs": 12,
    "jobs": [
        {
          "name": "Software Engineer",
          "location": [45.123, 47.232],
          "employer": "Cisco",
          "date": 20200405,
          "link": "https://google.com"
        },
        {
          "name": "Systems Architect",
          "location": [70.123, 47.232],
          "employer": "Cisco",
          "date": 20200410,
          "link": "https://google.com"
        },
        job, job, job, job, job, job, job, job, job, job
    ]
  };

  return (
    <div className="App">
      <div className="jobs-grid">
        {jobsArray.jobs.map((job, i) => <div className="col"><JobPosting key={i} job={job} /></div>)}
      </div>
    </div>
  );
}

export default App;
