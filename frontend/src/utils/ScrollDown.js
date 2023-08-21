
function scrollToElement(listQuerySelector, elementQuerySelector) {
  const messageList = document.querySelector(listQuerySelector)
  if (messageList){
    const unreadItem = messageList.querySelector(elementQuerySelector); // Найти первый элемент с классом unread

    if (unreadItem) {
      messageList.scrollTo({
        top: unreadItem.offsetTop - messageList.clientHeight,
        behavior: 'instant'
      });
    } else {
      scrollDown(listQuerySelector)
    }
  }
}
function scrollDown(listQuerySelector, smooth=false) {
  const messageList = document.querySelector(listQuerySelector)
  let behavior = smooth ? 'smooth' : 'instant'
  if (messageList) {
    messageList.scrollTo({
      top: messageList.scrollHeight,
      behavior: behavior
    });
  }
}


export {scrollToElement, scrollDown}