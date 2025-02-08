function createToast(message, status){
    var toast = document.createElement('div');
    toast.classList.add('position-fixed');
    //toast.classList.add('top-0');
    toast.style.top = "56px"
    toast.classList.add('end-0','p-3')
    toast.style.zIndex = "10000";
    toast.style.maxWidth = "100vw"
    var bg_color = "bg-success"
    if (status == 300){
        bg_color = "bg-info"
    }else if(status != 200){
        bg_color = "bg-danger"
    }
    var toast_html = `
    <div id="liveToast" class="toast hide ${bg_color}" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header">
        <strong class="me-auto">SoftConnect</strong>
        <small>Now</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body text-light">
        ${message}
    </div>
    </div>
    `
    toast.innerHTML = toast_html
    document.getElementById("body").appendChild(toast)
    $("#liveToast").show()
    setTimeout(function(){
        toast.remove()
    },5500)

}