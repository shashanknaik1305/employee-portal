import { useState } from "react";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";

function App() {

    const [loggedIn, setLoggedIn] = useState(
        !!localStorage.getItem("access_token")
    );

    const [showLogin, setShowLogin] = useState(true);

    if (loggedIn) {
        return <Dashboard setLoggedIn={setLoggedIn} />;
    }

    return (
        <>
            {
                showLogin
                    ? <Login
                        setLoggedIn={setLoggedIn}
                        setShowLogin={setShowLogin}
                    />
                    : <Signup
                        setShowLogin={setShowLogin}
                    />
            }
        </>
    );
}

export default App;