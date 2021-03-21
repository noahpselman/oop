import React, { Component } from "react";

class Restrictions extends Component {
  state = {};
  render() {
    let restriction = this.props.restrictions.map((restriction) => {
      return (
        <div>
          <p>{restriction}</p>
        </div>
      );
    });
    return (
      <div className="section">
        <p className="restrictions-heading section-header">Restrictions</p>
        {restriction}
      </div>
    );
  }
}

export default Restrictions;
