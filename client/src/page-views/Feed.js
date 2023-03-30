import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import apiURL from "../api";
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

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

    const responsive = {
        superLargeDesktop: {
            // the naming can be any, depends on you.
            breakpoint: { max: 4000, min: 3000 },
            items: 5
        },
        desktop: {
            breakpoint: { max: 3000, min: 1024 },
            items: 3
        },
        tablet: {
            breakpoint: { max: 1024, min: 464 },
            items: 2
        },
        mobile: {
            breakpoint: { max: 464, min: 0 },
            items: 1
        }
    };

    function sections(name) {
        <Carousel responsive={responsive}>
            <div>Item 1</div>
            <div>Item 2</div>
            <div>Item 3</div>
            <div>Item 4</div>
        </Carousel>;
    }

    return (<div className="feed">
        <header className="feed-header">
            <Link to="/" className="logo">Movies</Link>
        </header>
        <div className="feed-body">

        </div>
    </div>
    )
}

export default Feed