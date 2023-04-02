import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import Header from "../components/Header"
import LoadingSpinner from "../components/LoadingSpinner"
import Button from "react-bootstrap/Button"
import apiURL from "../api";


function ContentDetails(props) {
    const { id } = useParams();
    const { session } = props;
    const [content, setContent] = useState({});

    async function fetchContent() {
        try {
            const response = await fetch(`${apiURL}/content?token=${session.token}&content_id=${id}`);
            const responseData = await response.json();
            setContent(responseData);
        } catch (err) {
            console.log("Error with fetching content", err);
        }
    }

    async function watch() {
        try {
            const response = await fetch(`${apiURL}/watch?token=${session.token}&content_id=${id}`);
            const responseData = await response.json();
            alert(`You are watching ${content.title}`)
        } catch (err) {
            console.log("Error with fetching content", err);
        }
    }

    useEffect(() => {
        fetchContent();
    }, []);

    return (<div className="content-details">
        <Header />
        {!content ? (
            <LoadingSpinner />
        ) : (
            <div className="content-details-body">
                <div className="content-details-body-left">
                    <img src={content.image_url} alt={content.title} />
                </div>
                <div className="content-details-body-right">
                    <h1>{content.title}</h1>
                    <p>{content.description}</p>
                    <Button variant="primary" onClick={watch}>Watch Now</Button>
                </div>
            </div>
        )}
    </div>);
}

export default ContentDetails;