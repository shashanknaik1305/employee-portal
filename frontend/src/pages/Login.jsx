import { useState } from "react";

function Login({ setLoggedIn, setShowLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");

    const handleLogin = async () => {
        try {
            const response = await fetch("http://localhost:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Save token
                localStorage.setItem("access_token", data.access_token);
                
                // Show success feedback
                setMessage(data.message || "Login successful!");
                setMessageType("success");

                // Delay redirect slightly so user can read the success message
                setTimeout(() => {
                    setLoggedIn(true);
                }, 800);
            } else {
                // Server returned a 4xx or 5xx error
                setMessage(data.message || "Invalid credentials.");
                setMessageType("error");
            }
        } catch (error) {
            // Network failure or backend server offline
            setMessage("Unable to connect to the server.");
            setMessageType("error");
        }
    };

    return (
        <div>
            <h2>Login</h2>

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <br /><br />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <br /><br />

            {message && (
                <p style={{ color: messageType === "success" ? "green" : "red" }}>
                    {message}
                </p>
            )}

            <button onClick={handleLogin}>Login</button>
            <br /><br />

            <p>Don't have an account?</p>
            <button onClick={() => setShowLogin(false)}>Signup</button>
        </div>
    );
}

export default Login;