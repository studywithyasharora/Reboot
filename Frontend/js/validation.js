$('input[type="tel"]').on('input', function () {
    this.value = this.value.replace(/[^0-9.]/g, '');
});

$.validator.addMethod("startWith789", function (value, element) {
    return this.optional(element) || /^[789]/.test(value);
}, "Please enter a valid telephone number starting with 7, 8, or 9");


$.validator.addMethod("pwcheck", function (value) {
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(value);
}, "Password should be at least 8 characters, include uppercase and lowercase letters, numbers, and special characters");

$("#registrationForm").validate({
    rules: {
        fullName: {
            required: true,
            minlength: 3,
            maxlength: 50
        },
        email: {
            required: true,
            email: true
        },
        mobileNumber: {
            digits: true,
            minlength: 10,
            maxlength: 10,
            required: true,
            startWith789: true,
        },
        password: {
            required: true,
            minlength: 8,
            maxlength: 128,
            pwcheck: true
        }
    },
    errorPlacement: function (error, element) {
        error.appendTo(element.parent().parent());
    },
    invalidHandler: function (event, validator) {
        event.preventDefault();
    },
    submitHandler: function (form) {
        userRegistration();
    },
    errorClass: "error",
    errorElement: "div",
    highlight: function (element, errorClass) {
        $(element).addClass("is-invalid");
    },
    unhighlight: function (element, errorClass) {
        $(element).removeClass("is-invalid");
    }
});



$("#loginForm").validate({
    rules: {
        email: {
            required: true,
            email: true
        },
        password: {
            required: true,
            minlength: 8,
            maxlength: 128
        }
    },
    messages: {
        email: {
            required: "Please enter your email",
            email: "Please enter a valid email"
        },
        password: {
            required: "Please enter your password",
            minlength: "Password must be at least 8 characters",
            maxlength: "Password must not exceed 128 characters"
        }
    },
    errorPlacement: function (error, element) {
        error.appendTo(element.parent().parent());
    },
    invalidHandler: function (event, validator) {
        event.preventDefault();
    },
    submitHandler: function (form) {
        userLogin();
    },
    errorClass: "error",
    errorElement: "div",
    highlight: function (element, errorClass) {
        $(element).addClass("is-invalid");
    },
    unhighlight: function (element, errorClass) {
        $(element).removeClass("is-invalid");
    }
});




