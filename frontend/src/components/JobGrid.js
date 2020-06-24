import React from 'react';
import JobPostingCard from './JobPostingCard.js';
import CardDeck from 'react-bootstrap/CardDeck';
import './JobGrid.css';

const JobGrid = (props) => {
    const jobs = props.jobs;

    return (
        <CardDeck className="jobs-grid">
            {jobs.map((job, i) => <JobPostingCard key={i} job={job} />)}
        </CardDeck>
    );
}

export default JobGrid;