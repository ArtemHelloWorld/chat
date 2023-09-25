function scrollToElement(listQuerySelector, elementQuerySelector){
  const messageList = document.querySelector(listQuerySelector)

  if (messageList){
    const unreadItem = messageList.querySelector(elementQuerySelector)
    if (unreadItem) {
      messageList.scrollTo({
        top: unreadItem.offsetTop - messageList.clientHeight,
        behavior: "instant"
      })
    } else {
      scrollDown(listQuerySelector)
    }
  }
}

function scrollDown(listQuerySelector, smooth=false) {
  const messageList = document.querySelector(listQuerySelector)
  const behavior = smooth ? "smooth" : "instant"
  if (messageList) {
    messageList.scrollTo({
      top: messageList.scrollHeight,
      behavior: behavior
    })
  }
}

export {scrollToElement, scrollDown}