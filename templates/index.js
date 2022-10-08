function check_code() {
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    // show if hidden
    resultDiv.style.display = "block";
    const code = document.getElementById('code').value;

    $.getJSON("../reglists/checkin_codes.json", function (json) {
        let userData;
        // check if code is in reglists
        if (code in json) {
            userData = json[code];
            console.log(userData);
            const regCode = userData[4];
            // 0 is regular entry, 1 is soft early entry, 2 is hard early entry
            if (regCode == 0) {
                resultText.innerHTML = "Name: " + userData[0] + "<br>Email: " + userData[1] + "<br>Entry Time: 10am";
                resultText.style.color = "White";
                resultDiv.style.backgroundColor = "Green";
            } else if (regCode == 1) {
                resultText.innerHTML = "Name: " + userData[0] + "<br>Email: " + userData[1] + "<br>Entry Time: 9am";
                resultText.style.color = "White";
                resultDiv.style.backgroundColor = "Green";
            }
        } else {
            resultText.innerHTML = "Code invalid.";
            resultText.style.color = "White";
            resultDiv.style.backgroundColor = "red";
            return;
        }
    });
}