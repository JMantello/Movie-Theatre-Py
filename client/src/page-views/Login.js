import { Link } from "react-router-dom"
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'


function Login() {
    return (
        <div className="login">
            <header className="login-header">
                <Link to="/" className="logo">Movies</Link>
            </header>
            <main className="login-body">
                <div className="login-form-wrapper">
                    <h1>Log in</h1>
                    <Form className="rounded p-4 p-sm-3">
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
    );
}

export default Login;
