
import React from 'react'
import './App.css';
import LoginForm from './Components/LoginForm'

class App extends React.Component {
    constructor(props) {
        super(props)
        this.state = {}
        this.getMessage()
    }

    getMessage = () => {
        fetch('/api').then(res => res.json()).then(data => {
            (this.updateMessage(data.message));
        })
    }

    updateMessage = (messageValue) => {
        console.log(messageValue)
        this.setState({ message: messageValue })
    }

    render = () => {
        return (
            <div>
                <p>message is {this.state.message}</p>
                <LoginForm></LoginForm>
            </div>
        )

    }
}

// function App() {

//     const [message, setMessage] = useState(0);

//     useEffect(() => {
// fetch('/api').then(res => res.json()).then(data => {
//     setMessage(data.message);
// });
//     }, []);

//     return (
//         <div className="App">
//             <p>{message}</p>
//         </div>
//     );
// }

export default App;
