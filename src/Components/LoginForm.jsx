import React from 'react'

class LoginForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = { username: "", password: "" }
    }

    handleUsernameChange = (e) => {
        e.preventDefault();
        this.setState({username: e.target.value})
    }
    handlePasswordChange = (e) => {
        e.preventDefault();
        this.setState({password: e.target.value})
    }
    handleLoginSubmit = (e) => {

        e.preventDefault();
        console.log("handle login submit called")
        const url = `/user/auth?username=${this.state.username}&password=${this.state.password}`
        fetch(url).then(res => res.json()).then(data => {
            console.log(data)
        })
    }


    render = () => {
        return (
            <div>
                <h1>Login</h1>
                <form onSubmit={this.handleLoginSubmit}>
                    <input onChange={this.handleUsernameChange} type="text" value={this.state.username} placeholder="username"/>
                    <input onChange={this.handlePasswordChange} type="text" value={this.state.password} placeholder="password"/>
                    <button type="submit">Submit</button>
                </form>
            </div>
        )
    }
}

export default LoginForm