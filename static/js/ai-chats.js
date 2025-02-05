$(document).ready(function(){
    $("#chat_form").submit(function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        console.log("FormData", formData);

        fetch("/chat/", {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server error occurred!");
            }
            return response.json();
        })
        .then(data => {
            const message = data.message;
            const status = data.status;
            const prompt = data.prompt;
            const responseText = data.response;
            
            alert("Response: " + responseText); // Corrected alert syntax
        })
        .catch(error => {
            alert("Error occurred: " + error.message); // Corrected error alert
        });
    });
});
