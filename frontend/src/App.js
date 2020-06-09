import React, { useState, useEffect } from 'react';
import axios from 'axios';
import values from 'lodash/values';
import JobPosting from './components/JobPosting.js';
import { Container, Col, Form, Button } from 'react-bootstrap';
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

  let search = {
    "location": [45.123, 47.232],
    "name": "developer",
    "industry": "tech",
    "posted_after": 20200404
  };

  return (
    <div className="App">
      <Container fluid>
        <Form className="search-form">
          <Form.Row>
            <Form.Group as={Col}>
              <Form.Label>Keywords</Form.Label>
              <Form.Control type="text" placeholder="Search by title or skill" />
            </Form.Group>
            <Form.Group as={Col}>
                <Form.Label>Employer</Form.Label>
                <Form.Control type="text" placeholder="Example: Google" />
            </Form.Group>
            <Form.Group as={Col}>
              <Form.Label>Date Posted</Form.Label>
              <Form.Control type="text" placeholder="Example: 4 days ago" />
            </Form.Group>
            <Form.Group as={Col}>
              <Form.Label>Distance (Radius)</Form.Label>
              <Form.Control type="text" placeholder="Example: 15 miles" />
            </Form.Group>
            <Form.Group as={Col} xs="auto">
              <Button type="submit" className="align-self-end">Search</Button>
            </Form.Group>
          </Form.Row>
        </Form>
      </Container>
      <Container fluid>
        { jobs.length > 0 &&
          <div className="jobs-grid">
            {jobs.map((job, i) => <div className="col"><JobPosting key={i} job={job} /></div>)}
          </div>
        }
      </Container>
    </div>
  );
}

export default App;
