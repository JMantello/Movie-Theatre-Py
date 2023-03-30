import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import apiURL from "../api";

function Feed(props) {
    const { session } = props
    const [feed, setFeed] = useState({})

    async function fetchFeed() {
        try {
            // POST feed reqeust
            const response = await fetch(`${apiURL}/feed`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "token": session.token })
            });
            setFeed(await response.json())

        } catch (err) {
            console.log("Error with posting request to feed", err)
        }
    }

    useEffect(() => {
        fetchFeed();
    }, [])

    return (<div className="feed">
        <header className="feed-header">
            <Link to="/" className="logo">Movies</Link>
        </header>
        <p>Your Feed</p>
    </div>
    )
}

export default Feed