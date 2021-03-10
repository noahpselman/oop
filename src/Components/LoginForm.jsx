import React from 'react'

class LoginForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = { user_id: "", password: "" }
    }

    handleUsernameChange = (e) => {
        e.preventDefault();
        this.setState({user_id: e.target.value})
    }
    handlePasswordChange = (e) => {
        e.preventDefault();
        this.setState({password: e.target.value})
    }
    handleLoginSubmit = (e) => {

        e.preventDefault();
        console.log(`submitting ${this.state.user_id}`)
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({ user_id: this.state.user_id, password: this.state.password })
        };
        const url = '/auth'
        fetch(url, requestOptions)
            .then(res => res.json())
            .then(data => console.log(data))

        }
        // console.log("handle login submit called")
        // const url = `/user/auth?username=${this.state.username}&password=${this.state.password}`
        // fetch(url).then(res => res.json()).then(data => {
        //     console.log(data)
        // })


    render = () => {
        return (
            <div>
                <h1>Login</h1>
                <form onSubmit={this.handleLoginSubmit}>
                    <input onChange={this.handleUsernameChange} type="text" value={this.state.user_id} placeholder="user id"/>
                    <input onChange={this.handlePasswordChange} type="text" value={this.state.password} placeholder="password"/>
                    <button type="submit">Submit</button>
                </form>
            </div>
        )
    }
}

export default LoginForm