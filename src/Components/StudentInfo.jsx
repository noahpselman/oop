import React, { Component } from "react";

class StudentInfo extends Component {
  render() {
    const { entityData } = this.props;

    return (
      <div>
        <div id="user-data" className="section">
          <div className="user-data-element">
            <p>
              <strong>Name:</strong> {entityData.user_data.full_name}
            </p>
          </div>
          <div className="user-data-element">
            <p>
              <strong>ID:</strong> {entityData.user_data.id}
            </p>
          </div>
        </div>
      </div>
    );
  }
}

export default StudentInfo;
