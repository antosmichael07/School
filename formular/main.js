let states = [
    "This is a TRIANGLE !!!",
    "This is NOT a TRIANGLE !!!",
    "Bro, the angles have to be a positive number.",
    "Bro, the sides have to be a positive number."
];

let triangle = {
    alpha: 0,
    beta: 0,
    gamma: 0,
    a: 0,
    b: 0,
    c: 0,

    validate_angles: function(a = this.alpha, b = this.beta, c = this.gamma) {
        return a > 0 && b > 0 && c > 0 ? a + b + c == 180 ? 0 : 1 : 2;
    },

    validate_sides: function(a = this.a, b = this.b, c = this.c) {
        return a > 0 && b > 0 && c > 0 ? a + b > c && b + c > a && a + c > b ? 0 : 1 : 3;
    }
};

let angle_button = document.getElementById("angle-validate");
let alpha = document.getElementById("alpha");
let beta = document.getElementById("beta");
let gamma = document.getElementById("gamma");
let angle_result = document.getElementById("angle-result");

angle_button.addEventListener("click", function() {
    triangle.alpha = Number(alpha.value);
    triangle.beta = Number(beta.value);
    triangle.gamma = Number(gamma.value);

    let res = triangle.validate_angles();

    if (res == 0) {
        angle_result.classList.add("text-success");
        angle_result.classList.remove("text-danger");
    } else {
        angle_result.classList.remove("text-success");
        angle_result.classList.add("text-danger");
    }
    angle_result.innerHTML = states[res];
});

let side_button = document.getElementById("side-validate");
let a = document.getElementById("a");
let b = document.getElementById("b");
let c = document.getElementById("c");
let side_result = document.getElementById("side-result");

side_button.addEventListener("click", function() {
    triangle.a = Number(a.value);
    triangle.b = Number(b.value);
    triangle.c = Number(c.value);

    let res = triangle.validate_sides();

    if (res == 0) {
        side_result.classList.add("text-success");
        side_result.classList.remove("text-danger");
    } else {
        side_result.classList.remove("text-success");
        side_result.classList.add("text-danger");
    }
    side_result.innerHTML = states[res];
});
