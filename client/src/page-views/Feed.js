import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import apiURL from "../api";
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

function Feed(props) {
    const { session } = props
    const [feed, setFeed] = useState({})
    const [genres, setGenres] = useState()

    async function fetchFeed() {
        try {
            // POST feed reqeust
            const response = await fetch(`${apiURL}/feed`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "token": "bc5e7618-c791-4552-8d07-79f100dda864" })
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

    function thumbnail(content) {
        return <div className="content-thumbnail">
            <img src={content.image_url} alt={content.title} />
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

    return (<div className="feed">
        <header className="feed-header">
            <Link to="/" className="logo">Movies</Link>
        </header>
        <div className="feed-body">
            {genres.map(g => (genreCarousel(g)))}
        </div>
    </div>
    )
}

export default Feed