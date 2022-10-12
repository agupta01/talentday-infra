
const signedIn = {
    green: [],
    orange: [],
};

function check_code() {
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    // show if hidden
    resultDiv.style.display = "block";
    const code = document.getElementById('code').value;

    $.getJSON("../reglists/checkin_codes.json", function (json) {
        $.get("../reglists/venmo_flat.txt", function (file) {
            let userData;
            // check if code is in reglists
            if (code in json) {
                userData = json[code];
                console.log(userData);
                const regCode = userData[4];
                const paidDues = file.search(userData[2]) != -1 || file.search(userData[1]) != -1;
                console.log(paidDues);
                // 0 is regular entry, 1 is soft early entry, 2 is hard early entry
                if (regCode == 0) {
                    resultText.innerHTML = "Name: " + userData[0] + "<br>Email: " + userData[1] + "<br>Entry Time: 10am";
                    resultText.style.color = "White";
                    resultDiv.style.backgroundColor = "Green";
                    signedIn["green"].push(code);
                } else if (regCode == 1 || regCode == 2) {
                    resultText.innerHTML = "Name: " + userData[0] + "<br>Email: " + userData[1] + "<br>Entry Time: 9am";
                    resultText.style.color = "White";
                    resultDiv.style.backgroundColor = paidDues ? "Green" : "Orange";
                    (paidDues ? signedIn["green"] : signedIn['orange']).push(code)
                    if (regCode == 2) {
                        alert("This person has hard early entry. If they are not a DS3 member, they will not be allowed to enter.");
                    }
                }
            } else {
                resultText.innerHTML = "Code invalid.";
                resultText.style.color = "White";
                resultDiv.style.backgroundColor = "red";
                return;
            }
        }, 'text');
    });
}

// async function checkIfPaidDues(name, email) {
//     $.get("../reglists/venmo_flat.txt", function (file) {
//         console.log(file.search(email))
//         if (file.search(email) != -1 || file.search(name) != -1) {
//             return true;
//         } else {
//             return false;
//         }
//     }, 'text');
// }

// function main() {
//     document.getElementById('checkin').onclick = async () => {
//         await check_code();
//     }
// }