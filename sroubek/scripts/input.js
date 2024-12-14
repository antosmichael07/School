const inputUp     = 0;
const inputDown   = 1;
const inputLeft   = 2;
const inputRight  = 3;
const inputSquish = 4;

let inputs = [false, false, false, false, false];

document.addEventListener("keydown", function (e) {
    if (e.code == "KeyW") {
        inputs[inputUp] = true;
    }
    if (e.code == "KeyS") {
        inputs[inputDown] = true;
    }
    if (e.code == "KeyA") {
        inputs[inputLeft] = true;
    }
    if (e.code == "KeyD") {
        inputs[inputRight] = true;
    }
    if (e.code == "Space") {
        inputs[inputSquish] = true;
    }
    if (e.code == "KeyR") {
        newGame();
    }
});

document.addEventListener("keyup", function (e) {
    if (e.code == "KeyW") {
        inputs[inputUp] = false;
    }
    if (e.code == "KeyS") {
        inputs[inputDown] = false;
    }
    if (e.code == "KeyA") {
        inputs[inputLeft] = false;
    }
    if (e.code == "KeyD") {
        inputs[inputRight] = false;
    }
    if (e.code == "Space") {
        inputs[inputSquish] = false;
    }
});
