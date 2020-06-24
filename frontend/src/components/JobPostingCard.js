import React from 'react';
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';
import moment from 'moment';
import './JobPostingCard.css';

const JobPostingCard = (props) => {
    const job = props.job;
    const date = moment(job.date).format("M/D/YY");
    const location = (job.city ? job.city : "") + (job.state ? ", " + job.state : "");

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
                <Card.Text>{location ? "Location: " + location : ""}</Card.Text>
            </Card.Body>
            <Card.Footer>
                <Card.Link target="_blank" rel="noopener noreferrer" href={job.link}>Link</Card.Link>
            </Card.Footer>
        </Card>
    );
}

export default JobPostingCard;