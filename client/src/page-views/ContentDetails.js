import { useState, useEffect } from "react"
import { useLocation } from "react-router-dom"
import { Link } from "react-router-dom"
import { Button, Spinner } from "react-bootstrap"
import apiURL from "../api";


function ContentDetails() {
    const [session, setSession] = useState({
        user_id: 1,
        token: "bc5e7618-c791-4552-8d07-79f100dda864",
        content_id: 1
    })
    const [content, setContent] = useState({});
    // console.log(location);

    async function fetchContent() {
        try {
            const response = await fetch(`${apiURL}/content?token=${session.token}&content_id=${session.content_id}`);
            const responseData = await response.json();
            setContent(responseData);
        } catch (err) {
            console.log("Error with fetching content", err);
        }
    }

    useEffect(() => {
        fetchContent();
    }, []);

    return (<div className="content-details">
        <div className="content-details-header">
            <Link to="/feed" className="logo">Movies</Link>
        </div>
        {!content ? (
            <div className="loading-spinner">
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            </div>
        ) : (
            <div className="content-details-body">
                <div className="content-details-body-left">
                    <img src={content.image_url} alt={content.title} />
                </div>
                <div className="content-details-body-right">
                    <h1>{content.title}</h1>
                    <p>{content.description}</p>
                    <Button variant="primary">Watch Now</Button>
                </div>
            </div>
        )}
    </div>);
}

export default ContentDetails;