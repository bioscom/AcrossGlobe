import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import EventList from "./EventList";
import EventModal from "./EventModal";
import axios from "axios";
import { API_URL } from "../constants";

class Home extends Component {
  state = {
    events: []
  };

  componentDidMount() {
    this.resetState();
  }

  getEvents = () => {
    axios.get(API_URL).then(res => this.setState({ events: res.data }));
  };

  resetState = () => {
    this.getEvents();
  };

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Row>
          <Col>
            <EventList events={this.state.events} resetState={this.resetState} />
          </Col>
        </Row>
        <Row>
          <Col>
            <EventModal create={true} resetState={this.resetState} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Home;