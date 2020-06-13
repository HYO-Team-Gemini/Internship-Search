import React from 'react';
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';
import moment from 'moment';
import './JobPosting.css';

const JobPosting = (props) => {
    const job = props.job;
    // const date = moment(job.date.toString()).fromNow();
    const date = moment(job.date.$date.toString(), "x").format("M/D/YY");
    let location = job.location.city ? job.location.city : "";
    location += job.location.country ? ", " + job.location.country : "";

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
                <Card.Text>{location ? location : ""}</Card.Text>
                <Card.Link href={job.link}>Link</Card.Link>
            </Card.Body>
        </Card>
    );
}

// <Card.Text>{job.description ? job.description : "No Description"}</Card.Text>

export default JobPosting;