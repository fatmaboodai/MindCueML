let Peer = require('simple-peer')
//  connect with the host
let socket =  io()
const video = document.querySelector('video')
const t = document.getElementById('test')

// client 
let client = {}

// get the stream 
// if the user gave the permission 
navigator.mediaDevices.getDisplayMedia()
    .then(stream =>{
        // notify the backend that there is a client that gave us permission to record 
        socket.emit('NewClient')
        // display the users video for himself
        video.srcObject = stream
        video.play()

    //  define a new peer and return it
    function InitPeer(type){
        // init true -- > send offer
        // init false --> wait for an offer

        let peer = new Peer({initiator:(type=='init')?true:false,stream:stream,trickle:false})
        peer.on('stream',function(stream){
             CreateVideo(stream)
        })

        // when the peer is closed we have to destroy the video
        peer.on('close',function(){
            document.getElementById("peerVideo").remove()
            peer.destroy()

        })
        // return what ever the peer is
    return peer
    }
    function MakePeer() {
        client.gotAnswer=false
        let peer = InitPeer('init')
        // it is of type init ---> will send a signal / offer
        peer.on('signal', function(data) {
            if (!client.gotAnswer){
                // send offer because it does not exit
                socket.emit('Offer',data, socket);
            }
        })
        client.Peer = peer
    }

// Client 2
function FrontAnswer(offer) {
    let peer = InitPeer('notInit');
    peer.on('signal', function(data) {
        socket.emit('Answer', data);
    });
    peer.on('stream', function(stream) {
        CreateVideo(stream);
    });
    peer.signal(offer);
}

function CreateVideo(stream) {
    let video = document.createElement('video');
    video.srcObject = stream;
    document.querySelector('#peerDiv').appendChild(video);
    video.play();
}

//  if the answer is from the backend 
    function SignalAnswer(answer){
        client.gotAnswer = true
        let peer = client.Peer
        //  the answer from the other user will be connected 
        peer.signal(answer)
    }


// if there is an already existi recording session
    function SessionActive(){
        document.write("an active session is already there bye")

    }

    //  event where all the previpus functions will run 
    // if an offer is requested from the backend we should generate an answer 
    socket.on('BackOffer',FrontAnswer)
    socket.on('BackAnswer',SignalAnswer)
    socket.on('SessionActive',SessionActive)
    socket.on('CreatePeer',MakePeer)



})
.catch(err => document.write(err))


