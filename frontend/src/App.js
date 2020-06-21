import React, { useState } from 'react';
import axios from 'axios';
import values from 'lodash/values';
import JobGrid from './components/JobGrid.js';
import JobTable from './components/JobTable.js';
import { Container, Col, Form, Button, Alert, Pagination } from 'react-bootstrap';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [name, setName] = useState("");
  const [employer, setEmployer] = useState("");
  const [postAge, setPostAge] = useState("");
  const [distance, setDistance] = useState("");
  const [zipCode, setZipCode] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [displayMessage, setDisplayMessage] = useState("");
  const [currentPage, setCurrentPage] = useState(0);

  // 0 is table view, 1 is card view
  const [toggle, setToggle] = useState(0);

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
    setCurrentPage(pageNumber);
  };

  const getPage = (pageChange) => {
    const pageNumber = currentPage + pageChange;
    getData(pageNumber);
    setCurrentPage(pageNumber);
  };

  const handleToggleChange = () => {
    const newToggleValue = toggle === 0 ? 1 : 0;
    setToggle(newToggleValue);
  };

  return (
    <div className="App">
      <Container fluid className="search-bar">
        <Form className="search-form" onSubmit={handleSubmit}>
          <Form.Row>
            <Form.Group as={Col} lg={6}>
              <Form.Label>Keywords</Form.Label>
              <Form.Control type="text" value={name} onChange={e => setName(e.target.value)}
                            placeholder="Search by title or skill" />
            </Form.Group>
            <Form.Group as={Col} lg={6}>
                <Form.Label>Employer</Form.Label>
                <Form.Control type="text" value={employer} onChange={e => setEmployer(e.target.value)}
                              placeholder="Ex: Google" />
            </Form.Group>
            <Form.Group as={Col} lg={3}>
              <Form.Label>Post Age (days ago)</Form.Label>
              <Form.Control type="number" value={postAge} onChange={e => setPostAge(e.target.value)}
                            placeholder="Ex: 4 (days ago)" />
            </Form.Group>
            <Form.Group as={Col} lg={3}>
              <Form.Label>Distance (radius in miles)</Form.Label>
              <Form.Control type="number" value={distance} onChange={e => setDistance(e.target.value)}
                            placeholder="Ex: 15 (miles)" />
            </Form.Group>
            <Form.Group as={Col} lg={1}>
              <Form.Label>Zip Code</Form.Label>
              <Form.Control type="number" value={zipCode} onChange={e => setZipCode(e.target.value)}
                            placeholder="Ex: 73301" />
            </Form.Group>
            <Form.Group as={Col} lg={1}>
              <Form.Label>City</Form.Label>
              <Form.Control type="text" value={city} onChange={e => setCity(e.target.value)}
                            placeholder="Ex: Austin" />
            </Form.Group>
            <Form.Group as={Col} lg={1}>
              <Form.Label>State</Form.Label>
              <Form.Control type="text" value={state} onChange={e => setState(e.target.value)}
                            placeholder="Ex: Texas" />
            </Form.Group>
            <Form.Group as={Col} lg className="d-flex flex-column justify-content-end">
              <Button type="submit" value="Submit">Search</Button>
            </Form.Group>
          </Form.Row>
        </Form>
      </Container>
      <Container fluid className="job-results">
        { displayMessage && <Alert variant="secondary" className="display-message">{displayMessage}</Alert>}
        { jobs.length > 0 &&
          <div className="results-toggle-row">
            <div className="results-text">
              Results {(currentPage-1) * 50 + 1} - {(currentPage-1) * 50 + jobs.length}
            </div>
            <div className="custom-control custom-switch">
              <label className="toggle-label" id="left-toggle-label" htmlFor="toggle">
                Table View
              </label>
              <input
                type="checkbox"
                className="custom-control-input"
                id="toggle"
                checked={toggle}
                onChange={handleToggleChange}
                readOnly
              />
              <label className="custom-control-label toggle-label" id="right-toggle-label" htmlFor="toggle" >
                Card View
              </label>
            </div>
          </div>
        }
        { jobs.length > 0 && toggle === 0 && <JobTable jobs={jobs} /> }
        { jobs.length > 0 && toggle === 1 && <JobGrid jobs={jobs} /> }
        { jobs.length > 0 &&
            <div className="pagination-row">
              <Pagination className="pages-element prev-page">
                <Pagination.Prev className={currentPage === 1 ? "disabled" : ""} 
                                 onClick={() => { window.scrollTo({top: 0, behavior: "smooth"}); getPage(-1); }}/>
              </Pagination>
              <Pagination className="pages-element next-page">
                <Pagination.Next className={jobs.length < 50 ? "disabled" : ""} 
                                 onClick={() => { window.scrollTo({top: 0, behavior: "smooth"}); getPage(1); }}/>
              </Pagination>
            </div>
        }
      </Container>
    </div>
  );
}

export default App;
