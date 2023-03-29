import { Link } from "react-router-dom"
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import apiURL from "../api";

function Login() {
    async function postLogin(e) {
        e.preventDefault();
        const formData = new FormData(e.target)
        const loginData = {
            email: formData.get("email"),
            password: formData.get("password")
        };
        try {
            const response = await fetch(`${apiURL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "applications/json"
                },
                body: JSON.stringify(loginData)
            });
            const responseData = await response.json();
            console.log(responseData)
        } catch (err) {
            console.log("Error with posting login request")
        }
    }

    return (<>
        <div className="login-background-image"></div>
        <div className="login">
            <header className="login-header">
                <Link to="/" className="logo">Movies</Link>
            </header>
            <main className="login-body">
                <div className="login-form-wrapper">
                    <h1>Log in</h1>
                    <Form className="rounded p-4 p-sm-3" onSubmit={postLogin}>
                        <Form.Group className="mb-3" controlId="login-form-email">
                            <Form.Label>Email Address</Form.Label>
                            <Form.Control type="email" placeholder="Enter Email" />
                            <Form.Text className="text-muted">We'll never share your email with anyone else.</Form.Text>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="login-form-password">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Enter Password" />
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="login-form-remember-me-checkbox">
                            <Form.Check type="checkbox" label="Remember Me" />
                        </Form.Group>
                        <Button variant="primary" type="submit">Log In</Button>
                    </Form>
                </div>
            </main>
        </div>
    </>
    );
}

export default Login;
