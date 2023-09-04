import React, { Component } from "react";
import { Table } from "reactstrap";
import EventModal from "./EventModal";

import ConfirmRemovalModal from "./ConfirmRemovalModal";

class EventList extends Component {
  render() {
    const events = this.props.events;
    return (
      <Table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Author</th>
            <th>Event Name</th>
            <th>Venue</th>
            <th>Image</th>
            <th>Start Date</th>
            <th>Start Time</th>
            <th>End Date</th>
            <th>End Time</th>
            <th>Details</th>
            <th>Event Type</th>
            <th>Location</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Virtual Type</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!events || events.length <= 0 ? (
            <tr>
              <td colSpan="17" align="center">
                <b>Ops, no one here yet</b>
              </td>
            </tr>
          ) : (
            events.map(event => (
              <tr key={event.pk}>
                <td>{event.category}</td>
                <td>{event.author}</td>
                <td>{event.eventname}</td>
                <td>{event.eventvenue}</td>
                <td>{event.image}</td>
                <td>{event.startdate}</td>
                <td>{event.starttime}</td>
                <td>{event.enddate}</td>
                <td>{event.endtime}</td>
                <td>{event.details}</td>
                <td>{event.eventtype}</td>
                <td>{event.location}</td>
                <td>{event.latitude}</td>
                <td>{event.longitude}</td>
                <td>{event.virtual_type}</td>
                <td align="center">
                  <EventModal create={false} event={event} resetState={this.props.resetState} />
                </td>
                <td align="center">
                    <ConfirmRemovalModal pk={event.pk} resetState={this.props.resetState}/>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default EventList;