var register = document.getElementById("register_frm");
var login = document.getElementById("login_frm");
var search = document.getElementById("search_frm");
var review = document.getElementById("review_frm");

if (login) {
    login.onsubmit = function() {
        if (!login.username.value)
        {
            alert("missing username");
            return false;
        }
        else if (!login.password.value)
        {
            alert("missing password");
            return false;
        }
        return true;
    }
    // alert invalid inputs
    if (not_user) {alert("username doesn't exist");}
    if (wrong_password) {alert("password is not correct");}
};

if (register) {
    register.onsubmit = function() {
        if (!register.username.value)
        {
            alert("missing username");
            return false;
        }
        else if (!register.email.value)
        {
            alert("missing email");
            return false;
        }
        else if (!register.password.value)
        {
            alert("missing password");
            return false;
        }
        else if (register.password.value != register.password2.value)
        {
            alert("passwords don't match");
            return false;
        }
        return true;
    }
    // alert invalid inputs
    if (username_repeated) {alert("username already exists!");}
    if (email_repeated) {alert("email already exists!");}
};

if (search) {
    search.onsubmit = function() {
        if (!search.q.value)
        {
            alert("search field is empty");
            return false;
        }
        return true;
    }
};

if (review) {
    review.onsubmit = function() {
        if (!review.opinion.value)
        {
            alert("Nothing to say about the book?");
            return false;
        }
        else if (!review.rating.value)
        {
            alert("No rating is provided");
            return false;
        }
        return true;
    }
};


