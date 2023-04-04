import { Link, NavLink } from "react-router-dom"

function Header() {
    return (
        <header className="header">
            <nav>
                <Link to="/" className="logo">Movies</Link>
                <div className="nav-links">
                    <NavLink to="/feed" className="nav-link">Home</NavLink>
                    <NavLink to="/notFound" className="nav-link">TV Shows</NavLink>
                    <NavLink to="/notFound" className="nav-link">Movies</NavLink>
                    <NavLink to="/watchHistory" className="nav-link">Watch History</NavLink>
                    <NavLink to="/login" className="nav-link">Sign Out</NavLink>
                </div>
            </nav>
        </header>
    )
}

export default Header;