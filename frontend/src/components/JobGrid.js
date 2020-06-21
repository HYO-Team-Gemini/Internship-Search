import React from 'react';
import JobPosting from './JobPosting.js';
import './JobGrid.css';

const JobGrid = (props) => {
    const jobs = props.jobs;

    return (
        <div className="jobs-grid">
            {jobs.map((job, i) => <div className="col"><JobPosting key={i} job={job} /></div>)}
        </div>
    );
}

export default JobGrid;