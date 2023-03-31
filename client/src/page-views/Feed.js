import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { Spinner } from "react-bootstrap"
import apiURL from "../api";
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

function Feed() {
    const [session, setSession] = useState({
        user_id: 1,
        token: "bc5e7618-c791-4552-8d07-79f100dda864"
    })
    const [feed, setFeed] = useState([])
    const [genres, setGenres] = useState([])

    async function fetchFeed() {
        try {
            // POST feed reqeust
            const response = await fetch(`${apiURL}/feed`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(session)
            });

            const responseData = await response.json()
            setFeed(responseData)

        } catch (err) {
            console.log("Error with posting request to feed", err)
        }
    }

    async function fetchGenres() {
        try {
            const response = await fetch(`${apiURL}/genre`)
            const responseData = await response.json()
            setGenres(responseData)

        } catch (err) {
            console.log("Error with fetching genres", err)
        }
    }

    useEffect(() => {
        fetchFeed();
        fetchGenres();
    }, [])


    const responsive = {
        superLargeDesktop: {
            // the naming can be any, depends on you.
            breakpoint: { max: 4000, min: 2000 },
            items: 6
        },
        desktop: {
            breakpoint: { max: 2000, min: 1024 },
            items: 4
        },
        tablet: {
            breakpoint: { max: 1024, min: 664 },
            items: 3
        },
        mobile: {
            breakpoint: { max: 664, min: 0 },
            items: 1
        }
    };

    function thumbnail(content) {
        return <div className="content-thumbnail">
            <Link to={{
                pathname: "/content",
                state: {
                    session: session,
                    contentId: content.id
                }
            }}>
                <img src={content.image_url} alt={content.title} />
            </Link>
        </div>
    }

    function genreCarousel(genre) {
        const content = feed.filter(c => c.genre === genre);

        return (
            <section className="genre-section mb-3">
                <h2 className="mb-3">{genre}</h2>
                <Carousel responsive={responsive}>
                    {content.map(c => (thumbnail(c)))}
                </Carousel>
            </section>);
    }

    if (feed.length === 0 || genres.length === 0) {
        return (
            <div className="feed">
                <header className="feed-header">
                    <Link to="/" className="logo">Movies</Link>
                </header>
                <div className="loading-spinner">
                    <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>
                </div>
            </div>
        )
    }

    return (<div className="feed">
        <header className="feed-header">
            <Link to="/feed" className="logo">Movies</Link>
        </header>
        <div className="feed-body">
            {genres.map(g => (genreCarousel(g)))}
        </div>
    </div>
    )
}

export default Feed