import React from 'react';
import Table from 'react-bootstrap/Table';
import moment from 'moment';
import './JobTable.css';

const JobTable = (props) => {
    const jobs = props.jobs;

    const jobRows = jobs.map((job, i) => {
        const date = moment(job.date).format("M/D/YY");
        const location = (job.city ? job.city : "") + (job.state ? ", " + job.state : "");

        return (
            <tr key={i}>
                <td>{job.name}</td>
                <td>{job.employer}</td>
                <td>{location}</td>
                <td>{date}</td>
                <td><a class="external" href={job.link} target="_blank">Go</a></td>
            </tr>
        )
    });

    return (
        <Table striped bordered hover variant="dark">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Company</th>
                    <th>Location</th>
                    <th>Date</th>
                    <th>Link</th>
                </tr>
            </thead>
            <tbody>{jobRows}</tbody>
        </Table>
    );
}

export default JobTable;