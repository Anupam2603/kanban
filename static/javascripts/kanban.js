function validate1(event){
    title =  document.getElementById("title").value; 
    characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '<', '>', '~', '`']
    for (var i=0; i < title.length; i++){
        if (characters.includes(title[i])) {
            event.preventDefault();
            alert ("You can't use special characters in title name except '_'.");
            return false;
        }
    }   
    description = document.getElementById("description").value;
    if (description.length > 50) {
        event.preventDefault();
        alert("The charcter length of the description should be less than equal to 50")
        return false;
    }
    return true;
    
}
function validate2(event){
    title =  document.getElementById("title").value; 
    characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '<', '>', '~', '`']
    for (var i=0; i < title.length; i++){
        if (characters.includes(title[i])) {
            event.preventDefault();
            alert ("You can't use special characters in taskname except '_'.");
            return false;
        }
    }   
    content = document.getElementById("content").value;
    if (content.length > 50) {
        event.preventDefault();
        alert("The charcter length of the content should be less than equal to 50")
        return false;
    }
    deadline = document.getElementById("deadline").value;
    var date = new Date();
    var dd = String(date.getDate()).padStart(2,'0');
    var mm = String(date.getMonth() + 1).padStart(2,'0');
    var yyyy = String(date.getFullYear());
    var today = yyyy + '-' + mm + '-' + dd;
    if (deadline < today){
        event.preventDefault();
        alert("Please enter a future date")
        return false;
    }

    var completion = document.getElementById('completion');
    if (completion.checked) {
        event.preventDefault();
        alert("You can't check at the creation time")
        return false;
    }
    return true;
}

function check(event){
    var checkbox = document.getElementById("customSwitch1")
    if (checkbox.checked == true){
        alert("You can't check at creation time of task.")
        event.preventDefault();
        return false;
    }
    return true;
}
function validate3(event){
    title =  document.getElementById("title").value; 
    characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '<', '>', '~', '`']
    for (var i=0; i < title.length; i++){
        if (characters.includes(title[i])) {
            event.preventDefault();
            alert ("You can't use special characters in title name except '_'.");
            return false;
        }
    }
    return true;
}

function validate4(event){
    title =  document.getElementById("title").value; 
    characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '<', '>', '~', '`']
    for (var i=0; i < title.length; i++){
        if (characters.includes(title[i])) {
            event.preventDefault();
            alert ("You can't use special characters in taskname except '_'.");
            return false;
        }
    }   
    content = document.getElementById("content").value;
    if (content.length > 50) {
        event.preventDefault();
        alert("The charcter length of the content should be less than equal to 50")
        return false;
    }
    return true;
}

function validateuser(event){
    var username = document.getElementById('username').value
    valid_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    for (let i=0; i < username.length; i++){
        if (!valid_string.includes(username[i])){
            event.preventDefault()
            alert("Please use only alphanumeric characters.")
            return false;
        }
    }
    return true;
}