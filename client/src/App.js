import './App.css';
import { Route, Routes } from "react-router-dom"
import { useState } from "react"
import Login from './page-views/Login'
import Feed from './page-views/Feed'
import ContentDetails from './page-views/ContentDetails'
import WatchHistory from './page-views/WatchedHistory';

function App() {
  const [session, setSession] = useState({
    user_id: 1,
    token: "bc5e7618-c791-4552-8d07-79f100dda864"
  })

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login setSession={setSession} />} />
        <Route path="/login" element={<Login setSession={setSession} />} />
        <Route path="/feed" element={<Feed session={session} />} />
        <Route path="/content/:id" element={<ContentDetails session={session} />} />
        <Route path="/watchHistory" element={<WatchHistory session={session} />} />
        <Route path="/*" element={<h1>Not Found</h1>} />
      </Routes>
    </div>
  );
}

export default App;
