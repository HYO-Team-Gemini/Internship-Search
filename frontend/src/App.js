import React, { useState, useEffect } from 'react';
import axios from 'axios';
import values from 'lodash/values';
import JobPosting from './components/JobPosting.js';
import { Container, Col, Form, Button, Alert, Pagination } from 'react-bootstrap';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [name, setName] = useState("");
  const [employer, setEmployer] = useState("");
  const [postAge, setPostAge] = useState("");
  const [distance, setDistance] = useState("");
  const [displayMessage, setDisplayMessage] = useState("");
  const [currentPage, setCurrentPage] = useState(0);

  let pages = [];
  for (let i = 1; i <= 5; i++) {
    pages.push(
      <Pagination.Item key={i} active={ currentPage === i } onClick={() => getPage(i)}>{i}</Pagination.Item>
    );
  }

  const url = "https://gemini-jobs.herokuapp.com";

  const getData = (pageNumber) => {
    const query = {
      name: name.toLowerCase(),
      employer: employer.toLowerCase(),
      post_age: postAge ? postAge : 0,
      distance: distance ? distance : 0,
      page: pageNumber
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
          setJobs([]);
          setDisplayMessage("No Results Found");
        }
      })
      .catch(error => {
        setJobs([]);
        console.log(error);
        setDisplayMessage("Error Retrieving Results")
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const pageNumber = 1;
    getData(pageNumber);
  };

  const getPage = (pageNumber) => {
    getData(pageNumber);
    setCurrentPage(pageNumber);
  };

  return (
    <div className="App">
      <Container fluid className="search-bar">
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
            <Form.Group as={Col} xs="auto" className="d-flex flex-column justify-content-end">
              <Button type="submit" value="Submit">Search</Button>
            </Form.Group>
          </Form.Row>
        </Form>
      </Container>
      <Container fluid className="job-results">
        { displayMessage && <Alert variant="secondary" className="display-message">{displayMessage}</Alert>}
        { jobs.length > 0 &&
            <div className="jobs-grid">
              {jobs.map((job, i) => <div className="col"><JobPosting key={i} job={job} /></div>)}
            </div>
        }
        { jobs.length > 0 &&
            <Pagination className="pages-element">
              <Pagination.First />
              <Pagination.Prev />
              {pages}
              <Pagination.Next />
              <Pagination.Last />
            </Pagination>
        }
      </Container>
    </div>
  );
}

export default App;
