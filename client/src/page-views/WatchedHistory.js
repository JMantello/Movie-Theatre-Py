import { useState, useEffect } from "react"
import Header from "../components/Header"
import LoadingSpinner from "../components/LoadingSpinner";
import { Link } from "react-router-dom"
import apiURL from "../api";


function WatchHistory(props) {
    const { session } = props;
    const [watchHistory, setWatchHistory] = useState([]);

    async function fetchWatchHistory() {
        try {
            const response = await fetch(`${apiURL}/watchHistory?token=${session.token}`);
            const responseData = await response.json();
            setWatchHistory(responseData);
        } catch (err) {
            console.log("Error with fetching watch history", err);
        }
    }

    useEffect(() => {
        fetchWatchHistory();
    }, []);

    function contentListItem(content) {
        return (<li key={content.id}>
            <Link to={`/content/${content.id}`} className="watch-history-list-item">
                <div className="content-item-left">
                    <img src={content.image_url} alt={content.title} />
                </div>
                <div className="content-item-right">
                    <h2>{content.title}</h2>
                    <p>{content.description}</p>
                </div>
            </Link>
        </li>)
    }

    function watchHistoryList() {
        return (<div className="watch-history-list-container">
            <ul className="watch-history-list">
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