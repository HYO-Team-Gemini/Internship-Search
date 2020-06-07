import React from 'react';
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';
import moment from 'moment';
import './JobPosting.css';

const JobPosting = (props) => {
    const job = props.job;
    // const date = moment(job.date.toString()).fromNow();
    const date = moment(job.date.toString()).format("M/D/YY");

    return (
        <Card className="job-posting">
            <Card.Body>
                <Card.Title className="row">
                    <div className="col-md-8">
                        {job.name}
                    </div>
                    <div className="col-md-4">
                        <Badge variant="secondary" className="date-badge">{date}</Badge>
                    </div>
                </Card.Title>
                <Card.Subtitle className="mb-2 text-muted">{job.employer}</Card.Subtitle>
                <Card.Text>{job.description ? job.description : "No Description"}</Card.Text>
                <Card.Link href={job.link}>Link</Card.Link>
                <Card.Link href="">More Information</Card.Link>
            </Card.Body>
        </Card>
    );
}

export default JobPosting;