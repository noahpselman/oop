import React, { Component } from "react";

class Popup extends Component {
  state = {};
  render() {
    return (
      <div className="popup-surrounder">
        <div className="popup">
          <div className="popup-header">
            <p>{this.props.popupHeading}</p>
          </div>
          <div className="popup-body">
            <div>{this.props.children}</div>
            <div className="popup-button-holder">
              <div className="close-button" onClick={this.props.onClose}>
                Close
              </div>
              {this.props.popupButton}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Popup;
