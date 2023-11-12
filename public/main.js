let Peer = require('simple-peer')
//  connect with the host
let socket =  io()
const video = document.querySelector('video')
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
    // create peer of type init that send offer
    function MakePeer(){
        client.gotAnswer=false
        let peer = InitPeer('init')
        // it is of type init ---> will send a signal / offer
        peer.on('signal',function(data){
            if (!client.gotAnswer){
                // send offer because it does not exit
                socket.emit('Offer',data)
            }
        })
        client.Peer = peer
    }

//  if we got the offer --> we want to send an answer
    function FrontAnswer(offer){
        //  reciving the offer type (not innit) 
        let peer = InitPeer('notInit')
        peer.on('signal',(data)=>{
            //  if we got the signal 
            socket.emit('Answer',data)
        })
        peer.signal(offer)
    }
//  if the answer is from the backend 
    function SignalAnswer(answer){
        client.gotAnswer = true
        let peer = client.Peer
        //  the answer from the other user will be connected 
        peer.signal(answer)
    }

    function CreateVideo(stream){
        let video = document.createElement('video')
        video.srcObject = stream
        document.querySelector('#peerDiv').appendChild(video)
        video.play()
    }
    

// if there is an already existi recording session
    function SessionActive(){
        document.writte("an active session is already there bye")

    }

    //  event where all the previpus functions will run 
    // if an offer is requested from the backend we should generate an answer 
    socket.on('BackOffer',FrontAnswer)
    socket.on('BackAnswer',SignalAnswer)
    socket.on('SessionActive',SessionActive)
    socket.on('CreatePeer',MakePeer)



})
.catch(err => document.write(err))


