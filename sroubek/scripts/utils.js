function clearBackground(color) {
    c.fillStyle = color;
    c.fillRect(0, 0, canvas.width, canvas.height);
}

function fillTextCenter(text, font, color, y, shadowOffset) {
    c.font = font;
    c.fillStyle = "black";
    c.fillText(text, canvas.width / 2 - c.measureText(text).width / 2 + shadowOffset, y + shadowOffset);
    c.fillStyle = color;
    c.fillText(text, canvas.width / 2 - c.measureText(text).width / 2, y);

    console.log(text, font, color, y, canvas.width / 2 - c.measureText(text).width / 2);
}
