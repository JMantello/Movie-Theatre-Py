import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import apiURL from "../api";

function Login(props) {
    const { setSession } = props
    const [inputs, setInputs] = useState({
        email: "jman@email.com", password: "letmein"
    })

    const changeInput = (e) => {
        const name = e.target.name;
        const value = e.target.value;
        setInputs(values => ({ ...values, [name]: value }))
    }

    const navigate = useNavigate()
    const postLogin = async (event) => {
        event.preventDefault();

        const loginData = {
            email: inputs.email,
            password: inputs.password
        };

        try {
            // POST Login reqeust
            const response = await fetch(`${apiURL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(loginData)
            });

            // Get a session token from response
            const session = await response.json()
            setSession(session)
            navigate("/feed", { replace: true })

        } catch (err) {
            console.log("Error with posting login request", err)
        }
    }

    return (<>
        <div className="login-background-image"></div>
        <div className="login">
            <header className="login-header">
                <Link to="/login" className="logo">Movies</Link>
            </header>
            <main className="login-body">
                <div className="login-form-wrapper">
                    <h1>Log in</h1>
                    <Form className="rounded p-4 p-sm-3" onSubmit={postLogin}>
                        <Form.Group className="mb-3" controlId="login-form-email">
                            <Form.Label>Email Address</Form.Label>
                            <Form.Control
                                type="email"
                                name="email"
                                placeholder="Enter Email"
                                onChange={changeInput}
                                value={inputs.email || ""}
                            />
                            <Form.Text className="text-muted">We'll never share your email with anyone else.</Form.Text>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="login-form-password">
                            <Form.Label>Password</Form.Label>
                            <Form.Control
                                type="password"
                                name="password"
                                placeholder="Enter Password"
                                onChange={changeInput}
                                value={inputs.password || ""}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="login-form-remember-me-checkbox">
                            <Form.Check type="checkbox" label="Remember Me" />
                        </Form.Group>
                        <Button variant="primary" type="submit">Log In</Button>
                    </Form>
                </div>
            </main>
            <footer>
                <p className="text-muted">Questions? Call 1-855-555-2991</p>
            </footer>
        </div>
    </>
    );
}

export default Login;
