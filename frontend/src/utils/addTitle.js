import React from 'react'

function addUnreadTitle(listQuerySelector, elementQuerySelector) {
  const messageList = document.querySelector(listQuerySelector)
  if (messageList){
    const unreadItem = messageList.querySelector(elementQuerySelector); // Найти первый элемент с классом unread

    if (unreadItem) {
      unreadItem.insertAdjacentHTML('beforebegin', `<div>Непрочитанные сообщения</div>`)
    }
  }
}

export default addUnreadTitle;