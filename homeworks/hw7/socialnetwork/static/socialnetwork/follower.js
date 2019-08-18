// Sends a new request to update the to-do list
function getList() {
    console.log(window.date);

    $.ajax({
        url: "/socialnetwork/refresh-follower" + "?last_refresh=" + window.date.toISOString(),
        dataType : "json",
        success: updateList
    });

    // window.date = new Date();
}

function updateList(response) {
    // Removes the old to-do list items
    console.log(response);

    // Adds each new todo-list item to the list
    $(response).each(function() {
        if (this.model == "socialnetwork.comment") {
            console.log("comment");
            $("#id_comment_list_"+this.fields.post).append(
                "<li class='comment_text'><i>Comment by <a class='navlink' href=/socialnetwork/follower/" +
                this.fields.user + " id='id_comment_profile_" + this.pk + "'>" + this.fields.first + " " + 
                this.fields.last + "</a></i> - <span id='id_comment_text_" + this.pk + "'>" + 
                sanitize(this.fields.text) + "</span> -- <span id='id_comment_date_time_" +
                this.pk + "'><i>" + this.fields.time + "</i></span></li><br>"
            );
        } else {
            console.log("post");
            $("#id_post_list").prepend(
                "<div class='post_text'><i>Post by <a class='navlink' href=/socialnetwork/follower/" +
                this.fields.user + " id='id_post_profile_" + this.pk + "'>" + this.fields.first + " " + 
                this.fields.last + "</a></i> - <span id='id_post_text_" + this.pk + "'>" + 
                sanitize(this.fields.text) + "</span> -- <span id='id_post_date_time_" + this.pk + 
                "'><i>" + this.fields.time + "</i></span></div>" + "<ol id='id_comment_list_" + 
                this.pk + "'></ol>" + "<div class='comment_box'><label for='id_comment_text_input_" + 
                this.pk + "'>Comment:</label><input id='id_comment_text_input_" + this.pk + 
                "' type='text' name='newcomment'><button class='navlink' id='id_comment_button_" + 
                this.pk + "' onclick='addComment(" + this.pk + 
                ")'>Submit</button><span id='error' class='error'></span></div><br>"
            );
        }
    });

    window.date = new Date();
}

function addComment(id) {
    var commentTextElement = $("#id_comment_text_input_"+id);
    var commentTextValue   = commentTextElement.val();
    console.log(id);
    console.log(commentTextValue);

    // Clear input box and old error message (if any)
    commentTextElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment/"+id,
        type: "POST",
        data: "newcomment="+commentTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateList(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = getList;
window.date = new Date('2000-01-01T00:00:00');

// causes list to be re-fetched every 5 seconds
window.setInterval(getList, 5000);
