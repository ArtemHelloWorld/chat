
function scrollToElement(listQuerySelector, elementQuerySelector) {
  const messageList = document.querySelector(listQuerySelector)
  if (messageList){
    const unreadItem = messageList.querySelector(elementQuerySelector); // Найти первый элемент с классом unread

    if (unreadItem) {
      messageList.scrollTo({
        top: unreadItem.offsetTop - messageList.clientHeight,
      });
    } else {
      scrollDown(listQuerySelector)
    }
  }
}
function scrollDown(listQuerySelector) {
  const messageList = document.querySelector(listQuerySelector)
  messageList.scrollTo({
    top: messageList.scrollHeight,
  });
}
function scrollDownSmooth(querySelector, smooth=true) {
    var messageList = document.querySelector(querySelector)
    if (messageList){
      const lastMessage = messageList.lastElementChild;
        lastMessage.scrollIntoView({ behavior: 'smooth' });
        
        messageList.scrollTop =  messageList.scrollHeight
    }     
}



export {scrollToElement, scrollDown, scrollDownSmooth}