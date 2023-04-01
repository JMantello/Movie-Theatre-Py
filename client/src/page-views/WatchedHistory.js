import { useState, useEffect } from "react"
import Header from "../components/Header"
import LoadingSpinner from "../components/LoadingSpinner";
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

    function contentListItem(content) {
        return (<li key={content.id}>
            <Link to={`/content?content_id=${content.id}`}>
                <img src={content.image_url} alt={content.title} />
                <h2>{content.title}</h2>
                <p>{content.description}</p>
            </Link>
        </li>)
    }

    function watchHistoryList() {
        return (<div className="watch-history-list">
            <ul>
                {watchHistory.map((content) => (
                    contentListItem(content)
                ))}
            </ul>
        </div>)
    }

    return (<div className="watch-history">
        <Header />
        {!watchHistory ? (
            <LoadingSpinner />
        ) : (
            <div className="watch-history-body">
                <h1>Watch History</h1>
                {watchHistoryList()}
            </div>
        )}
    </div >);
}

export default WatchHistory;