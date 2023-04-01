import { useState, useEffect } from "react"
import { useLocation } from "react-router-dom"
import Header from "../components/Header"
import { Link } from "react-router-dom"
import { Button, Spinner } from "react-bootstrap"
import apiURL from "../api";


function WatchHistory() {
    const [session, setSession] = useState({
        user_id: 1,
        token: "bc5e7618-c791-4552-8d07-79f100dda864",
    })
    const [watchHistory, setWatchHistory] = useState({});
    // console.log(location);

    async function fetchWatchHistory() {
        try {
            const response = await fetch(`${apiURL}/content?token=${session.token}`);
            const responseData = await response.json();
            setContent(responseData);
        } catch (err) {
            console.log("Error with fetching watch history", err);
        }
    }

    useEffect(() => {
        fetchWatchHistory();
    }, []);

    return (<div className="watch-history">
        <Header />
        {!watchHistory ? (
            <div className="loading-spinner">
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            </div>
        ) : (
            <div className="watch-history-body">
            </div>
        )}
    </div>);
}

export default WatchHistory;