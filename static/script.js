document.addEventListener("DOMContentLoaded", function () {
    const appointmentForm = document.querySelector("form");

    if (appointmentForm) {
        appointmentForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let doctor = document.querySelector('input[name="doctor"]').value;
            let time = document.querySelector('input[name="time"]').value;

            if (doctor.trim() === "" || time.trim() === "") {
                alert("Please fill in all fields!");
                return;
            }

            fetch("/appointments", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams(new FormData(appointmentForm))
            })
            .then(response => {
                if (response.ok) {
                    alert("Appointment booked successfully!");
                    window.location.reload();
                } else {
                    alert("Error booking appointment. Try again!");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});
