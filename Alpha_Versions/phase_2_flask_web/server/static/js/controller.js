const moveButton =
    document.getElementById("moveButton");

const clickButton =
    document.getElementById("clickButton");

const scrollButton =
    document.getElementById("ScrollButton");

    

async function sendEvent(eventName) {

    const response = await fetch("/event", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            event: eventName
        })
    });


    const result = await response.json();

    console.log(result);
}


moveButton.addEventListener("click", () => {

    sendEvent("move");
});


clickButton.addEventListener("click", () => {

    sendEvent("click");
});

scrollButton.addEventListener("click", () => {

    sendEvent("scroll");
});