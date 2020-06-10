import React, { useState, useEffect } from 'react';
import axios from 'axios';
import values from 'lodash/values';
import JobPosting from './components/JobPosting.js';
import { Container, Col, Form, Button, Alert } from 'react-bootstrap';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [name, setName] = useState("");
  const [employer, setEmployer] = useState("");
  const [postAge, setPostAge] = useState("");
  const [distance, setDistance] = useState("");
  const [displayMessage, setDisplayMessage] = useState("");

  const url = "http://127.0.0.1:5000";

  // React effect hook for getting all jobs - does not use any values from component scope
  // useEffect(() => {
  //   const getData = () => {
  //     axios.get(url + "/jobs").then(response => {
  //       setJobs(values(response.data.jobs));
  //     });
  //   };

  //   getData();
  // }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    const query = {
      name: name.toLowerCase(),
      employer: employer.toLowerCase(),
      post_age: postAge ? postAge : 0,
      distance: distance ? distance : 0
    };

    console.log(query);

    axios.get(url + "/jobs", { params: query })
      .then(response => {
        const jobResults = values(response.data.jobs);
        if (jobResults.length > 0) {
          setJobs(jobResults);
          setDisplayMessage("");
        }
        else {
          setDisplayMessage("No Results Found");
        }
      })
      .catch(error => {
        console.log(error);
        setDisplayMessage("Error Retrieving Results")
      });
  };

  return (
    <div className="App">
      <Container fluid>
        <Form className="search-form" onSubmit={handleSubmit}>
          <Form.Row>
            <Form.Group as={Col}>
              <Form.Label>Keywords</Form.Label>
              <Form.Control type="text" value={name} onChange={e => setName(e.target.value)}
                            placeholder="Search by title or skill" />
            </Form.Group>
            <Form.Group as={Col}>
                <Form.Label>Employer</Form.Label>
                <Form.Control type="text" value={employer} onChange={e => setEmployer(e.target.value)}
                              placeholder="Example: Google" />
            </Form.Group>
            <Form.Group as={Col}>
              <Form.Label>Post Age (in days)</Form.Label>
              <Form.Control type="number" value={postAge} onChange={e => setPostAge(e.target.value)}
                            placeholder="Example: 4 days ago" />
            </Form.Group>
            <Form.Group as={Col}>
              <Form.Label>Distance (radius)</Form.Label>
              <Form.Control type="number" value={distance} onChange={e => setDistance(e.target.value)}
                            placeholder="Example: 15 miles" />
            </Form.Group>
            <Form.Group as={Col} xs="auto">
              <Button type="submit" value="Submit">Search</Button>
            </Form.Group>
          </Form.Row>
        </Form>
      </Container>
      <Container fluid>
        { displayMessage && <Alert variant="secondary">{displayMessage}</Alert>}
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
