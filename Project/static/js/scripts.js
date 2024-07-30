const socket = io();

socket.on('frame', (frame) => {
    console.log("Received frame");
    const img = document.getElementById('videoFeed');
    img.src = 'data:image/jpeg;base64,' + frame;
    console.log("Updated image source");
});

socket.on('connect', () => {
    console.log("Socket connected");
});

socket.on('disconnect', () => {
    console.log("Socket disconnected");
});

socket.on('connect_error', (error) => {
    console.error("Socket connection error: ", error);
});
