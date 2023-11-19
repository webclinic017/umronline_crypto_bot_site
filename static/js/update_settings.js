document.getElementById("updateButton").addEventListener("click", function () {
    var updatedSettings = {};
    var selects = document.querySelectorAll("select");
    selects.forEach(function (select) {
        var day = select.getAttribute("data-day");
        var target = select.value;
        updatedSettings[day] = target;
    });

    // Send the updated settings as JSON data via POST request
    fetch("/update_targets", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedSettings),
    })
        .then(function (response) {
            console.log(response)
            if (response.ok) {
                alert("Settings updated successfully!");
            } else {
                alert("Failed to update settings.");
            }
        })
        .catch(function (error) {
            alert("An error occurred: " + error);
        });
});

document.getElementById('bybitUpdateButton').addEventListener('click', function () {
    var api_key = document.getElementById('api_key').value;
    var secret = document.getElementById('secret').value;
    var trading_type = document.getElementById('trading_type').value;
    var stop_loss = document.getElementById('stop_loss').value;
    var order_size = document.getElementById('order_size').value;
    var bot_status = document.getElementById('bot_status').value;

    var data = {
        api_key: api_key,
        secret: secret,
        trading_type: trading_type,
        stop_loss: stop_loss,
        order_size: order_size,
        bot_status: bot_status
    };

    fetch('/update_bybit_settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(function (response) {
            console.log(response)
            if (response.ok) {
                alert("Settings updated successfully!");
            } else {
                alert("Failed to update settings.");
            }
        })
        .catch(function (error) {
            alert("An error occurred: " + error);
        });
});