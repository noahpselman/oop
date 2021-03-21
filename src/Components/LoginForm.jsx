import React from "react";

class LoginForm extends React.Component {
  constructor() {
    super();
    this.state = { userId: "", password: "" };
  }

  handleUsernameChange = (e) => {
    e.preventDefault();
    this.setState({ userId: e.target.value });
  };
  handlePasswordChange = (e) => {
    e.preventDefault();
    this.setState({ password: e.target.value });
  };

  render = () => {
    return (
      <div id="login">
        <p id="login-header">Login</p>
        <form
          onSubmit={(e) =>
            this.props.onSubmit(e, this.state.userId, this.state.password)
          }
        >
          <label for="userId">User ID</label>
          <input
            onChange={this.handleUsernameChange}
            type="text"
            value={this.state.user_id}
            name="userID"
            placeholder="user id"
          />
          <label for="password">Password</label>
          <input
            onChange={this.handlePasswordChange}
            type="text"
            value={this.state.password}
            name="password"
            placeholder="password"
          />
          <button id="login-submit" type="submit">
            Submit
          </button>
        </form>
      </div>
    );
  };
}

export default LoginForm;
