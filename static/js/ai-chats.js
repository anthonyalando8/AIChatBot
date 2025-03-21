$(document).ready(function(){
    var converter = new showdown.Converter();

    var user_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/user.png?updatedAt=1682239876486"
    var softchat_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/cpu.png?updatedAt=1715174298728"
    var converted_to_html_user_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex m-2 align-items-center flex-row my-2"><div markdown="1">![your image](${user_avatar} =32x32 "You")</div><div markdown="1" class="mx-md-3 mx-2">**You**</div></div>`)
    var converted_to_html_softchat_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex m-2 align-items-center flex-row my-2"><div markdown="1">![soft connect logo](${softchat_avatar} =32x32 "SoftChatAI")</div><div markdown="1" class="mx-md-3 mx-2"> **SoftChatAI**</div></div>`)
    adjustChatContainer();
    
    $('#id_message').on('input', function() {
        var text = $(this).val().trim(); 
        if (text === '') {
            $('#btn-submit').addClass('disabled');
        } else {
            $('#btn-submit').removeClass('disabled');
        }
    });

    function adjustChatContainer() {
        $("#chat-container").addClass("w-75");
        $(window).resize(function(){
            var viewportWidth = $(window).width();
            if (viewportWidth < 800){
                $("#chat-container").removeClass("w-75");
                $("#chat-container").addClass("w-100");
            }else{
                $("#chat-container").removeClass("w-100");
                $("#chat-container").addClass("w-75");
            }
        });
        $(window).resize();
    }

    $("#chat_form").submit(function(event) {
        event.preventDefault();
        $('#btn-submit').addClass('disabled');
        var submitButton = $('#chat_form button[type="submit"]');
        submitButton.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        submitButton.attr("disabled","disabled");
        const formData = new FormData(this);
        console.log("FormData", formData);
        this.reset();
        fetch("/chat/", {
            method: 'POST',
            body: formData
        })
        .then(response => {
            $('#btn-submit').removeClass('disabled');
            submitButton.html('<i class="fa-solid fa-paper-plane"></i>');
            submitButton.removeAttr("disabled");
            $('#id_message').attr('placeholder','Enter message');
            $('#id_message').focus();
            if (!response.ok) {
                createToast("Server error occurred!", -1)
                throw new Error("Server error occurred!");
            }
            
            return response.json();
        })
        .then(data => {
            const message = data.message;
            const status = data.status;
            const prompt = data.prompt;
            const image = data.immage;
            const responseText = data.response;

            var htmlData = ""
            var chathistory = "new_chat"
            var image_html = ""
                
            if(image != null && image != ""){
                image_html = converter.makeHtml(`<div markdown="1" style="max-width: 500px; max-height: 500px" class="m-2 overflow-hidden">![Image](${image})</div>`)
            }
            // Convert Markdown to HTML
            var response_to_html = converter.makeHtml(responseText);
            var response_ai_name = converted_to_html_softchat_avatar_name+`<div class="ml-2 m-2" >${response_to_html}</div>`;
            var message_user_name = converted_to_html_user_avatar_name + `<div class="ml-2 m-2">${image_html}${prompt}</div>`;
            htmlData += (message_user_name+response_ai_name);
        

            $("#chat").append(htmlData)

            hljs.highlightAll()

            //scroll bottom
            var chat = document.getElementById("chat");
            chat.scrollTop = chat.scrollHeight;
        })
        .catch(error => {
            $('#btn-submit').removeClass('disabled');
            submitButton.html('<i class="fa-solid fa-paper-plane"></i>');
            submitButton.removeAttr("disabled")
            createToast("Error occurred: " + error.message, -1)
        });
    });
});
