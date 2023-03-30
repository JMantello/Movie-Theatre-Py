import './App.css';
import { Route, Routes } from "react-router-dom"
import { useState } from "react"
import Login from './page-views/Login'
import Feed from './page-views/Feed'

function App() {
  const [session, setSession] = useState({})

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login setSession={setSession} />} />
        <Route path="/login" element={<Login setSession={setSession} />} />
        <Route path="/feed" element={<Feed session={session} />} />
        <Route path="/*" element={<h1>Not Found</h1>} />

      </Routes>
    </div>
  );
}

export default App;
