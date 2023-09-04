import React, { Component, Fragment } from "react";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import EventForm from "./EventForm";

class EventModal extends Component {
  state = {
    modal: false
  };

  toggle = () => {
    this.setState(previous => ({
      modal: !previous.modal
    }));
  };

  render() {
    const create = this.props.create;

    var title = "Editing Event";
    var button = <Button onClick={this.toggle}>Edit</Button>;
    if (create) {
      title = "Create New Event";

      button = (
        <Button color="primary" className="float-right" onClick={this.toggle} style={{ minWidth: "200px" }}>
          + Create New Event
        </Button>
      );
    }

    return (
      <Fragment>
        {button}
        <Modal isOpen={this.state.modal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>{title}</ModalHeader>
          <ModalBody>
            <EventForm resetState={this.props.resetState} toggle={this.toggle} event={this.props.event} />
          </ModalBody>
        </Modal>
      </Fragment>
    );
  }
}

export default EventModal;