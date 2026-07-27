import { useState } from "react";

function Signup({ setShowLogin }) {

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
const [messageType, setMessageType] = useState("");
    const handleSignup = async () => {

    const response = await fetch("http://localhost:5000/signup", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name,
            email,
            password
        })
    });

    const data = await response.json();

    if (response.ok){

    setMessage(data.message);
    setMessageType("success");

}
else{

    setMessage(data.message);
    setMessageType("error");

}
};
    return (
        <div>

            <h2>Signup</h2>

            <input
                type="text"
                placeholder="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />

            <br /><br />

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
{
    message && (

        <p
            style={{
                color:
                    messageType === "success"
                        ? "green"
                        : "red"
            }}
        >
            {message}
        </p>

    )
}
          <button onClick={handleSignup}>
    Signup
</button>
<br /><br />

<p>
    Already have an account?
</p>

<button onClick={() => setShowLogin(true)}>
    Login
</button>

        </div>
    );
}

export default Signup;