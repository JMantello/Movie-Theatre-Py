import { useState, useEffect } from "react"
import Header from "../components/Header"
import LoadingSpinner from "../components/LoadingSpinner"
import { Link } from "react-router-dom"
import Button from "react-bootstrap/Button"
import apiURL from "../api";
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

function Feed(props) {
    const { session } = props
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

    const featuredResponsive = {
        screen: {
            breakpoint: { max: 6000, min: 0 },
            items: 1
        }
    };

    function thumbnail(content) {
        return <div className="content-thumbnail">
            <Link to={{
                pathname: `/content/${content.id}`,
            }}>
                <img src={content.image_url} alt={content.title} />
            </Link>
        </div>
    }

    function categoryCarousel(genre) {
        const content = feed.filter(c => c.genre === genre);

        return (
            <section className="genre-section mb-3">
                <h2 className="mb-3">{genre}</h2>
                <Carousel
                    responsive={responsive}
                    swipeable={true}
                    keyBoardControl={true}
                >
                    {content.map(c => (thumbnail(c)))}
                </Carousel>
            </section>);
    }

    function featuredContent() {
        let content = []

        for (let i = 0; i < 5; i++) {
            let item = (
                <div className="featured-content-item">
                    <div className="featured-content-body">
                        <div className="featured-content-body-left">
                            <img src={feed[i].image_url} alt={feed[i].title} />
                        </div>
                        <div className="featured-content-body-right">
                            <h1>{feed[i].title}</h1>
                            <p>{feed[i].description}</p>
                            <Link to={`/content/${feed[i].id}`}>
                                <Button variant="primary">Watch Now</Button>
                            </Link>
                        </div>
                    </div>
                </div>
            )
            content.push(item)
        }

        return content;
    }

    return (<div className="feed">
        <Header />
        {feed.length === 0 || genres.length === 0 ? (
            <LoadingSpinner />
        ) : (
            <div className="feed-body">
                <h2 className="mt-5 p-1">Featured Content</h2>
                <Carousel
                    responsive={featuredResponsive}
                    infinite={true}
                    autoPlay={true}
                    autoPlaySpeed={8000}
                >
                    {featuredContent()}
                </Carousel>
                {genres.map(g => (categoryCarousel(g)))}
                <br />
            </div>
        )}
    </div>
    )
}

export default Feed