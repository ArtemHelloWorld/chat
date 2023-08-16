
function scrollDown(querySelector) {
  var messageList = document.querySelector(querySelector)
  messageList.scrollTop =  messageList.scrollHeight

}
function scrollDownSmooth(querySelector, smooth=true) {
    var messageList = document.querySelector(querySelector)
    if (messageList){
      const lastMessage = messageList.lastElementChild;
        lastMessage.scrollIntoView({ behavior: 'smooth' });
        
        messageList.scrollTop =  messageList.scrollHeight
    }     
}



export {scrollDown, scrollDownSmooth}