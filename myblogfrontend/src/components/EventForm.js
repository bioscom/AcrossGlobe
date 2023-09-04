import React from "react";
import { Button, Form, FormGroup, Input, Label, Dropdown, Row, Col } from "reactstrap";
import axios from "axios";
import { API_URL } from "../constants";

// import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
// import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
// import { DatePicker } from "@mui/x-date-pickers/DatePicker";

class EventForm extends React.Component {
  state = {
    pk: 0,
    category: "", 
    author: "", 
    eventname: "", 
    eventvenue: "", 
    image: "", 
    startdate: "", 
    starttime: "", 
    enddate: "", 
    endtime: "", 
    details: "", 
    eventtype: "", 
    location: "", 
    latitude: "", 
    longitude: "", 
    virtual_type: "", 
  };

  componentDidMount() {
    if (this.props.event) {
      const { pk, category, author, eventname, eventvenue, image, startdate, starttime, enddate, endtime, details, eventtype, location, latitude, longitude, virtual_type } = this.props.event;
      this.setState({ pk, category, author, eventname, eventvenue, image, startdate, starttime, enddate, endtime, details, eventtype, location, latitude, longitude, virtual_type });
    }
  }

  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  createEvent = e => {
    e.preventDefault();
    axios.post(API_URL, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  editEvent = e => {
    e.preventDefault();
    axios.put(API_URL + this.state.pk, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  defaultIfEmpty = value => {
    return value === "" ? "" : value;
  };

  render() {
    return (
      <Form onSubmit={this.props.event ? this.editEvent : this.createEvent}>

        <FormGroup>
            <Row>
                <Col xs="3">
                    <Label for="image">Attach Image:</Label>
                </Col>
                <Col>
                    <Input type="file" name="image" onChange={this.onChange} value={this.defaultIfEmpty(this.state.image)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
            <Row>
                <Col xs="3">
                    <Label for="category">Category:</Label>
                </Col>
                <Col>
                    <Input type="text" name="category" onChange={this.onChange} value={this.defaultIfEmpty(this.state.category)} />

                </Col>
            </Row>
        </FormGroup>
       
        <FormGroup>
            <Row>
                <Col xs="3">
                    <Label for="author">Author:</Label>
                </Col>
                <Col>
                    <Input type="text" name="author" onChange={this.onChange} value={this.defaultIfEmpty(this.state.author)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
            <Row>
                <Col xs="3">
                    <Label for="eventname">Event Name:</Label>
                </Col>
                <Col>
                    <Input type="text" name="eventname" onChange={this.onChange} value={this.defaultIfEmpty(this.state.eventname)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
            <Row>
                <Col xs="3">
                    <Label for="eventvenue">Event Venue:</Label>
                </Col>
                <Col>
                    <Input type="text" name="eventvenue" onChange={this.onChange} value={this.defaultIfEmpty(this.state.eventvenue)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
            <Row>
                <Col>
                    <Label for="startdate">Start Date:</Label>
                </Col>
                <Col>
                    {/* <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DatePicker name="startdate" onChange={this.onChange} value={this.defaultIfEmpty(this.state.startdate)} />
                    </LocalizationProvider> */}
                    <Input type="text" name="startdate" onChange={this.onChange} value={this.defaultIfEmpty(this.state.startdate)} />
                </Col>
          
                <Col>
                    <Label for="starttime">Start Time:</Label>
                </Col>
                <Col>
                    <Input type="text" name="starttime" onChange={this.onChange} value={this.defaultIfEmpty(this.state.starttime)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
            <Row>
                <Col>
                    <Label for="enddate">End Date:</Label>
                </Col>
                <Col>
                    <Input type="text" name="enddate" onChange={this.onChange} value={this.defaultIfEmpty(this.state.enddate)} />
                </Col>
           
                <Col>
                    <Label for="endtime">End Time:</Label>
                </Col>
                <Col>
                    <Input type="text" name="endtime" onChange={this.onChange} value={this.defaultIfEmpty(this.state.endtime)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
            <Row>
                <Col xs="3">
                    <Label for="eventtype">Event Type:</Label>
                </Col>
                <Col>
                    <Input type="text" name="eventtype" onChange={this.onChange} value={this.defaultIfEmpty(this.state.eventtype)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
            <Row>
                <Col xs="3">
                    <Label for="location">Location:</Label>
                </Col>
                <Col>
                    <Input type="text" name="location" onChange={this.onChange} value={this.defaultIfEmpty(this.state.location)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
            <Row>
                <Col xs="3">
                    <Label for="virtual_type">Virtual Type:</Label>
                </Col>
                <Col>
                    <Input type="text" name="virtual_type" onChange={this.onChange} value={this.defaultIfEmpty(this.state.virtual_type)} />
                </Col>
            </Row>
        </FormGroup>

        <FormGroup>
          <Label for="details">Details:</Label>
          <Input type="textarea" name="details" onChange={this.onChange} value={this.defaultIfEmpty(this.state.details)} />
        </FormGroup>

        <Button>Submit</Button>
      </Form>
    );
  }
}

export default EventForm;