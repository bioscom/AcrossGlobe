import React, { Component } from "react";

class Header extends Component {
  render() {
    return (
        <>
            <div style={{ marginRight: "20px" }}>
                <img src="https://acrossglobe.com:8000/media/logo/acrossglobe.gif" height="45"  style={{ marginTop: "10px" }} />
                <hr />
            </div>
            <div className="text-center">
                <h1>Discover Events</h1>
            </div>
        </>
    );
  }
}

export default Header;