const express = require('express')
const app = express()
// http server
const http = require('http').Server(app)

//  create an instance for socket.io
const io = require('socket.io')(http)

//  our port 
const port = process.env.PORT || 3000


// load static files
app.use(express.static(__dirname + "/public"))
// at the beggining there are not clients
let clients = 0 
// what should happen once the connection is made
io.on('connection',function(socket){
    socket.on('NewClient',function(){
        if(clients<2){
            if(clients==1){
                //  this will send a signal for other client
                this.emit('CreatePeer')
            }
        }
        else
        // more than 2 clients ( 2)
            this.emit('SessionActive')
        clients++
    })
    // an offer is coming from the front end
    socket.on('Offer',SendOffer)
    // an answer is coming from the front end
    socket.on('Answer',SendAnswer)
    // if we closed the browser window call the disconnect function
    socket.on('disconnect',Disconnect)

})


function Disconnect(){
    if(clients>0){
        clients--
    }
}


function SendOffer(offer){
    //  send the offer to the other user
    this.broadcast.emit('BackOffer',offer)
}


function SendAnswer(data){
    //  send the answer to the other user
    this.broadcast.emit('BackAnswer',data)
}


http.listen(port, ()=> console.log(`Active on ${port} port`))