import React, { Component } from "react";

class PopupContent extends Component {
  render() {
    return (
      <div>
        <div className="popup-content">
          <ul>{this.props.popupContent}</ul>
        </div>
        <div className="popup-search-holder">
          {this.props.popupSearchResultContent}
        </div>
      </div>
    );
  }
}

export default PopupContent;
