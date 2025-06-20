const socket = io();

const canvas = document.getElementById('canvas');
const c = canvas.getContext('2d');

const info = document.getElementById('info');
const playerInfo = document.getElementById('playerInfo');
const modalGameFull = new bootstrap.Modal(document.getElementById('gameFullModal'));

let thisPlayer = ' ';
let lastMove;
let tileCount;
let tileSize;
let symbolSize;
let symbolOffset;
const tileBorderColor = '#aaa';
const tileColor = '#fff';
const tileColorHighlighted = '#ff0';

function drawBackground() {
    c.fillStyle = tileBorderColor;
    c.fillRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < tileCount; i++) {
        for (let j = 0; j < tileCount; j++) {
            c.fillStyle = tileColor;
            c.fillRect(i * tileSize + 1, j * tileSize + 1, tileSize - 2, tileSize - 2);
        }
    }
}

function drawO(x, y) {
    c.strokeStyle = 'blue';
    c.lineWidth = 4;
    c.beginPath();
    c.arc(x * tileSize + tileSize / 2, y * tileSize + tileSize / 2, symbolSize / 2, 0, Math.PI * 2);
    c.stroke();
}

function drawX(x, y) {
    c.strokeStyle = 'red';
    c.lineWidth = 4;
    c.beginPath();
    c.moveTo(x * tileSize + symbolOffset, y * tileSize + symbolOffset);
    c.lineTo((x + 1) * tileSize - symbolOffset, (y + 1) * tileSize - symbolOffset);
    c.moveTo((x + 1) * tileSize - symbolOffset, y * tileSize + symbolOffset);
    c.lineTo(x * tileSize + symbolOffset, (y + 1) * tileSize - symbolOffset);
    c.stroke();
}

function drawSymbol(x, y, symbol) {
    if (lastMove !== null) {
        c.fillStyle = tileColor;
        c.fillRect(lastMove.x * tileSize + 1, lastMove.y * tileSize + 1, tileSize - 2, tileSize - 2);
        lastMove.symbol === 'X' ? drawX(lastMove.x, lastMove.y) : drawO(lastMove.x, lastMove.y);
    }

    c.fillStyle = tileColorHighlighted;
    c.fillRect(x * tileSize + 1, y * tileSize + 1, tileSize - 2, tileSize - 2);
    symbol === 'X' ? drawX(x, y) : drawO(x, y);

    lastMove = {x: x, y: y, symbol: symbol};
}

socket.on('initialData', (data) => {
    tileCount = data.tileCount;
    tileSize = data.tileSize;
    symbolSize = Math.ceil(tileSize * .75);
    symbolOffset = (tileSize - symbolSize) / 2;
    lastMove = null;

    canvas.width = tileCount * tileSize;
    canvas.height = tileCount * tileSize;
    drawBackground();

    for (let i = 0; i < tileCount; i++) {
        for (let j = 0; j < tileCount; j++) {
            if (data.board[i][j] !== ' ') {
                drawSymbol(i, j, data.board[i][j]);
            }
        }
    }
});

socket.on('player', (player) => {
    thisPlayer = player;
    playerInfo.innerHTML = `You are player '${thisPlayer}'`;
});

socket.on('gameFull', () => {
    modalGameFull.show();
    playerInfo.innerHTML = 'You are a spectator';
});

socket.on('drawSymbol', (data) => {
    drawSymbol(data.x, data.y, data.symbol);
});

socket.on('info', (msg) => {
    if (msg.player === thisPlayer) {
        let replace = new RegExp(`player '${msg.player}'`, 'gi');
        msg.msg = msg.msg.replace(replace, msg.replace);
        msg.msg = msg.msg.replace('wins', 'win');
    }

    info.innerHTML = msg.msg;
});

socket.on('win', (data) => {
    for (let i = 0; i < 5; i++) {
        const x = data.x + i * data.directionX;
        const y = data.y + i * data.directionY;

        c.fillStyle = tileColorHighlighted;
        c.fillRect(x * tileSize + 1, y * tileSize + 1, tileSize - 2, tileSize - 2);
        data.symbol === 'X' ? drawX(x, y) : drawO(x, y);
    }
});

canvas.addEventListener('click', (e) => {
    socket.emit('click', {
        x: Math.floor(e.offsetX / tileSize),
        y: Math.floor(e.offsetY / tileSize)
    });
});
