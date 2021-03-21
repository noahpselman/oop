import React, { Component } from "react";
import Button from "react-bootstrap/Button";

class NavBar extends Component {
  state = {};
  render() {
    return (
      <div className="navbar primary-color">
        <div className="nav-item ml-3">
          <p className="">Final Project University</p>
        </div>
        {this.renderButton()}
      </div>
    );
  }

  renderButton = () => {
    let result = <div></div>;
    if (this.props.loggedIn) {
      result = (
        <div className="nav-item">
          <div className="nav-button" onClick={this.props.onClick}>
            LogOut
          </div>
        </div>
      );
    }
    return result;
  };
}

export default NavBar;
