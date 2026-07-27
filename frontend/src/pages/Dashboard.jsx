import { useState } from "react";

function Dashboard({ setLoggedIn }) {

    const [photo, setPhoto] = useState(null);
    const [resume, setResume] = useState(null);

    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");

    const uploadPhoto = async () => {

        if (!photo) {
            setMessage("Please select a profile photo.");
            setMessageType("error");
            return;
        }

        const formData = new FormData();

        formData.append("photo", photo);

        const token = localStorage.getItem("access_token");

        const response = await fetch(
            "http://localhost:5000/upload/photo",
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`
                },
                body: formData
            }
        );

        const data = await response.json();

        if (response.ok) {

            setMessage(data.message);
            setMessageType("success");

        } else {

            setMessage(data.message);
            setMessageType("error");

        }

    };

    const uploadResume = async () => {

        if (!resume) {
            setMessage("Please select a resume.");
            setMessageType("error");
            return;
        }

        const formData = new FormData();

        formData.append("resume", resume);

        const token = localStorage.getItem("access_token");

        const response = await fetch(
            "http://localhost:5000/upload/resume",
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`
                },
                body: formData
            }
        );

        const data = await response.json();

        if (response.ok) {

            setMessage(data.message);
            setMessageType("success");

        } else {

            setMessage(data.message);
            setMessageType("error");

        }

    };

    const handleLogout = () => {

        localStorage.removeItem("access_token");

        setLoggedIn(false);

    };

    return (

        <div>

            <h1>Employee Dashboard</h1>

            <button onClick={handleLogout}>
                Logout
            </button>

            <hr />

            {
                message && (

                    <p
                        style={{
                            color: messageType === "success"
                                ? "green"
                                : "red",
                            fontWeight: "bold"
                        }}
                    >
                        {message}
                    </p>

                )
            }

            <h3>Upload Profile Photo</h3>

            <input
                type="file"
                accept=".png,.jpg,.jpeg"
                onChange={(e) => setPhoto(e.target.files[0])}
            />

            <br /><br />

            <button onClick={uploadPhoto}>
                Upload Photo
            </button>

            <hr />

            <h3>Upload Resume</h3>

            <input
                type="file"
                accept=".pdf"
                onChange={(e) => setResume(e.target.files[0])}
            />

            <br /><br />

            <button onClick={uploadResume}>
                Upload Resume
            </button>

        </div>

    );

}

export default Dashboard;