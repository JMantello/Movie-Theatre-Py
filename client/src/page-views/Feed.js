import { Link } from "react-router-dom"

function Feed(props) {
    const { token } = props

    return (<div className="feed">
        <header className="feed-header">
            <Link to="/" className="logo">Movies</Link>
        </header>
        <p>Your Feed</p>
    </div>
    )
}

export default Feed