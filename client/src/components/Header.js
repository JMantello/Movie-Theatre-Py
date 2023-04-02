import { Link, NavLink } from "react-router-dom"

function Header() {
    return (
        <header className="header">
            <Link to="/" className="logo">Movies</Link>
            <div className="nav-links">
                <NavLink to="/feed" className="nav-link">Home</NavLink>
                <NavLink to="/feed" className="nav-link">TV Shows</NavLink>
                <NavLink to="/feed" className="nav-link">Movies</NavLink>
                <NavLink to="/watchHistory" className="nav-link">Watch History</NavLink>
                <NavLink to="/feed" className="nav-link">Sign Out</NavLink>
            </div>
        </header>
    )
}

export default Header;