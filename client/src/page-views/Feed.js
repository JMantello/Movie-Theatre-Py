import { Link } from "react-router-dom"

function Feed(props) {
    const { token } = props

    return (
        <header className="feed-header">
            <Link to="/" className="logo">Movies</Link>
        </header>
    )
}

export default Feed