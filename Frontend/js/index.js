function togglePassword() {
  var passwordInput = document.getElementById("password");
  var eyeIcon = document.getElementById("eye-icon");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    eyeIcon.classList.remove("fa-eye");
    eyeIcon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    eyeIcon.classList.remove("fa-eye-slash");
    eyeIcon.classList.add("fa-eye");
  }
}

function displayMessage(message, duration) {
  $("#msg").html(message);
  $("#msg").delay(duration).fadeOut(1000);
}



function userRegistration() {

  let email = $("#email").val();
  let full_name = $("#fullName").val();
  let mobile_no = $("#mobileNumber").val();
  let password = $("#password").val();

  var settings = {
    url: "http://127.0.0.1:8000/registration/",
    method: "POST",
    timeout: 0,
    data: {
      email: email,
      full_name: full_name,
      mobile_no: mobile_no,
      password: password
    },
    statusCode: {
      404: function () {
        displayMessage("Something went wrong, Try again!", 5000);
      },
      400: function () {
        displayMessage("Invalid input! Check your details and try again.", 5000);
      },
    },
    error: function (xhr, status, error) {
      console.error("Error: ", error);
      displayMessage("Something went wrong. Please try again.", 5000);
    },
  };

  $.ajax(settings)
    .done(function (json) {
      try {
        debugger;

        switch (json.status) {
          case 201:
            Swal.fire({
              title: "We welcome you!",
              text: "Login to continue",
              imageUrl: "Images/logo.png",
              imageWidth: 300,
              imageHeight: 200,
              imageAlt: "Logo"
            }).then((result) => {
              window.location.href = "login.html";
            });
            break;

          case 400:
            const errorMessage = json.error;
            const parsedMessage = JSON.parse(errorMessage.replace(/'/g, '"'));
            displayMessage(parsedMessage[0], 10000);
            break;

          case 500:
            displayMessage("Something went wrong! Try again.", 10000);
            break;

          default:
            displayMessage("Invalid details. Please try again.", 10000);
        }
      } catch (e) {
        console.error("Error parsing response:", e);
        displayMessage("Unexpected error. Please try again.", 10000);
      }
    });
}





function userLogin() {

  let email = $("#email").val();
  let password = $("#password").val();

  var settings = {
    url: "http://127.0.0.1:8000/login/",
    method: "POST",
    timeout: 0,
    data: {
      email: email,
      password: password
    },
    statusCode: {
      404: function () {
        displayMessage("User not found! Try again.", 5000);
      },
      400: function () {
        displayMessage("Invalid input! Check your details and try again.", 5000);
      },
    },
    error: function (xhr, status, error) {
      console.error("Error: ", error);
      displayMessage("Something went wrong. Please try again.", 5000);
    },
  };


  $.ajax(settings)
    .done(function (json) {
      try {

        switch (json.status) {
          case 200:

            localStorage.setItem("access_token", json.token.access);
            localStorage.setItem("refresh_token", json.token.refresh);
            localStorage.setItem("student", json.id);
            window.location.href = "courses.html";
            break;

          case 401:
            displayMessage("Wrong password.", 10000);
            break;

          case 404:
            displayMessage("User not found!", 10000);
            break;

          case 400:
            const errorMessage = json.error;
            const parsedMessage = JSON.parse(errorMessage.replace(/'/g, '"'));
            displayMessage(parsedMessage[0], 10000);
            break;

          case 500:
            displayMessage("Something went wrong! Try again.", 10000);
            break;

          default:
            displayMessage("Invalid details. Please try again.", 10000);
        }
      } catch (e) {
        console.error("Error parsing response:", e);
        displayMessage("Unexpected error. Please try again.", 10000);
      }
    });
}


function courseList() {

  let access_token = localStorage.getItem('access_token');

  var settings = {
    url: "http://127.0.0.1:8000/courses/",
    method: "POST",
    timeout: 0,
    headers: {
      "Authorization": `Bearer ${access_token}`,
    },
    statusCode: {
      404: function () {
        displayMessage("Data not found! Try again.", 5000);
      },
      400: function () {
        displayMessage("Something went wrong!", 5000);
      },
      401: function () {
        window.location.href = "login.html";
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('student');
      },
    },
    error: function (xhr, status, error) {
      console.error("Error: ", error);
      displayMessage("Something went wrong. Please try again.", 5000);
    },
  };


  $.ajax(settings)
    .done(function (json) {
      try {
        switch (json.status) {
          case 200:
            $.each(json.data, function (index, course) {

              var flashcardHtml = `
            <div class="col-md-4 col-sm-6 col-xs-12 pt-5">
                <div class="flashcard" id="${course.id}" style="border: 1px solid #ddd; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <img src="${course.image}" class="flashcard-image" style="width: 100%; height: 200px; object-fit: cover; border-top-left-radius: 10px; border-top-right-radius: 10px;">
                    <div class="flashcard-body" style="padding: 20px;">
                        <div class="row">
                            <div class="col-xs-12" style="display: flex; justify-content: space-between; align-items: center;">
                                <button class="btn btn-primary flashcard-category">${course.category}</button>
                                <span class="flashcard-price" style="font-size: 18px; font-weight: bold;">${course.price} Rs</span>
                            </div>
                        </div>
                        <h5 class="flashcard-title" style="margin-top: 20px;">${course.title}</h5>
                    </div>
                </div>
            </div>
        `;


              $("#flashcard-container").append(flashcardHtml);
            });

            $(".flashcard").on("click", function () {
              var courseId = $(this).attr("id");
              var encryptedCourseId = btoa(courseId); // Encrypt the course ID using base64

              window.location.href = `http://localhost:5500/course-description.html?id=${encryptedCourseId}`;
            });

            break;

          case 404:
            displayMessage("Course not found!", 10000);
            break;

          default:
            displayMessage("Something went wrong. Please try again.", 10000);
        }
      } catch (e) {
        console.error("Error parsing response:", e);
        displayMessage("Unexpected error. Please try again.", 10000);
      }
    });
};












function coursePlaylist() {

  const urlParamsPlaylist = new URLSearchParams(window.location.search);
  const encryptedPlaylistId = urlParamsPlaylist.get("id");
  const playlistId = atob(encryptedPlaylistId);

  let access_token = localStorage.getItem('access_token');

  var settings = {
    url: "http://127.0.0.1:8000/course-module/" + playlistId + "/",
    method: "POST",
    timeout: 0,
    headers: {
      "Authorization": `Bearer ${access_token}`,
    },
    statusCode: {
      404: function () {
        displayMessage("Data not found! Try again.", 5000);
      },
      400: function () {
        displayMessage("Something went wrong!", 5000);
      },
      401: function () {
        window.location.href = "login.html";
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('student');
      },
    },
    error: function (xhr, status, error) {
      console.error("Error: ", error);
      displayMessage("Something went wrong. Please try again.", 5000);
    },
  };

  $.ajax(settings)
    .done(function (json) {

      try {
        switch (json.status) {
          case 200:
            $('#title-content').html(`
              <h2 class="title-heading">${json.data[0].title}</h2>
            `);

            $.each(json.data, function (index, course) {
              $('#course-tabs').append(`
                <li class="nav-item">
                  <a class="nav-link ${index === 0 ? 'active show' : ''}" data-bs-toggle="tab" href="#tab-${course.vedio_id}">
                    ${course.title}
                  </a>
                </li>
              `);

              $('#course-content').append(`
                <div class="tab-pane ${index === 0 ? 'active show' : ''}" id="tab-${course.vedio_id}">
                  <div class="row">
                    <div class="col-lg-12 text-center">
                      <iframe src="${course.video_link}" frameborder="0" allowfullscreen width="100%" height="500"></iframe>
                    </div>
                    <div class="col-lg-12 pt-3 details">
                      <p class="fst-italic">${course.description}</p>
                    </div>
                  </div>
                </div>
              `);
            });


            break;

          case 404:
            displayMessage("Course not found!", 10000);
            break;

          default:
            displayMessage("Something went wrong. Please try again.", 10000);
        }
      } catch (e) {
        console.error("Error parsing response:", e);
        displayMessage("Unexpected error. Please try again.", 10000);
      }
    });
};


function playVideo(videoLink) {
  $('#video-player').attr('src', videoLink);
}

function userDetails() {

  let access_token = localStorage.getItem('access_token');
  let userId = localStorage.getItem('student');

  var settings = {
    url: "http://127.0.0.1:8000/user/" + userId + "/",
    method: "POST",
    timeout: 0,
    headers: {
      "Authorization": `Bearer ${access_token}`,
    },
    statusCode: {
      404: function () {
        displayMessage("Data not found! Try again.", 5000);
      },
      400: function () {
        displayMessage("Something went wrong!", 5000);
      },
      401: function () {
        window.location.href = "login.html";
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('student');
      },
    },
    error: function (xhr, status, error) {
      console.error("Error: ", error);
      displayMessage("Something went wrong. Please try again.", 5000);
    },
  };

 
  $.ajax(settings)
    .done(function (json) {

      try {
        switch (json.status) {
          case 200:
            console.log(json.data);
            const navName = json.data.name;
            const navMob = json.data.mobile_no;
            const navEmail = json.data.email;

            $("#nav-name").text("Name: " + navName);
            $("#nav-mob").text("Contact: " + navMob);
            $("#nav-email").text("Email: " + navEmail);
            break;

          case 404:
            displayMessage("Course not found!", 10000);
            break;

          default:
            displayMessage("Something went wrong. Please try again.", 10000);
        }
      } catch (e) {
        console.error("Error parsing response:", e);
        displayMessage("Unexpected error. Please try again.", 10000);
      }
    });
}





$("#logout").click(function (event) {
  event.preventDefault();
  let refresh_token = localStorage.getItem("refresh_token");
  let access_token = localStorage.getItem("access_token");

  var settings = {
    "url": "http://127.0.0.1:8000/logout/",
    "method": "POST",
    "timeout": 0,
    "data": JSON.stringify({
      refresh_token: refresh_token
    }),
    "headers": {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${access_token}`,
    },
    "processData": false,
    "statusCode": {
      500: function (response) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("student");
        window.location.href = "login.html";
      },
    },
  };
  $.ajax(settings).done(function (json) {
    try {
      switch (json.status) {
        case 200:
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          localStorage.removeItem("student");
          window.location.href = "login.html";
          break;

        case 404:
          displayMessage("Something went wrng!", 10000);
          break;

        default:
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Something went wrong!",
          });
      }
    } catch (e) {
      console.error("Error parsing response:", e);
      displayMessage("Unexpected error. Please try again.", 10000);
    }
  });
});


